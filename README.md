# tests codes for "indentation and lint" errors
``` bash
docker compose run --rm app sh -c "python manage.py flake8"
```

# run tests
``` bash
docker compose run --rm app sh -c "python manage.py test"
```
``` bash
docker compose run --rm app sh -c "python manage.py wait_for_db"
```
``` bash
docker compose run --rm app sh -c "python manage.py wait_for_db && flake8" 
```
``` bash
docker compose run --rm app sh -c "python manage.py makemigrations"
```
# execute migrations
``` bash
docker compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"
```
# list all volumes
``` bash
docker volume ls
```
# removes a volume
``` bash
docker volume rm django-api_dev-db-data
```
# creates a superuser
``` bash
docker compose run --rm app sh -c "python manage.py createsuperuser"
```

# creates a new app
``` bash
docker compose run --rm app sh -c "python manage.py startapp core"
```
``` bash
docker compose run --rm app sh -c "python manage.py startapp user"
```

# consults a database data via django
``` bash
docker compose run --rm app sh -c "python manage.py dumpdata core.Recipe --indent 2"
```

# consults a database data via django postgre image
``` bash
docker compose exec db psql -U devuser -d devdb -c "SELECT * FROM core_recipe;"
```

# portainer
``` bash
docker run --name portainer --env ADMIN_USERNAME=admin --env ADMIN_PASS=84871771@Nick -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer/portainermanage.py migrate
```

# inspect a connection db and create models based on it
``` bash
docker compose run --rm app sh -c "python manage.py inspectdb --database=live_dw > temp_models.py"
```

# Runs a manage command with especific determined behavior
``` bash
docker compose exec app python manage.py test_cigam --type employees
```

# check folders inside a container
``` bash
docker exec -it livepro-painel ls -l /srv/app
```