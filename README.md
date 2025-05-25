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

1. Descărcați și instalați Thonny IDE de pe site-ul oficial: [https://thonny.org](https://thonny.org)
2. După instalare, porniți Thonny și asigurați-vă că puteți selecta interpreterul MicroPython pentru Raspberry Pi Pico W:

   * Mergeți la **Tools → Options → Interpreter**
   * Alegeți **MicroPython (Raspberry Pi Pico)**

### 2. Configurarea plăcuței Raspberry Pi Pico 2W

1. Conectați Raspberry Pi Pico 2W la calculator prin cablul USB.
2. Dacă este prima utilizare, țineți apăsat butonul BOOTSEL pe Pico W și conectați USB pentru a intra în modul bootloader.
3. Copiați firmware-ul MicroPython (`.uf2`) pe placa Pico 2W din pagina oficială Raspberry Pi.
4. Închideți și reconectați placa fără a mai apăsa BOOTSEL.
5. În Thonny, selectați portul serial corect (COMx pe Windows sau `/dev/ttyACM0` pe Linux/macOS).

### 3. Conectarea senzorilor și componentelor

TODO

### 4. Implementarea logicii în cod

1. Deschideți un fișier nou în Thonny și lipiți codul furnizat (`main.py`).
2. Configurați rețeaua Wi-Fi:

   ```python
   SSID = 'NumeleRețelei'
   PASS = 'ParolaWiFi'
   ```
3. Ajustați pragurile după preferințe:

   ```python
   MIN_WATER_PCT = 20.0      # Prag minim apă (%) pentru a permite udarea manuală
   SOIL_TARGET = 40.0        # Umiditate țintă a solului (%)
   LED_ON_THRESHOLD = 30.0   # Prag pornire LED (% apă)
   LED_OFF_THRESHOLD = 90.0  # Prag oprire LED (% apă)
   ```
4. Salvați fișierul cu numele `main.py` pe placa Pico W.

### 5. Testare și utilizare

1. După salvare, Pico W va reporni și va inițializa serverul web.
2. Deschideți un browser și accesați IP-ul afișat în consola Thonny (de exemplu `http://192.168.4.2`).
3. Interfața web afișează:

   * **Indicatori analogici** pentru nivelul apei și umiditatea solului
   * **Buton** pentru pornirea manuală a pompei atunci când nivelul apei este suficient
4. Monitorizați și reglați parametrii după necesități.

---

## Extensii posibile

* Implementarea autentificării pe interfața web
* Înregistrarea datelor și vizualizarea istorică (grafice)
* Notificări prin e-mail sau aplicație mobilă
* Integrare cu platforme IoT (Home Assistant, Blynk etc.)

---

Proiect realizat pentru demonstrarea controlului IoT și a utilizării senzorilor cu Raspberry Pi Pico 2W. Spor la implementare!
