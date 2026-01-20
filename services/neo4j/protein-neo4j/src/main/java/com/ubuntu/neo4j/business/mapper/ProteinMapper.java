package com.ubuntu.neo4j.business.mapper;

import com.ubuntu.neo4j.server.dto.ProteinDto;
import org.mapstruct.Mapper;

import com.ubuntu.neo4j.business.entity.Protein;
import com.ubuntu.neo4j.server.dto.CorrelationsDto;

import java.util.List;

@Mapper(componentModel = "spring")
public interface ProteinMapper {

    public Protein toEntity(CorrelationsDto source);
    public List<ProteinDto> toDto(List<Protein> source);
}
