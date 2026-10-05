<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

MeshMill to specjalistyczna aplikacja desktopowa służąca do pracy z geometrią siatkową, która jest
zbyt duża, zbyt gęsta lub trudna w obróbce. Umożliwia szybką inspekcję, analizę gęstości, zaznaczanie obszarów, przycinanie, usuwanie elementów
oraz kontrolowaną redukcję siatki – a wszystko to bez konieczności zakładania konta czy przesyłania geometrii na serwer.

Akcelerowane przez GPU renderowanie OpenGL umożliwia nawigację w rzutni, wybieranie sprzętu, wizualizację gęstości,
i interaktywna kontrola responsywna. Redukcja siatki działa obecnie w oddzielnych natywnych procesach roboczych procesora, (CPU)
utrzymywanie obliczeń długich geometrii z dala od interfejsu.

MeshMill obsługuje siatki pochodzące ze skanerów 3D, plików eksportowanych z systemów CAD i programów do modelowania,
procesów rekonstrukcji, wygenerowanej geometrii oraz innych źródeł. Przygotowuje geometrię do dalszej obróbki w innych edytorach, (STL)
narzędziach produkcyjnych i innych procesach roboczych związanych z siatkami. Ogólne modelowanie, rzeźbienie, animacja,
tworzenie materiałów czy scen wykraczają poza zakres funkcjonalności programu.

## Pobieranie

Pobierz jeden z poniższych plików z sekcji [Wydania GitHub](../../releases):

- `MeshMill-<version>-windows-x64-setup.exe`: instalator dla użytkownika, tworzący skróty w menu Start oraz (opcjonalnie)
  na pulpicie.
- `MeshMill-<version>-windows-x64-portable.zip`: aplikacja przenośna (portable). Wypakuj całe archiwum,
  a następnie uruchom `MeshMill.exe`.

Oba pakiety zawierają niezbędne środowisko uruchomieniowe aplikacji. Użytkownicy końcowi nie instalują zależności Python, Node.js ani
zależności. Wersja stabilna obsługuje systemy Windows 10 i Windows 11 na sprzęcie x64.

Niepodpisane pakiety podglądu krzemu dla systemów Linux x86-64 i macOS Intel/Apple mogą również pojawić się w wydaniach.
Są zbudowane na natywnych modułach uruchamiających hostowanych na GitHubie i przechodzą pakiety testów CLI i próbnych dymów z siatki,
ale nadal wymaga testów na prawdziwym sprzęcie. Zobacz [testowanie podglądu Linuksa i macOS](../../PLATFORM_TESTING.md) (Linux)
przed instalacją lub raportowaniem wyników.

Niepodpisane kompilacje społeczności mogą wyświetlać ostrzeżenie Windows SmartScreen lub macOS Gatekeeper. Zwolnij
sumy kontrolne są wymienione obok każdego wydania.

## Szybki start

1. Otwórz STL.
2. Sprawdź obiekt w trybie wyświetlania: cieniowanym (Shaded), gęstości (Density), szkieletowym (Wireframe) lub wierzchołkowym (Vertices).
3. Wybierz poziom jakości, algorytm oraz docelową liczbę trójkątów.
4. Wybierz **Optymalizuj** (Optimize), aby obliczyć wynik.
5. Porównaj oryginalną i zoptymalizowaną siatkę, a następnie wybierz **Zastosuj** (Apply), aby zatwierdzić operację.
6. Wybierz **Zapisz bieżący stan** (Save current state) lub naciśnij `Ctrl+S`.

MeshMill nigdy nie rozpoczyna optymalizacji tylko dlatego, że zmienił się plik lub ustawienie.

## Możliwości

