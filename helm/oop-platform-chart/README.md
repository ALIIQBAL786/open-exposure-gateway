# Open Operator Platform (OOP) Helm Chart

**Complete deployment of the Open Operator Platform for 6G networks**

## 🌟 Overview

This Helm chart deploys the complete Open Operator Platform (OOP), including:

- **SRM (Service Resource Manager)** - Manages service resources and lifecycle
- **OEG (Open Exposure Gateway)** - Provides standardized API exposure
- **Federation Manager** - Manages federation across multiple operators *(to be added)*

## 📋 Components

### Currently Deployed

## 📋 Components

### Deployed in `oop` namespace

| Component | Description | Pods | Services |
|-----------|-------------|------|----------|
| **SRM** | Service Resource Manager | srmcontroller | srm:32415 |
| | MongoDB for SRM | mongosrm | mongosrm:27017 |
| | Artifact Manager | artefact-manager | artefact-manager:30080 |
| **OEG** | Open Exposure Gateway | oegcontroller | oeg:32263 |
| | MongoDB for OEG | oegmongo | oegmongo:27017 |

**Total in `oop` namespace:** 5 pods, 5 services

### Deployed in `federation-manager` namespace

| Component | Description | Pods | Services |
|-----------|-------------|------|----------|
| **Federation Manager** | Federation management | federation-manager | federation-manager:30989 |
| **Keycloak** | OAuth2/OIDC authentication | keycloak | keycloak:30081 |

**Total in `federation-manager` namespace:** 2 pods, 2 services

### Complete Platform
**Total across all namespaces:** 7 pods, 7 services in 2 namespaces

## 🚀 Quick Start

### Prerequisites

- **Kubernetes** 1.19+ (MicroK8s, kind, k3s, or standard Kubernetes)
- **Helm** 3.x
- **kubectl** configured and working
- **Storage** directories for persistent data

### 1. Prepare Environment

```bash
# Create namespace
kubectl create namespace oop

# Create storage directories
sudo mkdir -p /mnt/data/mongodb_srm
sudo mkdir -p /mnt/data/mongodb_oeg
sudo chmod 777 /mnt/data/mongodb_srm /mnt/data/mongodb_oeg

# For kind, use /tmp/kind-storage instead
```

### 2. Create Service Account and Get Token

```bash
# Create service account
kubectl create serviceaccount oop-user -n oop

# Create cluster role binding
kubectl create clusterrolebinding oop-user-binding \
  --clusterrole=cluster-admin \
  --serviceaccount=oop:oop-user

# Get token (save this!)
kubectl create token oop-user -n oop --duration=87600h
```

### 3. Configure the Platform

```bash
# Edit values.yaml
nano values.yaml
```

**Update the Kubernetes token:**

```yaml
srm:
  srmcontroller:
    env:
      kubernetesMasterToken: "PASTE_YOUR_TOKEN_HERE"
```

### 4. Deploy Complete Platform

```bash
# Deploy everything with one command!
helm install oop-platform . -n oop

# Watch deployment
kubectl get pods -n oop -w
```

Press `Ctrl+C` when all 5 pods show `Running` status.

### 5. Verify Deployment

```bash
# Check all pods across both namespaces
kubectl get pods -n oop
kubectl get pods -n federation-manager

# Expected output in oop namespace:
# NAME                              READY   STATUS    RESTARTS   AGE
# mongosrm-xxx                      1/1     Running   0          2m
# srmcontroller-xxx                 1/1     Running   0          2m
# artefact-manager-xxx              1/1     Running   0          2m
# oegmongo-xxx                      1/1     Running   0          2m
# oegcontroller-xxx                 1/1     Running   0          2m

# Expected output in federation-manager namespace:
# NAME                              READY   STATUS    RESTARTS   AGE
# keycloak-xxx                      1/1     Running   0          2m
# federation-manager-xxx            1/1     Running   0          2m

# Check services
kubectl get svc -n oop
```

### 6. Access the Platform

```bash
# Get your node IP
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[0].address}')

# Display access URLs
echo "🌐 Open Operator Platform Access URLs:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SRM Dashboard:        http://$NODE_IP:32415"
echo "📦 Artifact Manager:     http://$NODE_IP:30080"
echo "🔌 OEG API:             http://$NODE_IP:32263/oeg/1.0.0/docs/"
echo "🔐 Keycloak:            http://$NODE_IP:30081"
echo "🌐 Federation Manager:  http://$NODE_IP:30989"
```

**For kind users:** Replace `$NODE_IP` with `localhost`

---

## ⚙️ Configuration

### Essential Configuration

```yaml
# Global settings
global:
  namespace: oop

# Enable/disable components
srm:
  enabled: true
oeg:
  enabled: true

# Kubernetes token (REQUIRED)
srm:
  srmcontroller:
    env:
      kubernetesMasterToken: "YOUR_TOKEN"
```

### Storage Configuration

#### For MicroK8s / k3s (hostPath)
```yaml
mongodb:
  persistence:
    storageClass: manual
    hostPath:
      enabled: true
      path: /mnt/data/mongodb_srm
```

#### For kind (Docker volumes)
```yaml
mongodb:
  persistence:
    storageClass: manual
    hostPath:
      enabled: true
      path: /mnt/data/mongodb_srm  # Mapped from /tmp/kind-storage
```

#### For Cloud Providers (dynamic provisioning)
```yaml
mongodb:
  persistence:
    storageClass: standard  # or gp2, pd-ssd, etc.
    hostPath:
      enabled: false
    createPV: false
```

### Resource Configuration

```yaml
# Adjust resources based on your needs
srmcontroller:
  resources:
    limits:
      cpu: 2000m
      memory: 2Gi
    requests:
      cpu: 1000m
      memory: 1Gi
```

