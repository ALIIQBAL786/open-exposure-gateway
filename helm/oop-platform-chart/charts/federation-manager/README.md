# Federation Manager Helm Chart

Helm chart for deploying Federation Manager with Keycloak authentication for the Open Operator Platform.

## Components

This chart deploys:

- **Federation Manager** - Manages federation across multiple operators
- **Keycloak** - OAuth2/OpenID Connect authentication server
- **OpenVPN Sidecar** (Optional) - For remote federation connections

## Prerequisites

- Kubernetes 1.19+
- Helm 3.x
- kubectl configured

## Installation

### Quick Install

```bash
# Install with default values
helm install federation-manager . -n federation-manager --create-namespace
```

### Custom Installation

```bash
# Create custom values file
cat > my-values.yaml << EOF
federationManager:
  config:
    mongodb:
      host: "mongodb.oop.svc.cluster.local"  # Update if using external MongoDB
    
    op_data:
      partnerOPFederationId: "your-federation-id"
      partnerOPCountryCode: "US"
      # ... customize other settings
EOF

# Install with custom values
helm install federation-manager . -n federation-manager -f my-values.yaml
```

## Configuration

### Keycloak Configuration

The default Keycloak realm configuration includes:

- **Realm**: `federation`
- **Admin User**: `admin` / `admin` (change in production!)
- **Client ID**: `originating-op-1`
- **Client Secret**: `dd7vNwFqjNpYwaghlEwMbw10g0klWDHb`

#### ⚠️ About Keycloak Credentials

The default client credentials provided are **generic OAuth2 credentials** and can be used for testing. However, for production deployments:

**Option 1: Keep defaults** (for testing/development)
- The provided credentials will work out of the box
- Quick to get started

**Option 2: Generate new credentials** (recommended for production)

1. Deploy with defaults first
2. Access Keycloak UI at `http://<NODE-IP>:30081`
3. Login with admin/admin
4. Navigate to: Realm Settings → Clients → originating-op-1
5. Regenerate secret under "Credentials" tab
6. Update `values.yaml` with new secret:
   ```yaml
   keycloak:
     realm:
       client:
         secret: "your-new-secret"
   
   federationManager:
     config:
       keycloak:
         client1_secret: "your-new-secret"
   ```
7. Upgrade the deployment:
   ```bash
   helm upgrade federation-manager . -n federation-manager
   ```

### Federation Manager Configuration

Key configuration sections:

```yaml
federationManager:
  config:
    # Keycloak OAuth2 settings
    keycloak:
      client1_id: "originating-op-1"
      client1_secret: "dd7vNwFqjNpYwaghlEwMbw10g0klWDHb"
      scope: "fed-mgmt"
    
    # MongoDB connection
    mongodb:
      host: "mongodb.mongodb.svc.cluster.local"
      port: "27017"
    
    # Operator data
    op_data:
      partnerOPFederationId: "your-federation-id"
      partnerOPCountryCode: "US"
      # ... other settings
    
    # Partner operator settings
    partner_op:
      role: "partner_op"  # or "originating_op"
      host: "127.0.0.1"
      server: "/operatorplatform/federation/v1"
      port: "8992"
```

### OpenVPN Configuration (Optional)

To enable VPN connectivity for remote federation:

1. Create VPN secret:
   ```bash
   kubectl create secret generic partner-ovpn \
     --from-file=icom-client-1.ovpn=your-vpn-config.ovpn \
     --from-file=auth.txt=your-vpn-auth.txt \
     -n federation-manager
   ```

2. Enable in values.yaml:
   ```yaml
   openvpn:
     enabled: true
     secretName: partner-ovpn
     configFile: icom-client-1.ovpn
     authFile: auth.txt
   ```

3. Upgrade deployment:
   ```bash
   helm upgrade federation-manager . -n federation-manager
   ```

## Access

After deployment:

```bash
# Get node IP
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[0].address}')

# Access URLs
echo "Federation Manager: http://$NODE_IP:30989"
echo "Keycloak: http://$NODE_IP:30081"
echo "Keycloak Admin: http://$NODE_IP:30081/admin (admin/admin)"
```

## Common Operations

### Check Status

```bash
kubectl get pods -n federation-manager
kubectl get svc -n federation-manager
```

### View Logs

```bash
# Federation Manager logs
kubectl logs -f deployment/federation-manager -c federation-manager -n federation-manager

# Keycloak logs
kubectl logs -f deployment/keycloak -n federation-manager

# OpenVPN logs (if enabled)
kubectl logs -f deployment/federation-manager -c openvpn -n federation-manager
```

