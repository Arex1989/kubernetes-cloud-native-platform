# Kubernetes Storage & Stateful Workloads

## Overview

Phase 6 extends the Kubernetes Cloud-Native Platform with persistent storage and stateful workload engineering.

The implementation demonstrates how Kubernetes separates application lifecycle from data lifecycle using PersistentVolumes (PVs), PersistentVolumeClaims (PVCs), StorageClasses, Deployments, StatefulSets, and dynamically provisioned storage.

The phase was implemented and validated on a local multi-node kind cluster using the Rancher local-path provisioner.

## Architecture

The storage architecture implements three primary workload patterns:

1. A Deployment consuming a persistent PVC.
2. A StatefulSet using dedicated, dynamically provisioned PVCs for each Pod ordinal.
3. A dedicated Retain-policy StorageClass demonstrating persistent-volume lifecycle and recovery.

### Deployment Storage

The persistent Deployment uses the following relationship:

    persistent-worker
           |
           v
      platform-data
           |
           v
    PersistentVolume
           |
           v
    standard StorageClass

The `platform-data` PVC requests 1Gi of `ReadWriteOnce` storage from the default `standard` StorageClass.

The workload mounts the claim at `/data`.

## Dynamic Provisioning

The cluster uses the Rancher local-path provisioner:

- Provisioner: `rancher.io/local-path`
- Default StorageClass: `standard`
- Volume binding mode: `WaitForFirstConsumer`
- Default reclaim policy: `Delete`

`WaitForFirstConsumer` delays volume provisioning and binding until a Pod consuming the PVC is scheduled.

This allows Kubernetes to consider workload placement before selecting and provisioning storage.

## Persistent Data Lifecycle

Persistence was validated by writing application state to the mounted volume and deleting the consuming Pod.

Kubernetes recreated the Pod while preserving:

- the PVC identity;
- the PersistentVolume identity;
- the data stored on the filesystem.

This demonstrated that Pod lifecycle and persistent-data lifecycle are independent.

## Reclaim Policy Testing

### Delete Policy

The default `standard` StorageClass uses:

    reclaimPolicy: Delete

The lifecycle test confirmed that deleting a dynamically provisioned PVC caused its associated PersistentVolume to transition through release and subsequently be deleted.

A newly created PVC therefore received a newly provisioned PersistentVolume and did not contain the old data.

### Retain Policy

A dedicated StorageClass named `platform-retain` was created with:

    reclaimPolicy: Retain
    volumeBindingMode: WaitForFirstConsumer

A PVC backed by this StorageClass was populated with test data.

After deleting the PVC, the PersistentVolume remained available in the cluster rather than being deleted.

The retained PV was then recovered by:

1. removing the obsolete claim reference;
2. creating a recovery PVC targeting the original PersistentVolume;
3. binding the recovery PVC to that PV;
4. mounting it into a recovery Pod;
5. verifying the original data.

This demonstrated manual recovery of retained Kubernetes storage.

## Stateful Deployment Workload

A persistent Deployment named `persistent-worker` was created to consume the `platform-data` PVC.

The workload continuously writes heartbeat information to `/data` and maintains application state on the persistent volume.

The following behavior was validated:

- Deployment creation;
- PVC mounting;
- filesystem accessibility;
- persistent application state;
- Pod deletion and automatic recreation;
- reuse of the same PVC and PersistentVolume;
- survival of stored data across Pod recreation.

## StatefulSet Engineering

A two-replica StatefulSet named `stateful-worker` was implemented with a headless Service.

The StatefulSet uses a `volumeClaimTemplates` definition named `stateful-data`.

Each StatefulSet Pod receives its own persistent storage:

    stateful-worker-0
           |
           v
    stateful-data-stateful-worker-0
           |
           v
    Dedicated PersistentVolume

    stateful-worker-1
           |
           v
    stateful-data-stateful-worker-1
           |
           v
    Dedicated PersistentVolume

