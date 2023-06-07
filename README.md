# druid-rc

Acesta este repo-ul care conține fișierele cu programele care stau la baza funcționării robotului.

## Descriere

* folderul `detect_cubes` contine in fisierul `main.py` un program care determina ce culoare are cubul care se afla in fata robotului.
* folderul `raspberry` contine in fisierul `main.py` programul care se ocupa de miscarea robotului pe harta, in functie de pereti.

## main.py

In `main.py` sunt initializati senzorii de Time-Of-Flight si Gyro. Este pornit procesul gryo de a calcula continuu unghiul facut cu peretele si procesul de senzor color pentru ca liniile de culoare sa nu fie pierdute (?). Este initializat programul PID (Proportional–Integral–Derivative Control System) si motorul.

## sensors.py

## motors.py

## pid.py

## SSH

Modul de comunicare cu placa Raspberry Pi este prin SSH (Secure Shell), un protocol de comunicare securizat prin care placa poate sa fie accesata de pe orice dispozitiv oferind acces la un terminal. Conectarea se face prin comanda `ssh [user]@[ipadress] -p [port]` unde user este user-ul de pe placa (implicit "pi"); ipadress este adresa ip locala a placii si port este portul ssh deschis pe placa (implicit 22) de exemplu modul implicit de conectare arata asa: `ssh pi@192.168.x.x -p 22` si cand este solicitata se introduce parola user-ului, setata in momentul crearii imaginii si sistemului de operare (implicit raspberry). 

## Instructiuni instalare 

1. Instalarea sistemului de operare pe placa raspberry
2. Conectarea prin SSH la placa
3. Clonarea repository-ului de git: `git clone git@github.com:inventronica/druid-rc.git` 
4. Deschiderea folderului; `cd druid-rc/raspberry`
5. Rularea aplicatiei cu comanda `python3 main.py`


## Conexiunea cu raspberry 

Descarca si instaleaza Raspberry Pi Imager pe un calculator cu un cititor de carduri SD. Pune cardul SD pe care o sa il folosesti cu Raspberry Pi in cititor si deschide Raspberry Pi Imager. 
www.raspberrypi.com/software/



