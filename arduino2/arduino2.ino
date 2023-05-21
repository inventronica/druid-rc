#include "HCSR04.h"
#include <ESP32_Servo.h>
#include <stdio.h>

#include <Wire.h>
#include "LIDARLite_v4LED.h"

LIDARLite_v4LED myLIDAR;

#define INA 18 // R_IS
#define INB 19 // L_IS
#define PWM 23 // R_PWM

#define MAX_SPEED 48
#define MIN_SERVO 70
#define MAX_SERVO 170
#define SERVO_PIN 32

double set_point = 30.0; // desired value of sensor output
double kp = 2.0;
double ki = 0.0;  // integrative constant
double kd = 0.0;    // derivative constant
double damp = 0.5;
#define LOGS true
#define DEBUG false

Servo myservo;

void setup() {
    // if(LOGS)
    Serial.begin(9600);
    if (DEBUG)
        Serial.println("START SETUP");

    // while (!Serial) {}
    // Serial.begin(115200);
    Wire.begin();
    Wire.setClock(400000); // use 400 kHz I2C
    // sensor.setTimeout(500);
    if (DEBUG)
        Serial.println("1");
    if (myLIDAR.begin() == false) {
        Serial.println("Failed to detect and initialize sensor!");
        while (1);
    }
    if (DEBUG)
        Serial.println("2");
    // sensor.setDistanceMode(VL53L10X::Long);
    // sensor.setMeasurementTimingBudget(50000);
    // sensor.startContinuous();
    // put your setup code here, to run once:
    pinMode(INA, OUTPUT);
    pinMode(INB, OUTPUT);
    pinMode(PWM, OUTPUT);
    // TODO: make speed more clever
    myservo.attach(SERVO_PIN);  // attaches the servo on pin 9 to the servo object
    set_speed(MAX_SPEED);
    if (DEBUG)
        Serial.println("END OF SETUP");

    
}

void loop() {
    if (DEBUG)
        Serial.println("BEGINING OF LOOP");
    // if (Serial.available() > 0) {
    //     String incomingString = Serial.readStringUntil('\n');
    //     Serial.print("I received: ");
    //     Serial.println(incomingString);
    //     int a, b, c, d;
    //     sscanf(incomingString.c_str(), "%d %d %d %d", &a, &b, &c, &d);
    //     set_point=a/1000.0, kp=b/1000.0, ki=c/1000.0, kd=d/1000.0;
    // }
    int output = PID_output();
    set_direction(output);
}

void set_speed(int my_speed) {
    if(my_speed > MAX_SPEED) my_speed = MAX_SPEED;
    if(my_speed < -MAX_SPEED) my_speed = -MAX_SPEED;
    if(my_speed > 0) {
        digitalWrite(INA, HIGH);
        digitalWrite(INB, LOW);
        analogWrite(PWM, my_speed);
    }
    else if(my_speed < 0) {
        digitalWrite(INA, LOW);
        digitalWrite(INB, HIGH);
        analogWrite(PWM, -my_speed);
    }
    else {
        digitalWrite(INA, HIGH);
        digitalWrite(INB, HIGH);
    }
    return;
}


void set_direction(int position) {
    if (position < -100) position = -100;
    if (position > 100) position = 100;
    position = map(position, 100, -100, MIN_SERVO, MAX_SERVO);
    myservo.write(position);
    Serial.print(" Servo: ");
    Serial.println(position);
}

double get_error_tof() {
    static double output = 0;
    double sensor_value = myLIDAR.getDistance();
    if(LOGS){
        Serial.print(" Sensor: ");
        Serial.print(sensor_value);
        Serial.print(" Sensor status: ");
        // Serial.print(sensor.ranging_data.range_status);
    }
    // if (sensor.ranging_data.range_status != 0) sensor_value = set_point+20;
    // else if (sensor_value > set_point+20) sensor_value = set_point+20;
    // else if (sensor_value < set_point-20) sensor_value = set_point-20;
    output = sensor_value-set_point;
    Serial.print("Sensor: ");
    Serial.print(output);
    return (output);
}

int PID_output() {
    double error = get_error_tof();
    if(LOGS) {
        Serial.print(" Error: ");
        Serial.print(error);
    }
    static double integral = 0;
    integral = integral * damp + error;
    static double last_error = 0;
    double derivative = error - last_error;
    last_error = error;
    int output = int(error*kp + integral*ki + derivative*kd);
    if(LOGS) {
        Serial.print(" Output: ");
        Serial.println(output);
    }
    return output;
}