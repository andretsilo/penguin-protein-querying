package com.ubuntu.neo4j.business.service;

import java.util.ArrayList;
import java.util.List;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ubuntu.neo4j.business.entity.Protein;
import com.ubuntu.neo4j.business.mapper.JaccardMapper;
import com.ubuntu.neo4j.business.mapper.ProteinMapper;
import com.ubuntu.neo4j.business.repository.ProteinRepository;
import com.ubuntu.neo4j.server.dto.CorrelationsDto;

@Slf4j
@Service
public class CorrelatorService {

    @Autowired
    private ProteinRepository repository;

    @Autowired
    private ProteinMapper proteinMapper;

    @Autowired
    private JaccardMapper jaccardMapper;

    public void correlate(CorrelationsDto dto) {
        Protein mainProtein = proteinMapper.toEntity(dto);

        List<Protein> correlatedProteins = new ArrayList<>(dto.getJaccardCorrelations().stream().map(j -> jaccardMapper.toEntity(j)).toList());
        correlatedProteins.add(mainProtein);
        correlatedProteins.forEach(protein -> log.info("Created protein: {}", protein));

        repository.saveAll(correlatedProteins);
        log.info("Persisted nodes");

        dto.getJaccardCorrelations()
                .forEach(j -> {
                    mainProtein.correlatedWith(jaccardMapper.toEntity(j), j.getJaccard());
                    log.info("Correlating {} with {} with coefficient: {}", mainProtein.getEntry(), j.getEntry(), j.getJaccard());
                });
        repository.save(mainProtein);
        log.info("Persited relationships");
    }
}
