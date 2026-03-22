#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Servo.h>

#define servoPin 37
#define BME280_ADDR 0x76

const int QMC5883P_ADDRESS = 0x2C;
// Register addresses for the QMC5883P
const int MODE_REGISTER = 0x0A;
const int CONFIG_REGISTER = 0x0B;
const int X_LSB_REGISTER = 0x01;
const int STATUS_REGISTER = 0x09;

Adafruit_BME280 bme;
Servo servo;

int angle;

// Setup functions
void setup_BME280();
void setup_QMC5883P();

// Control/data functions
void read_data();
void steering();

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  setup_BME280();
  setup_QMC5883P();
  servo.attach(servoPin);
  angle = 0;
}

void loop() {
  read_data();
  steering();
}

// ---------------------------------------------------------------------------------------------------- //

void setup_BME280() {
  if (!bme.begin(BME280_ADDR)) {
    Serial.println("Sensor not found!");
    while (true);
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

void setup_QMC5883P() {
  // Set continuous measurement mode, 200Hz output rate
  Wire.beginTransmission(QMC5883P_ADDRESS);
  Wire.write(MODE_REGISTER);
  Wire.write(0xCF);
  Wire.endTransmission();

  // Enable Set/Reset, range ±8 Gauss
  Wire.beginTransmission(QMC5883P_ADDRESS);
  Wire.write(CONFIG_REGISTER);
  Wire.write(0x08);
  Wire.endTransmission();
}

void read_data() {
  float temperature = bme.readTemperature();
  float pressure = bme.readPressure();
  float humidity = bme.readHumidity();

  Serial.print(temperature); Serial.print(",");
  Serial.print(pressure); Serial.print(",");
  Serial.print(humidity); Serial.print(",");

  // ------------------------------------------------------

  Wire.beginTransmission(QMC5883P_ADDRESS);
  Wire.write(X_LSB_REGISTER);
  Wire.endTransmission(false);

  // Read 6 bytes: X_LSB, X_MSB, Y_LSB, Y_MSB, Z_LSB, Z_MSB
  Wire.requestFrom(QMC5883P_ADDRESS, 6);

  if (Wire.available() == 6) {
    byte xLow  = Wire.read();
    byte xHigh = Wire.read();
    byte yLow  = Wire.read();
    byte yHigh = Wire.read();
    byte zLow  = Wire.read();
    byte zHigh = Wire.read();

    float scale = 800.0 / 32768.0;
    int16_t xValue = ((xHigh << 8) | xLow) * scale;
    int16_t yValue = ((yHigh << 8) | yLow) * scale;
    int16_t zValue = ((zHigh << 8) | zLow) * scale;

    Serial.print(xValue); Serial.print(",");
    Serial.print(yValue); Serial.print(",");
    Serial.println(zValue);
  }

  delay(100);
}

void steering() {
  for (angle = 0; angle <= 180; angle += 10) 
  {
    servo.write(angle);
    delay(20);
  }

  for (angle = 180; angle >= 0; angle -= 10)
  {
    servo.write(angle);
    delay(20);
  }
}

