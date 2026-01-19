# 🚀 Quick Deployment Guide - Open Operator Platform

## One-Command Deployment

Deploy the complete Open Operator Platform with a single command!

---

## Step-by-Step (5 Minutes)

### Step 1: Prepare (2 minutes)

```bash
# Create namespace
kubectl create namespace oop

# Create storage
sudo mkdir -p /mnt/data/mongodb_{srm,oeg}
sudo chmod 777 /mnt/data/mongodb_{srm,oeg}

# Create service account
kubectl create serviceaccount oop-user -n oop
kubectl create clusterrolebinding oop-user-binding \
  --clusterrole=cluster-admin \
  --serviceaccount=oop:oop-user

# Get token and copy it
kubectl create token oop-user -n oop --duration=87600h
```

---

### Step 2: Configure (1 minute)

```bash
# Edit values.yaml
nano values.yaml

# Find this line (around line 69):
# kubernetesMasterToken: "YOUR_KUBERNETES_TOKEN_HERE"

# Replace with your token from Step 1

# Save: Ctrl+X, Y, Enter
```

---

### Step 3: Deploy (1 minute)

```bash
# Deploy complete platform!
helm install oop-platform . -n oop

# Watch it start
kubectl get pods -n oop -w
```

Wait for all 5 pods to show `Running` (1/1)

Press `Ctrl+C` when done.

---

### Step 4: Access (1 minute)

```bash
# Get node IP
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[0].address}')

# Show URLs
echo "✅ Open Operator Platform Deployed!"
echo ""
echo "🌐 Access URLs:"
echo "   SRM:              http://$NODE_IP:32415"
echo "   Artifact Manager: http://$NODE_IP:30080"
echo "   OEG:              http://$NODE_IP:32263/oeg/1.0.0/docs/"
```

---

## ✅ Verification

```bash
# Check everything is running
kubectl get pods -n oop
kubectl get svc -n oop

# Test access
curl http://$NODE_IP:32415
```

---

## 🎯 Expected Result

```
NAME                              READY   STATUS    RESTARTS   AGE
artefact-manager-xxx              1/1     Running   0          2m
mongosrm-xxx                      1/1     Running   0          2m
srmcontroller-xxx                 1/1     Running   0          2m
oegmongo-xxx                      1/1     Running   0          2m
oegcontroller-xxx                 1/1     Running   0          2m
```

**All 5 pods Running = Success!** 🎉

---

## 🔧 Common Issues

### Token error
```bash
# Generate new token
kubectl create token oop-user -n oop --duration=87600h
# Update values.yaml and redeploy
```

### Storage error
```bash
# Check directories exist
ls -la /mnt/data/
# Fix permissions
sudo chmod 777 /mnt/data/mongodb_*
```

### Pod pending
```bash
# Check what's wrong
kubectl describe pod <pod-name> -n oop
```

---

## 🗑️ Clean Up

```bash
# Remove everything
helm uninstall oop-platform -n oop
kubectl delete namespace oop
```

---

**That's it! Your Open Operator Platform is ready!** 🚀
