from sqlalchemy import Column, Integer, String, Float
from database import Base

# Define tables that will be created inside of DB

class SensorData(Base):
    __tablename__ = "DataWave"
    id = Column(Integer, primary_key = True, index = True)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    magX = Column(Float)
    magY = Column(Float)
    magZ = Column(Float)
    timestamp = Column(String(50))
