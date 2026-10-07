# Kubernetes Networking

## Overview

Phase 4 implements and validates the Kubernetes networking layer for the
Cloud-Native Platform Engineering project.

The phase extends the Kubernetes workload foundation created in Phase 3 by
providing stable service discovery, internal load balancing, DNS-based
communication, namespace-aware service resolution, and HTTP ingress routing.

## Architecture

Application traffic follows this path:

Client
  |
  v
NGINX Ingress Controller
  |
  | Host: platform.local
  v
Ingress: platform-api
  |
  v
ClusterIP Service: platform-api:80
  |
  | targetPort: 8080
  v
EndpointSlice
  |
  +-- Application Pod :8080
  |
  +-- Application Pod :8080

The Service provides a stable network identity while individual Pod IP
addresses can change as workloads are recreated or scaled.

## Pod Networking

The platform Deployment runs two application replicas in the `project4`
namespace.

Each Pod receives an independent IP address from the Kubernetes Pod network.

Direct Pod-to-Pod connectivity was validated from a dedicated network test
Pod by sending HTTP requests directly to both application Pod IP addresses.

This demonstrated basic Kubernetes Pod networking before introducing the
Service abstraction.

## ClusterIP Service

A declarative ClusterIP Service was created for the application:

- Service: `platform-api`
- Namespace: `project4`
- Service type: `ClusterIP`
- Service port: `80`
- Target port: `8080`

The Service selects application Pods using:

- `app=cloud-native-platform-api`
- `managed-by=deployment`

The Service therefore provides a stable virtual IP and DNS identity while
forwarding traffic to the dynamically managed application Pods.

## EndpointSlices

Kubernetes EndpointSlices were inspected to validate the relationship between
the Service and its backend Pods.

The EndpointSlice dynamically contained the IP addresses of the healthy
application Pods and exposed their application port `8080`.

Pod replacement and Deployment scaling tests demonstrated that Kubernetes
automatically updates Service endpoints as the backend workload changes.

## Service Load Distribution

Repeated HTTP requests were sent through the `platform-api` Service.

Responses returned different Pod hostnames, demonstrating that the Service
can distribute requests across multiple healthy backend replicas without the
client needing to know individual Pod IP addresses.

The Deployment was temporarily scaled from two replicas to four replicas.

The EndpointSlice automatically expanded to include the additional Pods and
Service traffic continued to reach the available replicas.

The declarative Deployment manifest was then reapplied, returning the
workload to its repository-defined baseline of two replicas.

## Service Resilience

A running application Pod was deliberately deleted to simulate workload
failure.

The Deployment controller created a replacement Pod automatically.

During this process:

- The `platform-api` Service remained available.
- Kubernetes removed the deleted Pod from the Service endpoints.
- The replacement Pod was added to the EndpointSlice when it became ready.
- Clients continued using the same Service DNS name and ClusterIP.

This demonstrated the separation between stable service discovery and
ephemeral application Pods.

## Kubernetes DNS

CoreDNS provides DNS-based service discovery inside the cluster.

Within the `project4` namespace, the application Service can be accessed by
its short name:

`platform-api`

The fully qualified Kubernetes Service name is:

`platform-api.project4.svc.cluster.local`

Cross-namespace resolution was tested from a temporary client namespace.

A short Service name did not resolve from the separate namespace because DNS
search paths are namespace-aware.

The namespace-qualified name:

`platform-api.project4`

and the fully qualified name:

`platform-api.project4.svc.cluster.local`

successfully resolved and routed traffic to the application.

This demonstrated Kubernetes namespace-aware DNS service discovery.

## Ingress Controller

NGINX Ingress Controller was installed into the `ingress-nginx` namespace for
the local kind environment.

The controller watches Kubernetes Ingress resources and converts their
routing definitions into NGINX configuration.

The `nginx` IngressClass was validated before creating the application
Ingress resource.

## Application Ingress

A declarative Ingress resource exposes the application through:

- Host: `platform.local`
- Path: `/`
- IngressClass: `nginx`
- Backend Service: `platform-api`
- Backend Service port: `80`

The routing chain is:

`platform.local -> NGINX Ingress -> platform-api Service -> application Pods`

HTTP requests were successfully routed through the NGINX Ingress Controller
to the application root, health, and version endpoints.

Ingress access logs confirmed successful HTTP 200 requests and showed traffic
being forwarded to multiple backend application Pods.

## Host Access

The Kubernetes application was also tested from the macOS host.

A local port-forward was used to expose the Ingress Controller path to the
host, after which requests containing:

`Host: platform.local`

were successfully routed through Kubernetes Ingress to the application.

The following application endpoints returned HTTP 200 responses:

- `/`
- `/health`
- `/version`

This validated the complete request path from the development workstation
into the Kubernetes networking stack.

## Declarative Networking Manifests

Phase 4 stores the application networking configuration in:

- `kubernetes/networking/service.yaml`
- `kubernetes/networking/ingress.yaml`

Both manifests were validated using client-side and server-side Kubernetes
dry runs.

The NGINX Ingress Controller itself is an external cluster component and is
not copied into the application's networking manifests.

## Phase 4 Validation

Phase 4 was validated with:

- Pod IP discovery and direct Pod connectivity.
- ClusterIP Service creation.
- Service selectors and port mapping.
- EndpointSlice inspection.
- Service-based application access.
- Service traffic distribution across replicas.
- Pod failure and automatic backend replacement.
- Deployment scaling with dynamic endpoint updates.
- Declarative reconciliation back to two replicas.
- CoreDNS service discovery.
- Same-namespace short-name resolution.
- Cross-namespace DNS behavior.
- Namespace-qualified service resolution.
- Fully qualified Kubernetes DNS resolution.
- NGINX Ingress Controller installation.
- IngressClass validation.
- Host-based Ingress routing.
- Root, health, and version requests through Ingress.
- NGINX access-log verification.
- macOS-to-Kubernetes HTTP access.

## Phase 4 Result

Phase 4 establishes the networking and service-discovery layer of the
cloud-native platform.

The application has progressed from a Kubernetes-managed workload into a
network-accessible service with stable discovery, internal load distribution,
DNS-based communication, namespace-aware resolution, dynamic backend
management, and HTTP ingress routing.

The platform is now ready to progress to configuration and secret management
using ConfigMaps, Secrets, and environment-specific configuration.
