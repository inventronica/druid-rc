#define PWML 5
#define PWMR 6

#define MY_5V 8

#define MAX_SPEED 255

void setup() {
    // put your setup code here, to run once:
    pinMode(PWML, OUTPUT);
    pinMode(PWMR, OUTPUT);
    pinMode(MY_5V, OUTPUT);
    digitalWrite(MY_5V, HIGH);
}

void loop() {
    // put your main code here, to run repeatedly:
    for(int i=-255; i<255; i++) {
        set_speed(i);
        delay(50);
    }
    delay(500);
    for(int i=255; i>-255; i--) {
        set_speed(i);
        delay(50);
    }
//  analogWrite(PWMR, 0);
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
