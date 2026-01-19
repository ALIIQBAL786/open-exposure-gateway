# SRM Helm Chart

Service Resource Manager with MongoDB and Artifact Manager for Sunrise 6G Platform.

## Quick Deploy on MicroK8s

```bash
# 1. Prepare
kubectl create namespace sunrise6g
sudo mkdir -p /mnt/data/mongodb_srm
sudo chmod 777 /mnt/data/mongodb_srm

# 2. Deploy
helm install srm . -n sunrise6g

# 3. Verify
kubectl get pods -n sunrise6g
kubectl get svc -n sunrise6g

# 4. Access (get your node IP first)
kubectl get nodes -o wide
# Then access: http://<NODE-IP>:32415 (SRM)
# And: http://<NODE-IP>:30080 (Artifact Manager)
```

## What's Included

- **SRM Controller** - Service Resource Manager
- **MongoDB** - Database with persistent storage
- **Artifact Manager** - Artifact management service

## Components

| Component | Service Type | Port | NodePort |
|-----------|-------------|------|----------|
| SRM Controller | NodePort | 8080 | 32415 |
| Artifact Manager | NodePort | 8000 | 30080 |
| MongoDB (SRM) | ClusterIP | 27017 | - |

## Configuration

Edit `values.yaml` to customize:

### Service Types
```yaml
srmcontroller:
  service:
    type: NodePort  # or ClusterIP, LoadBalancer
    nodePort: 32415 # Remove for ClusterIP
```

### Resources
```yaml
srmcontroller:
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
```

### MongoDB Storage
```yaml
mongodb:
  persistence:
    size: 200Mi  # Adjust as needed
    hostPath:
      path: /mnt/data/mongodb_srm
```

### Important: Update Kubernetes Token

Get your token:
```bash
kubectl create serviceaccount sunrise-user -n sunrise6g
kubectl create clusterrolebinding sunrise-user-binding \
  --clusterrole=cluster-admin \
  --serviceaccount=sunrise6g:sunrise-user

TOKEN=$(kubectl get secret $(kubectl get serviceaccount sunrise-user -n sunrise6g -o jsonpath='{.secrets[0].name}') -n sunrise6g -o jsonpath='{.data.token}' | base64 -d)
echo $TOKEN
```

Update in `values.yaml`:
```yaml
srmcontroller:
  env:
    kubernetesMasterToken: "YOUR_TOKEN_HERE"
```

## Deployment Options

### Enable/Disable Components

```yaml
mongodb:
  enabled: true  # Set to false to use external MongoDB

artifactManager:
  enabled: true  # Set to false if deployed separately
```

### Use External MongoDB

```yaml
mongodb:
  enabled: false

srmcontroller:
  env:
    empStorageUri: "mongodb://external-mongo:27017"
```

## Access Methods

### NodePort (Default)
```bash
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
echo "SRM: http://$NODE_IP:32415"
echo "Artifact Manager: http://$NODE_IP:30080"
```

### Port Forward
```bash
# SRM
kubectl port-forward svc/srm 8080:8080 -n sunrise6g
# Access: http://localhost:8080

# Artifact Manager
kubectl port-forward svc/artefact-manager-service 8000:8000 -n sunrise6g
# Access: http://localhost:8000
```

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods -n sunrise6g
kubectl describe pod <pod-name> -n sunrise6g
```

### View Logs
```bash
# SRM logs
kubectl logs -f deployment/srmcontroller -n sunrise6g

# MongoDB logs
kubectl logs -f deployment/mongosrm -n sunrise6g

# Artifact Manager logs
kubectl logs -f deployment/artefact-manager -n sunrise6g
```

### PVC Issues
```bash
# Check PVC status
kubectl get pvc -n sunrise6g
kubectl describe pvc mongo-db -n sunrise6g

# Ensure directory exists
sudo mkdir -p /mnt/data/mongodb_srm
sudo chmod 777 /mnt/data/mongodb_srm
```

## Upgrade

```bash
# Edit values.yaml, then:
helm upgrade srm . -n sunrise6g

# Or with command line overrides:
helm upgrade srm . --set srmcontroller.replicaCount=2 -n sunrise6g
```

## Uninstall

```bash
helm uninstall srm -n sunrise6g
kubectl delete pv mongodb-pv-volume  # If using hostPath
```

## For More Information

See **MICROK8S_GUIDE.md** for complete step-by-step deployment instructions.
