from pydantic import BaseModel, Field

class SensorData(BaseModel):
    temperature: float #= Field(..., description = "T")
    pressure: float #= Field(..., description = "P")
    humidity: float #= Field(..., description = "Humidity")
    magX: float #= Field(..., description = "X")
    magY: float #= Field(..., description = "Y")
    magZ: float #= Field(..., description = "Z")
    timestamp: str #= Field(..., description = "Time of measurement")

class CreateSensorData(SensorData):
    pass
