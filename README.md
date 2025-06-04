# Smart Pump - Pompă de Apă Inteligentă

## Introducere

Acest proiect vizează realizarea unei pompe de apă inteligente, controlabile de la distanță prin intermediul unui server web încorporat pe un microcontroler Raspberry Pi Pico 2W. Sistemul monitorizează nivelul de apă și umiditatea solului cu ajutorul senzorilor, declanșând pompa automat atunci când sunt îndeplinite condițiile prestabilite. De asemenea, utilizatorul poate porni pompa manual printr-o interfață web simplă și intuitivă.

## Componente și resurse necesare

* Raspberry Pi Pico 2W  
* Senzor de nivel al apei (ADC) cu alimentare digitală  
* Senzor de umiditate a solului (ADC) cu alimentare digitală  
* Pompa de apă și driver (sau tranzistor/MOSFET)  
* LED de semnalizare  
* Cablu USB pentru alimentare și programare  
* Calculator cu Windows/Linux/macOS  

## Proces de implementare

Următorii pași descriu modul de pregătire și implementare a proiectului, astfel încât oricine să poată reproduce și utiliza pompa de apă inteligentă.

### 1. Instalarea Thonny

1. Descărcați și instalați Thonny IDE de pe site-ul oficial: https://thonny.org  
2. După instalare, porniți Thonny și asigurați-vă că puteți selecta interpreterul MicroPython pentru Raspberry Pi Pico W:  
   * Mergeți la Tools → Options → Interpreter  
   * Alegeți MicroPython (Raspberry Pi Pico)

### 2. Configurarea plăcuței Raspberry Pi Pico 2W

1. Conectați Raspberry Pi Pico 2W la calculator prin cablul USB.  
2. Dacă este prima utilizare, țineți apăsat butonul BOOTSEL pe Pico W și conectați USB pentru a intra în modul bootloader.  
3. Copiați firmware-ul MicroPython (.uf2) pe placa Pico 2W din pagina oficială Raspberry Pi.  
4. Închideți și reconectați placa fără a mai apăsa BOOTSEL.  
5. În Thonny, selectați portul serial corect (COMx pe Windows sau /dev/ttyACM0 pe Linux/macOS).

### 3. Conectarea senzorilor și componentelor

| Componentă           | Pin Raspberry Pi Pico 2W | Funcție/Descriere                                 |
|----------------------|--------------------------|--------------------------------------------------|
| Senzor nivel apă     | GP26 (ADC0)              | Citirea nivelului apei (semnal analogic)         |
| Alimentare senzor apă| 3.3V                     | Alimentare senzor nivel apă                       |
| Control senzor apă   | GP0 (GPIO0)              | Control alimentare digitală senzor nivel apă     |
| Senzor umiditate sol | GP27 (ADC1)              | Citirea umidității solului (semnal analogic)     |
| Alimentare senzor sol| 3.3V                     | Alimentare senzor umiditate sol                   |
| Control senzor sol   | GP1 (GPIO1)              | Control alimentare digitală senzor umiditate sol |
| Pompa de apă         | GP6 (GPIO6)              | Control pornire/oprit pompa (prin driver/tranzistor) |
| LED indicator        | GP15 (GPIO15)            | Indică starea sistemului (pornit/oprit)          |
| GND                  | GND                      | Masă comună pentru toate componentele            |
| 3.3V                 | 3.3V                     | Alimentare pentru senzori și placa                |

> Notă: Asigurați-vă că toate componentele au masa (GND) comună pentru a funcționa corect.

### 4. Implementarea logicii în cod

1. Deschideți un fișier nou în Thonny și lipiți codul furnizat (main.py).  
2. Configurați rețeaua Wi-Fi în variabilele SSID și PASS.  
3. Ajustați pragurile de udare și indicatori în cod:  
4. Salvați fișierul cu numele main.py pe placa Pico 2W.

### 5. Testare și utilizare

1. După salvare, Pico 2W va reporni și va inițializa serverul web.  
2. În consola Thonny, va apărea adresa IP locală a plăcii, de exemplu 192.168.4.2.  
3. Deschideți un browser web și accesați adresa IP afișată.  
4. Veți vedea o interfață web cu:  
* Indicatori grafici pentru nivelul apei și umiditatea solului  
* Buton pentru pornirea manuală a pompei, activabil doar dacă nivelul apei este suficient  
5. Monitorizați în timp real și ajustați pragurile după nevoie.

---

## Extensii posibile

* Implementarea autentificării pentru securitatea interfeței web.  
* Înregistrarea și vizualizarea datelor istorice (grafică).  
* Trimiterea notificărilor prin email sau aplicații mobile.  
* Integrarea cu platforme IoT populare (Home Assistant, Blynk, Node-RED).  
* Adăugarea unui sistem de alertă sonoră sau vizuală suplimentară (buzzer).  

---

## Sfaturi și recomandări

* Verificați conexiunile electrice înainte de alimentarea sistemului pentru a evita deteriorarea componentelor.  
* Folosiți surse de alimentare stabile și adecvate pentru pompă și senzori.  
* Pentru medii umede, protejați electronică cu carcase sau izolații corespunzătoare.  
* Testați pragurile de umiditate și nivel apă pentru condițiile locale specifice culturii.  

---

## Licență și mulțumiri

Proiectul este open-source și poate fi extins conform nevoilor. Mulțumiri comunității Raspberry Pi și MicroPython pentru resurse și suport.
