# Penguin Protein Querying

A microservices-based system for analyzing and querying protein data from emperor penguins using MongoDB, Neo4j, and Jaccard similarity coefficients.

## Overview

This project processes protein data from UniProt for emperor penguins, computing similarity metrics between proteins and storing the results in a graph database for efficient querying and visualization.

## Architecture

The system consists of four main services:

### 1. **Mongo Service** (FastAPI)
- REST API built with FastAPI
- Connects to MongoDB to retrieve protein data
- Sends protein data in batches to the Jaccard service for similarity computation
- Entry point for data processing pipeline

### 2. **Jaccard Service** (gRPC - Python)
- gRPC server for high-performance computation
- Calculates Jaccard similarity coefficients between protein sequences
- Sends computed results to the Neo4j service for persistence
- Handles batch processing efficiently
- Includes utilities for data injection, state management, and recalculation

### 3. **Neo4j Service** (Spring Boot)
- Spring Boot application with Neo4j integration
- Persists protein relationships and similarity data as a graph
- Provides query capabilities for protein network analysis
- Stores computed Jaccard coefficients as relationship properties

### 4. **Frontend** (React + Vite)
- Modern React-based web interface
- Built with Vite for fast development and optimized builds
- Material-UI and Radix UI components for rich user experience
- Visualizes protein networks and similarity data
- Interactive protein querying and exploration

## Data Flow

```
MongoDB → FastAPI Service → gRPC Jaccard Service → Spring Boot Service → Neo4j
```

1. Protein data is stored in MongoDB
2. FastAPI service retrieves and batches protein data
3. Jaccard service computes similarity coefficients
4. Spring Boot service persists results to Neo4j graph database

## Dataset

The project uses emperor penguin protein data from UniProt:
- Location: `services/mongo/data/protein_penguin.tsv`
- Format: TSV (Tab-Separated Values)
- Also available in compressed format: `protein_penguin.tsv.gz`

## Project Structure

```
penguin-protein-querying/
│
├── services/
│   ├── mongo/              # FastAPI service
│   ├── neo4j/              # Spring Boot service
│   ├── jaccard/            # gRPC Python service
│   └── docker-compose.yml  # Docker orchestration
│
├── frontend/               # React + Vite web interface
│
├── penguins-protein.postman_collection.json
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.8+
- Java 17+ (for Spring Boot)
- MongoDB
- Neo4j
- Node.js 18+ (for frontend)
- Docker (optional, for containerized deployment)

### Installation

Each service has its own README with specific setup instructions. Navigate to the respective service directory for details:

- [Mongo Service](./services/mongo/README.md)
- [Neo4j Service](./services/neo4j/README.md)
- [Jaccard Service](./services/jaccard/README.md)
- [Frontend](./frontend/README.md)

### Docker Deployment

The project includes Docker support for easy deployment:

```bash
cd services
docker-compose up -d --build
```

This will start the Mongo and Neo4j services in containers.

## Technologies

- **FastAPI**: Modern Python web framework for the MongoDB service
- **gRPC**: High-performance RPC framework for Jaccard computation
- **Spring Boot**: Java framework for Neo4j integration
- **React**: Frontend library for building user interfaces
- **Vite**: Next-generation frontend build tool
- **Material-UI & Radix UI**: Component libraries for rich UI
- **MongoDB**: Document database for raw protein data
- **Neo4j**: Graph database for protein relationships
- **Python**: Primary language for data processing
- **Java**: Language for Neo4j service
- **TypeScript**: Type-safe frontend development
- **Docker**: Containerization for deployment

## Use Cases

- Protein similarity analysis
- Protein network visualization
- Comparative proteomics research
- Evolutionary relationship studies
- Functional annotation prediction
