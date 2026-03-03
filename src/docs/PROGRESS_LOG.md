Poniżej fragment PROGRESS_LOG.md – dziennik postępu projektu.
Na tej podstawie:

- napisz tytul w formie ROK-MIESIAC-DZIEN - TYTUL
- napisz co zostalo zrobione nadaj naglowek ### Co zostalo zrobione
- oceń, czy kierunek prac jest sensowny i dlaczego takie kroki zostaly wykonane w ### Dlaczego
- napisz następne kroki kolejności.
  Nie powtarzaj oczywistych rzeczy, skup się na decyzjach technicznych. Napisz to w codex

---

# Progress Log

---

## 2026-02-02 — Projekt startowy / konfiguracja środowiska

### Co zostało zrobione

- Utworzono lokalne repozytorium Git dla projektu `robot_follow_me`.
- Skonfigurowano podstawową strukturę projektu (`README.md`, katalog `docs/`).
- Wykonano pierwszy commit inicjalizujący projekt.
- RepozytoriumS zostało opublikowane na GitHubie.

### Dlaczego

- Celem było ustabilizowanie workflow (Git + GitHub) przed rozpoczęciem implementacji.
- Zapewnienie kontroli wersji i porządku w dokumentacji od pierwszego dnia pracy.

### Decyzje / wnioski

- Przyjęto workflow: małe, logiczne commity + regularny push na GitHuba.
- Repozytorium będzie centralnym punktem pracy nad projektem (kod, dokumentacja, logi).

### Następne kroki

- Uzupełnienie plików `README.md` oraz `THESIS_CONCEPT.md`.
- Przygotowanie środowiska Ubuntu 22.04 pod ROS2 Humble.

## 2026-02-03 — Konfiguracja ROS2 Humble i struktury projektu

### Co zostało zrobione

- Zainstalowano i skonfigurowano ROS2 Humble na Ubuntu 22.04.
- Utworzono workspace ROS2 (`ros2_ws`) wraz z narzędziem budowania `colcon`.
- Utworzono pierwszy własny pakiet ROS2 (`my_first_pkg`) w architekturze `ament_python`.
- Zaimplementowano prosty node testowy i zarejestrowano go jako executable poprzez `setup.py`.
- Przeprowadzono pełny cykl: build → source → uruchomienie node’a (`ros2 run`).
- Zintegrowano workspace ROS2 z istniejącym repozytorium GitHub projektu.
- Skonfigurowano `.gitignore` dla artefaktów generowanych przez ROS2 (`build/`, `install/`, `log/`).
- Wykonano pierwszy commit zawierający kod ROS2 oraz strukturę workspace.

### Dlaczego

- Wczesna konfiguracja środowiska ROS2 minimalizuje ryzyko problemów kompatybilności (Ubuntu ↔ ROS ↔ Python) na późniejszych etapach projektu.
- Integracja z GitHubem na tym etapie zapewnia kontrolę wersji wyłącznie nad kodem i konfiguracją, bez artefaktów builda.

### Następne kroki

- Zdefiniowanie docelowej architektury systemu ROS2 (pakiety, node’y, komunikacja).
- Wybór i konfiguracja środowiska symulacyjnego (Gazebo / Ignition + RViz).

## 2026-02-04 — Konfiguracja środowiska symulacyjnego ROS2 (Ignition Gazebo)

### Co zostało zrobione

- Wybrano **Ignition Gazebo (Fortress)** jako docelowe środowisko symulacyjne projektu.
- Skonfigurowano integrację **ROS2 Humble ↔ Ignition Gazebo** z wykorzystaniem `ros_gz_sim`.
- Utworzono i zweryfikowano logiczny podział pakietów:
   - `robot_description` – opis struktury robota (URDF, zasoby wspólne),
   - `robot_simulation` – środowisko symulacyjne (world, launch, spawn robota).
- Przygotowano minimalny świat symulacyjny oraz mechanizm spawnowania robota do działającego świata.
- Skonfigurowano poprawną instalację zasobów pakietów (`launch`, `worlds`) zgodnie z wymaganiami `ament_python`.
- Zweryfikowano poprawność uruchamiania systemu:
   - start świata w Ignition Gazebo,
   - uruchomienie launch file ROS2,
   - poprawna komunikacja ROS2 ↔ Gazebo.
- Zidentyfikowano problemy stabilności środowiska graficznego jako **niezależne od projektu** (GPU / system), co pozwoliło oddzielić kwestie systemowe od architektury ROS.

