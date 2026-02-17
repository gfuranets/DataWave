#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SDA 16
#define SCL 17
#define BME280_ADDR 0x76

Adafruit_BME280 bme;

void setup() {
  Wire.begin(SDA, SCL);
  Serial.begin(9600);

  if (!bme.begin(BME280_ADDR)) {
    Serial.println("Sensor not found!");
    while (1);
  }

  // Optional: customize oversampling/filter
  bme.setSampling(
      Adafruit_BME280::MODE_NORMAL,
      Adafruit_BME280::SAMPLING_X1,  // temp
      Adafruit_BME280::SAMPLING_X1,  // pressure
      Adafruit_BME280::SAMPLING_X1,  // humidity
      Adafruit_BME280::FILTER_OFF
  );
}

void loop() {
  float temperature = bme.readTemperature();
  float pressure = bme.readPressure();
  float humidity = bme.readHumidity();

  Serial.print("t = "); Serial.print(temperature); Serial.print(", P = "); Serial.print(pressure); Serial.print(", humidity = "); Serial.println(humidity);
  delay(1000);
}
