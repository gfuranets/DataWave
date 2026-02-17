#include <Servo.h>

#define SERVO_PIN 26

Servo servo;
int pos = 0;

void setup() {
  Serial.begin(9600);
  servo.attach(SERVO_PIN);
  servo.write(pos);
}

void loop() {
  char cmd;
  if (Serial.available()) {
    cmd = Serial.read();

    if (cmd == 'A') {
      pos += 10;
      if (pos > 180) pos = 180;
    }

    if (cmd == 'D') {
      pos -= 10;
      if (pos < 0) pos = 0;
    }
  }

  servo.write(pos);
  delay(10);
}
