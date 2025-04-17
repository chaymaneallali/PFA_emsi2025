package com.MyMovie.MyMovie.dao.entities;


import com.MyMovie.MyMovie.dao.embeddable.TagId;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "tags")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class Tag {
    @EmbeddedId
    private TagId id;

    @Column(name = "\"timestamp\"")
    private LocalDateTime timestamp;


}