- Obsługa danych wejściowych w formatach binarnym i ASCII (STL) oraz wyjściowych w formacie binarnym (STL)
- Redukcja Fast QEM z zachowaniem gęstości, kształtu i topologii
- Akcelerowany przez GPU rzutnia OpenGL, wybieranie sprzętu i wizualizacja gęstości
- Natywne procesy robocze geometrii tła do redukcji siatki
- Tryby wyświetlania: cieniowany, gęstość, szkieletowy (wireframe) i wierzchołkowy
- Automatyczne cele redukcji wyznaczane na podstawie geometrii, a nie sztywnego limitu liczby trójkątów
- Wybór wielokątów z możliwością dodawania kolejnych obszarów do zaznaczenia
- Przycinanie, usuwanie lub optymalizacja tylko wybranego obszaru
- Porównywanie wersji siatki (oryginalnej, poprzedniej i bieżącej) przechowywanych w pamięci podręcznej
- Funkcje cofania i ponawiania wprowadzonych zmian w geometrii
- Informacje o odchyleniu wymiarów, stopniu redukcji i szacowanym rozmiarze danych wyjściowych
- Jednostki wyświetlania: milimetry, centymetry, metry, cale i stopy
- Metryki dotyczące CPU, pamięci, GPU oraz aktywności związanej z geometrią
- Ładowanie ograniczonego podglądu w przypadku przekroczenia skonfigurowanego limitu pamięci przez plik binarny STL
- Aplikacje z interfejsem graficznym (GUI) oraz wierszem poleceń
- Przetwarzanie lokalne bez konieczności posiadania konta, przesyłania danych (telemetrii/uploadu) czy korzystania z chmury

## Sprawdź geometrię przed jej zmniejszeniem

Zacieniony wyświetlacz zapewnia wyraźny widok powierzchni i sylwetki. Przydaje się do porównań
zachowanie kształtu przed zastosowaniem przejścia optymalizacyjnego.

![Zacieniony widok MeshMill pokazujący dołączoną przykładową siatkę](../../images/meshmill-shaded.png)

Wyświetlacz wierzchołków przedstawia rzeczywisty rozkład punktów. Gęste obszary skanowania, obszary rzadkie i
nagłe zmiany w próbkowaniu są widoczne bez zmiany geometrii. Rozwinięty panel metryk
śledzi aktywność procesora, pamięci, procesora graficznego i przetwarzania geometrii podczas pracy z siatką. (GPU) (CPU)

![Wyświetlanie wierzchołków MeshMill z rozszerzonymi metrykami wydajności](../../images/meshmill-vertices.png)

Wyświetlacz Wireframe bezpośrednio pokazuje strukturę trójkąta. Pomaga zidentyfikować niepotrzebne zagęszczenie,
nieregularna triangulacja oraz obszary, w których uproszczenie może spowodować usunięcie znacznej geometrii.

![Ekran szkieletowy MeshMill pokazujący różnice w gęstości trójkątów](../../images/meshmill-wireframe.png)

## Przeanalizuj gęstość siatki

Ekran Gęstość odwzorowuje względną gęstość lokalną w całym modelu. Rzadkie regiony pozostają chłodne
coraz gęstsze obszary przechodzą przez jaśniejsze kolory, dzięki czemu nierówne próbkowanie jest widoczne na pierwszy rzut oka.

![Wyświetlacz gęstości MeshMill pokazujący względną gęstość siatki](../../images/meshmill-density.png)

Gęstość pozostaje dostępna podczas oceny tymczasowej optymalizacji. Zestaw narzędzi zgłasza
algorytm, cel, wynikowa liczba trójkątów i wierzchołków, procent redukcji, wymiary i
szacowany rozmiar wyjściowy przed zastosowaniem przejścia.

![Ekran MeshMill Density pokazujący tymczasową optymalizację](../../images/meshmill-density-overview.png)

Przytrzymaj prawy przycisk myszy, aby sprawdzić region za pomocą okrągłej lupy. Powiększony widok
pozostaje wyśrodkowany na wskaźniku i ukazuje lokalną gęstość bez zmiany pozycji głównej kamery.

![Wyświetlanie gęstości MeshMill za pomocą lupy w rzutni](../../images/meshmill-density-zoom.png)

## Sterowanie widokiem

