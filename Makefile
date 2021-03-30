

test:
	docker-compose -f docker-compose.local.yml run web pytest

init:
	@cp .env.template .env
	@cp .secrets.yaml.template .secrets.yaml
	@read -sp 'Inform the password for the new local database: ' dbpass; \
    sed -i 's/SecretPassword/'"$$dbpass"'/' .secrets.yaml ; \
    sed -i 's/SecretPassword/'"$$dbpass"'/' .env
	@clear
	@printf "Building Docker image..."
	@make build > /dev/null 2>&1
	@printf "OK\n"
	@printf "Installing pre-commit hooks..."
	@docker-compose -f docker-compose.local.yml run web pre-commit install -t pre-commit > /dev/null 2>&1
	@docker-compose -f docker-compose.local.yml run web pre-commit install -t pre-push > /dev/null 2>&1
	@printf "OK\n"
	@printf "Migrating django models..."
	@make migrate > /dev/null 2>&1
	@printf "OK\n"
	@printf "Loading fixtures..."
	@make load-fixtures > /dev/null 2>&1
	@printf "OK\n"
	@printf "Done!\n"

build:
	docker-compose -f docker-compose.local.yml build

run:
	docker-compose -f docker-compose.local.yml up

down:
	docker-compose -f docker-compose.local.yml down

lock:
	docker-compose -f docker-compose.local.yml run web poetry lock

clean:
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;

migrations:
	docker-compose -f docker-compose.local.yml run web python manage.py makemigrations

migrate:
	docker-compose -f docker-compose.local.yml run web python manage.py migrate

clean-migrations:
	@find ./* -name '00*_*.py' -exec rm -rf {} \;

clean-db:
	docker-compose -f docker-compose.local.yml run web python manage.py reset_db --close-sessions --noinput

load-fixtures:
	docker-compose -f docker-compose.local.yml run web python manage.py loaddata fixtures/development/*.json

dump-data:
	docker-compose -f docker-compose.local.yml run web python manage.py dumpdata --indent 2 $(cmd)

shell-plus:
	docker-compose -f docker-compose.local.yml run web python manage.py shell_plus

update-movies:
	docker-compose -f docker-compose.local.yml run web python manage.py update_movies

reset-db: clean-db clean-migrations migrations migrate load-fixtures