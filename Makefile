# Makefile
DOCKERHUB_USERNAME:=poridhi
tag:=v1.0

build:
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-frontend:${tag} ./frontend
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-backend:${tag} ./backend
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-postgres:${tag} ./database

docker-push:
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-frontend:${tag} ./frontend
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-backend:${tag} ./backend
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-postgres:${tag} ./database
	@ docker push $(DOCKERHUB_USERNAME)/todo-frontend:${tag}
	@ docker push $(DOCKERHUB_USERNAME)/todo-backend:${tag}
	@ docker push $(DOCKERHUB_USERNAME)/todo-postgres:${tag}

deploy:
	@ kubectl apply -f k8s/

clean:
	@ kubectl delete -f k8s/