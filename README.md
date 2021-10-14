# Skrypt migrujący dane pomiędzy tabelami

#### Główne pliki z logiką:

- engine/models.py
- engine/management/commands/migrate_data.py
- engine/migrations/0002_create_fake_data.py
- engine/tests.py

### Komendy:

```shell script
docker-compose build
```

kolejnno

```shell script
docker-compose run backend bash
```

następnie w terminalu:

```shell script
python manage.py migrate
```

by dokonać migracji danych należy wywołać:

```shell script
python manage.py migrate_data
```

Wywołanie testu jednostkowego:

```shell script
python manage.py test
```