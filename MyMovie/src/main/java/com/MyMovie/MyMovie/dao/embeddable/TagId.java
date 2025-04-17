package com.MyMovie.MyMovie.dao.embeddable;


import java.io.Serializable;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.*;

@Embeddable
@AllArgsConstructor @NoArgsConstructor
@Getter
@Setter
@EqualsAndHashCode
public class TagId implements Serializable {
    @Column(name = "user_id")
    private Integer userId;

    @Column(name = "movie_id")
    private Integer movieId;

    private String tag;

}