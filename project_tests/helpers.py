import sys
import asyncio
import warnings
from http.cookies import SimpleCookie
import os
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from database import Base

warnings.simplefilter("ignore", DeprecationWarning)


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()


class ASGIResponse:
    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    @property
    def text(self):
        return self.body.decode("utf-8")


class ASGITestClient:
    def __init__(self, app):
        self.app = app
        self.cookies = {}

    def get(self, path, follow_redirects=True):
        return self.request("GET", path, follow_redirects=follow_redirects)

    def post_form(self, path, data, follow_redirects=True):
        body = "&".join(f"{key}={value}" for key, value in data.items()).encode("utf-8")
        return self.request(
            "POST",
            path,
            body=body,
            headers={"content-type": "application/x-www-form-urlencoded"},
            follow_redirects=follow_redirects,
        )

    def request(self, method, path, body=b"", headers=None, follow_redirects=True):
        response = asyncio.run(self._request(method, path, body, headers or {}))
        self._store_cookies(response.headers.get("set-cookie", []))

        if follow_redirects and response.status_code in {301, 302, 303, 307, 308}:
            location = response.headers["location"][0]
            return self.get(location, follow_redirects=True)

        return response

    async def _request(self, method, path, body, headers):
        raw_headers = [
            (name.lower().encode("latin-1"), value.encode("latin-1"))
            for name, value in headers.items()
        ]
        if self.cookies:
            cookie = "; ".join(f"{key}={value}" for key, value in self.cookies.items())
            raw_headers.append((b"cookie", cookie.encode("latin-1")))

        scope = {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1",
            "method": method,
            "scheme": "http",
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": b"",
            "headers": raw_headers,
            "client": ("testclient", 50000),
            "server": ("testserver", 80),
        }
        messages = [{"type": "http.request", "body": body, "more_body": False}]
        status_code = None
        response_headers = {}
        body_parts = []

        async def receive():
            if messages:
                return messages.pop(0)
            return {"type": "http.disconnect"}

        async def send(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                for key, value in message.get("headers", []):
                    header_name = key.decode("latin-1")
                    header_value = value.decode("latin-1")
                    response_headers.setdefault(header_name, []).append(header_value)
            elif message["type"] == "http.response.body":
                body_parts.append(message.get("body", b""))

        await self.app(scope, receive, send)
        return ASGIResponse(status_code, response_headers, b"".join(body_parts))

    def _store_cookies(self, cookie_headers):
        for cookie_header in cookie_headers:
            parsed = SimpleCookie()
            parsed.load(cookie_header)
            for name, morsel in parsed.items():
                if morsel["max-age"] == "0":
                    self.cookies.pop(name, None)
                else:
                    self.cookies[name] = morsel.value


class FastAPIIntegrationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_cwd = os.getcwd()
        os.chdir(APP_DIR)

        import main

        cls.main = main
        cls.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)

        def override_get_db():
            db = cls.SessionLocal()
            try:
                yield db
            finally:
                db.close()

        cls.main.app.dependency_overrides[cls.main.get_db] = override_get_db

    @classmethod
    def tearDownClass(cls):
        cls.main.app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=cls.engine)
        cls.engine.dispose()
        os.chdir(cls.old_cwd)

    def setUp(self):
        self.client = ASGITestClient(self.main.app)
