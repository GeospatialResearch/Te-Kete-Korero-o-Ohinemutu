PROD=-f docker-compose-base.yml -f docker-compose-prod.yml
DEV=-f docker-compose-base.yml -f docker-compose-dev.yml

# Logging things
logs-api:
	docker-compose $(DEV) logs api

# Running things
run:
	docker-compose $(DEV) up

stop:
	docker-compose $(DEV) stop

run-prod:
	docker-compose $(PROD) up

stop-prod:
	docker-compose $(PROD) stop

# Building things
build-dev-www:
	docker-compose $(DEV) build www

build-api:
	docker-compose $(DEV) build api

build-prod:
	docker-compose $(PROD) build

build-prod-www:
	docker-compose $(PROD) build www

build-api-nginx:
	docker-compose $(PROD) build api-nginx

# Get rid of local folders that are built
clean:
	-rm -rf node_modules

# Get rid of docker-compose containers
docker-clean:
	docker-compose $(DEV) rm --force


# Get a command line for the node dev system
# This is used to add packages, using `yarn add` and using `-D` for development only
node-cmd:
	docker-compose $(DEV) exec www bash

django-cmd:
	docker-compose $(DEV) exec api bash

# Manage the Django database
make-migrations:
	docker-compose $(DEV) exec api python3 manage.py makemigrations

show-migrations:
	docker-compose $(DEV) exec api python3 manage.py showmigrations

migrate:
	docker-compose $(DEV) exec api python3 manage.py migrate

fake-migrate:
	docker-compose $(DEV) exec api python3 manage.py migrate --fake app <migrationName>

get-db:
	docker-compose $(DEV) exec api python3 manage.py dbshell

create-superuser:
	docker-compose $(DEV) exec api python3 manage.py createsuperuser

load-translations:
	docker-compose $(DEV) exec api python3 manage.py load_website_translations --ignoredb no

load-atua:
	docker-compose $(DEV) exec api python3 manage.py load_atua

load-storytypes:
	docker-compose $(DEV) exec api python3 manage.py load_story_types

load-contenttypes:
	docker-compose $(DEV) exec api python3 manage.py load_content_types

# initialise-db: migrate load-test
# 	docker-compose $(DEV) restart api

# load-test:
# 	docker-compose $(DEV) exec api \
# 		python3 manage.py load_test_data
#
# load-test-prod:
# 	docker-compose $(PROD) exec api \
# 		python3 manage.py load_test_data
#
# reset-db-and-load:
# 	-docker-compose $(DEV) stop db
# 	docker-compose $(DEV) rm --force db
# 	docker-compose $(DEV) up -d db && sleep 10
# 	make initialise-db
#
db-backup:
	docker exec <container-name> pg_dump -a -T public.django_migrations -T public.django_content_type -T public.auth_permission -U mapuser <database-name> > db_backup.sql

db-restore:
	docker exec -i <container-name> psql -U mapuser -d <database-name> < db_backup.sql

reset-db:
	docker-compose $(DEV) stop db
	docker-compose $(DEV) rm --force db
	docker-compose $(DEV) up -d db && sleep 10
	make migrate

initialise-db: create-superuser load-translations load-atua load-storytypes load-contenttypes

# Code checking
check: flake8 eslint

flake8:
	docker-compose $(DEV) exec api flake8 .

eslint:
	docker-compose $(DEV) exec www yarn run lint

# # Careful, these push docker images.
# # Use this only to avoid bitbucket pipeline usage
build-push-www:
	docker build \
	    -t geospatialri/bicultool:develop \
	    --build-arg API_HOST=https://api.maptool.test.geospatial.ac.nz \
	    --build-arg WEB_HOST=https://www.maptool.test.geospatial.ac.nz \
	    -f DockerfileNodeNginx \
	    .
	docker push geospatialri/bicultool:develop
#
# build-www-kube:
# 	docker build \
# 	    -t geospatialri/esp-v2-kube:develop \
# 			--build-arg DATA_HOST=https://data.esp.gritool.com \
# 	    --build-arg API_HOST=https://api.esp.geospatial.ac.nz \
# 	    --build-arg WEB_HOST=https://www.esp.geospatial.ac.nz \
# 	    --build-arg AUTH_HOST=https://staging.accounts.crcsi.com.au \
# 	    --build-arg AUTH_CLIENT_ID=487960 \
# 	    -f DockerfileNodeNginx \
# 	    .
# 	docker push geospatialri/esp-v2-kube:develop
#
#
build-push-api:
	docker build \
	    -t geospatialri/bicultool-django:develop \
	    -f DockerfileDjango \
	    .
	docker push geospatialri/bicultool-django:develop
#
#
# # attention: for kube, the build-api/nginx-api-default.conf must have server localhost: 8000; instead of server api:8000;
build-push-api-nginx:
	docker build \
	    -t geospatialri/bicultool-django-nginx:develop \
	    -f DockerfileDjangoNginx \
	    .
	docker push geospatialri/bicultool-django-nginx:develop


build-push-nginx-proxy:
	docker build \
	    -t geospatialri/nginx-proxy:develop \
	    -f DockerfileNginxProxy \
	    .
	docker push geospatialri/nginx-proxy:develop


#
# set-images:
# 	kubectl set image --namespace=esp deployment/esp-www esp-www=geospatialri/esp-v2-kube:develop
# 	kubectl set image --namespace=esp deployment/esp-api esp-api=geospatialri/esp-v2-django:develop
