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
| 4 | Kubernetes Networking | Services, DNS, Ingress, traffic flow | ⬜ Planned |
| 5 | Configuration & Secrets | ConfigMaps, Secrets, environment configuration | ⬜ Planned |
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

Phase 1 established the local engineering workstation and repository foundation required for the cloud-native platform.

Completed milestones:

- Audited the Apple Silicon ARM64 workstation
- Validated Git and Homebrew
- Installed and validated Docker Desktop and Docker Engine
- Validated Docker Compose
- Installed and validated kubectl
- Installed and validated Helm
- Validated Terraform
- Validated Azure CLI and Azure authentication
- Validated GitHub CLI and GitHub authentication
- Established a security-aware `.gitignore`
- Created the production-oriented repository structure
- Defined the complete 15-phase engineering roadmap
- Initialized Git version control
- Created the GitHub repository
- Configured the `origin` remote
- Published the initial `main` branch to GitHub

### Next Phase

**Phase 2 — Container Engineering**

The next phase will build the project's application workload and establish the container engineering lifecycle, including Dockerfiles, image construction, image optimization, registries, and multi-stage builds.

