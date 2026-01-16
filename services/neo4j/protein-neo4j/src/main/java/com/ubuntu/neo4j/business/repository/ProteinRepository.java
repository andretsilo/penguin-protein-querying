package com.ubuntu.neo4j.business.repository;

import java.util.List;

import org.springframework.data.neo4j.repository.Neo4jRepository;

import com.ubuntu.neo4j.business.entity.Protein;

public interface ProteinRepository extends Neo4jRepository<Protein, Long> {
}
