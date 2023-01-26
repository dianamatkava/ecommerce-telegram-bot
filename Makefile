HEROKU_APP_NAME=vp-gifts

deploy: login d-build d-release

login:
	sudo heroku container:login

d-build:
	sudo heroku container:push web --app $(HEROKU_APP_NAME)
	sudo heroku container:push bot --app $(HEROKU_APP_NAME)
	sudo heroku container:push binance --app $(HEROKU_APP_NAME)
	sudo heroku container:push redis --app $(HEROKU_APP_NAME)
	sudo heroku container:push celery --app $(HEROKU_APP_NAME)
	sudo heroku container:push celery-beat --app $(HEROKU_APP_NAME)

d-release:
	sudo heroku container:release web --app $(HEROKU_APP_NAME)
	sudo heroku container:release bot --app $(HEROKU_APP_NAME)
	sudo heroku container:release binance --app $(HEROKU_APP_NAME)
	sudo heroku container:release redis --app $(HEROKU_APP_NAME)
	sudo heroku container:release celery --app $(HEROKU_APP_NAME)
	sudo heroku container:release celery-beat --app $(HEROKU_APP_NAME)



run-build:
	docker-compose -f docker-compose-prod.yml up --build

run-d:
	docker-compose -f docker-compose-prod.yml up -d

run:
	docker-compose -f docker-compose-prod.yml up

down:
	docker-compose -f docker-compose-prod.yml down

down-v:
	docker-compose -f docker-compose-prod.yml down -v