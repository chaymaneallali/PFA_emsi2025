package com.MyMovie.MyMovie.web;



import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HomeController {
    @GetMapping("/")
    public String home() {
        return "Home Page";

    }



    @GetMapping("/admin/home")
    public String getAdminHome() {
        return "Admin Home Page";
    }

    @GetMapping("/client/home")
    public String getClientHome() {
        return "Client Home Page";
    }
}
