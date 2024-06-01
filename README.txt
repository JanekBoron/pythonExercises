Projekt : Konsolowa Aplikacja Bankowa

Opis:
Twoim zadaniem jest stworzenie aplikacji konsolower, która symuluje prostą aplikację bankową. Aplikacja powinna umożliwiać użytkownikom tworzenie kont, logowanie, wykonywanie przelewów pomiędzy kontami, sprawdzanie stanu konta oraz przeglądanie historii transakcji. Dane użytkowników powinny być przechowywane w bazie danych SQL Server.
Wymagania:
1.Rejestracja użytkownika:

-    Użytkownik powinien mieć możliwość założenia konta, podając nazwę użytkownika, hasło i początkowe saldo.
-   Każdy użytkownik powinien mieć unikalny numer konta generowany losowo.
-  Dane użytkowników (nazwa użytkownika, hasło, numer konta, saldo, transakcje) powinny być przechowywane w bazie danych.

2.Logowanie:

- Użytkownik powinien mieć możliwość zalogowania się do swojego konta, podając nazwę użytkownika i hasło.
- Po pomyślnym zalogowaniu, użytkownik powinien mieć dostęp do głównego menu aplikacji.

3.Główne menu:

-  Po zalogowaniu użytkownik powinien mieć dostęp do następujących opcji:
- Wyświetlenie listy użytkowników.
- Wykonanie przelewu.
- Wyświetlenie historii transakcji.
- Sprawdzenie stanu konta.
- Wylogowanie się.

4.Przelewy:

- Użytkownik powinien mieć możliwość wykonania przelewu na inne konto, podając numer konta odbiorcy, kwotę i tytuł przelewu.
- Aplikacja powinna sprawdzać, czy na koncie nadawcy znajduje się wystarczająca ilość środków.
-  Nie można wykonywać przelewów na to samo konto.

5. Historia transakcji:

  -  Użytkownik powinien mieć możliwość przeglądania historii wykonanych i otrzymanych transakcji.
   - Historia powinna zawierać datę, tytuł, kwotę oraz numer konta nadawcy lub odbiorcy.
  -  Użytkownik powinien mieć możliwość filtrowania transakcji według daty.

6. Sprawdzanie stanu konta:

  -  Użytkownik powinien mieć możliwość sprawdzenia bieżącego stanu swojego konta.

7. Obsługa błędów:

   - Aplikacja powinna obsługiwać błędy, takie jak podanie nieprawidłowych danych logowania, próba przelewu na to samo konto, niewystarczające środki na koncie oraz inne błędy związane z operacjami na bazie danych.
   - Użytkownik powinien otrzymywać odpowiednie komunikaty o błędach.


Sugestie dodatkowe:
   - Zaimplementuj funkcję sortowania transakcji według daty.
  -  Użyj biblioteki datetime do obsługi dat i czasu w aplikacji.
  -  Stosuj dobre praktyki programistyczne



S23370
Jan Boroń
