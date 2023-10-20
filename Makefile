.PHONY: tests

tests:
	docker-compose exec api /bin/bash -c "PYTHONPATH=. pytest tests"

initdb:
	docker-compose exec api /bin/bash -c "PYTHONPATH=. python app/main.py initdb"

build:
	docker-compose -p demo-questions build

up:
	docker-compose -p demo-questions up
