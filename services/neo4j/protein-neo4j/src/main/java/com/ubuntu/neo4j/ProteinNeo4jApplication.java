package com.ubuntu.neo4j;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.neo4j.repository.config.EnableNeo4jRepositories;

@SpringBootApplication
@EnableNeo4jRepositories
public class ProteinNeo4jApplication {

	public static void main(String[] args) {
		SpringApplication.run(ProteinNeo4jApplication.class, args);
	}

}