---

### Dlaczego

- Wybór Ignition Gazebo zapewnia **spójność z ekosystemem ROS2 oraz Nav2** i umożliwia późniejsze przejście z symulacji na rzeczywisty hardware bez zmiany architektury.
- Wczesne uruchomienie pełnego łańcucha: _ROS2 → launch → symulator → robot_ pozwala ograniczyć ryzyko błędów architektonicznych na późniejszych etapach projektu.
- Rozdzielenie opisu robota od środowiska symulacyjnego wymusza **czystą strukturę systemu** i ułatwia dalsze projektowanie (mechanika, elektronika, sterowanie).
- Zamykanie etapu symulacji na poziomie „działa i jest zweryfikowane” zapobiega niekontrolowanemu rozrostowi zakresu przed zakończeniem fazy projektowania systemu.

---

### Następne kroki

1. Projektowanie robota jako systemu fizycznego:
   - przygotowanie **BOM**,
   - wstępny schemat elektryczny (zasilanie, napęd, enkodery).
2. Opracowanie **modelu kinematycznego robota mobilnego** (napęd różnicowy).
3. Rozszerzenie opisu robota w `robot_description` o:
   - koła,
   - jointy,
   - podstawowe parametry geometryczne.
4. Dopiero po zamknięciu powyższych punktów:
   - implementacja kinematyki w symulacji (diff-drive),
   - uruchomienie sterowania ruchem (`cmd_vel`).

#### 2026-02-11 — Modelowanie matematyczne i weryfikacja założeń sterowania

##### Co zostało zrobione

- **Opracowano model kinematyczny** robota w przestrzeni stanów (podejście _white-box_) dla układu Ackermanna.
   - Zdefiniowano wektor stanu $\mathbf{x} = [x, y, \theta]^T$ oraz wektor sterowań $\mathbf{u} = [v, \phi]^T$.

##### Dlaczego

- Posiadanie modelu analitycznego jest niezbędne do poprawnej implementacji algorytmu sterowania w ROS2 – robot musi „wiedzieć”, jak zadaną prędkość kątową z `cmd_vel` przetłumaczyć na fizyczny kąt wychylenia serwomechanizmu.

##### Następne kroki

1. **Aktualizacja `ARCHITECTURE.md`:** Szczegółowe rozpisanie przepływu danych między węzłami ROS2 z uwzględnieniem interfejsów wynikających z modelu matematycznego.
2. **Implementacja URDF:** Przeniesienie parametrów geometrycznych z modelu (głównie rozstawu osi $L$) do pliku opisu robota w `robot_description`.
3. **Projekt mechaniczny:** Rozpoczęcie prac nad uchwytem kamery (CAD), równolegle do prac programistycznych.

## 2026-02-12 — 2026-02-18 — Implementacja estymacji stanu i konteneryzacja

### Co zostalo zrobione

- Zaimplementowano `odometry_node` odpowiedzialny za obliczanie i publikowanie stanu robota.
- Skonfigurowano rozgłaszanie transformacji układów współrzędnych (**TF**) dla relacji `odom` → `base_link`.
- Wdrożono publikację wiadomości typu `nav_msgs/msg/Odometry` na topicu `/odom`.
- Przeprowadzono weryfikację wizualną w **RViz2**, potwierdzając poprawność modelu kinematycznego poprzez wymuszenie stałych nastaw prędkości liniowej $v$ i kąta skrętu $\phi$.
- Dokonano pełnej migracji środowiska deweloperskiego do **Dockera**, tworząc dedykowane obrazy zawierające ROS2 Humble, Ignition Gazebo oraz niezbędne zależności systemowe.
- Zrestrukturyzowano projekt w celu wsparcia pracy w kontenerach (wolumeny dla kodu źródłowego, przekierowanie X11 dla GUI).

### Dlaczego

- Publikacja TF i Odometrii jest krytycznym warunkiem dla działania stosu nawigacji (Nav2) oraz poprawnej fuzji danych z czujników w późniejszych etapach.
- Test "open-loop" ze stałymi wartościami sterującymi pozwolił na szybką walidację poprawności implementacji równań różniczkowych modelu Ackermanna bez wpływu szumu z sensorów.
- Przejście na Docker zapewnia determinizm środowiska ("works on my machine") i izoluje skomplikowane zależności bibliotek symulatora od systemu gospodarza, co ułatwi skalowanie projektu i CI/CD.

### Nastepne kroki

-



