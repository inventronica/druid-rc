#include <Servo.h>

#define MIN_SERVO 40
#define MAX_SERVO 140
#define SERVO_PIN 6
#define INA 10
#define INB 12
#define PWM 3
#define MAX_SPEED 255

Servo myservo;
int pos=0;
#define TEST_FUNCTION false

void setup()  {
    Serial.begin(9600);
    myservo.attach(SERVO_PIN);
    pinMode(INA, OUTPUT);
    pinMode(INB, OUTPUT);
    pinMode(PWM, OUTPUT);
}

void loop() {
//  analogWrite(PWM, 155);
    if(Serial.available()>0) {
        pos = Serial.parseInt();
        Serial.println(pos);
        if(TEST_FUNCTION) {
////            set_direction(pos);
            set_speed(pos);
////            analogWrite(PWM, pos);
        }
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
