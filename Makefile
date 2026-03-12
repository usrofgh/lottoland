local-up:
	docker compose --env-file envs/.env.desktop -f docker/docker-compose-base.yml -f docker/docker-compose-local.yml up --build

up:
	docker compose --env-file envs/.env.dev -f docker/docker-compose-base.yml -f docker/docker-compose-dev.yml up --build