### Update Configuration

```bash
# Edit values.yaml
nano values.yaml

# Upgrade deployment
helm upgrade federation-manager . -n federation-manager
```

### Scale

```bash
# Scale Federation Manager
helm upgrade federation-manager . -n federation-manager --set federationManager.replicaCount=2

# Scale Keycloak
helm upgrade federation-manager . -n federation-manager --set keycloak.replicaCount=2
```

## Integration with OOP Platform

To integrate with the main OOP platform:

### Option 1: Add as Subchart

1. Copy this chart to OOP platform:
   ```bash
   cp -r federation-manager-chart oop-platform-chart/charts/federation-manager
   ```

2. Update OOP platform `Chart.yaml`:
   ```yaml
   dependencies:
     - name: federation-manager
       version: "1.0.0"
       condition: federationManager.enabled
   ```

3. Add to OOP platform `values.yaml`:
   ```yaml
   federationManager:
     enabled: true
     # ... federation manager configuration
   ```

4. Deploy complete platform:
   ```bash
   helm install oop-platform . -n oop
   ```

### Option 2: Deploy Separately

Deploy Federation Manager in its own namespace but configure to connect to OOP services:

```yaml
federationManager:
  config:
    mongodb:
      host: "mongosrm.oop.svc.cluster.local"  # Connect to SRM MongoDB
```

## Troubleshooting

### Keycloak Not Starting

```bash
# Check logs
kubectl logs deployment/keycloak -n federation-manager

# Common issues:
# - Realm import failed: Check ConfigMap
# - Port conflict: Ensure port 8080 is available
```

### Federation Manager Configuration Issues

```bash
# Check secret
kubectl get secret federation-manager-config -n federation-manager -o yaml

# Decode config
kubectl get secret federation-manager-config -n federation-manager \
  -o jsonpath='{.data.config\.cfg}' | base64 -d

# Check logs
kubectl logs deployment/federation-manager -c federation-manager -n federation-manager
```

### OpenVPN Connection Issues

```bash
# Check VPN secret exists
kubectl get secret partner-ovpn -n federation-manager

# Check OpenVPN logs
kubectl logs deployment/federation-manager -c openvpn -n federation-manager

# Check tun0 interface
kubectl exec -it deployment/federation-manager -c openvpn -n federation-manager -- ip a
```

## Security Considerations

### Production Deployment

1. **Change Keycloak Admin Password**
   ```yaml
   keycloak:
     admin:
       username: admin
       password: "StrongPassword123!"
   ```

2. **Regenerate Client Secrets** (see Keycloak Configuration section above)

3. **Use Secrets for Sensitive Data**
   ```bash
   kubectl create secret generic keycloak-admin \
     --from-literal=username=admin \
     --from-literal=password=secure-password \
     -n federation-manager
   ```

4. **Enable TLS/HTTPS**
   ```yaml
   keycloak:
     ingress:
       enabled: true
       tls:
         - secretName: keycloak-tls
           hosts:
             - keycloak.yourdomain.com
   ```

5. **Resource Limits**
   - Already configured with appropriate limits
   - Adjust based on your workload

## Uninstall

```bash
# Uninstall chart
helm uninstall federation-manager -n federation-manager

# Delete namespace (removes all resources)
kubectl delete namespace federation-manager

# Delete VPN secret (if created separately)
kubectl delete secret partner-ovpn -n federation-manager
```

## Values Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `keycloak.enabled` | Enable Keycloak deployment | `true` |
| `keycloak.service.nodePort` | NodePort for Keycloak | `30081` |
| `keycloak.admin.username` | Keycloak admin username | `admin` |
| `keycloak.admin.password` | Keycloak admin password | `admin` |
| `keycloak.realm.client.secret` | OAuth2 client secret | (see values.yaml) |
| `federationManager.enabled` | Enable Federation Manager | `true` |
| `federationManager.service.nodePort` | NodePort for Federation Manager | `30989` |
| `federationManager.config.partner_op.role` | Role: `partner_op` or `originating_op` | `partner_op` |
| `openvpn.enabled` | Enable OpenVPN sidecar | `false` |
| `openvpn.secretName` | Name of VPN secret | `partner-ovpn` |

For complete values reference, see `values.yaml`.

## Support

For issues and questions:
- **Repository**: https://labs.etsi.org/rep/oop
- **Issues**: Create an issue in the repository

## License

[Your License Here]
