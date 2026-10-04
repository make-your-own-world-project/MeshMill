# Rozwiązywanie problemów

## Windows blokuje pobieranie

Niepodpisane kompilacje społeczności mogą uruchomić funkcję Microsoft Defender SmartScreen. Porównaj pobrane
skrót SHA-256 pliku z `SHA256SUMS.txt` z tej samej wersji GitHub. Podpisane wydania identyfikują
ich wydawcę we właściwościach pliku Windows.

## Kompilacja przenośna nie uruchamia się

Wyodrębnij cały plik ZIP przed uruchomieniem `MeshMill.exe`. Katalog `_internal` musi pozostać następny
do obu plików wykonywalnych. Nie uruchamiaj pliku wykonywalnego z poziomu przeglądarki ZIP.

## Otwiera się duży widok STL

Szacowany zestaw roboczy przekracza budżet pamięci w Ustawieniach. Tryb przeglądu jest celowo
tylko do odczytu. Zwiększ budżet tylko wtedy, gdy maszyna ma wystarczającą ilość dostępnej pamięci, lub zmniejsz
mesh przed otwarciem go do edycji.

## Widok standardowy nie został zapisany

Naciśnij skrót widoku zmodyfikowanego z klawiszem Ctrl, a następnie wybierz **Zapisz** lub naciśnij klawisz Enter w potwierdzeniu
okno dialogowe. Zapisanie jednego widoku aktualizuje również jego przeciwieństwo. Linia stanu informuje o zapisanym widoku.

## Skróty nawigacyjne nie reagują

Najpierw zamknij dowolne modalne okno dialogowe. Przejrzyj lub zresetuj skróty w Ustawieniach, jeśli zostały dostosowane. The
domyślne skróty widoku używają Wstaw, Strona główna, Strona w górę, Usuń, Koniec i Strona w dół.

## Utwórz dziennik diagnostyczny orientacji lokalnej

Rejestrowanie diagnostyczne jest domyślnie wyłączone. Aby lokalnie zarejestrować routing klawiatury i stan kamery:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

Dziennik może zawierać ścieżkę otwartego pliku. Przejrzyj i zredaguj go przed udostępnieniem. Geometria siatki nie jest
zapisano do dziennika.

## Zgłoś problem

Uwzględnij wersję MeshMill, wersję Windows, model GPU, liczbę trójkątów siatki, dokładne działanie
kolejność i czy użyto pakietu instalacyjnego czy przenośnego. Użyj próbki podlegającej redystrybucji
siatkę, jeśli to możliwe. Nie dołączaj prywatnych skanów ani dzienników diagnostycznych bez ich uprzedniego przejrzenia.
