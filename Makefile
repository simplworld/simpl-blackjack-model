.PHONEY: shell

shell:
	docker-compose run --rm model.backend bash