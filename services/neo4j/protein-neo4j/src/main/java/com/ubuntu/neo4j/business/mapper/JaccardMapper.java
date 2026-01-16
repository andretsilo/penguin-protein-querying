package com.ubuntu.neo4j.business.mapper;

import org.mapstruct.Mapper;

import com.ubuntu.neo4j.business.entity.Protein;
import com.ubuntu.neo4j.server.dto.JaccardDto;

@Mapper(componentModel = "spring")
public interface JaccardMapper {

    public Protein toEntity(JaccardDto source);
}
