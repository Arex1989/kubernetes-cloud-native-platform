# Kubernetes Configuration and Secrets

## Overview

Phase 5 introduces externalized application configuration and sensitive-data
management to the Kubernetes cloud-native platform.

The application configuration is no longer coupled directly to the container
image. Kubernetes ConfigMaps provide non-sensitive configuration, while
Kubernetes Secrets provide sensitive runtime values.

This phase also introduces environment-specific configuration and
volume-mounted configuration files.

## Architecture

The configuration flow is:

Application Deployment
        |
        +-- ConfigMap environment variables
        |
        +-- Kubernetes Secret references
        |
        +-- ConfigMap volume
                |
                v
        /etc/platform/application.properties

Environment-specific configuration is maintained separately for development
and production.

## ConfigMap Environment Configuration

The platform uses ConfigMaps to externalize non-sensitive application
configuration.

Configuration includes:

- Application environment
- Logging level
- Health endpoint configuration
- Metrics endpoint configuration
- Application identity

The Deployment consumes configuration using `envFrom` and a ConfigMap
reference.

This allows configuration to change independently of the container image.

## Configuration Update Behaviour

ConfigMap environment variables are injected when a Pod is created.

Updating the ConfigMap does not automatically modify environment variables
inside already-running containers.

A controlled Deployment rollout was therefore used to recreate the Pods and
load the updated configuration.

This behaviour was validated by changing the logging configuration and
observing the difference between the ConfigMap state and the existing Pod
environment before restarting the workload.

## Volume-Mounted Configuration

A second ConfigMap provides file-based application configuration.

The ConfigMap contains:

`application.properties`

The Deployment mounts this configuration read-only at:

`/etc/platform`

This demonstrates Kubernetes projected configuration using ConfigMap-backed
volumes.

Unlike environment-variable configuration, mounted ConfigMap files can be
updated by kubelet without requiring the Pod to be recreated.

This behaviour was validated by modifying the ConfigMap and observing the
updated configuration propagate into both running Pods while their identities
remained unchanged.

## Kubernetes Secrets

Sensitive runtime configuration is managed using a Kubernetes Secret.

The Deployment retrieves:

- `API_USERNAME`
- `API_TOKEN`

using `secretKeyRef`.

Secret values are not embedded in the Deployment manifest.

The lab Secret was created directly in the cluster rather than being stored as
a repository manifest.

This prevents runtime credential material from being committed to Git.

## Secret Rotation

Secret rotation behaviour was tested by updating the runtime Secret.

Because Secret-backed environment variables are loaded when containers start,
existing Pods retained the previous values.

A controlled Deployment rollout recreated the Pods and loaded the rotated
Secret values.

The Secret value itself was not printed during validation.

## Environment-Specific Configuration

Separate configuration manifests are maintained for:

- Development
- Production

Development configuration uses:

- `APP_ENV=development`
- `LOG_LEVEL=debug`

Production configuration uses:

- `APP_ENV=production`
- `LOG_LEVEL=info`

The same Deployment and container image can therefore operate with different
runtime configuration without rebuilding the application image.

Development-to-production promotion was tested by changing the referenced
environment configuration and performing a controlled rollout.

The container image remained unchanged during the promotion.

The workload was subsequently restored to the development configuration.

## Repository Safety

Sensitive values are intentionally excluded from repository-managed
manifests.

The repository stores only Secret references.

Validation confirmed:

- No Kubernetes Secret manifest is stored in the repository.
- Runtime demonstration tokens are absent from repository files.
- Deployment manifests contain `secretKeyRef` references only.
- Secret values are not committed to Git.

## Phase 5 Validation

Phase 5 was validated through:

- ConfigMap creation and server-side validation.
- ConfigMap-backed environment variable injection.
- ConfigMap update behaviour testing.
- Controlled Deployment rollouts.
- File-based ConfigMap volume mounting.
- Live mounted ConfigMap propagation.
- Kubernetes Secret creation at runtime.
- Secret-backed environment variable injection.
- Secret rotation.
- Verification that secret values remain outside repository manifests.
- Development and production configuration separation.
- Development-to-production configuration promotion.
- Container image consistency across environments.
- Development configuration restoration.
- Service and EndpointSlice continuity.
- Final server-side manifest validation.
- Repository secret-safety scanning.

## Phase 5 Result

Phase 5 establishes the configuration and secret-management layer of the
cloud-native platform.

Application configuration is now externalized from the container image,
environment-specific configuration is separated from workload definitions,
file-based configuration can be projected into Pods, and sensitive values are
consumed through Kubernetes Secret references without storing credential
material in Git.

The platform is now ready to progress to persistent storage and stateful
workload engineering using PersistentVolumes, PersistentVolumeClaims, and
StorageClasses.
