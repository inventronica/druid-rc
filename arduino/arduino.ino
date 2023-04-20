#include "HCSR04.h"
#include <Servo.h>
#include <stdio.h>


#include <Wire.h>
#include <VL53L1X.h>

VL53L1X sensor;

#define S0 40
#define S1 41
#define S2 42
#define S3 43
#define Color_Out 44

int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;

int redColor = 0;
int greenColor = 0;
int blueColor = 0;

#define PWML 5
#define PWMR 6

#define MY_5V 8

#define MAX_SPEED 100
#define MIN_SERVO 50
#define MAX_SERVO 104

#define SET_POINT 20.0 // desired value of sensor output
#define KP 7     // proportional constant
#define KI 0.0  // integrative constant
#define KD 0.0    // derivative constant
#define DAMP 0.7
#define LOGS true

Servo myservo;
#define TRIGGER_PIN 12
#define ECHO_PIN 13
UltraSonicDistanceSensor distanceSensor(TRIGGER_PIN, ECHO_PIN);

void setup() {
    // if(LOGS)
         Serial.begin(9600);

    // while (!Serial) {}
    // Serial.begin(115200);
    // Wire.begin();
    // Wire.setClock(400000); // use 400 kHz I2C
    // sensor.setTimeout(500);
    // if (!sensor.init()) {
    //     Serial.println("Failed to detect and initialize sensor!");
    //     while (1);
    // }
    // Use long distance mode and allow up to 50000 us (50 ms) for a measurement.
    // You can change these settings to adjust the performance of the sensor, but
    // the minimum timing budget is 20 ms for short distance mode and 33 ms for
    // medium and long distance modes. See the VL53L1X datasheet for more
    // information on range and timing limits.
    sensor.setDistanceMode(VL53L1X::Long);
    sensor.setMeasurementTimingBudget(50000);
    sensor.startContinuous(50);
    // put your setup code here, to run once:
    pinMode(PWML, OUTPUT);
    pinMode(PWMR, OUTPUT);
    pinMode(MY_5V, OUTPUT);
    digitalWrite(MY_5V, HIGH);
    // TODO: make speed more clever
    myservo.attach(9);  // attaches the servo on pin 9 to the servo object
    set_speed(0);
    set_direction(100);

    pinMode(S0, OUTPUT);
    pinMode(S1, OUTPUT);
    pinMode(S2, OUTPUT);
    pinMode(S3, OUTPUT);
    pinMode(Color_Out, INPUT);
    digitalWrite(S0, HIGH);
    digitalWrite(S1, LOW);



}

void loop() {
    // Serial.println(sensor.read());
    // int output = PID_output();
    // set_direction(output);
    // delay(100);

    //RED
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
    redFrequency = pulseIn(Color_Out, LOW);
    // redColor = map(redFrequency, 70, 120, 255, 0);

    Serial.print("R = ");
    Serial.print(redFrequency);

    //GREEN
    digitalWrite(S2, HIGH);
    digitalWrite(S3, HIGH);
    greenFrequency = pulseIn(Color_Out, LOW);
    Serial.print(" G = ");
    Serial.println(greenFrequency);

    delay(100);



}

void set_speed(int my_speed) {
    if(my_speed > MAX_SPEED) my_speed = MAX_SPEED;
    if(my_speed < -MAX_SPEED) my_speed = -MAX_SPEED;
    if(my_speed > 0) {
        analogWrite(PWMR, my_speed);
        digitalWrite(PWML, LOW);
    }
    else if(my_speed < 0) {
        digitalWrite(PWMR, LOW);
        analogWrite(PWML, my_speed);
    }
    else {
        digitalWrite(PWMR, LOW);
        digitalWrite(PWML, LOW);
    }
    return;
}

void set_direction(int position) {
    if (position < -100) position = -100;
    if (position > 100) position = 100;
    position = map(position, 100, -100, MIN_SERVO, MAX_SERVO);
    myservo.write(position);
}

double get_error_sonic() {
    static double output = SET_POINT;
    double sensor_value = distanceSensor.measureDistanceCm();
    if(LOGS){
        Serial.print(" Sensor: ");
        Serial.print(sensor_value);
    }
    if (sensor_value < 0) return output;
    else if (sensor_value > 70) sensor_value = 70;
    else if (sensor_value < 30) sensor_value = 30;
    output = sensor_value-SET_POINT;
    return (output);
}

double get_error_tof() {
    sensor.read();
    static double output = 0;
    double sensor_value = sensor.ranging_data.range_mm/10.0;
    if(LOGS){
        Serial.print(" Sensor: ");
        Serial.print(sensor_value);
        Serial.print(" Sensor status: ");
        Serial.print(sensor.ranging_data.range_status);
    }
    if (sensor.ranging_data.range_status != 0) sensor_value = SET_POINT+20;
    else if (sensor_value > SET_POINT+20) sensor_value = SET_POINT+20;
    else if (sensor_value < SET_POINT-20) sensor_value = SET_POINT-20;
    output = sensor_value-SET_POINT;
    return (output);
}

int PID_output() {
    double error = get_error_tof();
    if(LOGS) {
        Serial.print(" Error: ");
        Serial.print(error);
    }
    static double integral = 0;
    integral = integral * DAMP + error;
    static double last_error = 0;
    double derivative = last_error - error;
    int output = int(error*KP + integral*KI + derivative*KD);
    if(LOGS) {
        Serial.print(" Output: ");
        Serial.println(output);
    }
    return output;
}