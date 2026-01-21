# Kubernetes Deployment Guide

## Prerequisites

- Kubernetes cluster (minikube, EKS, GKE, AKS, etc.)
- kubectl configured
- Docker images built and pushed to a registry

## Build and Push Docker Images

```bash
# Build Mongo API
cd services/mongo
docker build -t your-registry/mongo-api:latest .
docker push your-registry/mongo-api:latest

# Build Neo4j Service
cd ../neo4j/protein-neo4j
docker build -t your-registry/protein-neo4j:latest .
docker push your-registry/protein-neo4j:latest

# Build Jaccard Service (create Dockerfile first)
cd ../../jaccard
docker build -t your-registry/jaccard-service:latest .
docker push your-registry/jaccard-service:latest
```

## Update Image References

Before deploying, update the image references in the YAML files:
- `jaccard-service.yaml`: Replace `your-registry/jaccard-service:latest`
- `mongo-api.yaml`: Replace `your-registry/mongo-api:latest`
- `protein-neo4j.yaml`: Replace `your-registry/protein-neo4j:latest`

## Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy ConfigMaps and Secrets
kubectl apply -f k8s/mongo-configmap.yaml
kubectl apply -f k8s/neo4j-secret.yaml

# Deploy databases
kubectl apply -f k8s/mongodb.yaml
kubectl apply -f k8s/neo4j.yaml

# Wait for databases to be ready
kubectl wait --for=condition=ready pod -l app=mongodb -n penguin-protein --timeout=300s
kubectl wait --for=condition=ready pod -l app=neo4j -n penguin-protein --timeout=300s

# Deploy services
kubectl apply -f k8s/jaccard-service.yaml
kubectl apply -f k8s/mongo-api.yaml
kubectl apply -f k8s/protein-neo4j.yaml
```

## Verify Deployment

```bash
# Check all pods
kubectl get pods -n penguin-protein

# Check services
kubectl get svc -n penguin-protein

# Check logs
kubectl logs -f deployment/mongo-api -n penguin-protein
kubectl logs -f deployment/protein-neo4j -n penguin-protein
kubectl logs -f deployment/jaccard-service -n penguin-protein
```

## Access Services

```bash
# Get external IPs (for LoadBalancer services)
kubectl get svc -n penguin-protein

# Port forward for local testing
kubectl port-forward svc/mongo-api 8000:80 -n penguin-protein
kubectl port-forward svc/protein-neo4j 8080:8080 -n penguin-protein
kubectl port-forward svc/neo4j 7474:7474 -n penguin-protein
```

## Scale Services

```bash
# Scale Mongo API
kubectl scale deployment mongo-api --replicas=3 -n penguin-protein

# Scale Neo4j Service
kubectl scale deployment protein-neo4j --replicas=3 -n penguin-protein
```

## Update Deployment

```bash
# Update image
kubectl set image deployment/mongo-api mongo-api=your-registry/mongo-api:v2 -n penguin-protein

# Rollback
kubectl rollout undo deployment/mongo-api -n penguin-protein
```

## Clean Up

```bash
# Delete all resources
kubectl delete namespace penguin-protein
```

## Notes

- MongoDB and Neo4j use PersistentVolumeClaims for data persistence
- Adjust resource limits based on your cluster capacity
- For production, consider using StatefulSets for databases
- Update Neo4j password in `neo4j-secret.yaml` before deploying
- Services use LoadBalancer type; change to NodePort or Ingress as needed
