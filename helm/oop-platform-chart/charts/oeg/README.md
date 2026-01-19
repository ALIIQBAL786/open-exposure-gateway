# OEG Helm Chart

A production-ready Helm chart for deploying OEG Controller with MongoDB on Kubernetes.

## Overview

This Helm chart deploys:
- **OEG Controller**: Main application server
- **MongoDB**: Database for OEG Controller
- **Ingress**: External access configuration
- **PersistentVolume/PersistentVolumeClaim**: Data persistence

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Traefik ingress controller (or modify for your ingress)
- StorageClass configured (for dynamic provisioning)

## Installation

### Quick Start

```bash
# Add the chart repository (if published)
helm repo add oeg https://your-repo-url
helm repo update

# Install with default values
helm install oeg ./oeg-chart -n sunrise6g --create-namespace

# Or install with specific environment values
helm install oeg ./oeg-chart -f values-dev.yaml -n sunrise6g-dev --create-namespace
```

### Installation Commands by Environment

**Development:**
```bash
helm install oeg-dev ./oeg-chart \
  -f values-dev.yaml \
  -n sunrise6g-dev \
  --create-namespace
```

**Staging:**
```bash
helm install oeg-staging ./oeg-chart \
  -f values-staging.yaml \
  -n sunrise6g-staging \
  --create-namespace
```

**Production:**
```bash
helm install oeg-prod ./oeg-chart \
  -f values-prod.yaml \
  -n sunrise6g \
  --create-namespace
```

## Configuration

### Key Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.namespace` | Kubernetes namespace | `sunrise6g` |
| `mongodb.enabled` | Enable MongoDB deployment | `true` |
| `mongodb.image.tag` | MongoDB image tag | `latest` |
| `mongodb.persistence.size` | PVC storage size | `50Mi` |
| `mongodb.persistence.storageClass` | Storage class name | `manual` |
| `mongodb.persistence.createPV` | Create PersistentVolume | `true` |
| `oegcontroller.enabled` | Enable OEG Controller | `true` |
| `oegcontroller.replicaCount` | Number of replicas | `1` |
| `oegcontroller.image.tag` | Controller image tag | `1.0.1` |
| `oegcontroller.env.mongoUri` | MongoDB connection URI | `mongodb://oegmongo:27017` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.host` | Ingress hostname | `isiath.duckdns.org` |
| `ingress.path` | Ingress path | `/oeg` |

### Environment Variables

The following environment variables can be configured for the OEG Controller:

- `MONGO_URI`: MongoDB connection string
- `SRM_HOST`: SRM service host URL
- `FEDERATION_MANAGER_HOST`: Federation manager service URL
- `PARTNER_API_ROOT`: Partner API root URL
- `TOKEN_ENDPOINT`: OAuth token endpoint URL

## Storage Configuration

### Local Development (hostPath)

For local development with minikube or kind:

```yaml
mongodb:
  persistence:
    hostPath:
      enabled: true
      path: /mnt/data/mongodb_oeg
    createPV: true
```

### Cloud Environments (Dynamic Provisioning)

For cloud providers (AWS, GCP, Azure):

```yaml
mongodb:
  persistence:
    storageClass: standard  # or gp2, pd-standard, etc.
    hostPath:
      enabled: false
    createPV: false
```

## Upgrading

```bash
# Upgrade with new values
helm upgrade oeg ./oeg-chart -f values-prod.yaml -n sunrise6g

# Upgrade with specific parameters
helm upgrade oeg ./oeg-chart \
  --set oegcontroller.image.tag=1.0.2 \
  -n sunrise6g
```

## Uninstalling

```bash
helm uninstall oeg -n sunrise6g
```

**Note:** PersistentVolumes may need to be manually deleted:

```bash
kubectl delete pv mongodb-oeg-pv-volume
```

## Common Operations

### Check Deployment Status

```bash
kubectl get pods -n sunrise6g
kubectl get svc -n sunrise6g
kubectl get ingress -n sunrise6g
```

### View Logs

```bash
# OEG Controller logs
kubectl logs -f deployment/oegcontroller -n sunrise6g

# MongoDB logs
kubectl logs -f deployment/oegmongo -n sunrise6g
```

### Access MongoDB

```bash
# Port forward to MongoDB
kubectl port-forward svc/oegmongo 27017:27017 -n sunrise6g

# Connect using mongo client
mongo mongodb://localhost:27017
```

### Scale the Application

```bash
helm upgrade oeg ./oeg-chart \
  --set oegcontroller.replicaCount=3 \
  -n sunrise6g
```

## Troubleshooting

### Pod Not Starting

```bash
kubectl describe pod <pod-name> -n sunrise6g
kubectl logs <pod-name> -n sunrise6g
```

### PVC Pending

Check if the StorageClass exists:
```bash
kubectl get storageclass
```

For manual provisioning, ensure the PV is created:
```bash
kubectl get pv
```

### Ingress Not Working

Verify ingress controller is running:
```bash
kubectl get pods -n kube-system | grep traefik
```

Check ingress resource:
```bash
kubectl describe ingress oegcontroller-ingress -n sunrise6g
```

## Advanced Configuration

### Using External MongoDB

To use an external MongoDB instance:

```yaml
mongodb:
  enabled: false

oegcontroller:
  env:
    mongoUri: "mongodb://external-mongo.example.com:27017/oeg"
```

### Adding Secrets

For sensitive data, use Kubernetes secrets:

```bash
kubectl create secret generic oeg-secrets \
  --from-literal=mongo-password=yourpassword \
  -n sunrise6g
```

Then reference in values:

```yaml
oegcontroller:
  env:
    mongoUri: "mongodb://user:$(MONGO_PASSWORD)@oegmongo:27017"
  envFrom:
    - secretRef:
        name: oeg-secrets
```

### Resource Limits

Adjust resource limits based on your workload:

```yaml
oegcontroller:
  resources:
    limits:
      cpu: 2000m
      memory: 2Gi
    requests:
      cpu: 1000m
      memory: 1Gi
```

## Values Files Structure

The chart includes environment-specific values files:

- `values.yaml` - Base configuration with defaults
- `values-dev.yaml` - Development environment overrides
- `values-staging.yaml` - Staging environment configuration
- `values-prod.yaml` - Production environment configuration

## Best Practices

1. **Use specific image tags** in production (avoid `latest`)
2. **Enable resource limits** to prevent resource exhaustion
3. **Use dynamic provisioning** for cloud environments
4. **Enable TLS** for production ingress
5. **Set appropriate replica counts** for high availability
6. **Use secrets** for sensitive configuration
7. **Implement backup strategy** for MongoDB data

## Support

For issues and questions:
- Check the [troubleshooting section](#troubleshooting)
- Review Kubernetes events: `kubectl get events -n sunrise6g`
- Check application logs

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]
