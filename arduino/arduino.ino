#define PWML 5
#define PWMR 6

#define MY_5V 8

#define MAX_SPEED 255

#define SET_POINT 5.0 // desired value of sensor output
#define KP 1     // proportional constant
#define KI 0.0  // integrative constant
#define KD 0    // derivative constant

void setup() {
    // put your setup code here, to run once:
    pinMode(PWML, OUTPUT);
    pinMode(PWMR, OUTPUT);
    pinMode(MY_5V, OUTPUT);
    digitalWrite(MY_5V, HIGH);
    // TODO: make speed more clever
    set_speed(50);
}

void loop() {
    set_direction(PID_output());
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
    // TODO: control servo
}

double get_error() {
    double sensor_value;
    // TODO: read sensor
    return (sensor_value-SET_POINT);
}

double PID_output() {
    static double last_error = 0;
    static double integral = 0;
    double error = get_error();
    double derivative;
    integral += error;
    derivative = last_error - error;
    return (error*KP + integral*KI + derivative*KD);
}