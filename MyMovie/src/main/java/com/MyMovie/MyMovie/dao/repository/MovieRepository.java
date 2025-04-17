package com.MyMovie.MyMovie.dao.repository;


import com.MyMovie.MyMovie.dao.entities.Movie;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface MovieRepository extends JpaRepository<Movie, Integer> {
    List<Movie> findByTitleContainingIgnoreCase(String title);
}
