# trello_move

![logo](https://github.com/Shigerman/trello_move/raw/main/trello.jpg)

Moves all cards from "doing" and "done" lists back to "todo" every day at 4:00 AM.
Targets boards named "tasks" under organizations with "family" in the name.

## Local development

```sh
uv sync
uv run python trello_main.py   # one-shot run
uv run python trello_service.py        # scheduler (triggers at 4:00 AM)
uv run python trello_service.py --now  # scheduler, run immediately
```

Environment variables are loaded from `.env`:

```
TRELLO_API_KEY=...
TRELLO_API_SECRET=...
```

## Deploy to Kubernetes

### Create the secret (one-time)

```sh
kubectl create secret generic trello-move-secret \
  --from-literal=TRELLO_API_KEY=your_key \
  --from-literal=TRELLO_API_SECRET=your_secret
```

### Build and push the image

```sh
docker build -t server01:5000/trello-move:latest .
docker push server01:5000/trello-move:latest
```

### Apply the manifest

```sh
kubectl apply -f k8s.yml
```

### Update after code changes

```sh
docker build -t server01:5000/trello-move:latest .
docker push server01:5000/trello-move:latest
kubectl rollout restart cronjob/trello-move
```
