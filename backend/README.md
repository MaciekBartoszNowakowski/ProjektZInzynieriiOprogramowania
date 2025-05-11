# Przewodnik konfiguracji projektu

## Dostęp administracyjny
```
Username: admin
Email: admin@agh.edu.pl
Password: admin
```

## Uruchamianie projektu
Aby uruchomić projekt w trybie deweloperskim z automatycznym przeładowaniem zmian:
```bash
docker compose watch
```

## Tworzenie nowych modułów
1. Utwórz nową aplikację Django:
```bash
docker compose exec backend python manage.py startapp <nazwa>
```

2. Zarejestruj nową aplikację w ustawieniach projektu, dodając jej nazwę do listy `INSTALLED_APPS` w pliku `thesis_system/settings.py`.

## Zarządzanie migracjami bazy danych
Zastosuj migracje do bazy danych:
```bash
docker compose exec backend python manage.py migrate
```

## Testy

### Struktura testów
Dla każdego modułu utwórz następującą strukturę:
```
<nazwa_modułu>/
  └── tests/
      ├── __init__.py
      ├── test_*.py
```

- Katalog `tests/` musi zawierać plik `__init__.py`
- Nazwy plików testowych muszą zaczynać się od prefiksu `test_`

### Uruchamianie testów
Aby uruchomić wszystkie testy w projekcie:
```bash
docker compose exec backend python manage.py test
```

Aby przetestować konkretny moduł:
```bash
docker compose exec backend python manage.py test <nazwa_modułu>
```

### Przykładowe dane testewe:

W common.management.commands znajdują się pliki generate_data i delete_data, dzięki którym możnna tworzyć i usuwać przykładową zawartość bazy danych, wystarczy wywołać 

```bash
docker compose exec backend python manage.py generate_data
```

lub 


```bash
docker compose exec backend python manage.py delete_data
```
