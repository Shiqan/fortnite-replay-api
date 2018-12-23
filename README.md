# Ray - Go 86 em

Fortnites favorite assistent is here to show you your stats based on your replay files.

## Getting started
* Run `docker-compose up` which will create a postgres container and an adminer container.
* Go to adminer interface and create replays database.
* Run `pipenv run python .\manage.py db upgrade`.
* If you want to persist your data, setup a docker volume.

## License

Licensed under the [MIT License](LICENSE).
