# Phase 3 — Kubernetes Fundamentals

## Objective

Build practical Kubernetes operational knowledge by deploying and managing the
Cloud Native Platform API on a local multi-node Kubernetes cluster.

## Environment

- Kubernetes v1.37
- kind local Kubernetes cluster
- 1 control-plane node
- 1 worker node
- Namespace: `project4`
- Application image: `cloud-native-platform-api:2.0.0`

## Kubernetes Resource Progression

This phase intentionally demonstrates the progression of Kubernetes workload
management:

1. Pod
2. ReplicaSet
3. Deployment

The standalone Pod and ReplicaSet manifests are retained as learning artifacts.
The Deployment manifest represents the current declarative application workload.

## Pod Fundamentals

A standalone Pod was created for the Platform API and used to validate:

- Pod scheduling
- Container execution
- Pod IP addressing
- Labels
- Application logs
- Container image execution
- Namespace placement

Deleting the standalone Pod demonstrated that unmanaged Pods are not
automatically recreated.

## ReplicaSet Fundamentals

A ReplicaSet was introduced to manage multiple copies of the application.

The lab demonstrated:

- Desired replica state
- Pod ownership
- ReplicaSet selectors
- Automatic Pod replacement
- Self-healing behavior
- Horizontal scaling

Replica counts were changed dynamically to demonstrate Kubernetes reconciliation.

## Deployment Fundamentals

The workload was migrated to a Kubernetes Deployment.

The Deployment manages:

Deployment
    -> ReplicaSet
        -> Pods

The Deployment was validated with two healthy application replicas.

## Self-Healing

A Deployment-managed Pod was manually deleted.

Kubernetes immediately created a replacement Pod through the ReplicaSet
controller, restoring the desired replica count automatically.

This demonstrated Kubernetes reconciliation and self-healing.

## Scaling

The Deployment was scaled from two replicas to four replicas.

Kubernetes created additional Pods until:

- Desired: 4
- Ready: 4
- Available: 4

The workload was subsequently returned to its declarative baseline.

## Rolling Updates

A change to the Deployment Pod template triggered a rolling update.

Kubernetes:

1. Created a new ReplicaSet.
2. Started replacement Pods.
3. Gradually terminated Pods from the previous ReplicaSet.
4. Maintained application availability.
5. Completed the rollout successfully.

## Rollback and Revision History

Deployment revision history was inspected and a rollback operation was tested.

This demonstrated how Kubernetes Deployments maintain rollout history and allow
previous workload configurations to be restored.

The declarative manifest was subsequently reapplied to restore the repository
baseline.

## Namespaces

Namespace isolation was tested using:

- `project4`
- `project4-test`

Resources with the same name were successfully created in separate namespaces,
demonstrating Kubernetes namespace isolation.

The temporary test namespace was deleted after validation.

## Labels and Selectors

Labels were inspected across Deployments, ReplicaSets, and Pods.

Label selectors were used to query workloads by:

- Application
- Management controller
- Combined label criteria

This demonstrated how Kubernetes controllers identify and manage their Pods.

## Declarative Desired State

The Deployment manifest declares:

```yaml
replicas: 2

This represents the desired state stored in the repository.

A temporary runtime change was introduced by scaling the Deployment to three replicas:

```bash
kubectl scale deployment platform-api \
  -n project4 \
  --replicas=3
```

The live cluster temporarily contained three replicas while the declarative manifest continued to specify two.

Reapplying the manifest reconciled the workload:

```bash
kubectl apply -f kubernetes/base/deployment.yaml
```

Kubernetes returned the Deployment to two replicas, demonstrating the relationship between declarative configuration and live cluster state.

## Phase 3 Validation

The Kubernetes fundamentals implementation was validated with:

- A two-node local kind cluster consisting of one control-plane node and one worker node.
- A dedicated `project4` namespace.
- The locally built `cloud-native-platform-api:2.0.0` container image loaded into the kind nodes.
- Pod creation and scheduling.
- ReplicaSet self-healing after Pod deletion.
- ReplicaSet scaling from two to four replicas and back down.
- Migration from a standalone ReplicaSet to a Deployment.
- Deployment-managed Pod recovery after simulated failure.
- Deployment scaling.
- Rolling updates and ReplicaSet revision creation.
- Deployment rollback and revision history.
- Namespace isolation.
- Labels and label selectors.
- Declarative desired-state reconciliation.

The final baseline state contains a healthy Deployment with two desired, ready, and available replicas.

## Phase 3 Result

Phase 3 establishes the Kubernetes workload-management foundation for the platform.

The application has progressed from a locally hardened container image to a declaratively managed Kubernetes workload capable of replication, self-healing, scaling, rolling updates, rollback, namespace isolation, and desired-state reconciliation.

This foundation will be extended in the next phase with Kubernetes networking, Services, DNS, and Ingress.
