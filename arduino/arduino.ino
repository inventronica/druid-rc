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
#define MIN_SPEED 60
#define MIN_SERVO 30
#define MAX_SERVO 150
#define SERVO_PIN 9

double set_point = 15.0; // desired value of sensor output
double kp = 3.0;
double ki = 0.05;  // integrative constant
double kd = 0.0;  // derivative constant
double damp = 0.5;
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
    Wire.begin();
    Wire.setClock(400000); // use 400 kHz I2C
    sensor.setTimeout(500);
    if (!sensor.init()) {
        Serial.println("Failed to detect and initialize sensor!");
        while (1);
    }
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
    myservo.attach(SERVO_PIN);  // attaches the servo on pin 9 to the servo object
    set_speed(MAX_SPEED);

    pinMode(S0, OUTPUT);
    pinMode(S1, OUTPUT);
    pinMode(S2, OUTPUT);
    pinMode(S3, OUTPUT);
    pinMode(Color_Out, INPUT);
    digitalWrite(S0, HIGH);
    digitalWrite(S1, LOW);
}

void loop() {
    if (Serial.available() > 0) {
        String incomingString = Serial.readStringUntil('\n');
        Serial.print("I received: ");
        Serial.println(incomingString);
        Serial.write("incomingString");
        int a, b, c, d;
        sscanf(incomingString.c_str(), "%d %d %d %d", &a, &b, &c, &d);
        set_point=a/1000.0, kp=b/1000.0, ki=c/1000.0, kd=d/1000.0;
    }
    int output = PID_output();
    set_speed(max(MIN_SPEED, MAX_SPEED-abs(output)));
    set_direction(output);
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

double get_error_tof() {
    sensor.read();
    static double output = 0;
    double sensor_value = sensor.ranging_data.range_mm/10.0;
    // if(LOGS){
    //     Serial.print(" Sensor: ");
    //     Serial.print(sensor_value);
    //     Serial.print(" Sensor status: ");
    //     Serial.print(sensor.ranging_data.range_status);
    // }
    if (sensor.ranging_data.range_status != 0) sensor_value = set_point+20;
    else if (sensor_value > set_point+20) sensor_value = set_point+20;
    else if (sensor_value < set_point-20) sensor_value = set_point-20;
    output = sensor_value-set_point;
    return (output);
}

int PID_output() {
    double error = get_error_tof();
    // if(LOGS) {
    //     Serial.print(" Error: ");
    //     Serial.print(error);
    // }
    static double integral = 0;
    integral = integral * damp + error;
    static double last_error = 0;
    double derivative = error - last_error;
    last_error = error;
    int output = int(error*kp + integral*ki + derivative*kd);
    // if(LOGS) {
    //     Serial.print(" Output: ");
    //     Serial.println(output);
    // }
    return output;
}