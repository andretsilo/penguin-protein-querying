#!/bin/bash

# Deploy all Kubernetes resources in order

echo "Creating namespace..."
kubectl apply -f namespace.yaml

echo "Creating ConfigMaps and Secrets..."
kubectl apply -f mongo-configmap.yaml
kubectl apply -f neo4j-secret.yaml

echo "Deploying databases..."
kubectl apply -f mongodb.yaml
kubectl apply -f neo4j.yaml

echo "Waiting for databases to be ready..."
kubectl wait --for=condition=ready pod -l app=mongodb -n penguin-protein --timeout=300s
kubectl wait --for=condition=ready pod -l app=neo4j -n penguin-protein --timeout=300s

echo "Deploying application services..."
kubectl apply -f jaccard-service.yaml
kubectl apply -f mongo-api.yaml
kubectl apply -f protein-neo4j.yaml

echo "Deployment complete!"
echo ""
echo "Check status with:"
echo "  kubectl get pods -n penguin-protein"
echo "  kubectl get svc -n penguin-protein"
