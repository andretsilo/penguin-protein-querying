package com.ubuntu.neo4j.business.entity;

import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

import org.springframework.data.neo4j.core.schema.GeneratedValue;
import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;

@Node("Protein")
public class Protein {

    @Id
    @GeneratedValue
    private Long id;
    private String entry;

    @Relationship(type = "CORRELATES")
    public Set<Protein> correlatedProteins;

    public Protein() {

    }

    public Protein(String entry) {
	this.entry = entry;
    }

    public void correlatedWith(Protein protein, Double index) {
	if (correlatedProteins == null) {
	    correlatedProteins = new HashSet<>();
	}
	if (index > 0.4) {
	    correlatedProteins.add(protein);
	}
    }

    public String getEntry() {
	return entry;
    }

    public void setEntry(String entry) {
	this.entry = entry;
    }

    @Override
    public boolean equals(Object o) {
	if (o == null || getClass() != o.getClass())
	    return false;
	Protein protein = (Protein) o;
	return Objects.equals(id, protein.id) && Objects.equals(entry, protein.entry)
		&& Objects.equals(correlatedProteins, protein.correlatedProteins);
    }

    @Override
    public int hashCode() {
	return Objects.hash(id, entry, correlatedProteins);
    }
}
