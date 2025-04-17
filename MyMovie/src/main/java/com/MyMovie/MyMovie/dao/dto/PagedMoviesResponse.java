package com.MyMovie.MyMovie.dao.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PagedMoviesResponse {
    private int page;
    private int perPage;
    private int totalMovies;
    private List<MovieDTO> results;  // Changed from List<Object>

    // Add empty results constructor
    public PagedMoviesResponse(int page, int perPage, int totalMovies) {
        this.page = page;
        this.perPage = perPage;
        this.totalMovies = totalMovies;
        this.results = List.of();
    }
}