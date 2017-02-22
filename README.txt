Program "Ruletka"

Wywołanie programu : main("nazwa_użytkownika")
Po zalogowaniu gracz automatycznie dostaje 1000$. Można odbstawiać na stole liczby, przedziały liczb, parzyste/nieparzyste, kolory dowolna ilosc razy. Obstawione zakłady sa widoczne w ramce poniżej stołu. Po skończonym obstawianiu należy kliknąć na ramkę "SPIN" w celu "zakręcenia kołem ruletki". Po wylosowaniu liczby gracz otrzymuje wygraną(o ile jest) na swoje konto i informacje o wygranej. W momencie przerwania gry i wznowienia jej z tą sama nazwa_użytkownika nie zostanie stracony aktualny stan konta(połaczenie z bazą  danych, przed wyjsciem z programu zostaje uaktualniony wpis w bazie, także w trakcie gry po każdym losowaniu). Gra kończy sie gdy użytkownik wyda całą kwotę. 


Struktura programu:
1.Użyta biblioteka do rysowania elementów: PyGame; 
Wyrysowaniem elementów i sterowaniem zajmuje się klasa Table . 
2.Połączenie z baza danych: SQLITE3.
Przy pierwszym uruchomieniu tabela w bazie danych jest automatycznie tworzona (zapytanie: CREATE IF NOT EXISTS..). Tworzony jest obiekt player a w konstuktorze nazwa_użytkownika jest wrzucana do bazy danych. Po obstawieniu i skończeniu gry wpis jest uaktualniany.
3. Liczeniem wyniku zajmuje się funkcja check_spin. Wszystkie zakłady przechowywane są w słowniku. 
4. Korzystałam z zasad stołu europejskiego, również tak są przeliczane zakłady. 
