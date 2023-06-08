# Rodroizii - Future Engineers

Acesta este repository-ul care conține fișierele cu programele care stau la baza funcționării robotului.

## Descriere

* folderul `detect_cubes` conține în fișierul `main.py` un program care determină ce culoare are cubul care se află în fața robotului.
* folderul `raspberry` contine in fisierul `main.py` programul care se ocupa de miscarea robotului pe harta, in functie de pereti.

## main.py

în `main.py` sunt inițializați senzorii de Time-Of-Flight si Gyro. Este pornit procesul gryo de a calcula continuu unghiul facut cu peretele si procesul de senzor color pentru ca liniile de culoare sa nu fie pierdute (?). Este initializat programul PID (Proportional–Integral–Derivative Control System) si motorul.

## sensors.py

[Sensors.py](../master/src/sensors.py) conține clasele tuturor senzorilor, dar și teste, pentru fiecare clasă, pentru a ne permite să verificăm eficiența programului.

```python
class Color()
```
În acestă clasă se află funcția `color_read()`, care returnează _0_ dacă senzorul de culoare nu vede nici albastru, nici oranj, _1_ dacă vede culoarea oranj și _2_ dacă vede albastru. Această funcție ne ajută pentru detectarea direcției în care merge robotul și pentru a face curbele necesare, în direcția potrivită.
Biblioteca senzorului de culoare ne oferă capacitatea de a primi date prin valori **R**, **G**, **B**. Astfel, folosind o funcție matematică, putem determina culoarea pe care o vede senzorul.

În această clasă, se mai află și funcțiile `power_off()` și `power_on()`, care se ocupă de resetarea senzorului.

```python
class Gyro()
```
Această clasă cuprinde funcția `calculate_angle()`, care folosind viteza unghiulară redată de giroscop, reușește printr-o formulă matematică să ne returneze unghiul la care se află robotul, față de unghiul inițial la care a fost, când acesta a fost pornit.

```python
class Tof()
```
Deoarece senzorii de distanță și senzorul de culoare au aceeași adresă, la inițializarea obiectului folosim instrucțiunile prin care putem să le schimbăm adresa, succesiv, doar la începutul programului. Adresa inițială este _0x29_, iar senzorii de distanță dispun de un pin _XSHUT_, pentru resetare. Astfel, mai întâi avem ambii senzori de distanță conectați și senzorul de culoare oprit (folosind un tranzistor). Apoi, schimbăm adresa senzorilor de distanță, în continuare resetăm un senzor de distanță, apoi îi schimbăm și lui adresa. În final, pornim senzorul de culoare, care rămâne pe adresa inițială, deoarece librăria acestuia nu cuprinde o funcție pentru schimbarea adresei. Toate aceste lucruri se pot apela în funcțiile `change_address()` și `reset_address()`.

Funcția `get_distance()` returnează cu ușurință, printr-o valoare de tip _double_, distanța pe care o face cu peretele, în centrimetri.

## motors.py
În fișierul [motors.py](../master/src/motors.py) se află codul necesar controlării servomotorului și a motorului responsabil de mișcarea mașinii.
```python
class Motors()
```
La început se ințializează niște limite pentru puterea motoarelor și pentru minimul și maximul la care funcționează servomotorul, dar și pinii necesari pentru control.

În această clasă se află funcția `set_speed()`, care inițial verifică integritatea parametrilor și îi încadrează între limite, dacă este cazul, apoi, în funcție de viteza setată, trimite date pe pinii _PWM_, pentru a determina mișcarea mașinii.

În aceeași clasă se află și funcția `set_direction`, care primește ca parametru unghiul dorit, pe care să îl facă servomotorul, iar apoi printr-un _mapping_ calculat, transformă aceste valori și modifică orientarea roților.
## pid.py
Fișierul [pid.py](../master/src/pid.py) conține codul esențial pentru eficientizarea mișcării robotului. 
Folosind PID, putem reduce eroarea, prin componentele de proporționalitate, derivatele și integralele.

Funcția `set_point()`, setează pentru PID-ul senzorilor de distanță, valoarea dorită pentru a determina distanța mașinii față de perete.

Pentru a reuși integrarea cât mai eficientă a componentelor, folosim un PID pentru giroscop și unul pentru senzorii de distanță. 

Prin funcția `get_error`, îmbinăm unghiul de la giroscop cu distanța față de perete, astfel, reușim să îndreptăm robotul pe traseu, acesta urmânt un curs cât mai eficient. Aici setăm peretele după care să se orienteze și returnăm eroarea, pe care robotul trebuie să o aducă cât mai aproape de 0.

Funcția `get_output()`, esențială pentru eficiența programului, calculează și returnează unghiul la care robotul trebuie să se orienteze pentru a face schimbări mici, prin care acesta să ajungă pe drumul potrivit.

## SSH

Modul de comunicare cu placa Raspberry Pi este prin SSH (Secure Shell), un protocol de comunicare securizat prin care placa poate să fie accesată de pe orice dispozitiv oferind acces la un terminal. Conectarea se face prin comanda `ssh [user]@[ipadress] -p [port]` unde user este user-ul de pe placa (implicit "pi"); ipadress este adresa ip locala a placii si port este portul ssh deschis pe placa (implicit 22) de exemplu modul implicit de conectare arata asa: `ssh pi@192.168.x.x -p 22` si cand este solicitata se introduce parola user-ului, setata in momentul crearii imaginii si sistemului de operare (implicit raspberry). 

## Instructiuni instalare 

1. Instalarea sistemului de operare pe placa raspberry
2. Conectarea prin SSH la placa
3. Clonarea repository-ului de git: `git clone git@github.com:inventronica/druid-rc.git` 
4. Deschiderea folderului; `cd druid-rc/raspberry`
5. Rularea aplicatiei cu comanda `python3 main.py`


## Conexiunea cu raspberry 

Descarca si instaleaza Raspberry Pi Imager pe un calculator cu un cititor de carduri SD. Pune cardul SD pe care o sa il folosesti cu Raspberry Pi in cititor si deschide Raspberry Pi Imager. 
www.raspberrypi.com/software/



