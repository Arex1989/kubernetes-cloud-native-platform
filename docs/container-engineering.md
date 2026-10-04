# Phase 2 — Container Engineering

## Objective

Build, package, harden, inspect, configure, version, and validate the cloud-native platform API as a production-oriented container workload.

## Application

The project uses a lightweight Python Flask API served by Gunicorn.

### Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Application metadata and runtime identity |
| `/health` | Application health endpoint |
| `/ready` | Application readiness endpoint |
| `/version` | Application version information |
| `/metrics` | Prometheus-compatible application metrics |

These endpoints are intentionally designed for reuse in later Kubernetes and observability phases.

## Container Engineering Progression

### 1. Baseline Image — `1.0.0`

The initial container image established the basic application packaging workflow.

Characteristics:

- Python 3.14 slim base image
- Gunicorn production WSGI server
- Port 8080
- Environment-based configuration
- Application dependencies installed with pip
- Cache-friendly dependency installation order

Observed image size:

- Approximately 170 MB

Initial inspection identified that the application processes were running as root.

### 2. Runtime Configuration Validation

The same immutable `1.0.0` image was started with runtime overrides:

- `ENVIRONMENT=production`
- `APP_VERSION=1.0.1-runtime-test`

The application returned the overridden values without rebuilding the image.

This validated separation between immutable application artifacts and environment-specific runtime configuration.

## Docker Build Cache Validation

A repeated image build reused the Docker BuildKit cache for:

- Working directory configuration
- Requirements copy
- Python dependency installation
- Application source copy

This demonstrated why dependency manifests are copied and installed before frequently changing application source files.

## Security Hardening — `1.1.0`

The image was hardened by introducing:

- Dedicated `appuser`
- Dedicated `appgroup`
- Non-root application execution
- Explicit application-file ownership
- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONUNBUFFERED=1`
- Docker health check against `/health`

Runtime validation confirmed:

- Gunicorn executed as UID 999 rather than root
- Application health endpoint remained functional
- Docker reported the container as healthy

Observed image size:

- Approximately 161 MB

## Multi-Stage Build — `2.0.0`

The production Dockerfile was refactored into two stages.

### Builder Stage

The builder stage:

- Uses Python 3.14 slim
- Creates `/opt/venv`
- Installs application dependencies into the virtual environment

### Runtime Stage

The runtime stage:

- Uses a clean Python 3.14 slim base
- Creates the non-root application identity
- Copies `/opt/venv` from the builder stage
- Copies only the application source required at runtime
- Runs Gunicorn as `appuser`
- Exposes port 8080
- Includes the Docker health check

Runtime validation confirmed:

- Python path: `/opt/venv/bin/python`
- Gunicorn path: `/opt/venv/bin/gunicorn`
- Runtime identity: `appuser`
- Application health: healthy

Observed image size:

- Approximately 172 MB

The multi-stage image is slightly larger than the hardened single-stage image for this workload. This is expected because the application has no compiler-heavy build dependencies to discard, while the copied virtual environment introduces additional filesystem overhead.

The multi-stage design is retained because it demonstrates explicit separation between dependency construction and the production runtime environment.

## Image Comparison

| Version | Purpose | Runtime User | Approx. Size |
|---|---|---|---:|
| `1.0.0` | Baseline | root/default | 170 MB |
| `1.1.0` | Hardened single-stage | appuser | 161 MB |
| `2.0.0` | Multi-stage production image | appuser | 172 MB |

## Image Tagging

The `2.0.0` production image was additionally tagged as:

- `cloud-native-platform-api:latest`
- `cloud-native-platform-api:phase2`

All three tags resolve to the same local SHA256 image identity.

A registry-style reference was also created:

`example.azurecr.io/cloud-native-platform-api:2.0.0`

No image was pushed because the project's Azure Container Registry will be provisioned later with the AKS infrastructure.

## Key Engineering Lessons

1. Container images should remain immutable while runtime configuration is supplied externally.
2. Dockerfile instruction ordering materially affects build-cache efficiency.
3. A running process does not necessarily mean a healthy application.
4. Application containers should run with the minimum privileges required.
5. Tags are mutable references; image IDs and registry digests identify immutable artifacts.
6. Multi-stage builds provide build/runtime separation but do not automatically guarantee smaller images.
7. Docker health checks and Kubernetes liveness/readiness probes solve related but distinct runtime-health problems.
8. Build context should be intentionally constrained with `.dockerignore`.

## Phase Outcome

Phase 2 established a reproducible and security-conscious container engineering lifecycle that will serve as the application foundation for subsequent Kubernetes phases.
