.PHONY: build up down logs shell clean

# Build and start services
build:
	docker-compose build

up:
	docker-compose up

# Start services in detached mode
up-d:
	docker-compose up -d

# Stop services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Access shell in web container
shell:
	docker-compose exec web bash

# Clean up containers, volumes, and build cache
clean:
	docker-compose down -v
	docker system prune -f