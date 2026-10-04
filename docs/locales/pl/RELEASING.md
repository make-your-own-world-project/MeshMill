# Zwalnianie MeshMill

Potok wydań tworzy artefakty Windows na modułach Windows hostowanych przez GitHub. Użytkownicy końcowi otrzymują
samodzielny instalator lub przenośny plik ZIP i nie instaluj Python, Node.js ani zależności.

Przed budowaniem odśwież i sprawdź katalogi źródłowe lokalizacji:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Przed pierwszym publicznym wydaniem

1. Zakończ i zatwierdź zaplanowane tłumaczenia aplikacji i dokumentacji.
2. Zapoznaj się z licencją GPL i powiadomieniami stron trzecich.
3. Przetestuj instalację, uruchomienie, ładowanie, optymalizację, eksport i dezinstalację STL na czystym poziomie
   Konto Windows lub maszyna wirtualna.
4. Uruchom CI przeciwko `samples/sample-scan.stl`. Sprawdź każdy zrzut ekranu dokumentacji i wytnij
   pasek zadań, karnacja okna niebędąca częścią MeshMill, powiadomienia, ścieżki prywatne, konto
   szczegółowe informacje i niepowiązaną zawartość komputerową przed publikacją.
5. Skonfiguruj lokalnego autora Git w repozytorium z adresem GitHub konta bez odpowiedzi przed
   pierwsze zatwierdzenie. Potwierdź to za pomocą `git config --local --get user.email`.
6. Skonfiguruj opcjonalne sekrety podpisywania Authenticode:
   - `WINDOWS_CERTIFICATE_BASE64`: Certyfikat PFX zakodowany w formacie Base64.
   - `WINDOWS_CERTIFICATE_PASSWORD`: Hasło PFX.

Bez certyfikatu podpisującego wygenerowane pliki nadal działają, ale Windows SmartScreen może wyświetlać
ostrzeżenie o nierozpoznanym wydawcy. Nie opisuj niepodpisanych kompilacji jako podpisanych lub zaufanych.

## Oryginalny skan i Git LFS

`samples/original-scan.stl` jest śledzony przez Git LFS, ponieważ przekracza normalne 100 MiB GitHub
limit plików. Przed pierwszym zatwierdzeniem sprawdź:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Filtr musi mieć wartość `lfs`, a identyfikator obiektu wskaźnikowego musi odpowiadać `samples/SHA256SUMS.txt`. Wydanie
Workflow sprawdza zawartość LFS i publikuje oryginalny STL jako oddzielny zasób wydania. CI używa
mniejszą próbkę normalnego Gita i nie pobiera obiektu LFS.

## Przetestuj kompilację wydania bez publikowania

Otwórz **Akcje**, wybierz **Zwolnij**, wybierz **Uruchom przepływ pracy** i wprowadź wersję liczbową, np.
`0.1.0`. Ręczne uruchomienie przesyła artefakty przepływu pracy do testowania, ale nie tworzy publicznego GitHub
Zwolnij.

## Opublikuj wydanie

Z czystego, sprawdzonego oddziału `main`:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

Tag rozpoczyna przepływ pracy związany z wydaniem. To:

1. instaluje przypięte zależności kompilacji;
2. generuje pasujące metadane wersji Windows;
3. buduje samodzielne pliki wykonywalne GUI i CLI;
4. podpisuje pliki wykonywalne, gdy skonfigurowane są sekrety podpisywania;
5. buduje instalator Inno Setup dla każdego użytkownika;
6. podpisuje instalatora podczas konfiguracji;
7. tworzy przenośny plik sumy kontrolnej ZIP i SHA-256;
8. przesyła artefakty przepływu pracy;
9. tworzy wydanie GitHub dla wypchniętego znacznika.

Przed ogłoszeniem wydania sprawdź instalator i przenośne archiwum na czystym systemie Windows.
Zachowaj źródło odpowiadające każdemu dostępnemu dystrybuowanemu plikowi binarnemu pod tym samym znacznikiem wydania.
Upewnij się, że przycisk GitHub wskazuje końcowy adres URL publicznego repozytorium przed oznaczeniem pierwszego
zwolnić.
