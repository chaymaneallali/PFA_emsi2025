package com.MyMovie.MyMovie.service;


import com.MyMovie.MyMovie.dao.entities.Tag;
import com.MyMovie.MyMovie.dao.repository.TagRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class TagService {
    private final TagRepository tagRepository;

    public TagService(TagRepository tagRepository) {
        this.tagRepository = tagRepository;
    }

    public List<Tag> getTagsForMovie(Integer movieId) {
        return tagRepository.findById_MovieId(movieId);
    }

    public List<Tag> getTagsByUser(Integer userId) {
        return tagRepository.findById_UserId(userId);
    }

    public Tag saveTag(Tag tag) {
        return tagRepository.save(tag);
    }
}