This provides stable storage identity independently for each Pod ordinal.

## Stable Pod Identity

The StatefulSet creates predictable Pod identities:

- `stateful-worker-0`
- `stateful-worker-1`

Using the headless `stateful-worker` Service, the expected stable DNS identities are:

    stateful-worker-0.stateful-worker.project4.svc.cluster.local
    stateful-worker-1.stateful-worker.project4.svc.cluster.local

Each Pod writes its hostname and ordinal-specific state to its own persistent volume.

## StatefulSet Persistence Validation

Persistent state was written independently to both StatefulSet replicas.

`stateful-worker-0` was then deleted.

Kubernetes recreated the same ordinal and reattached:

- the same PVC;
- the same PersistentVolume;
- the previously stored state.

The second ordinal remained unaffected.

This demonstrated the stable identity and persistent-storage guarantees provided by StatefulSets.

## StatefulSet Scaling and PVC Lifecycle

The StatefulSet was scaled from two replicas down to one.

During scale-down:

- `stateful-worker-1` was removed;
- its PVC remained Bound;
- its PersistentVolume remained Bound;
- `stateful-worker-0` remained unaffected.

The StatefulSet was then scaled back to two replicas.

`stateful-worker-1` returned and reclaimed its original PVC and PersistentVolume.

Its previously written state was successfully recovered.

This validates an important StatefulSet behavior: scaling down a StatefulSet does not automatically delete the persistent claims created by its volume claim templates.

## Storage Relationships

The validated Phase 6 runtime contains three primary claims:

    platform-data
        -> persistent-worker

    stateful-data-stateful-worker-0
        -> stateful-worker-0

    stateful-data-stateful-worker-1
        -> stateful-worker-1

All claims use `ReadWriteOnce` access mode and request 1Gi of storage.

## Recovery After Workstation Migration

During Phase 6 development, the workstation was restored from a Time Machine backup onto a replacement Mac.

The repository contents were successfully recovered, while the previous local kind cluster was unavailable because the Docker-backed cluster runtime was not part of the restored active environment.

The Kubernetes environment was reconstructed by:

1. restoring Docker Desktop;
2. recreating the multi-node kind cluster;
3. restoring the `project4` namespace;
4. rebuilding the application container image;
5. loading the image into the kind nodes;
6. restoring the Phase 5 application configuration;
7. reconstructing the Phase 6 storage baseline.

The recovered environment was validated before Phase 6 implementation continued.

This demonstrated an additional operational principle: declarative manifests and source-controlled infrastructure definitions allow an environment to be reconstructed even when ephemeral local runtime state is lost.

## Key Engineering Outcomes

Phase 6 demonstrates practical experience with:

- Kubernetes PersistentVolumes;
- PersistentVolumeClaims;
- StorageClasses;
- dynamic volume provisioning;
- `WaitForFirstConsumer` binding;
- `ReadWriteOnce` storage;
- reclaim policies;
- Delete-policy lifecycle behavior;
- Retain-policy lifecycle behavior;
- retained-volume recovery;
- persistent Deployment workloads;
- StatefulSets;
- headless Services;
- stable Pod identity;
- stable DNS identity;
- per-Pod persistent storage;
- `volumeClaimTemplates`;
- Pod recreation and data survival;
- StatefulSet scaling;
- PVC lifecycle behavior during scaling;
- recovery and reconstruction of a local Kubernetes environment.

## Phase 6 Result

Phase 6 successfully introduced persistent storage and stateful workload engineering into the Kubernetes Cloud-Native Platform.

The implementation progressed from basic PVC provisioning through lifecycle and reclaim-policy testing to Deployment persistence, StatefulSet identity, per-Pod storage, scale-down/scale-up recovery, and retained-volume recovery.

The final runtime demonstrated healthy application workloads together with multiple Bound PVC/PV relationships and verified persistent state across Pod recreation and StatefulSet scaling.
