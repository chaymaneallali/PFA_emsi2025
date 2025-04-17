package com.MyMovie.MyMovie.dao.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.security.core.userdetails.User;

import java.util.List;

@Data @NoArgsConstructor

public class MovieDTO {
    @JsonProperty("movieId")
    private Integer movieId;

    private String title;

    @JsonProperty("genres")
    private List<String> genres;

    @JsonProperty("poster_path")
    private String posterPath;


    @JsonProperty("avg_rating")
    private Double avgRating;

    @JsonProperty("num_ratings")
    private Integer numRatings;

    private String overview;
    private Integer releaseYear;
    private Integer duration;
    private String language;

    @JsonProperty("userRating")
    private Double userRating;
    @JsonProperty("tmdbRating")
    private Double tmdbRating;
    @JsonProperty("voteCount")
    private Integer voteCount;

}
