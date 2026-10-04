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
| 1 | Workstation & Repository Foundation | Docker, kubectl, Helm, Git | 🚧 In Progress |
| 2 | Container Engineering | Dockerfiles, images, registries, multi-stage builds | ⬜ Planned |
| 3 | Kubernetes Fundamentals | Pods, Deployments, ReplicaSets, Namespaces | ⬜ Planned |
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
