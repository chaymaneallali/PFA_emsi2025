package com.MyMovie.MyMovie.dao.dto;




import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;


@Getter @Setter
public class RegisterDto {

    @NotEmpty
    private String firstName;
    @NotEmpty
    private String lastName;
    @NotEmpty
    private String username;
    @NotEmpty
    private String email;
    @NotEmpty
    @Size(min = 6, message = "Password must be at least 6 characters long")
    private String password;


    private String phone;

    private String address;
}
