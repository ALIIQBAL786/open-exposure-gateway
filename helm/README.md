# Open Operator Platform (OOP)

## KIND Deployment via Helm

---

## 1. Introduction

This repository provides a **Helm-based reference deployment of the Open Operator Platform (OOP)** on a **local Kubernetes-in-Docker (KIND) cluster**.

The deployment enables **fast, reproducible installation** of core OOP components for:

* Local development
* Integration testing
* API experimentation
* Research and demonstrations

This setup is for development and testing only and MUST NOT be used in production environments.

You can deploy the charts and in non-kind environments

This is work in progress.


## 2. Deployed Components

The solution deploys the following components inside a single KIND cluster:

* **Open Exposure Gateway (OEG)**

  * Northbound API entry point for tenants/applications
  * Handles application onboarding and exposure workflows
  * Acts as the main entry point to the Operator Platform
  * Backed by MongoDB

* **Service Resource Manager (SRM)**

  * Manages application artefacts and lifecycle
  * Interfaces with edge/cloud resources
  * Supports southbound orchestration workflows
  * Backed by MongoDB with PV/PVC support

* **Federation Manager (FM)**

  * Manages inter-operator federation workflows
  * Handles partner Operator (OP) discovery and onboarding
  * Supports federated artefact creation and exchange
  * Enables cross-domain and multi-operator edge deployments
  * Backed by MongoDB

---

## 3. Prerequisites

### 3.1 Required Software

| Tool | Minimum Version |
|---|---|
| Docker | 20.x |
| KIND | 0.20 |
| kubectl | 1.25 |
| Helm | v3+ |
| Bash | 4+ |

### 3.2 Verify Installation

```bash
docker --version
kind --version
kubectl version --client
helm version
````

---

## 4. Deployment Methods

Two deployment approaches are supported:

1. **Automatic deployment** (recommended)
2. **Manual step-by-step deployment**

---

## 5. Automatic Deployment (Recommended)

### 5.1 Description

The automatic deployment method:

* Creates a KIND cluster
* Configures Kubernetes networking
* Installs all OOP components via Helm

All steps are executed by a single script.

### 5.2 Steps

```bash
chmod +x deploy-on-kind.sh
./deploy-on-kind.sh
```

### 5.3 What This Script Does

1. Creates a KIND cluster using `kind-oop-config.yaml`
2. Configures `kubectl` context
3. Deploys the umbrella Helm chart (`oop-platform-chart`)
4. Waits for core services to start

---

## 6. Manual Deployment (Step-by-Step)

### 6.1 Create the KIND Cluster

```bash
kind create cluster \
  --name oop \
  --config kind-oop-config.yaml
```

Verify cluster:

```bash
kubectl cluster-info
```

---

### 6.2 Deploy OOP Using Helm

From the repository root:

```bash
helm install oop-platform ./oop-platform-chart
```

To upgrade an existing deployment:

```bash
helm upgrade oop-platform ./oop-platform-chart
```

---

### 6.3 Verify Deployment

```bash
kubectl get pods -A
kubectl get svc -A
```

All pods should reach `Running` or `Completed` state.

---

## 7. Configuration

All configuration parameters are centralized in:

```
oop-platform-chart/values.yaml
```

Supported configuration options include:

* Container images and tags
* Service ports
* MongoDB configuration
* Ingress enablement
* Resource limits and requests

After modifying values:

```bash
helm upgrade oop-platform ./oop-platform-chart
```

---

## 8. Accessing Services

Services are exposed via Kubernetes `Service` objects.

Typical access methods:

* `kubectl port-forward`
* Ingress (if enabled)
* NodePort (local testing) --> current deployment


---

## 9. Verification & Health Checks

```bash
kubectl get deployments -A
kubectl get statefulsets -A
kubectl describe pod <pod-name>
```

Refer to:

```
oop-platform-chart/VERIFICATION.txt
```

---

## 10. Cleanup

### 10.1 Remove Helm Deployment

```bash
helm uninstall oop-platform
```

### 10.2 Delete KIND Cluster

```bash
kind delete cluster --name oop
```

---

## 11. Troubleshooting

### Pods Not Starting

```bash
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

### Helm Errors

```bash
helm status oop-platform
```

### Reset Everything

```bash
kind delete cluster --name oop
./deploy-on-kind.sh
```

---



