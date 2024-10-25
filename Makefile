IMAGE_NAME = sagoresarker/ams
TAG = 1.0.0

all: build push

build:
	@ docker build -t $(IMAGE_NAME):$(TAG) .

push:
	@ docker push $(IMAGE_NAME):$(TAG)

clean:
	@ docker rmi $(IMAGE_NAME):$(TAG)

docker_run:
	@ docker run -it --rm -p 8000:8000 $(IMAGE_NAME):$(TAG)

run:
	@ python3 manage.py runserver

migrate:
	@ python3 manage.py makemigrations && python3 manage.py migrate

superuser:
	@ python3 manage.py createsuperuser

