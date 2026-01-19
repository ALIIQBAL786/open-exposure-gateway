#!/bin/bash
set -e

echo "Open Operator Platform Deployment (Multi-Release Mode)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Namespaces
OOP_NS="oop"
FM_NS="federation-manager"

# Release names
OOP_RELEASE="oop-platform"
FM_RELEASE="federation-manager"

echo ""
echo " Step 1/5: Creating namespaces..."
kubectl create namespace $OOP_NS 2>/dev/null || echo "   Namespace $OOP_NS already exists"
kubectl create namespace $FM_NS 2>/dev/null || echo "   Namespace $FM_NS already exists"

echo ""
echo "Step 2/5: Creating OOP service account..."
kubectl create serviceaccount oop-user -n $OOP_NS 2>/dev/null || echo "   Service account exists"
kubectl create clusterrolebinding oop-user-binding \
  --clusterrole=cluster-admin \
  --serviceaccount=$OOP_NS:oop-user \
  2>/dev/null || echo "   Binding exists"

TOKEN=$(kubectl -n $OOP_NS create token oop-user)

echo ""
echo "Updating values.yaml with token..."
sed -i "s|kubernetesMasterToken:.*|kubernetesMasterToken: \"$TOKEN\"|g" values.yaml

echo ""
echo "Step 3/5: Deploying SRM + OEG..."
helm install $OOP_RELEASE . \
  -n $OOP_NS \
  --create-namespace \
  --set federationManager.enabled=false

echo ""
echo "Step 4/5: Deploying Federation Manager..."
helm install $FM_RELEASE ./charts/federation-manager \
  -n $FM_NS \
  --create-namespace \
  --set createNamespace=true

echo ""
echo "Deployment completed!"
echo ""
echo " SRM + OEG in namespace:       $OOP_NS"
echo " Federation Manager in:         $FM_NS"
echo ""
echo "Check pods:"
echo "   kubectl get pods -n $OOP_NS"
echo "   kubectl get pods -n $FM_NS"
