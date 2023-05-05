#include <Servo.h>

#define MIN_SERVO 40
#define MAX_SERVO 140
#define SERVO_PIN 9

Servo myservo;
int pos=90;
#define TEST_FUNCTION false

void setup() {
    Serial.begin(9600);
    myservo.attach(SERVO_PIN);
}

void loop() {
    if(Serial.available()>0) {
        pos = Serial.parseInt();
        Serial.println(pos);
        if(TEST_FUNCTION)
            set_direction(pos);
        else
            myservo.write(pos);
    }
}

void set_direction(int position) {
    if (position < -100) position = -100;
    if (position > 100) position = 100;
    position = map(position, 100, -100, MIN_SERVO, MAX_SERVO);
    myservo.write(position);
}