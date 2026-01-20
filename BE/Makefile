.PHONY: install run migrate makemigrations createsuperuser collectstatic test clean

install:
	uv sync

run:
	uv run python manage.py runserver

migrate:
	uv run python manage.py migrate

makemigrations:
	uv run python manage.py makemigrations

createsuperuser:
	uv run python manage.py createsuperuser

collectstatic:
	uv run python manage.py collectstatic --noinput

test:
	uv run python manage.py test

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +

shell:
	uv run python manage.py shell
