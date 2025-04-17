package com.MyMovie.MyMovie.dao.repository;


import com.MyMovie.MyMovie.dao.embeddable.TagId;
import com.MyMovie.MyMovie.dao.entities.Tag;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface TagRepository extends JpaRepository<Tag, TagId> {
    List<Tag> findById_MovieId(Integer movieId);
    List<Tag> findById_UserId(Integer userId);
}
