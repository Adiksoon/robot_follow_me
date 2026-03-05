# Cel dokumentu

Celem tego dokumentu jest opisanie aktualnej i planowanej architektury systemu ROS2
w sposób umożliwiający:

- świadome podejmowanie decyzji implementacyjnych,
- utrzymanie spójności projektu w czasie,
- szybkie odtworzenie kontekstu projektowego po przerwach.

Dokument opisuje **strukturę logiczną systemu**, a nie szczegóły algorytmiczne.

---

### Stos Technologiczny

Projekt realizowany jest w oparciu o:

- **Hardware:** Raspberry Pi 4 + Platforma PiRacer (układ Ackermann) + Kamera OAK-D Lite [4, 6].
- **System operacyjny:** Ubuntu 22.04 (Server).
- **Middleware:** ROS2 Humble [1].
- **Język:** Python (ament_python).
- **Środowisko uruchomieniowe:** Ignition Gazebo (Fortress) – symulacja fizyki i sensora kame

### Koncepcja Sterowania (Sterowanie Kaskadowe)

Zgodnie z założeniami pracy, architektura została rozdzielona na dwie warstwy [4]:

1. **Warstwa Nadrzędna (High-Level - Vision & Decision):**
   - Analiza obrazu z OAK-D Lite (detekcja/klasyfikacja obiektu).
   - Estymacja odległości i błędu kątowego względem celu.
   - Generowanie komend ruchu (prędkość liniowa i kątowa).

2. **Warstwa Podrzędna (Low-Level - Hardware Control):**
   - Przeliczanie komend ruchu na specyfikę układu **Ackermanna** [5].
   - Regulator PID prędkości kół (obsługa enkoderów i PWM) [7].
   - Bezpośrednie sterowanie serwem skrętu.

### Workspace

### Struktura Pakietów (ROS2 Packages)

System został podzielony na **7 pakietów**, co zapewnia wysoką modularność i separację poszczególnych funkcji systemu:

1. **`robot_description`**
   - Przechowuje opis fizyczny robota (URDF, XACRO, siatki).
   - Definiuje ramy odniesienia (Transforms - TF).

2. **`robot_simulation`**
   - Zawiera pliki startowe (`launch`) dla symulatora Ignition Gazebo.
   - Definiuje światy wirtualne (`.sdf`) i mostek ROS-Ignition.

3. **`robot_calibration`** (Warstwa Konfiguracji)
   - Odpowiada za inicjalizację parametrów śledzenia przed rozpoczęciem jazdy.
   - Pozwala na wybór obiektu do śledzenia.

4. **`robot_perception`** (Warstwa Wizyjna)
   - Obsługuje kamerę OAK-D Lite.
   - Realizuje detekcję obiektów i estymację ich odległości od robota.

5. **`robot_control`** (Warstwa Nadrzędna - High Level)
   - Realizuje algorytm "Follow Me" (Regulator $G_{C2}$).
   - Wyznacza zadaną trajektorię ruchu (prędkość liniową i kąt skrętu).

6. **`piracer_control`** (Warstwa Podrzędna - Low Level)
   - Realizuje regulator PID prędkości ($G_{C1}$) oraz kinematykę Ackermanna.
   - Przelicza komendy ruchu na sygnały sterujące elementami wykonawczymi.
   - Odometria on na podstawie encoder_reader_node i tematu /wheel_speed znając rozstaw osi i promien kol oblicza obecna pozycje robota. Serwa nie mierza kata z jakim sa skrecone z tego wzgledu odometry_node musi subskrybowac /cmd_ackermann. Publikuje temat /odom (gdzie robot się znajduje)

7. **`robot_hardware_interface`** (Warstwa Sprzętowa - HAL)
   - Bezpośrednia obsługa sterowników sprzętowych (PWM, GPIO).

---

### Architektura Węzłów (Nodes) i Przepływ Danych (Topics)

1. Pakiet robot_calibration: Initialization_node pub:/Taget_config sub: Follow_Me_node & Target_Detection_Node
2. Pakiet robot_perception: Target_Detection_node pub:/Target_Detection pub:Estimate_Target_node. Estimate_Target_node pub:/Target_Pose sub:/Follow_Me_node
3. Pakiet robot_control: Follow_Me_node pub:/cmd_ackermann sub:/PiRacer_Control_node & odometry_node
4. Pakiet piracer_control: PiRacer_Control_node pub:/cmd_motion sub: PWM_Driver_node; pub:/Steering_Servo sub:Servo_Driver_node; odometry_node pub:/odom sub:/follow_me_node
5. Pakiet robot_hardware_interface: PWM_Driver_node, Servo_Driver_node, Encoder_Reader_node pub:/Wheel_speed sub:PiRacer_Control_Node & odometry_node

###uchyby beda liczone wzgledem base_linka; z tego wzgledu nalezy zrobic tf /target_pose do base_link

#Follow_me_node.py

Node realizujący funkcję regulatora nadrzędnego GC2 w kaskadowej
strukturze sterowania robota mobilnego.

Node działa deterministycznie (stały okres próbkowania Ts).

Subskrybowane tematy:
- /target_config  → konfiguracja zadania (wartość zadana odległości, tryb pracy)
- /target_pose    → pozycja celu względem kamery (camera_link) -> tf do (base_link)
- /odom           → estymacja stanu robota (pozycja i orientacja base_link)

Wewn. maszyna stanow:
Tryby pracy:
-CALIBRATING
-TRACKING
-SEARCHING
-STOPPED

Dwa regulatory sprzezone SISO
Follow_me_node
│
├─ Subscribers
│   ├─ /target_config
│   ├─ /target_pose
│   └─ /odom
│
├─ TF
│   camera_link → base_link
│
├─ FSM (state machine)
│   CALIBRATING
│   TRACKING
│   SEARCHING
│   STOPPED
│
├─ Controller (GC2)
│   distance controller → v
│   heading controller  → φ
│
└─ Publisher
    /cmd_ackermann

### Workspace Layout

```text
ros2_ws/
├── docker/
│   ├── Dockerfile              # Definicja obrazu deweloperskiego
│   └── docker-compose.yml      # Konfiguracja uruchomieniowa (wolumeny, GUI, sieć)
├── src/
│   ├── robot_description/      # URDF, Meshes
│   ├── robot_simulation/       # Gazebo worlds, launch files
│   └── robot_calibration/
│   ├── robot_perception/       # Detekcja, obsługa OAK-D
│   ├── robot_control/          # Logika Follow-Me (High-Level PID)
│   └── piracer_driver/         # Obsługa sprzętu (Low-Level PID + Ackermann)
│   └── robot_hardware_interface/
```
