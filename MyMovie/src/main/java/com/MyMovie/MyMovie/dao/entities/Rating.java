package com.MyMovie.MyMovie.dao.entities;


import com.MyMovie.MyMovie.dao.embeddable.RatingId;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "ratings")
@AllArgsConstructor @NoArgsConstructor @Getter
@Setter
public class Rating {
    @EmbeddedId
    private RatingId id;

    private Double rating;

    @Column(name = "\"timestamp\"") // timestamp is a reserved word in SQL
    private LocalDateTime timestamp;



}
