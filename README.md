# workflow-tester

A simple FastAPI calculator app used to test a self-hosted Kubernetes deployment workflow.

## API

The app runs on port **8000** and exposes the following endpoints:

| Method | Endpoint | Params | Description |
|--------|----------|--------|-------------|
| GET | `/health` | — | Health check |
| GET | `/add` | `a`, `b` | Add two numbers |
| GET | `/subtract` | `a`, `b` | Subtract b from a |
| GET | `/multiply` | `a`, `b` | Multiply two numbers |
| GET | `/divide` | `a`, `b` | Divide a by b |

Example:
```
GET /add?a=3&b=4  →  {"result": 7.0}
```

## Running locally

```bash
uv sync --group dev
uv run uvicorn main:app --reload --port 8000
```

Interactive docs available at `http://localhost:8000/docs`.

## Tests

```bash
uv run pytest
```

## GitHub Workflow

The workflow in `.github/workflows/deploy.yml` runs on every push or pull request to `main` and has two jobs:

### 1. `test` (ubuntu-latest)
Runs on GitHub-hosted runners. Installs dependencies with `uv` and runs the pytest suite. Both jobs below require this to pass first.

### 2. `build-and-push` (self-hosted, push to main only)
Runs on the self-hosted runner attached to the Kubernetes cluster. Only triggers on direct pushes to `main` (not PRs).

1. **Reads the version** from `pyproject.toml`
2. **Builds the Docker image** — the Dockerfile runs tests again as part of a multi-stage build before producing the final image, so a failed test also blocks the image from being built
3. **Pushes the image** to the local registry at `localhost:30500`
4. **Deploys to Kubernetes** by patching `k8s/deployment.yaml` with the versioned image tag and applying it with `kubectl`
5. **Cleans up old images** from the registry, keeping the two most recent versions
6. **Runs registry garbage collection** to reclaim disk space from deleted image layers

## Docker

The Dockerfile uses a two-stage build:

- **Stage 1 (`test`)** — installs all dependencies (including dev), copies source, and runs pytest. If tests fail, the build stops here.
- **Stage 2 (`final`)** — starts from a clean base, installs only production dependencies, and copies only the app source from the test stage. The `COPY --from=test` instruction creates a hard dependency on stage 1, so a failed test also prevents the final image from being produced.

Build and run manually:
```bash
docker build -t workflow-tester .
docker run -p 8000:8000 workflow-tester
```

## Kubernetes

The app is deployed to the `yonyawn` namespace with the following setup:

- **Deployment** — 1 replica, pulling from the local registry (`localhost:30500`), resource limits of 128Mi memory and 500m CPU
- **Service** — `NodePort` exposing the app on port **30800**, reachable at `http://<node-ip>:30800` from any device on the same network
- **Liveness probe** — hits `/health` every 30s; restarts the pod if it fails
- **Readiness probe** — hits `/health` every 10s; only routes traffic to the pod once it responds successfully