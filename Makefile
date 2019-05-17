PROD=-f docker-compose-base.yml -f docker-compose-prod.yml
DEV=-f docker-compose-base.yml -f docker-compose-dev.yml

# Logging things
logs-api:
	docker-compose $(DEV) logs api

# Running things
run:
	docker-compose $(DEV) up

run-prod:
	docker-compose $(PROD) up

# Building things
build-dev:
	docker-compose $(DEV) build api

build-prod:
	docker-compose $(PROD) build

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

get-db:
	docker-compose $(DEV) exec api python3 manage.py dbshell

create-superuser:
	docker-compose $(DEV) exec api python3 manage.py createsuperuser

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
# reset-db:
# 	-docker-compose $(DEV) stop db
# 	docker-compose $(DEV) rm --force db
# 	docker-compose $(DEV) up -d db && sleep 10
# 	make migrate
#
# # Code checking
# check: flake8 eslint
#
flake8:
	docker-compose $(DEV) exec api flake8 .

# eslint:
# 	docker-compose $(DEV) exec www yarn run lint
#
# # Careful, these push docker images.
# push-image-esp-www:
# 	docker build \
# 		--build-arg ENVIRONMENT=master \
# 		--tag crcsi/esp-v2:latest \
# 		--file DockerfileNodeNginx \
# 		.
# 	docker push crcsi/esp-v2:latest
#
# push-image-esp-api:
# 	docker build \
# 		--tag crcsi/esp-v2-django:latest \
# 		--file DockerfileDjango \
# 		.
#
# 	docker push crcsi/esp-v2-django:latest
#
#
# # Use this only to avoid bitbucket pipeline usage
# build-www:
# 	docker build \
# 	    -t geospatialri/esp-v2:develop \
# 			--build-arg DATA_HOST=https://data.esp.gritool.com \
# 	    --build-arg API_HOST=https://api.esp.staging.geospatial.ac.nz \
# 	    --build-arg WEB_HOST=https://www.esp.staging.geospatial.ac.nz \
# 	    --build-arg AUTH_HOST=https://staging.accounts.crcsi.com.au \
# 	    --build-arg AUTH_CLIENT_ID=487960 \
# 	    -f DockerfileNodeNginx \
# 	    .
# 	docker push geospatialri/esp-v2:develop
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
# build-api:
# 	docker build \
# 	    -t geospatialri/esp-v2-django:develop \
# 	    -f DockerfileDjango \
# 	    .
# 	docker push geospatialri/esp-v2-django:develop
#
#
# # attention: for kube, the build-api/nginx-api-default.conf must have server localhost: 8000; instead of server api:8000;
# build-api-nginx:
# 	docker build \
# 	    -t geospatialri/esp-v2-django-nginx:develop \
# 	    -f DockerfileDjangoNginx \
# 	    .
# 	docker push geospatialri/esp-v2-django-nginx:develop
#
# set-images:
# 	kubectl set image --namespace=esp deployment/esp-www esp-www=geospatialri/esp-v2-kube:develop
# 	kubectl set image --namespace=esp deployment/esp-api esp-api=geospatialri/esp-v2-django:develop
#
#
#
# #------------------------------------ code in the bitbucket pipeline
# IMAGE_TAG=master
# KUBE_CLUSTER='gtg.prod.greyfieldplanning.com.au'
# KUBE_SERVER=https://api.gtg.prod.greyfieldplanning.com.au
# KUBE_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLXZmenhwIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiIzYTkyYzk2MC01OGJlLTExZTgtOTY4MS0wMjIxYTU4ODg4MDQiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.NMdQpNeG15Ylgpg3FoJ-z7ukyfVn_s9erVKsxwihShTxzZUb4V4yMWdEvoD5bsFE7rDK8wD0Up84xXKKH3q2-POHbiXuJIEbkweq4SA-M2OUaOW2hbJbUWLSMmYra_onaQuAQIZFe-zt62enERgkHfNHQh1iszDvUy2Yc9huJKaamWPThZ_U45Z8vYLcjUSGkqXvItjGKYOp7zwWVtbO5vjnBjrOV5bbSW5VzEbc-OZbWHPuAtZYaMfXCgzmM9hmmzqcbRhRJ-_4yZOOroLNcx8OvbNHDu-V3TNlguL2J0SYPoP4bRR1ItOJgJeZer84z4myG-jG7zjQbW2arWM4lg
# #staging
# #kube-token eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLWtoNGs4Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJlNDEwNzdjMS01ODliLTExZTgtYjM3Mi0wNjg4NWVkOTZlMzIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.c7pLATqhyYdl_aSm-cQhgmpTCVon8a5ZyHMgu7vEnvg3h7tXY4Ijn8kGDmeaBP4HmF46iO1Pmf2lCuxsYrjoKKFmS63bb_h37Mq3WcfNaahaRMJDAx43WCqQiyaSBGe5_A7bVqvUEED-B2jArGne1x7lW7RLo0gRhoxnu6vqeSSVbe4koXHRIukxtqC_XSjV5A8hxlj0XwuNJDnNYwC6oFdgrakbqFvp6VkDakVjii3sDqtCAXlKzM-5s5Onv9pZxXdfSq9y3H15MLkpTLgOXhypUFzfrkIaE5s7UVG9Wffdjv1yvPvyB2gKRa_IsoQPsyalH0tADwIuUXGtujfKvA
# #kube-cluster
# #'gtg.staging.frontiersi.io'
# #kube-server
# #https://api.gtg.staging.frontiersi.io
# API_HOST=https://api.espv2.greyfieldplanning.com.au
# WEB_HOST=https://www.espv2.greyfieldplanning.com.au
# AUTH_HOST=https://accounts.crcsi.com.au
# AUTH_ID=890012
#
# deploy-prod:
# 	# # Install and log in to Kubernetes
# 	# ./pipeline/install-kubectl.sh
# 	# ./pipeline/kube-config.sh
# 	set -xe
# 	kubectl config set-cluster $(KUBE_CLUSTER) --server=$(KUBE_SERVER) --insecure-skip-tls-verify=true
# 	kubectl config set-credentials admin-user --token=$(KUBE_TOKEN)
# 	kubectl config set-context esp --cluster=$(KUBE_CLUSTER) --user=admin-user
# 	kubectl config use-context esp
# 	# Log in to Docker
#   # - docker login --username $DOCKER_HUB_USERNAME --password $DOCKER_HUB_PASSWORD
# 	# Build and push the WebApp image
# 	# ./pipeline/build-webapp.sh
# 	# set -xe
# 	# docker build \
# 	#     -t crcsi/esp-v2:$(IMAGE_TAG) \
# 	#     --build-arg API_HOST=$(API_HOST) \
# 	#     --build-arg WEB_HOST=$(WEB_HOST) \
# 	#     --build-arg AUTH_HOST=$(AUTH_HOST) \
# 	#     --build-arg AUTH_CLIENT_ID=$(AUTH_ID) \
# 	#     -f DockerfileNodeNginx \
# 	#     .
# 	# docker push crcsi/esp-v2:$(IMAGE_TAG)
# 	# docker tag crcsi/esp-v2:$(IMAGE_TAG) crcsi/esp-v2:latest
# 	# docker push crcsi/esp-v2:latest
# 	# Build and push the API image
# 	# ./pipeline/build-api.sh
# 	# set -xe
# 	# docker build \
# 	#     -t crcsi/esp-v2-django:$(IMAGE_TAG) \
# 	#     -f DockerfileDjango \
# 	#     .
# 	# docker push crcsi/esp-v2-django:$(IMAGE_TAG)
# 	# docker tag crcsi/esp-v2-django:$(IMAGE_TAG) crcsi/esp-v2-django:latest
# 	# docker push crcsi/esp-v2-django:latest
#   # # Configure kubectl
#   # # Update images
# 	kubectl set --namespace=esp image deployment/esp-www esp-www=crcsi/esp-v2:$(IMAGE_TAG)
# 	kubectl set --namespace=esp image deployment/esp-api esp-api=crcsi/esp-v2-django:$(IMAGE_TAG)
