DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
EXEC = docker exec -it
DB_CONTAINER = ams-db
LOGS = docker logs
ENV = --env-file .env
BACK_FILE = docker_compose/back.yaml
FRONT_FILE = docker_compose/front.yaml
BACK_CONTAINER = ams-back
FRONT_CONTAINER = ams-front
WORKERS_FILE = docker_compose/workers.yaml
WORKER_CONTAINER = celery-worker
MANAGE_PY = python manage.py

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${BACK_FILE} ${env} -f ${FRONT_FILE} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: back-logs
back-logs:
	${LOGS} ${BACK_CONTAINER} -f

.PHONY: front-logs
front-logs:
	${LOGS} ${FRONT_CONTAINER} -f

.PHONY: worker-logs
worker-logs:
	${LOGS} ${WORKER_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${BACK_FILE} -f ${FRONT_FILE} -f ${STORAGES_FILE} down --remove-orphans

.PHONY: db-logs
db-logs:
	${DC} -f ${STORAGES_FILE} logs -f

.PHONY: migrate
migrate:
	${EXEC} ${BACK_CONTAINER} ${MANAGE_PY} migrate

.PHONY: migrations
migrations:
	${EXEC} ${BACK_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: superuser
superuser:
	${EXEC} ${BACK_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: collectstatic
collectstatic:
	${EXEC} ${BACK_CONTAINER} ${MANAGE_PY} collectstatic

.PHONY: shell
shell:
	${EXEC} ${BACK_CONTAINER} ${MANAGE_PY} shell
