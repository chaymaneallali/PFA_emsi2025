package com.MyMovie.MyMovie.web;


import com.MyMovie.MyMovie.dao.entities.AppUser;
import com.MyMovie.MyMovie.dao.dto.LoginDto;
import com.MyMovie.MyMovie.dao.dto.RegisterDto;
import com.MyMovie.MyMovie.dao.repository.AppUserRepository;
import com.nimbusds.jose.jwk.source.ImmutableSecret;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.security.oauth2.jwt.NimbusJwtEncoder;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/account")
public class AccountController {

    @Autowired
    private AuthenticationManager authenticationManager; //exist in securityconfig

    private final AppUserRepository appUserRepository;

    @Value("${security.jwt.secret}")
    private String jwtSecretKey;

    @Value("${security.jwt.issuer}")
    private String jwtIssuer;

    public AccountController(AppUserRepository appUserRepository) {
        this.appUserRepository = appUserRepository;
    }

    // Method to create a JWT token for the user
    private String createJwtToken(AppUser appUser) {
        Instant now = Instant.now();

        JwtClaimsSet claims = JwtClaimsSet.builder()
                .claim("userId", appUser.getId()) // Add user ID claim

                .issuer(jwtIssuer)
                .issuedAt(now)
                .expiresAt(now.plusSeconds(24 * 3600))
                .subject(appUser.getUsername())
                .claim("role", appUser.getRole())
                .build();

        var encoder = new NimbusJwtEncoder(new ImmutableSecret<>(jwtSecretKey.getBytes()));
        var params = JwtEncoderParameters.from(JwsHeader.with(MacAlgorithm.HS256).build(), claims);
        return encoder.encode(params).getTokenValue();
    }

    @PostMapping("/register")
    public ResponseEntity<Object> register(
            @Valid @RequestBody RegisterDto registerDto,
            BindingResult result) {

        // If validation errors exist, return them
        if (result.hasErrors()) {
            Map<String, String> errorsMap = new HashMap<>();
            for (FieldError error : result.getFieldErrors()) {
                errorsMap.put(error.getField(), error.getDefaultMessage());
            }
            return ResponseEntity.badRequest().body(errorsMap);
        }

        var bCryptEncoder = new BCryptPasswordEncoder();

        // Create and populate AppUser
        AppUser appUser = new AppUser();
        appUser.setFirstName(registerDto.getFirstName());
        appUser.setLastName(registerDto.getLastName());
        appUser.setEmail(registerDto.getEmail());
        appUser.setUsername(registerDto.getUsername());
        appUser.setRole("USER"); // Default role
        appUser.setCreatedAt(new Date());
        appUser.setPassword(bCryptEncoder.encode(registerDto.getPassword()));
        appUser.setPhone(registerDto.getPhone());
        appUser.setAddress(registerDto.getAddress());

        try {
            // Check for duplicate username
            AppUser otherUser = appUserRepository.findByUsername(registerDto.getUsername());
            if (otherUser != null) {
                return ResponseEntity.badRequest().body("Username already exists");
            }
            // Check for duplicate email
            otherUser = appUserRepository.findByEmail(registerDto.getEmail());
            if (otherUser != null) {
                return ResponseEntity.badRequest().body("Email already exists");
            }
            // Save the new user
            appUserRepository.save(appUser);
            // Generate JWT token for the new user
            String token = createJwtToken(appUser);
            // Build response map with user details and token (excluding password)
            Map<String, Object> responseMap = new HashMap<>();
            responseMap.put("firstName", appUser.getFirstName());
            responseMap.put("lastName", appUser.getLastName());
            responseMap.put("username", appUser.getUsername());
            responseMap.put("email", appUser.getEmail());
            responseMap.put("phone", appUser.getPhone());
            responseMap.put("address", appUser.getAddress());
            responseMap.put("role", appUser.getRole());
            responseMap.put("token", token);

            return ResponseEntity.ok(responseMap);
        } catch (Exception ex) {
            ex.printStackTrace();
            return ResponseEntity.badRequest().body("An error occurred during registration: " + ex.getMessage());
        }
    }



    @PostMapping("/login")
    public ResponseEntity<Object> login(
            @Valid @RequestBody LoginDto loginDto
            , BindingResult result
    ){
        if(result.hasErrors()){
            var errorList = result.getAllErrors();
            var errorsMap = new HashMap<String , String>();

            for (int i=0; i< errorList.size(); i++) {
                var error = (FieldError) errorList.get(i);
                errorsMap.put(error.getField(), error.getDefaultMessage());
            }
            return ResponseEntity.badRequest().body(errorsMap);
        }
        try{
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            loginDto.getUsername() ,
                            loginDto.getPassword()
                    )
            );

            AppUser appUser = appUserRepository.findByUsername(loginDto.getUsername());
            String jwtToken = createJwtToken(appUser); //Create The token for the user

            var response = new HashMap<String, Object>();
            response.put("token", jwtToken);
            response.put("user",appUser);

            return ResponseEntity.ok(response);
        }
        catch (Exception ex){
            System.out.println("There is an Exception : ");
            ex.printStackTrace();
        }
        return ResponseEntity.badRequest().body("Bad Username Or Password");
    }


    //AUTHENTICATE USER BY TOKEN
    @GetMapping("/profile")
    public ResponseEntity<Object> profile(Authentication auth){
        var response = new HashMap<String , Object>();
        response.put("Username",auth.getName());
        response.put("Authorities",auth.getAuthorities());

        var appUser = appUserRepository.findByUsername(auth.getName());
        response.put("User",appUser);

        return ResponseEntity.ok(response);
    }


}

