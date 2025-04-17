package com.MyMovie.MyMovie.dao.entities;


import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter @Setter
@Table(name = "to_watch_movies")
public class ToWatchMovie {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private int userId;
    private int movieId;

    private LocalDateTime addedDate;

    @PrePersist
    public void prePersist() {
        this.addedDate = LocalDateTime.now();
    }


}
