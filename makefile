rs:
	@echo "building docker container"
	@docker compose up --build -d


isort:
	@isort ./app


black:
	@black ./app


flake8:
	@flake8 ./app

