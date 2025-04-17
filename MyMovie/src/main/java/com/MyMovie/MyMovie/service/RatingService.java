package com.MyMovie.MyMovie.service;


import com.MyMovie.MyMovie.dao.entities.Rating;
import com.MyMovie.MyMovie.dao.repository.RatingRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class RatingService {
    private final RatingRepository ratingRepository;

    public RatingService(RatingRepository ratingRepository) {
        this.ratingRepository = ratingRepository;
    }

    public List<Rating> getRatingsByUser(Integer userId) {
        return ratingRepository.findById_UserId(userId);
    }

    public List<Rating> getRatingsForMovie(Integer movieId) {
        return ratingRepository.findById_MovieId(movieId);
    }

    public Rating saveRating(Rating rating) {
        return ratingRepository.save(rating);
    }
}
