package com.MyMovie.MyMovie.dao.entities;


import jakarta.persistence.Table;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@Table(name = "watched_movies")
public class WatchedMovie {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private int userId;
    private int movieId;

    private LocalDateTime watchedDate;

    @PrePersist
    public void prePersist() {
        this.watchedDate = LocalDateTime.now();
    }


}
