/*
  Ship controller — WebSocket version
  
  Sends sensor telemetry as CSV over WebSocket.
  Receives servo commands in format: SX:90,SY:90,SZ:90
    SX = servoX     (pin 32, mouse horizontal)
    SY = servoY     (pin 33, mouse vertical)
    SZ = servoMotor (pin 14, A/D keys)
*/

#include <Wire.h>
#include <WiFi.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <ArduinoWebsockets.h>
#include <ESP32Servo.h>

using namespace websockets;

// I2C pins
#define SDA 27
#define SCL 26

// Sensor addresses
#define BME280_ADDRESS    0x76
#define QMC5883P_ADDRESS  0x2C

// Servo pins  (GPIO34-39 are input-only on ESP32 — cannot drive PWM)
#define SERVO_X 32
#define SERVO_Y 33
#define SERVO_M 14

// WiFi credentials
const char* ssid     = "gkf";
const char* password = "12345678";

// WebSocket server
const char* server_url = "ws://172.20.10.2:8000/ws/1?token=6d3c41c380aa90781b44d6804949afcafc2f1d991f314e050a14cc6267ef37c1";

Adafruit_BME280 bme;
WebsocketsClient ws_client;

Servo servoX;
Servo servoY;
Servo servoMotor;

// Timing and reconnection
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 2000;
bool wsConnected = false;
unsigned long lastReconnectAttempt = 0;
const unsigned long reconnectInterval = 5000;


// --------------------------------------------------------------------------
void executeCommand(String command) {
    int firstComma  = command.indexOf(',');
    int secondComma = command.indexOf(',', firstComma + 1);

    if (firstComma == -1 || secondComma == -1) {
        Serial.println("Unknown command: " + command);
        return;
    }

    int angleX = command.substring(3, firstComma).toInt();
    int angleY = command.substring(firstComma + 4, secondComma).toInt();
    int angleMotor = command.substring(secondComma + 4).toInt();

    angleX = constrain(angleX, 0, 180);
    angleY = constrain(angleY, 0, 180);
    angleMotor = constrain(angleMotor, 0, 180);

    servoX.write(angleX);
    servoY.write(angleY);
    servoMotor.write(angleMotor);

    Serial.printf("X: %d  Y: %d  Motor: %d\n", angleX, angleY, angleMotor);
}


// --------------------------------------------------------------------------
void connectToWebSocket() {
    Serial.print("Connecting to WebSocket... ");
    if (ws_client.connect(server_url)) {
        Serial.println("OK");
        wsConnected = true;
    } else {
        Serial.println("Failed");
        wsConnected = false;
    }
}

void handleWebSocketReconnection() {
    if (!wsConnected && (millis() - lastReconnectAttempt > reconnectInterval)) {
        lastReconnectAttempt = millis();
        connectToWebSocket();
    }
}


// --------------------------------------------------------------------------
void setup() {
    Serial.begin(115200);
    Wire.begin(SDA, SCL);
    Wire.setClock(100000);

    // Servos
    servoX.attach(SERVO_X);
    servoY.attach(SERVO_Y);
    servoMotor.attach(SERVO_M);
    servoX.write(90);
    servoY.write(90);
    servoMotor.write(90);
    Serial.println("Servos ready");

    // WiFi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected, IP: " + WiFi.localIP().toString());

    // WebSocket
    ws_client.onMessage([](WebsocketsMessage message) {
        String command = message.data();
        Serial.println("Received: " + command);
        executeCommand(command);
    });

    ws_client.onEvent([](WebsocketsEvent event, String data) {
        if (event == WebsocketsEvent::ConnectionOpened) {
            Serial.println("WebSocket opened.");
            wsConnected = true;
        } else if (event == WebsocketsEvent::ConnectionClosed) {
            Serial.println("WebSocket closed.");
            wsConnected = false;
        }
    });

    connectToWebSocket();

    // BME280
        if (!bme.begin(BME280_ADDRESS)) {
        Serial.println("BME280 not found! Check wiring.");
        while (1) delay(100);
    }
    bme.setSampling(Adafruit_BME280::MODE_NORMAL,
                    Adafruit_BME280::SAMPLING_X1,
                    Adafruit_BME280::SAMPLING_X1,
                    Adafruit_BME280::SAMPLING_X1,
                    Adafruit_BME280::FILTER_OFF);

    // QMC5883P
    Wire.beginTransmission(QMC5883P_ADDRESS);
    Wire.write(0x0A);   // mode register: continuous, 200 Hz
    Wire.write(0xCF);
    Wire.endTransmission();

    Wire.beginTransmission(QMC5883P_ADDRESS);
    Wire.write(0x0B);   // config: enable set/reset, ±8 Gauss
    Wire.write(0x08);
    Wire.endTransmission();

    Serial.println("Ready.");
}


// --------------------------------------------------------------------------
void readMagnetometer(float &x, float &y, float &z) {
    Wire.beginTransmission(QMC5883P_ADDRESS);
    Wire.write(0x01);   // X_LSB register
    Wire.endTransmission(false);
    Wire.requestFrom(QMC5883P_ADDRESS, 6);

    if (Wire.available() == 6) {
        int16_t xRaw = Wire.read() | (Wire.read() << 8);
        int16_t yRaw = Wire.read() | (Wire.read() << 8);
        int16_t zRaw = Wire.read() | (Wire.read() << 8);
        const float scale = 800.0f / 32768.0f;  // ±8 Gauss → µT
        x = xRaw * scale;
        y = yRaw * scale;
        z = zRaw * scale;
    } else {
        x = y = z = 0.0;
        Serial.println("Magnetometer read error");
    }
}


// --------------------------------------------------------------------------
void sendTelemetry() {
    float temp  = bme.readTemperature();
    float press = bme.readPressure();
    float hum   = bme.readHumidity();

    float magX, magY, magZ;
    readMagnetometer(magX, magY, magZ);

    String csv = String(temp)  + "," +
                 String(press) + "," +
                 String(hum)   + "," +
                 String(magX)  + "," +
                 String(magY)  + "," +
                 String(magZ);

    ws_client.send(csv);
    Serial.println("Sent: " + csv);
}


// --------------------------------------------------------------------------
void loop() {
    ws_client.poll();
    handleWebSocketReconnection();

    if (wsConnected && (millis() - lastSendTime >= sendInterval)) {
        sendTelemetry();
        lastSendTime = millis();
    }
}