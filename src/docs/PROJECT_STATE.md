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
