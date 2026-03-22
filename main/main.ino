#include <BluetoothSerial.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Servo.h>

#define SDA 16
#define SCL 17
#define steeringPin 12
#define BME280_ADDR 0x76

BluetoothSerial SerialBT;
Adafruit_BME280 bme;
Servo servo;

// Setup functions
void setup_BME280(int addr);
void setup_GY271(int addr);

// Control/data functions
uint8_t* prepareData();
void send_data(uint8_t* data);
void steering(int servo);

void setup() {
  SerialBT.begin("ESP32_Device");
  Serial.begin(112500);
  Wire.begin(SDA, SCL);
  
  setup_BME280(BME280_ADDR);
  setup_GY271(GY271_ADDR);

  int angle = 0;
}

void loop() {
  send_data(prepare_data());
  steering(steeringServo);
}

// ---------------------------------------------------------------------------------------------------- //

setup_BME280(int addr) {
  if (!bme.begin(addr)) {
    Serial.println("Sensor not found!");
    while (1);
  }

  // Customize oversampling/filter
  bme.setSampling(
    Adafruit_BME280::MODE_NORMAL,
    Adafruit_BME280::SAMPLING_X1,  // temperature
    Adafruit_BME280::SAMPLING_X1,  // pressure
    Adafruit_BME280::SAMPLING_X1,  // humidity
    Adafruit_BME280::FILTER_OFF
  );
}

void setup_GY271(int addr) {
  //
}

uint8_t* prepare_data() {
  float temperature = bme.readTemperature();
  float pressure = bme.readPressure();
  float humidity = bme.readHumidity();
  float magX = 1.f;
  float magY = 1.f;
  float magZ = 1.f;

  uint8_t* arr = new uint8_t[12];

  Serial.print("t = "); Serial.print(temperature); 
  Serial.print(", P = "); Serial.print(pressure); 
  Serial.print(", humidity = "); Serial.print(humidity);
  Serial.print(", Bx = "); Serial.print(magX);
  Serial.print(", By = "); Serial.print(magY);
  Serial.print(", Bz = "); Serial.println(magZ);
  delay(1000);

  return arr;
}

void send_data(uint8_t* data) {
  SerialBT.write(data, 12);
}

void steering(int servo) {
  while(SerialBT.available()) {
    char command = SerialBT.read();

    switch (command) {
      case 'a':
        break;

      case 'd':
        break;

      case 'w':
        break;

      case 's':
        break;

      default:

    }
  }
}
