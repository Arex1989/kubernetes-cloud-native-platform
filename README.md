# Kubernetes & Cloud-Native Platform Engineering

A production-style cloud-native engineering project designed to demonstrate hands-on experience with containerization, Kubernetes operations, application delivery, security, observability, Infrastructure as Code, Azure Kubernetes Service, CI/CD, and GitOps.

## Project Objective

The objective of this project is to build and operate a production-style Kubernetes platform rather than simply deploy individual workloads.

The platform will progressively integrate:

- Docker container engineering
- Kubernetes workload orchestration
- Kubernetes networking and service discovery
- Configuration and secret management
- Persistent storage
- Workload resilience and autoscaling
- Helm application packaging
- Kubernetes security controls
- Prometheus and Grafana observability
- GitHub Actions CI/CD
- Container image security scanning
- Azure Container Registry (ACR)
- Azure Kubernetes Service (AKS)
- Terraform Infrastructure as Code
- Argo CD GitOps delivery
- Failure testing and troubleshooting

## Target Architecture

```text
Developer
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    +-- Test
    +-- Build Docker Image
    +-- Security Scan
    +-- Push Image
              |
              v
             ACR
              |
              v
        +-------------+
        |     AKS     |
        | Kubernetes  |
        +------+------+
               |
       +-------+--------+
       |       |        |
       v       v        v
    Ingress  Service  Workloads
                       |
                +------+------+ 
                |      |      |
                v      v      v
              Pods   Config  Storage
                       |
                       v
                    Secrets

               AKS
                |
        +-------+-------+
        |               |
        v               v
   Prometheus          Logs
        |
        v
     Grafana

GitHub
   |
   v
Argo CD
   |
   v
GitOps Deployment
   |
   v
AKS

## Engineering Roadmap

| Phase | Engineering Milestone | Main Skills | Status |
|---|---|---|---|
| 1 | Workstation & Repository Foundation | Docker, kubectl, Helm, Git | ✅ Completed |
| 2 | Container Engineering | Dockerfiles, images, registries, multi-stage builds | ✅ Completed |
| 3 | Kubernetes Fundamentals | Pods, Deployments, ReplicaSets, Namespaces | ✅ Completed |
| 4 | Kubernetes Networking | Services, DNS, Ingress, traffic flow | ✅ Completed |
| 5 | Configuration & Secrets | ConfigMaps, Secrets, environment configuration | ✅ Completed |
| 6 | Storage & Stateful Workloads | PV, PVC, StorageClasses | ⬜ Planned |
| 7 | Production Workload Engineering | Probes, resources, HPA, disruption/resilience | ⬜ Planned |
| 8 | Helm & Application Packaging | Helm charts, values, environments | ⬜ Planned |
| 9 | Kubernetes Security | RBAC, ServiceAccounts, security contexts, scanning | ⬜ Planned |
| 10 | Observability | Prometheus, Grafana, metrics, logs | ⬜ Planned |
| 11 | CI/CD & Container Security | GitHub Actions, image builds, scanning, registry | ⬜ Planned |
| 12 | AKS Infrastructure with Terraform | AKS, ACR, identity, networking, Terraform | ⬜ Planned |
| 13 | GitOps Platform Engineering | Argo CD, declarative delivery | ⬜ Planned |
| 14 | Failure Testing & Troubleshooting | Pod/node/network/application failures | ⬜ Planned |
| 15 | Production Validation & Portfolio Closure | Architecture, documentation, teardown, GitHub | ⬜ Planned |

## Repository Structure

```text
.
├── .github/
│   └── workflows/
├── app/
├── docker/
├── docs/
│   └── architecture/
├── gitops/
├── helm/
├── kubernetes/
│   ├── base/
│   └── environments/
│       ├── dev/
│       └── prod/
├── observability/
├── scripts/
├── security/
├── terraform/
│   └── aks/
├── .gitignore
└── README.md

## Current Status

### Phase 1 — Workstation & Repository Foundation ✅ Completed

Established the local engineering workstation, repository structure, tooling, Git workflow, and project foundation.

### Phase 2 — Container Engineering ✅ Completed

Built and hardened the application container using multi-stage Docker builds, image optimization, runtime validation, and container engineering practices.

### Phase 3 — Kubernetes Fundamentals ✅ Completed

Implemented Kubernetes Pods, ReplicaSets, Deployments, namespaces, scaling, self-healing, rolling updates, rollback, labels and selectors, and declarative desired-state reconciliation.

Detailed implementation:

[`docs/kubernetes-fundamentals.md`](docs/kubernetes-fundamentals.md)

### Phase 4 — Kubernetes Networking ✅ Completed

Implemented Kubernetes Services, EndpointSlices, Pod-to-Pod communication, CoreDNS service discovery, namespace-aware DNS, dynamic backend management, NGINX Ingress, host-based routing, and end-to-end HTTP access.

Detailed implementation:

[`docs/kubernetes-networking.md`](docs/kubernetes-networking.md)

### Phase 5 — Configuration & Secrets ✅ Completed

Externalized application configuration using Kubernetes ConfigMaps, environment variables, and volume-mounted configuration files.

Implemented Kubernetes Secret consumption using `secretKeyRef`, validated Secret rotation, demonstrated configuration update behaviour, and verified that sensitive runtime values are not stored in repository manifests.

Created separate development and production configuration, validated environment promotion without rebuilding the container image, and restored the workload to the development state.

Detailed implementation:

[`docs/kubernetes-configuration-secrets.md`](docs/kubernetes-configuration-secrets.md)

### Current Phase

**Phase 6 — Storage & Stateful Workloads 🚧 In Progress**

Phase 6 introduces persistent application storage and stateful workload engineering using:

- PersistentVolumes
- PersistentVolumeClaims
- StorageClasses
- Dynamic and static provisioning concepts
- Access modes
- Volume lifecycle behaviour
- Pod-to-storage integration
- Persistent data validation
- Stateful workload concepts

### Next Phase

**Phase 7 — Production Workload Engineering**

The next phase will introduce production workload controls including health probes, resource requests and limits, autoscaling, disruption handling, and workload resilience.
