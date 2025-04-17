package com.MyMovie.MyMovie.dao.repository;

import com.MyMovie.MyMovie.dao.embeddable.RatingId;
import com.MyMovie.MyMovie.dao.entities.Rating;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface RatingRepository extends JpaRepository<Rating, RatingId> {
    List<Rating> findById_UserId(Integer userId);
    List<Rating> findById_MovieId(Integer movieId);


}
