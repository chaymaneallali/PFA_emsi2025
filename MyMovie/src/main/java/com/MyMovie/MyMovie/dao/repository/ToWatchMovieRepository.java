package com.MyMovie.MyMovie.dao.repository;

// src/main/java/com/MyMovie/MyMovie/repository/ToWatchMovieRepository.java

import com.MyMovie.MyMovie.dao.entities.ToWatchMovie;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ToWatchMovieRepository extends JpaRepository<ToWatchMovie, Long> {
    // You can add query methods if needed.
}
