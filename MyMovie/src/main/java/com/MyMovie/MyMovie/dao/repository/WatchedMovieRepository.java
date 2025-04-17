package com.MyMovie.MyMovie.dao.repository;

// src/main/java/com/MyMovie/MyMovie/repository/WatchedMovieRepository.java

import com.MyMovie.MyMovie.dao.entities.WatchedMovie;
import org.springframework.data.jpa.repository.JpaRepository;

public interface WatchedMovieRepository extends JpaRepository<WatchedMovie, Long> {
    // You can add query methods if needed.
}
