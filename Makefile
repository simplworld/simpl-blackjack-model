.PHONEY: shell rebuild

rebuild:
	docker-compose rm -f model.backend
	docker-compose build --force-rm model.backend

shell:
	docker-compose run --rm model.backend bash