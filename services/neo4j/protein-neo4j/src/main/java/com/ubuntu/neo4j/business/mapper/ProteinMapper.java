package com.ubuntu.neo4j.business.mapper;

import org.mapstruct.Mapper;

import com.ubuntu.neo4j.business.entity.Protein;
import com.ubuntu.neo4j.server.dto.CorrelationsDto;

@Mapper(componentModel = "spring")
public interface ProteinMapper {

    public Protein toEntity(CorrelationsDto source);

}
