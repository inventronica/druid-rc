# druid-rc

Acesta este repo-ul care contine fisierele cu programele care stau la baza functionarii robotului.

## Descriere

* folderul `detect_cubes` contine in fisierul `main.py` un program care determina ce culoare are cubul care se afla in fata robotului.
* folderul `raspberry` contine in fisierul `main.py` programul care se ocupa de miscarea robotului pe harta, in functie de pereti.
* folderul `servo_calib` contine in fisierul `servo_calib.ino` calibrarea servo-motorului de pe robot.

## main.py

In `main.py` sunt initializati senzorii de Time-Of-Flight si Gyro. Este pornit procesul gryo de a calcula continuu unghiul facut cu peretele si procesul de senzor color pentru ca liniile de culoare sa nu fie pierdute (?). Este initializat programul PID (Proportional–Integral–Derivative Control System) si motorul.

## sensors.py

## motors.py

## pid.py

## Conexiunea cu raspberry 

Descarca si instaleaza Raspberry Pi Imager pe un calculator cu un cititor de carduri SD. Pune cardul SD pe care o sa il folosesti cu Raspberry Pi in cititor si deschide Raspberry Pi Imager. 
www.raspberrypi.com/software/



