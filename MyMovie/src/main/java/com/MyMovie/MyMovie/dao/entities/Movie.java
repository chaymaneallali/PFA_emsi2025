package com.MyMovie.MyMovie.dao.entities;


import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@Entity
@Table(name = "movies")
@AllArgsConstructor @NoArgsConstructor
@Getter
@Setter
public class Movie {
    @Id
    @Column(name = "movieId")
    private Integer movieId;

    private String title;

    @Column(length = 2048)
    private String genres;

    @Column(name = "poster_path")
    private String posterPath;

    @Column(name = "release_year")
    private Integer releaseYear;

    @Column(name = "duration")
    private Integer duration;

    @Column(name = "tmdb_rating")
    private Double tmdbRating;

    @Column(name = "vote_count")
    private Integer voteCount;

    @Column(length = 2000)
    private String overview;

    private String language;



}