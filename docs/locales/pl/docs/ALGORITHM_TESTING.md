# Testowanie algorytmów i wkład

Algorytmy MeshMill powinny umożliwić zarządzanie trudną geometrią przy jednoczesnym zachowaniu widoczności ich efektów,
mierzalne i odwracalne przed zastosowaniem wyniku.

## Oprawy referencyjne

Użyj obu dołączonych wersji złożonej geometrii próbki:

- `samples/sample-scan.stl` to mniejsze, normalne urządzenie Git do rutynowego, zautomatyzowanego programowania
  sprawdza i uczy się sterowania.
- `samples/original-scan.stl` to pełne urządzenie Git LFS do obsługi dużych plików, nadmiarowych warstw,
  nierówna gęstość, nakładanie się i wydajność.

Nadmiarowe i gęste obszary są zamierzonymi cechami testowymi. Test może być na nie nastawiony, ale
nie należy zakładać, że każda nakładająca się powierzchnia jest jednorazowa. Dodaj zwarte siatki syntetyczne, gdy a
zmiana wymaga znanej granicy, krzywizny, topologii, gęstości lub niezmiennika nakładania się.

## Lista kontrolna porównania

W przypadku zmiany algorytmu lub parametru zapisz:

- Wersja lub zatwierdzenie MeshMill;
- urządzenie wejściowe i suma kontrolna;
- algorytm, ustawienia jakości, ustawienia docelowe i zaawansowane;
- pierwotna i wynikowa liczba trójkątów i wierzchołków;
- procent redukcji, wymiary i dryft wymiarowy;
- czas, który upłynął i pamięć szczytowa, jeśli istotna jest wydajność;
- zrzuty ekranu z tych samych zapisanych widoków i trybów wyświetlania;
- widoczne zmiany granicy, dziury, samoprzecięcia, nałożenia lub zniekształcenia;
- niezależnie od tego, czy wynik pochodzi z operacji obejmującej całą siatkę, czy tylko z zaznaczenia.

Porównaj z bieżącym zachowaniem tego samego celu, a nie tylko z innym ustawieniem wstępnym za pomocą a
inna liczba wyjść. W stosownych przypadkach sprawdź wyświetlanie cieniowania, gęstości, modelu szkieletowego i wierzchołków.

## Wskazówki dotyczące akceptacji

Zmiana optymalizacji powinna unikać nieoczekiwanych zmian wymiarów, oczywistej inwersji powierzchni,
pęknięcia między przetworzonymi regionami, utrata znaczących granic i duże regresje jakościowe w a
podobna liczba wyjść. Zmiany zorientowane na gęstość powinny wykazać, że tak było w przypadku usuniętego stężenia
nie mają użytecznej krzywizny ani topologii.

Wyniki wydajności powinny identyfikować procesor, pojemność pamięci, sprzęt graficzny i działanie
system, rozmiar danych wejściowych i to, czy dane zostały już zapisane w pamięci podręcznej. Walidacja strukturalna i zrzuty ekranu
wspierają przegląd, ale nie zastępują inspekcji przez autorów zaznajomionych z geometrią źródłową.

## Testy regresyjne

Preferuj testy deterministyczne z wyraźnymi tolerancjami. Utrzymuj nowe urządzenia na tyle małe, że mieszczą się w normalnym Gicie,
dokumentuj ich pochodzenie i licencję oraz korzystaj z geometrii syntetycznej, gdy rzeczywiste dane źródłowe nie są potrzebne.
Testy powinny obejmować anulowanie i przywrócenie stanu, gdy operacja może modyfikować geometrię.
