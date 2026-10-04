# Plan działania MeshMill

## Wsparcie platformy

Windows to platforma w pakiecie. Architektura aplikacji i formaty siatki to:
wieloplatformowe, a przyszłe wydania powinny zawierać natywne pakiety Linux i macOS. Praca na platformie
obejmuje pakowanie, integrację aplikacji, metryki sprzętu, zachowanie systemu plików i automatyzację
testowanie wersji przy jednoczesnym zachowaniu tego samego projektu i przepływów pracy STL w każdym obsługiwanym systemie.

- Dodaj pakiety Linux x86-64 i obsługę CI.
- Dodaj pakiety krzemowe macOS Apple i pakiety x86-64, podpisywanie, notarialne i ubezpieczenie CI.
- Dodaj natywnych dla platformy dostawców metryk CPU, pamięci i GPU za współdzielonym interfejsem.
- Przechowuj zapisane ustawienia, mapowania klawiatury, zachowanie wiersza poleceń i dane projektu w sposób przenośny.

Ten plan działania rejestruje zaplanowane prace. Nie opisuje funkcji dostępnych w bieżącej wersji.

## Zakres

MeshMill zarządza geometrią, gęstością siatki, gęstością punktów, optymalizacją, czyszczeniem, walidacją i STL
wymiany, dzięki czemu duże lub ciężkie pliki siatki pozostają przydatne w dalszych procesach edycji.

Modelowanie ogólnego przeznaczenia, rzeźbienie, malowanie, animacja, renderowanie, kompozycja scen, materiały,
rigging i inne systemy tworzenia treści wykraczają poza ten plan działania. Obowiązuje synteza rozproszona
do operacji zarządzania siatką MeshMill i nie rozszerza produktu do edytora ogólnego.

## Geometria odniesienia

Dołączona siatka kompozytowa jest powszechnym elementem rozwoju obecnych algorytmów i planu działania
praca. Celowo nadmiarowe warstwy i nierówna gęstość umożliwiają powtarzalne porównania
jakość redukcji, analiza gęstości, obsługa nakładania się, operacje regionalne, przetwarzanie poza rdzeniem,
i przyszłą syntezę. Wdrożenia planu działania powinny raportować wyniki w odniesieniu do tego urządzenia i są małe
specjalnie zbudowanych siatek regresji, zamiast optymalizować zachowanie tylko dla jednego modelu.

## Przestrzenie robocze Multi-STL i synteza statystyczna

Obszar roboczy powinien akceptować wiele wejść STL jako oddzielne, niezależnie widoczne obiekty źródłowe.
MeshMill powinien wyrównać te źródła, zmierzyć ich zgodność geometryczną i zsyntetyzować jedno użyteczne
siatki bez zachowywania zduplikowanych powierzchni wewnętrznych lub powtarzającej się geometrii nakładania się.

Planowane zachowanie:

- dodawać, usuwać, ukrywać, izolować, zmieniać kolejność i sprawdzać wiele źródeł STL w jednym obszarze roboczym;
- zachować tożsamość źródła, jednostki, transformacje, granice, rozdzielczość i historię operacji;
- zapewniają automatyczną rejestrację z ręczną kontrolą wyrównania i mierzalną jakością dopasowania;
- przed porównaniem podziel źródła na regiony przestrzenne, tak aby duże dane wejściowe pozostały ograniczone;
- analizować obłożenie, odległość do najbliższej powierzchni, normalną zgodność, lokalną gęstość, wariancję i
  liczba obserwacji w nakładających się regionach;
- klasyfikować pasujące powierzchnie, sprzeczne powierzchnie, szum skanowania, przerwy i unikalną geometrię;
- skonsoliduj statystycznie zgodne powierzchnie w reprezentatywną powierzchnię z zarejestrowanymi danymi
  pewność siebie zamiast układania zduplikowanych trójkątów;
- usuń zamkniętą, zbieżną i współdzieloną geometrię, która nie wnosi żadnych szczegółów kształtu zewnętrznego;
- zachowaj niezachodzącą na siebie geometrię źródłową i eksponuj niejednoznaczne regiony do wizualnej oceny;
- zezwalaj na ważenie według źródła i regionu, gdy jeden skan jest czystszy i bardziej szczegółowy;
- sprawdzić wodoszczelność, granice, normalne, wymiary i topologię po syntezie;
- rejestruje pochodzenie źródła i parametry syntezy, aby połączona siatka była odtwarzalna;
- wyświetl wcześniej oczekiwaną liczbę trójkątów, granice, usunięte nakładanie się i rozkład ufności
  zatwierdzanie zsyntetyzowanego wyniku.

