make docker_build:
	docker build -t winedash .

make docker_run:
	docker run -p 8080:8080 -ti winedash:latest

make gcloud_submit:
	gcloud builds submit --tag gcr.io/independent-tea-246616/winedash

make gcloud_deploy:
	gcloud beta run deploy winedash \
		--image gcr.io/independent-tea-246616/winedash \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated \
		--memory 512Mi
