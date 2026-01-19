#!/bin/bash

# ====================================================================
# Deploy Open Operator Platform (OOP) on kind
# ====================================================================

set -e

echo "OOP Platform Deployment on kind"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check prerequisites
echo " Checking prerequisites..."

if ! command -v kind &> /dev/null; then
    echo " kind is not installed"
    echo "   Install: https://kind.sigs.k8s.io/"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo " kubectl is not installed"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo " helm is not installed"
    exit 1
fi

echo " All prerequisites met"
echo ""

# Step 1: Create storage directories
echo " Step 1/5: Creating storage directories..."
sudo mkdir -p /tmp/kind-oop/mongodb_srm /tmp/kind-oop/mongodb_oeg 2>/dev/null || true
sudo chmod -R 777 /tmp/kind-oop/ 2>/dev/null || true
echo "   Storage directories ready"
echo ""

# Step 2: Create kind cluster
echo " Step 2/5: Creating kind cluster..."

if kind get clusters | grep -q "oop-cluster"; then
    echo "   Cluster 'oop-cluster' already exists"
    read -p "   Delete and recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kind delete cluster --name oop-cluster
    else
        echo "   Using existing cluster"
    fi
fi

if ! kind get clusters | grep -q "oop-cluster"; then
    kind create cluster --config kind-oop-config.yaml
    echo "   Cluster created"
else
    echo "   Using existing cluster"
fi

# Set context
kubectl config use-context kind-oop-cluster
echo ""

# Step 3: Wait for cluster ready
echo " Step 3/5: Waiting for cluster to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=120s
echo "   Cluster ready"
echo ""

# Step 4: Deploy OOP platform
echo " Step 4/5: Deploying OOP Platform..."

if [ -d "oop-platform-chart" ]; then
    cd oop-platform-chart
    ./deploy.sh
else
    echo " oop-platform-chart directory not found"
    echo "   Please extract oop-platform-chart.zip first"
    exit 1
fi

echo ""

# Step 5: Show access information
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Access URLs (via localhost)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   SRM Dashboard:        http://localhost:32415"
echo "   Artifact Manager:     http://localhost:30080"
echo "   OEG API:             http://localhost:32263/oeg/1.0.0/docs/"
echo "   Keycloak:            http://localhost:30081"
echo "   Keycloak Admin:      http://localhost:30081/admin"
echo "      (Username: admin / Password: admin)"
echo "   Federation Manager:  http://localhost:30989"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Deployment complete!"
echo ""
echo "Useful commands:"
echo "   kubectl get pods -n oop"
echo "   kubectl get pods -n federation-manager"
echo "   kubectl logs -f deployment/srmcontroller -n oop"
echo "   kind delete cluster --name oop-cluster  # To cleanup"
echo ""
