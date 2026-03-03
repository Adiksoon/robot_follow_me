Poniżej wklejam koncepcję pracy inżynierskiej (THESIS_CONCEPT.md).
Oceń ją krytycznie pod kątem:

-  poziomu inżynierskiego,
-  spójności zakresu,
-  realności wykonania,
-  potencjalnych ryzyk.
   Nie proponuj rozszerzeń, jeśli nie są konieczne do obrony pracy.

---

Tytuł projektu 
Projekt i implementacja mobilnego robota PiRacer AI realizującego zadanie śledzenia obiektu z wykorzystaniem kamery Luxonis OAK-D Lite w środowisku ROS2. 

 

Cel projektu 
Celem pracy jest opracowanie algorytmu sterowania w architekturze ROS2 na platformie Raspberry Pi 4 oraz dołożenie do mobilnego robota kamery OAK-D Lite, która umożliwi detekcję i klasyfikację obiektu w celu autonomicznego podążania za zadanym obiektem (np. butem użytkownika) lub kolorem. 

 

Zakres projektu 
1. Architektura systemu (Sterowanie Kaskadowe): 
Ze względu na specyfikę przetwarzania obrazu oraz sterowanie w czasie rzeczywistym rozdzieliłem architekturę na dwa poziomy: 

•Warstwa nadrzędna odpowiedzialna za przetwarzanie obrazu (detekcja/klasyfikacja) i generowanie komend prędkości i skrętu. 

 
	•Warstwa podrzędna: Realizowana jako dedykowany węzeł w systemie ROS2 na Raspberry Pi 4 . Odpowiada za bezpośrednią obsługę sprzętu: generowanie sygnałów PWM dla sterownika silników platformy PiRacer oraz odczyt sygnałów z enkoderów w celu stabilizacji prędkości obrotowej kół (programowy regulator PID w pętli wewnętrznej). 

 

------------------------------------------------------------------------------------------------------------------------------- 

2. Zakres funkcjonalności: 
	•Detekcja i Klasyfikacja Obiektu: Wykorzystanie kamery do detekcji wybranego obiektu (buta, piłki) w celu wyznaczenia położenia celu. 

•Estymacja Odległości: do określenia dystansu robota od śledzonego obiektu. 

•Implementacja algorytmu podejmowania decyzji, aby robot nie gubił celu w momencie pojawienia się podobnych obiektów w kadrze. 

•Unikanie przeszkód- podzielona na dwa obszary  
1) robot widzi przeszkodę z daleka -> koryguje tor jazdy   
2) przeszkoda jest zbyt blisko, by ją wyminąć robot zatrzymuje się  
ewentualnie w tym miejscu próbuje się cofać i ominąć przeszkodę (do przemyślenia). 

------------------------------------------------------------------------------------------------------------------------------- 

3. Dodatkowe elementy projektu: 

•Projekt i wykonanie mocowania kamery: Zaprojektowanie w środowisku CAD i wykonanie z wykorzystaniem druku 3D dedykowanego uchwytu montażowego dla kamery OAK-D Lite. Zapewniający odpowiedni kąt nachylenia w celu optymalizacji pola widzenia.	 

•Wizualizacja danych w środowisku ROS (RViz2) do podglądu w czasie rzeczywistym. 

•Symulacja: opracowanie modelu robota w formacie URDF i uruchomienie symulacji w Ignition Gazebo w celu weryfikacji algorytmów przed implementacją na rzeczywistym robocie. 

------------------------------------------------------------------------------------------------------------------------------- 

HARMONOGRAM 

ETAP PROJEKTOWANIE SYSTEMU (Luty) 

▪️Opracowanie modelu matematycznego dla układu kierowniczego typu Ackermann. 

▪️Zaprojektowanie dedykowanego uchwytu montażowego dla kamery. 

▪️Konfiguracja modelu robota (URDF) odwzorowująca geometrię platformy PiRacer. 
 

ETAP INTEGRACJA SPRZĘTOWA (Marzec) 

▪ Montaż uchwytu kamery oraz instalacja dodatkowych enkoderów na kołach napędowych. 

▪Konfiguracja systemu Ubuntu 22.04 oraz środowiska ROS2 Humble na Raspberry Pi4. 

▪ Implementacja węzła ROS2 odpowiedzialnego za obsługę sygnałów PWM oraz odczyt prędkości z enkoderów. 

▪ Implementacja i dostrojenie programowego regulatora PID dla prędkości kół. 

 
 

ETAP OPROGRAMOWANIE WYSOKIEGO POZIAMU (Kwiecień-Sierpień) 

▪ Uruchomienie kamery OAK-D Lite w środowisku ROS2 i implementacja detekcji wybranego obiektu. 

▪ Implementacja algorytmu sterowania utrzymującego obiekt śledzony wg wartości zadanej. 

▪ Implementacja algorytmu zapobiegania gubienia celu PID w pętli zewnętrznej. 

▪ Implementacja algorytmu reakcji na przeszkody. 

▪ Konfiguracja narzędzia RViz2 do zdalnego podglądu stanu robota. 

 

ETAP TESTY I OPRACOWANIE WYNIKÓW (Wrzesień - Październik) 

▪️Przeprowadzenie testów 

▪️Opracowanie wykresów i analiz 

▪️Pisanie i finalizacja pracy 

 

 

 

 

 

 

 

 