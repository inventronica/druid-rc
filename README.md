# Rodroizii - Future Engineers

Acesta este repository-ul care conține fișierele cu programele care stau la baza funcționării robotului.

## Descriere

* folderul [`detect_cubes`](../master/src/detect_cubes) conține în fișierul [`main.py`](../master/src/detect_cubes/main.py) un program care determină ce culoare are cubul care se află în fața robotului.
* folderul [`src`](../master/src) conține în fișierul [`main.py`](../master/src/main.py) programul care se ocupă de toată misiunea de pe hartă.

## main.py

în [`main.py`](../master/src/main.py) sunt inițializați senzorii de Time-Of-Flight și Gyro. Aici se află și:
```python
class CubeDetection()
```
În această clasă se inițializează camera și verifică prin funcția `update_next()`, ce culoare are următorul cub, folosind aria pe care o are cadranul în care este inclus cubul. Astfel, o arie mai mare, înseamnă că paralelipipedul este mai aproape de robot.

Folosind funcțiile din [follower.py](../master/src/follower.py), putem schimba "banda" pe care se află robotul, adică în cazul cuburilor verzi, robotul le va ocoli prin stânga, iar în cazul celor roșii, le va ocoli prin dreapta. 


## [follower.py](../master/src/follower.py)

[Follower.py](../master/src/follower.py) conține funcțiile necesare mișcării robotului pe hartă, orientându-se după giroscop și senzorii de distanță și de culoare. 

```python
class Follower()
```
Aici se inițializează componentele `gyro` și `pid (pentru disanță)`. Tot în `__init__` se modifică și adresele senzorilor, pentru a funcționa totul cum trebuie. Procesele din spate se inițializează tot în această parte a clasei, pentru a putea citi senzorii independent de restul proceselor din program.

Funcția `run_follower()` se ocupă de urmărirea pereților și de păstrarea distanței față de aceștia. Aceasta este și funcția necesară pentru etapa de calificare, unde nu există obstacole pe hartă. Funcția lucrează cu PID-ul distanței, împreună cu cel al giroscopului pentru a crea un traseu optim pentru robot.

Funcția `run_gyro_follower` face un lucru asemănător cu funcția `run_follower()`, doar că distanța setată, va reprezenta unghiul la care vrem să ajungem.

`change_lane()`, folosește niște instrucțiuni prin care robotul poate să schimbe "banda" pe care se află. Pentru a fi un transfer cât mai sigur, robotul va face mai întâi un unghi de 45<sup>o</sup> față de unghiul la care se afla înainte, iar apoi se redresează pe traiectoria inițială, însă cu peretele verificat de senzorul de distanță schimbat.

## [sensors.py](../master/src/sensors.py)

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

## [motors.py](../master/src/motors.py)
În fișierul [motors.py](../master/src/motors.py) se află codul necesar controlării servomotorului și a motorului responsabil de mișcarea mașinii.
```python
class Motors()
```
La început se ințializează niște limite pentru puterea motoarelor și pentru minimul și maximul la care funcționează servomotorul, dar și pinii necesari pentru control.

În această clasă se află funcția `set_speed()`, care inițial verifică integritatea parametrilor și îi încadrează între limite, dacă este cazul, apoi, în funcție de viteza setată, trimite date pe pinii _PWM_, pentru a determina mișcarea mașinii.

În aceeași clasă se află și funcția `set_direction`, care primește ca parametru unghiul dorit, pe care să îl facă servomotorul, iar apoi printr-un _mapping_ calculat, transformă aceste valori și modifică orientarea roților.
## [pid.py](../master/src/pid.py)
Fișierul [pid.py](../master/src/pid.py) conține codul esențial pentru eficientizarea mișcării robotului. 
Folosind PID, putem reduce eroarea, prin componentele de proporționalitate, derivatele și integralele.

Funcția `set_point()`, setează pentru PID-ul senzorilor de distanță, valoarea dorită pentru a determina distanța mașinii față de perete.

Pentru a reuși integrarea cât mai eficientă a componentelor, folosim un PID pentru giroscop și unul pentru senzorii de distanță. 

Prin funcția `get_error`, îmbinăm unghiul de la giroscop cu distanța față de perete, astfel, reușim să îndreptăm robotul pe traseu, acesta urmânt un curs cât mai eficient. Aici setăm peretele după care să se orienteze și returnăm eroarea, pe care robotul trebuie să o aducă cât mai aproape de 0.

Funcția `get_output()`, esențială pentru eficiența programului, calculează și returnează unghiul la care robotul trebuie să se orienteze pentru a face schimbări mici, prin care acesta să ajungă pe drumul potrivit.

> [dependencies.txt](../master/dependencies.txt) este fișierul de pe care, la instalarea codului, trebuie inserate comenzile responsabile de încărcarea bibliotecilor necesare funcționării.

## Conectarea prin SSH

Modul de comunicare cu placa Raspberry Pi este prin SSH (Secure Shell), un protocol de comunicare securizat prin care placa poate să fie accesată de pe orice dispozitiv oferind acces la un terminal. Conectarea se face prin comanda `ssh [user]@[ipadress] -p [port]` unde user este user-ul de pe placă (implicit "pi"); ipadress este adresa ip locală a plăcii și port este portul ssh deschis pe placă (implicit 22) de exemplu modul implicit de conectare arată așa: `ssh pi@192.168.x.x -p 22` și când este solicitată, se introduce parola user-ului, setată în momentul creării imaginii și sistemului de operare (implicit _raspberry_). 

## Instrucțiuni instalare 

1. Instalarea sistemului de operare pe placa raspberry
2. Conectarea prin SSH la placă
3. Clonarea repository-ului de git: `git clone git@github.com:inventronica/druid-rc.git` 
4. Instalarea bibliotecilor din fișierul [dependencies.txt](../master/dependencies.txt), prin terminalul plăcii
5. Deschiderea folderului: `cd druid-rc/src/`
6. Rularea aplicației cu comanda `python3 main.py`


## Conexiunea cu Raspberry 

Descarcă și instalează [Raspberry Pi Imager](https://www.raspberrypi.com/software) pe un calculator cu un cititor de carduri SD. Pune cardul SD pe care îl vei folosi cu Raspberry Pi în cititor și deschide Raspberry Pi Imager. Urmează pașii de instalare din aplicație, apoi introdu cardul SD în placă și bucură-te de noul tău sistem de operare.



