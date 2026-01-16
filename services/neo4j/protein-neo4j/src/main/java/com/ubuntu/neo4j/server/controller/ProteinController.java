package com.ubuntu.neo4j.server.controller;

import java.util.ArrayList;
import java.util.List;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.ubuntu.neo4j.business.service.CorrelatorService;
import com.ubuntu.neo4j.server.dto.CorrelationsDto;

@RestController
@RequestMapping("/api")
@Slf4j
public class ProteinController {

    @Autowired
    private CorrelatorService svc;

    @PostMapping("/proteins")
    public ResponseEntity<String> addProteins(@RequestBody List<CorrelationsDto> proteins) {
    log.info("Received: {}", proteins.toString());
	proteins.forEach(p -> svc.correlate(p));
	return ResponseEntity.ok().build();
    }

}
