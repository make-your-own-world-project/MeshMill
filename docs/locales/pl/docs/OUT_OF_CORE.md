# Architektura siatkowa poza rdzeniem

Obecne zabezpieczenie dużych plików MeshMill szacuje pamięć roboczą przed całkowitym przydzieleniem
siatka. Pliki przekraczające skonfigurowany budżet można otwierać jako ograniczone przeglądy nawigacji. An
przegląd to próbkowana geometria, jest widocznie oznaczony jako taki i nie można go edytować ani eksportować jako
chociaż było to pełne źródło.

Prawdziwe szczegóły zależne od powiększenia wymagają trwałego indeksu przestrzennego. Poniższy projekt to definiuje
kolejny etap realizacji.

## Format indeksu

Każda siatka źródłowa otrzymuje wersjonowany katalog `.meshmill-index` zawierający:

- `manifest.json`, z rozmiarem źródła, czasem modyfikacji, skrótami próbkowanej treści, granicami,
  liczba trójkątów, wersja indeksu, dokładność współrzędnych i opisy poziomów;
- kafelki przestrzenne adresowane za pomocą poziomu oktrego i kodu Mortona;
- gruboziarnista siatka wyświetlania dla każdego zajętego kafelka nadrzędnego;
- zapisy trójkątów w pełnej rozdzielczości w kafelkach liści; I
- własność granic i nakładające się metadane wykorzystywane podczas operacji regionalnych i montażu.

Tworzenie indeksu odczytuje źródło sekwencyjnie w ograniczonych blokach. Zapisuje tymczasowe przebiegi płytek i
niepodzielnie publikuje manifest po tym, jak każdy wymagany plik przejdzie weryfikację. Przerwany lub
nieaktualny indeks zostanie wykryty w jego manifeście i można go wznowić lub odbudować bez otwierania pełnego
siatka w pamięci.

## Przesyłanie strumieniowe rzutni

Rzutnia wybiera kafelki na podstawie błędu ścięcia kamery i błędu przestrzeni ekranu. Grube płytki nadrzędne są
pokazany jako pierwszy. Widoczne kafelki podrzędne zastępują je w miarę zbliżania się kamery i przebywania poza ekranem
Płytki o niskim wpływie pozostają szorstkie. RAM i VRAM mają niezależne budżety i są najrzadziej używane
skrytki. Zwolnienie szczegółów nigdy nie powoduje zwolnienia ogólnej reprezentacji całego obiektu.

Harmonogram rejestruje następujące stany kafelków: w kolejce, czytanie, przetwarzanie, przesyłanie, rezydentne, niepowodzenie,
i anulowane. Rzutnia może kolorować kostki według stanu i wypełniać każdą kostkę proporcjonalnie do jej stanu
postęp. Anulowanie usuwa częściowe wyniki i pozostawia aktywną ostatnią pełną reprezentację.

## Przetwarzanie i pojemność

Lokalna jednostka pracy to kafelek plus deterministyczne nakładanie się wymagane przez jego działanie. Współbieżność
jest ograniczone przez aktualnie dostępny RAM, skonfigurowany procent pamięci, liczbę procesorów logicznych i
zmierzony rozmiar jednostki roboczej. Przesyłanie i wyświetlanie GPU ma oddzielny budżet VRAM. Zgłaszane równolegle
pojemność jest szacunkowa do momentu zmierzenia reprezentatywnych płytek.

Operacje zachowują jednego właściciela dla każdego elementu granicy. Montaż potwierdza wspólne granice,
usuwa duplikaty, sprawdza liczbę i granice oraz rejestruje dokładne użyte parametry. Ta sama praca
Format jednostki i wyniku można później zaplanować w rozproszonych węzłach syntezy.

## Zasady bezpieczeństwa

- Próbka globalna jest oznaczona jako przegląd, a nie jako szczegół rzutni w pełnej rozdzielczości.
- Przeglądu nie można zastąpić ani wyeksportować jako kompletnej siatki źródłowej.
- Żądania pełnego obciążenia, które przekraczają bieżący budżet, wymagają wyraźnego wyboru.
- Generowanie indeksów, przetwarzanie płytek i montaż można anulować, zachowując poprzednie
  stan kompletny.
- Wartości pojemności są szacunkowe i określają, czy opisują bieżący silnik, czy planowany
  wykonanie płytek równoległych.
