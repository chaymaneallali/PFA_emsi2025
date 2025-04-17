package com.MyMovie.MyMovie.dao.dto;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Data
@Getter @Setter
public class MovieDetailResponse {
    private MovieDTO movie;
    private List<MovieDTO> recommendations;


}