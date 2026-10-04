# Wkład

Wpłaty są mile widziane poprzez zgłaszanie problemów i żądania ściągnięcia.

## Zakres projektu

MeshMill umożliwia zarządzanie dużymi, gęstymi lub trudnymi plikami siatki w celu późniejszej edycji i
przepływy pracy produkcyjnej. Wkład powinien ulepszyć kontrolę geometrii, gęstość siatek i punktów
zarządzanie, optymalizacja, selekcja, kadrowanie, czyszczenie, walidacja, wymiana STL, wydajność,
lub koordynację tych działań.

Projekt nie obejmuje modelowania ogólnego, rzeźbienia, malowania, animacji, renderowania,
kompozycję sceny, materiały, olinowanie lub inne systemy tworzenia treści. Propozycje wprowadzające
funkcje te wykraczają poza zakres projektu.

Nowe funkcje powinny skupiać uwagę na aplikacji i zachować bezpośrednie przepływy pracy, które zmieniają źródło
geometrię w łatwe do zarządzania siatki i unikaj przekształcania elementów sterujących w ogólną edycję
środowisko.

## Lokalizacja

Tekst źródłowy interfejsu użytkownika w języku angielskim jest przechowywany w `locales/en-US.json`. Metadane regionalne są przechowywane w
`locales/manifest.json`. Przetłumaczone katalogi interfejsu użytkownika używają tych samych stabilnych kluczy i nazwy pliku
`<locale>.json`. Przetłumaczona dokumentacja używa pasującej nazwy pliku głównego w pliku
`docs/locales/<locale>/`.

Po zmianie etykiet, podpowiedzi, okien dialogowych lub innego tekstu widocznego dla użytkownika uruchom:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Przejrzyj razem zmiany w źródle i ponownie wygenerowane klucze.

## Zmiany geometrii i algorytmów

Użyj dołączonej geometrii próbki podczas zmiany optymalizacji, analizy gęstości, selekcji, kadrowania,
obsługa dużych plików lub zachowanie porównywania rzutni. Celowo zawiera nadmiarowe warstwy
i nierówna gęstość, więc użyteczny wynik powinien poprawić łatwość zarządzania bez ukrywania zniekształceń,
odrzucanie znaczących granic lub ciche usuwanie geometrii zachowywanej przez inny algorytm.

Zapisz dane wejściowe, algorytm, ustawienia, liczbę trójkątów, wymiary, dryf wymiarowy, czas, który upłynął,
oraz odpowiednie zrzuty ekranu do porównań. Przetestuj zarówno mniejsze urządzenie Normal-Git, jak i, gdy
zmiana dotyczy dużej lub warstwowej geometrii, oryginalnej oprawy Git LFS. Nie dostrajaj algorytmu
wyłącznie do tego urządzenia. Dodaj małe syntetyczne przypadki dla konkretnego niezmiennika lub regresji
przetestowane.

Zobacz [Testowanie algorytmów i wkład](docs/ALGORITHM_TESTING.md), aby zapoznać się z listą kontrolną porównania.

## Konfiguracja deweloperska

1. Zainstaluj 64-bitową wersję Python 3.12 na Windows.
2. Utwórz i aktywuj środowisko wirtualne.
3. Zainstaluj `requirements-dev.txt`.
4. Uruchom `python meshmill.py` dla GUI lub `python meshmill.py --help` dla użycia CLI.
5. Uruchom `python -m py_compile meshmill.py` przed przesłaniem zmiany.

Zachowaj prywatne siatki, wygenerowane pliki wykonywalne, zrzuty ekranu zawierające prywatne informacje i lokalne
buduj katalogi z zatwierdzeń. Redystrybucyjna geometria testowa należy do `samples/` wraz z jej
udokumentowane źródło, licencja, wymiary i metoda generowania. Nowe pliki źródłowe powinny używać rozszerzenia
Identyfikator SPDX `GPL-3.0-or-later`.

Przytnij każdy zrzut ekranu dokumentacji do zawartości aplikacji MeshMill. Nie uwzględniaj
pasek zadań, niepowiązana karnacja okna, powiadomienia, szczegóły konta, ścieżki prywatne lub tło
zawartość pulpitu.