| Dane wejściowe | Akcja |
| --- | --- |
| Przeciąganie środkowym przyciskiem | Obrót |
| Shift + przeciąganie środkowym przyciskiem | Przesuwanie |
| Kółko myszy | Powiększanie w kierunku kursora |
| Ctrl + kółko myszy | Obrót zgodnie lub przeciwnie do ruchu wskazówek zegara |
| Klawisze strzałek | Obrót wokół środka widoku |
| Ctrl + klawisze strzałek | Przesuwanie |
| Ctrl + Shift + strzałka w górę/w dół | Powiększanie/pomniejszanie |
| Ctrl + Shift + Lewo/Prawo | Rolka |
| `F1` / `F2` / `F3` / `F4` | Cieniowane / Gęstość / Model szkieletowy / Wierzchołki |
| Przytrzymaj prawy przycisk myszy | Lupa |
| Shift + lewy przycisk myszy | Dodaj lub usuń punkty linijki |
| Ctrl + przeciągnięcie lewym przyciskiem | Narysuj wielokąt zaznaczenia |
| `Ctrl+C` | Dodaj wielokąt do zapisanego zaznaczenia |
| `Ctrl+X` | Przytnij do zaznaczenia |
| `Ctrl+Space` | Zoptymalizuj wybór |
| `Delete` | Usuń zaznaczenie |
| `Escape` | Wyczyść aktywne zaznaczenie lub linijkę |
| `Ctrl+Z` / `Ctrl+Y` | Cofnij / ponów |
| `Ctrl+S` | Zapisz aktualny stan siatki |

Klawisze widoku standardowego są zgodne z sześcioklawiszowym blokiem nawigacyjnym:

| Klucz | Zobacz | Ctrl + klawisz |
| --- | --- | --- |
| `Insert` | Lewy | Ustaw bieżącą orientację jako Lewa |
| `Home` | Przód | Ustaw bieżącą orientację jako Przód |
| `Page Up` | Jasne | Ustaw bieżącą orientację jako Prawa |
| `Delete` | Na górze, gdy nie ma żadnego wyboru | Ustaw bieżącą orientację jako Góra |
| `End` | Powrót | Ustaw aktualną orientację jako Wstecz |
| `Page Down` | Dół | Ustaw bieżącą orientację jako Dół |

Zapisanie widoku aktualizuje także widok przeciwny. Lewa i prawa, przód i tył oraz góra i dół
pozostańcie w parze. W oknie dialogowym potwierdzenia domyślną akcją jest **Zapisz**, więc Enter zapisuje plik
orientacja. Przód pojawia się u góry zarówno widoków Górnego, jak i Dolnego.

Skróty można zmienić lub zresetować w Ustawieniach.

## Proces selekcji

Przytrzymaj klawisz Ctrl i przeciągnij lewym przyciskiem myszy, aby narysować wielokąt. Przeciągnij rogi, aby zmienić jego kształt, kliknij lewym przyciskiem myszy krawędź, aby dodać
punkt lub kliknij prawym przyciskiem myszy krawędź, aby ją usunąć. Dodaj więcej regionów za pomocą `Ctrl+C`. Poruszanie kamerą ukrywa się
wielokąt przestrzeni ekranu, zachowując wybraną geometrię.

Optymalizacja z aktywnym wyborem wpływa tylko na ten wybór. Wynik pozostaje tymczasowy
aż zostanie wybrana opcja **Zastosuj**. **Anuluj** odrzuca tymczasowy wynik i zachowuje wybór
można spróbować innej konfiguracji. Operacje przycinania i usuwania stają się normalnymi, cofalnymi edycjami siatki.

Panel wyboru podaje skumulowane wybrane wierzchołki, trójkąty, udział siatki, oszacowane
rozmiar i wymiary. Jego działania przycinają, dodają, optymalizują, usuwają, cofają lub usuwają zachowane
zaznaczenie bez ukrywania otaczającej geometrii.

![MeshMill przedstawiający zachowany wybór regionalny i statystyki dotyczące jego geometrii](../../images/meshmill-crop-selection.png)

## Duże siatki

Przed przydzieleniem binarnego STL, MeshMill porównuje swoją szacunkową pamięć roboczą ze skonfigurowaną
budżet pamięci. Plik znajdujący się nad budżetem zostanie otwarty jako ograniczony przegląd tylko do odczytu. Raporty przeglądowe
pełna liczba trójkątów źródłowych, ale uniemożliwia edycję i eksport, ponieważ jest to próbka, a nie pełna
obiekt. Planowane jest indeksowane, zależne od powiększenia przetwarzanie poza rdzeniem
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Linia poleceń

