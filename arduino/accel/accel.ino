#include <Wire.h>
// библиотека для работы с модулями IMU
#include <TroykaIMU.h>
Accelerometer accel;

// Переменные для данных с гироскопа и акселерометра
float gx, gy, gz, ax, ay, az;

void setup() {
  accel.begin(); //Подключаем акселерометр
  Serial.begin(38400);

}

void loop() {
  float x, y, z;
  int b = 0.5;
  int c = 2;
  accel.readAXYZ(&x, &y, &z);
  int speed = sqrt((pow(x, c) + pow(y, c)));
  Serial.print(abs(x));Serial.print("\t");Serial.print(abs(y));Serial.print("\t");Serial.print(abs(z));
  Serial.print("\t");Serial.println(speed);
  // Serial.write((uint8_t)(x));

}