### Service Types

```yaml
# Change service types
srmcontroller:
  service:
    type: LoadBalancer  # Instead of NodePort for cloud
```

---

## 🎯 Selective Deployment

### Deploy Only SRM

```bash
helm install srm-only . -n oop --set oeg.enabled=false
```

### Deploy Only OEG

```bash
helm install oeg-only . -n oop --set srm.enabled=false
```

### Deploy with Custom Resources

```bash
helm install oop-platform . -n oop \
  --set srm.srmcontroller.replicaCount=3 \
  --set oeg.oegcontroller.replicaCount=2
```

---

## 🔄 Operations

### Upgrade Platform

```bash
# Update values.yaml, then:
helm upgrade oop-platform . -n oop

# Or upgrade specific component
helm upgrade oop-platform . -n oop --set srm.srmcontroller.image.tag=1.0.2
```

### Check Status

```bash
# Helm release status
helm status oop-platform -n oop

# Pod status
kubectl get pods -n oop

# Service status
kubectl get svc -n oop

# Check logs
kubectl logs -f deployment/srmcontroller -n oop
kubectl logs -f deployment/oegcontroller -n oop
```

### Scale Components

```bash
# Scale SRM
helm upgrade oop-platform . -n oop --set srm.srmcontroller.replicaCount=3

# Scale OEG
helm upgrade oop-platform . -n oop --set oeg.oegcontroller.replicaCount=2
```

### Rollback

```bash
# View history
helm history oop-platform -n oop

# Rollback to previous version
helm rollback oop-platform -n oop

# Rollback to specific revision
helm rollback oop-platform 2 -n oop
```

---

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Describe the pod
kubectl describe pod <pod-name> -n oop

# Check events
kubectl get events -n oop --sort-by='.lastTimestamp'

# View logs
kubectl logs <pod-name> -n oop
kubectl logs <pod-name> -n oop --previous  # Previous crash
```

### PVC Not Binding

```bash
# Check PVC status
kubectl get pvc -n oop
kubectl describe pvc <pvc-name> -n oop

# Ensure directories exist
ls -la /mnt/data/
sudo chmod 777 /mnt/data/mongodb_*
```

### Service Connection Issues

```bash
# Check service endpoints
kubectl get endpoints -n oop

# Test connectivity from within cluster
kubectl run test-pod --image=curlimages/curl -it --rm --restart=Never -n oop -- \
  curl http://srm:8080
```

### Token Issues

If you see authentication errors:

```bash
# Generate new token
kubectl create token oop-user -n oop --duration=87600h

# Update values.yaml and upgrade
helm upgrade oop-platform . -n oop
```

---

## 🗑️ Uninstall

### Remove Platform

```bash
# Uninstall Helm release
helm uninstall oop-platform -n oop

# Delete namespace (removes all resources)
kubectl delete namespace oop

# Clean up persistent volumes (optional)
kubectl delete pv mongodb-pv-volume mongodb-oeg-pv-volume

# Remove storage directories (optional)
sudo rm -rf /mnt/data/mongodb_srm /mnt/data/mongodb_oeg
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────┐
│           Open Operator Platform (OOP)              │
│                  Namespace: oop                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  SRM (Service Resource Manager)              │  │
│  │  ├─ MongoDB (mongosrm) :27017               │  │
│  │  ├─ SRM Controller :8080 (NodePort :32415)  │  │
│  │  └─ Artifact Manager :8000 (NodePort :30080)│  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  OEG (Open Exposure Gateway)                 │  │
│  │  ├─ MongoDB (oegmongo) :27017               │  │
│  │  └─ OEG Controller :8080 (NodePort :32263)  │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  Federation Manager (Coming Soon)            │  │
│  │  └─ To be added                              │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🔐 Security Considerations

### Production Deployments

1. **Use Secrets for Tokens**
   ```bash
   kubectl create secret generic oop-secrets \
     --from-literal=k8s-token=YOUR_TOKEN \
     -n oop
   ```

2. **Enable TLS/HTTPS**
   ```yaml
   ingress:
     enabled: true
     tls:
       enabled: true
   ```

3. **Use Specific Image Tags**
   ```yaml
   image:
     tag: "1.0.1"  # Not "latest"
   ```

4. **Set Resource Limits**
   ```yaml
   resources:
     limits:
       cpu: 1000m
       memory: 1Gi
   ```

---

## 🌐 Multi-Cluster Deployment

This chart can be deployed to multiple clusters:

```bash
# Cluster 1
kubectl config use-context cluster1
helm install oop-platform . -n oop

# Cluster 2
kubectl config use-context cluster2
helm install oop-platform . -n oop
```

---

## 📈 Monitoring

### Prometheus Integration (Optional)

```yaml
# Add to values.yaml
monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
```

### Basic Monitoring

```bash
# Watch resource usage
kubectl top pods -n oop
kubectl top nodes

# Check pod restarts
kubectl get pods -n oop -o wide
```

---

## 🤝 Contributing

To contribute to this Helm chart:

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a merge request

---

## 📞 Support

For issues and questions:
- **Repository:** https://labs.etsi.org/rep/oop/code/open-exposure-gateway
- **Issues:** Create an issue in the repository
- **Documentation:** See docs/ directory

---

## 📝 License

[Your License Here]

---

## 🎉 Quick Reference

```bash
# Deploy
helm install oop-platform . -n oop

# Upgrade
helm upgrade oop-platform . -n oop

# Status
kubectl get pods -n oop

# Logs
kubectl logs -f deployment/srmcontroller -n oop

# Uninstall
helm uninstall oop-platform -n oop
```

---

**Open Operator Platform - Empowering 6G Network Innovation** 🚀
