package com.MyMovie.MyMovie.service;


import com.MyMovie.MyMovie.dao.dto.MovieDTO;
import com.MyMovie.MyMovie.dao.dto.MovieDetailResponse;
import com.MyMovie.MyMovie.dao.dto.PagedMoviesResponse;
import com.MyMovie.MyMovie.dao.entities.ToWatchMovie;
import com.MyMovie.MyMovie.dao.entities.WatchedMovie;
import com.MyMovie.MyMovie.dao.repository.ToWatchMovieRepository;
import com.MyMovie.MyMovie.dao.repository.WatchedMovieRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;

@Service
public class RecommendationService {
    private final RestTemplate restTemplate;

    private static final Logger logger = LoggerFactory.getLogger(RecommendationService.class);
    private final String flaskBaseUrl;

    public RecommendationService(RestTemplateBuilder restTemplateBuilder,
                                 @Value("${flask.api.base-url}") String flaskBaseUrl) {
        this.restTemplate = restTemplateBuilder.build();
        this.flaskBaseUrl = flaskBaseUrl;
    }

    public List<MovieDTO> getHybridRecommendations(int userId, int topN) {
        String url = String.format("%s/api/recommendations/hybrid/%d?top_n=%d",
                flaskBaseUrl, userId, topN);
        return Arrays.asList(restTemplate.getForObject(url, MovieDTO[].class));
    }

    public List<MovieDTO> getTopRated(int minRatings) {
        String url = String.format("%s/api/recommendations/top-rated?min_ratings=%d",
                flaskBaseUrl, minRatings);
        return Arrays.asList(restTemplate.getForObject(url, MovieDTO[].class));
    }

    // RecommendationService.java (Spring)
    public MovieDetailResponse getMovieDetails(int movieId) {
        try {
            // Get movie details from Flask
            String url = String.format("%s/api/movies/%d", flaskBaseUrl, movieId);
            ResponseEntity<MovieDetailResponse> response = restTemplate.getForEntity(url, MovieDetailResponse.class);

            if (!response.getStatusCode().is2xxSuccessful()) {
                throw new HttpClientErrorException(response.getStatusCode());
            }

            return response.getBody();
        } catch (HttpClientErrorException.NotFound ex) {
            throw ex; // Forward 404 errors
        } catch (Exception ex) {
            logger.error("Failed to fetch movie details", ex);
            throw new RuntimeException("Service unavailable");
        }
    }

    public PagedMoviesResponse getAllMovies(int page, int perPage) {
        String url = String.format("%s/api/movies?page=%d&per_page=%d",
                flaskBaseUrl, page, perPage);
        return restTemplate.getForObject(url, PagedMoviesResponse.class);
    }

    // RecommendationService.java
    public List<MovieDTO> getCollaborativeRecommendations(int userId, int topN) {
        String url = String.format("%s/api/recommendations/collaborative/%d?top_n=%d",
                flaskBaseUrl, userId, topN);
        return Arrays.asList(restTemplate.getForObject(url, MovieDTO[].class));
    }



    @Autowired
    private WatchedMovieRepository watchedRepository;

    @Autowired
    private ToWatchMovieRepository toWatchRepository;

    // Other recommendation methods...

    public WatchedMovie markAsWatched(int userId, int movieId) {
        WatchedMovie record = new WatchedMovie();
        record.setUserId(userId);
        record.setMovieId(movieId);
        return watchedRepository.save(record);
    }

    public ToWatchMovie markAsToWatch(int userId, int movieId) {
        ToWatchMovie record = new ToWatchMovie();
        record.setUserId(userId);
        record.setMovieId(movieId);
        return toWatchRepository.save(record);
    }




}