`MeshMillCLI.exe` jest zawarty w obu pakietach wydań:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Uruchom `.\MeshMillCLI.exe --help` dla wszystkich opcji. MeshMill nie chce nadpisać swojego pliku wejściowego.

## Przykładowa geometria

Dostępne są dwie wersje przykładu rozwojowego. Próbką jest siatka kompozytowa z
celowe warstwy o redundantnej geometrii i zróżnicowanej gęstości. Daje to osobom nieposiadającym skanera a
realistyczne urządzenie do porównywania algorytmów, sprawdzania gęstości, wykonywania operacji regionalnych,
i opracowywanie funkcji planu działania. MeshMill nie wymaga zeskanowanych danych wejściowych.

| Plik | Trójkąty | Rozmiar | Dostawa | Najlepsze dla |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249 999 | 11,9 MB | Normalny Git | Szybka ocena, CI i nauka kontroli | (249,999)
| [`oryginalny-skan.stl`](../../../samples/original-scan.stl) | 4 126 315 | 196,8 MB | Git LFS | Testowanie gęstej geometrii źródła i wydajności dużych oczek | (4,126,315)

Mniejsza próbka jest pobierana z każdym normalnym klonem. Nienaruszony oryginał jest opcjonalny i
zarządzane przez Git LFS, więc nie zawyża zwykłej historii repozytorium. Pulpit GitHub zawiera
Git LFS. Użytkownicy wiersza poleceń mogą zainstalować Git LFS i uruchomić:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Oznaczone wydania publikują również oryginalny STL do bezpośredniego pobrania dla osób, które nie korzystają z Git.
Zobacz [`samples/README.md`](../../../samples/README.md), aby poznać pochodzenie, wymiary i sumy kontrolne.

Twórcy algorytmów powinni również przeczytać
[Przewodnik testowania algorytmów](docs/ALGORITHM_TESTING.md) przed porównaniem lub zmianą redukcji
zachowanie.

## Jednostki STL

STL nie koduje jednostki. Zmiana jednostek modelu powoduje zmianę etykiet i pomiarów bez skalowania
zapisane współrzędne. Wybierz jednostkę opisującą geometrię źródłową.

## Prywatność

MeshMill odczytuje i zapisuje pliki lokalne. Nie zawiera żadnych kont, danych telemetrycznych, przesyłania, reklam ani
funkcja przetwarzania w chmurze. Bieżąca implementacja metryk GPU wykorzystuje lokalną wydajność Windows
liczniki. Planowani są równoważni dostawcy metryk natywnych dla Linux i macOS.

Aby rozwiązać problemy diagnostyczne, programiści mogą uruchomić GUI za pomocą
`--diagnostic-log <local-file.jsonl>`. Dziennik rejestruje lokalnie routing wejść i stan kamery
wyłączone podczas normalnego użytkowania.

## Rozwój i wydanie

Zlokalizowany tekst interfejsu użytkownika i dokumentacja są początkowo tworzone przy użyciu zewnętrznego tłumaczenia maszynowego
usług i automatycznie sprawdzane pod kątem uszkodzeń konstrukcyjnych. Tłumaczenie maszynowe nadal może być
nienaturalne lub nieprawidłowe. Zachęcamy native speakerów do sprawdzania i poprawiania tłumaczeń
proces wkładu.

- [Wkład](CONTRIBUTING.md)
- [Proces wydania](RELEASING.md)
- [Plan działania](ROADMAP.md)
- [Rozwiązywanie problemów](docs/TROUBLESHOOTING.md)
- [Powiadomienia stron trzecich](THIRD_PARTY_NOTICES.md)

## Wsparcie MeshMill

MeshMill jest rozwijany i utrzymywany niezależnie. Przeczytaj
[dlaczego wspieranie tej pracy ma znaczenie](SUPPORT.md) lub wspieranie ciągłego rozwoju
[Kup mi kawę] (https://buymeacoffee.com/tednv).

MeshMill jest objęty licencją GNU General Public License w wersji 3 lub nowszej. Zobacz
[`LICENSE`](../../../LICENSE).
