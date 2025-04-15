// MovieController.java (updated)
package com.MyMovie.MyMovie.web;

import com.MyMovie.MyMovie.dao.dto.MovieDTO;
import com.MyMovie.MyMovie.dao.dto.MovieDetailResponse;
import com.MyMovie.MyMovie.dao.dto.PagedMoviesResponse;
import com.MyMovie.MyMovie.dao.dto.RecommendationResponse;
import com.MyMovie.MyMovie.dao.embeddable.RatingId;
import com.MyMovie.MyMovie.dao.entities.AppUser;
import com.MyMovie.MyMovie.dao.entities.Rating;
import com.MyMovie.MyMovie.dao.repository.AppUserRepository;
import com.MyMovie.MyMovie.dao.repository.RatingRepository;
import com.MyMovie.MyMovie.service.RecommendationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpClientErrorException;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
@RestController
@RequestMapping("/api/movies")
public class MovieController {

    private final RecommendationService recommendationService;

    public MovieController(RecommendationService recommendationService) {
        this.recommendationService = recommendationService;
    }

    @Autowired
    private AppUserRepository appUserRepository;

    @Autowired
    private RatingRepository ratingRepository;

    @GetMapping("/recommendations/hybrid/{userId}")
    public ResponseEntity<?> getHybridRecommendations(
            @PathVariable int userId,
            @RequestParam(defaultValue = "10") int top_n) {
        try {
            return ResponseEntity.ok(recommendationService.getHybridRecommendations(userId, top_n));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Recommendation failed", "detail", e.getMessage()));
        }
    }

    @GetMapping("/top-rated")
    public List<MovieDTO> getTopRated(@RequestParam(defaultValue = "100") int minRatings) {
        return recommendationService.getTopRated(minRatings);
    }

    @GetMapping("/{movieId}")
    public ResponseEntity<?> getMovieDetailsWithRecommendations(@PathVariable int movieId) {
        try {
            MovieDetailResponse response = recommendationService.getMovieDetails(movieId);
            return ResponseEntity.ok(response);
        } catch (HttpClientErrorException.NotFound ex) {
            return ResponseEntity.notFound().build();
        } catch (Exception ex) {
            return ResponseEntity.internalServerError()
                    .body(Map.of("error", "Failed to fetch movie details"));
        }
    }
    @GetMapping
    public PagedMoviesResponse getAllMovies(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "100") int perPage) {
        return recommendationService.getAllMovies(page, perPage);
    }

    // NEW
    @GetMapping("/recommendations/collaborative/{userId}")
    public ResponseEntity<?> getCollaborativeRecommendations(
            @PathVariable int userId,
            @RequestParam(defaultValue = "10") int top_n) {
        try {
            return ResponseEntity.ok(recommendationService.getCollaborativeRecommendations(userId, top_n));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Recommendation failed", "detail", e.getMessage()));
        }
    }
    @PostMapping("/{movieId}/rate")
    public ResponseEntity<?> rateMovie(
            @PathVariable Integer movieId,
            @RequestBody Map<String, Object> ratingRequest,
            Authentication authentication
    ) {
        try {
            String username = authentication.getName();
            AppUser user = appUserRepository.findByUsername(username);
            Double rating = Double.parseDouble(ratingRequest.get("rating").toString());

            RatingId ratingId = new RatingId();
            ratingId.setUserId(user.getId());
            ratingId.setMovieId(movieId);

            Rating userRating = ratingRepository.findById(ratingId).orElse(new Rating());
            userRating.setId(ratingId);
            userRating.setRating(rating);
            userRating.setTimestamp(LocalDateTime.now());

            ratingRepository.save(userRating);

            // Update average rating
            List<Rating> allRatings = ratingRepository.findById_MovieId(movieId);
            double avg = allRatings.stream()
                    .mapToDouble(Rating::getRating)
                    .average()
                    .orElse(0.0);

            return ResponseEntity.ok(Map.of(
                    "avg_rating", Math.round(avg * 10) / 10.0,
                    "num_ratings", allRatings.size()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Rating failed"));
        }
    }
}