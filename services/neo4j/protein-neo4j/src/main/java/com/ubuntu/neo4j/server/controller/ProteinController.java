package com.ubuntu.neo4j.server.controller;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import com.ubuntu.neo4j.server.dto.ProteinDto;
import com.ubuntu.neo4j.server.requests.CorrelatedRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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

    @GetMapping("/proteins")
    public ResponseEntity<List<ProteinDto>> getCorrelatedProteins(@RequestBody CorrelatedRequest request) {
        log.info("Received: {}",  request.toString());
        return ResponseEntity.of(Optional.ofNullable(svc.getCorrelations(request.getEntry())));
    }

}