W tym przepływie pracy powinien być używany ten sam pozardzeniowy model indeksu przestrzennego i jednostki roboczej, który jest planowany dla dużych
siatki. Porównanie statystyczne i konsolidacja nakładania się powinny być również dostępne w skali lokalnej
lub zdalne węzły MeshMill.

## Synteza rozproszona

Klaster MeshMill powinien koordynować wiele węzłów działających równolegle na wielu
stacje robocze. Węzeł może sprawdzać, wybierać, redukować, weryfikować, naprawiać lub łączyć przypisany region lub
jednostka pracy. Wersje tekstów pozostają niezależne, dopóki nie zostaną sprawdzone i uwzględnione
do wersji obiektu współdzielonego.

System powinien wspierać:

- równoczesny wkład wielu operatorów i zautomatyzowanych węzłów;
- deterministyczne dane wejściowe, parametry, zależności i wyniki jednostek roboczych;
- planowanie uwzględniające możliwości w oparciu o CPU, GPU, pamięć, algorytmy i bieżące obciążenie;
- partycjonowanie uwzględniające zależności siatek, regionów, przejść walidacyjnych i etapów syntezy;
- trwałe kolejki z możliwością wstrzymywania, wznawiania, anulowania, ponawiania prób, ponownego przypisania i odzyskiwania po awarii;
- artefakty adresowane do treści i kontrole integralności między węzłami;
- odtwarzalna synteza z zarejestrowanego zestawu zaakceptowanych wersji wkładu;
- stacje robocze offline lub połączone sporadycznie, które można zsynchronizować później;
- operacja lokalna z wyraźną kontrolą nad uczestniczącymi węzłami i udostępnionymi danymi projektu.

## Wersjonowana współpraca

Każdy wkład powinien rejestrować wersję obiektu nadrzędnego, wybrany region lub jednostkę pracy, operację,
parametry, tożsamość węzła, znaczniki czasu, zależności, wyniki walidacji i wyjściowa suma kontrolna.

Planowane zachowanie w ramach współpracy:

- projekty zawierają obiekty, gałęzie, punkty kontrolne, wkłady i wersje syntetyczne;
- współautorzy mogą pracować z tej samej wersji nadrzędnej bez wzajemnego nadpisywania;
- nienakładające się wpisy mogą zostać automatycznie połączone po zatwierdzeniu;
- nakładająca się geometria lub niezgodne zależności powodują wyraźny konflikt;
- konflikty umożliwiają wizualne porównanie, wybór na poziomie regionu, zmianę bazy, ponowne uruchomienie i ręczne rozwiązywanie;
- stany przeglądu obejmują oczekujące, zaakceptowane, odrzucone, zastąpione, sprzeczne i włączone;
- ostateczny manifest syntezy identyfikuje każdy włączony wkład i zależność.

## Interfejs koordynacyjny

Aplikacja komputerowa powinna zarządzać pracą rozproszoną bez konieczności korzystania z osobnego wiersza poleceń
lub przepływ pracy związany z administracją serwerem. Planowane widoki obejmują:

- **Projekty:** obiekty, gałęzie, wersje, współautorzy i status syntezy.
- **Klaster:** połączone stacje robocze i węzły, możliwości, stan, obciążenie i bieżące przypisanie.
- **Kolejka:** oczekujące, aktywne, wstrzymane, zablokowane, zakończone niepowodzeniem i ukończone jednostki pracy.
- **Wkład:** autor, węzeł, wersja nadrzędna, region, którego dotyczy problem, parametry, kontrole i stan przeglądu.
- **Porównaj:** zsynchronizowane widoki 3D, różnice w geometrii, metryki i inspekcja granic.
- **Konflikty:** nakładające się regiony, konflikty zależności, wybory rozwiązań i wyniki walidacji.
- **Synteza:** wykres zależności, łączny postęp, wybrane wersje wkładu i wynik końcowy.
- **Historia:** wykres gałęzi, punkty kontrolne, połączenia, wersje syntetyczne i manifesty odtwarzalności.

Widoczny obszar powinien pokazywać własność, przypisane regiony, ukończoną pracę, oczekujące zmiany, konflikty,
i różnice w wersjach bez zmiany podstawowej siatki.

## Koordynacja i transport

Pierwsza faza projektowania powinna zdefiniować granice protokołów przed wyborem transportu. Protokół
powinien oddzielać metadane koordynacyjne od artefaktów o dużej siatce, obsługiwać transfer z możliwością wznawiania oraz
można z nich korzystać w sieci lokalnej bez konta zewnętrznego lub usługi hostowanej.

