package com.ubuntu.neo4j.server.dto;

import java.util.List;

import lombok.Data;

@Data
public class CorrelationsDto {
    private String entry;
    private List<JaccardDto> jaccardCorrelations;
}