Wymagane koncepcje koordynacyjne:

- wybór koordynatora lub wyraźnie wybrany koordynator;
- wykrywanie węzłów i ręczna rejestracja węzłów;
- uwierzytelnione sesje i autoryzacja na poziomie projektu;
- dzierżawy i pulsy dotyczące własności pracy;
- idempotentne przesłanie pracy i akceptacja wyników;
- negocjowanie wersji pomiędzy różnymi wydaniami MeshMill;
- uporządkowane zdarzenia dotyczące postępu, dzienników, walidacji, niepowodzeń i ponownych prób;
- odzyskiwanie po przerwaniu pracy koordynatora, stacji roboczej, sieci lub węzła.

## Fazy dostawy

### Faza 0: przetwarzanie dużych oczek poza rdzeniem

Indeks, przesyłanie strumieniowe, pamięć podręczna, jednostka robocza i umowa bezpieczeństwa są udokumentowane w
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Oszacuj liczbę trójkątów i pamięć roboczą przed przydzieleniem całej siatki.
- Otwieraj duże pliki binarne STL jako ograniczone, równomiernie próbkowane przeglądy nawigacji.
- Podziel geometrię w pełnej rozdzielczości na przestrzenne kostki z deterministycznymi nakładającymi się granicami.
- Odczytuj, analizuj i optymalizuj niezależne kostki jednocześnie w ramach CPU i limitów pamięci.
- Przesyłaj strumieniowo poziomy rzutni od zgrubnej do dokładnej, zamiast wymagać pełnej siatki w pamięci.
- Narysuj stan kostki bezpośrednio w rzutni: w kolejce, odczyt, przetwarzanie, ukończona i nieudana.
- Pokaż postęp w poszczególnych kostkach, wypełniając każdą kostkę i zachowując widok całego obiektu na wysokim poziomie.
- Składaj przetworzone kostki z walidacją granic, usuwaniem duplikatów i powtarzalnymi ustawieniami.
- W późniejszych fazach rozszerzaj lokalny program planujący kostki na rozproszone jednostki syntezy.

### Faza 1: wersjonowana baza lokalna

- Zdefiniuj formaty obiektu, operacji, wkładu, gałęzi i manifestu.
- Dodaj obszary robocze obejmujące wiele STL z widocznością dla poszczególnych źródeł, transformacjami, metadanymi i pochodzeniem.
- Dodaj metryki jakości rejestracji i klasyfikację nakładania się przestrzennego.
- Syntetyzuj statystycznie zgodne powierzchnie, usuwając zduplikowaną i zamkniętą geometrię.
- Dodaj wizualny przegląd konfliktów, luk, pewności i geometrii unikalnej dla jednego źródła.
- Zachowaj lokalną historię w sesjach aplikacji.
- Dodaj wizualne porównania siatek i regionów.
- Spraw, aby operacje były deterministyczne i niezależnie odtwarzalne.

### Faza 2: skoordynowane węzły lokalne

- Uruchamiaj węzły robocze na jednej stacji roboczej.
- Dodaj kolejkowanie, raportowanie możliwości, przydzielanie pracy i anulowanie.
- Wyświetl stan węzła i jednostki roboczej w interfejsie użytkownika MeshMill.
- Sprawdź lokalnie partycjonowanie i składanie wyników.

### Faza 3: synteza wielostanowiskowa

- Dodaj uwierzytelnione wykrywanie i rejestrację sieci LAN.
- Przesyłaj wkłady pracy i wyniki oparte na treści, korzystając ze wsparcia w zakresie CV.
- Koordynuj jednoczesną pracę na wielu stacjach roboczych.
- Odzyskaj przypisania po awarii węzła lub sieci.

### Faza 4: wspólne wersjonowanie

- Dodaj współautorów, gałęzie, stany recenzji i uprawnienia.
- Scal nienakładające się wpisy.
- Wykrywaj i rozwiązuj nakładające się konflikty lub konflikty zależności.
- Zsyntetyzuj wybrane wkłady w odtwarzalną wersję obiektową.

### Faza 5: hartowanie produkcyjne

- Dodaj testy zgodności protokołów i obsługę wersji mieszanych.
- Dodaj testy audytu, integralności, korupcji, przerw i odzyskiwania.
- Porównaj wydajność planowania, partycjonowania, przesyłania, łączenia i syntezy.
- Wdrażanie dokumentów, tworzenie kopii zapasowych, migracja i odzyskiwanie incydentów.
