# Spring Boot

ShieldCode aplica padrões idiomáticos do Spring Boot.

## SQL Injection

Use **Spring Data JPA**:

```java
// SEGURO - JPA derived query
List<User> findByEmail(String email);

// SEGURO - JPQL com parâmetros nomeados
@Query("SELECT u FROM User u WHERE u.email = :email")
List<User> findUsers(@Param("email") String email);

// SEGURO - Native query com parâmetros
@Query(value = "SELECT * FROM users WHERE email = ?1", nativeQuery = true)
List<User> findUsersNative(String email);
```

NUNCA concatene strings em `@Query` com input do usuário.

## Input validation

Use **Bean Validation** (Jakarta):

```java
public record UserCreateRequest(
    @NotBlank
    @Email
    String email,

    @Size(min = 8, max = 128)
    String password,

    @Min(18)
    int age
) {}

@PostMapping("/users")
public User create(@Valid @RequestBody UserCreateRequest req) {
    // req validado automaticamente
}
```

## Spring Security

ShieldCode sugere configuração base segura:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .headers(h -> h
                .frameOptions(f -> f.deny())
                .contentSecurityPolicy(c -> c.policyDirectives("default-src 'self'"))
                .strictTransportSecurity(s -> s.maxAgeInSeconds(31536000).includeSubDomains(true))
            )
            .build();
    }
}
```

## Senha

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12);
}

// Uso
String hashed = passwordEncoder.encode(rawPassword);
boolean valid = passwordEncoder.matches(rawPassword, hashed);
```

NUNCA `MD5`, `SHA1` ou senha em plaintext.

## JWT

Use **jjwt** ou **Nimbus JOSE+JWT**:

```java
String token = Jwts.builder()
    .setSubject(userId)
    .setIssuedAt(new Date())
    .setExpiration(new Date(System.currentTimeMillis() + 15 * 60 * 1000))
    .signWith(SignatureAlgorithm.HS256, secretKey)
    .compact();
```

Algoritmo SEMPRE definido (NUNCA aceitar `alg: none`).

## CORS

```java
@Configuration
public class CorsConfig {
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("https://meu-frontend.com"));
        config.setAllowCredentials(true);
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
        config.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}
```

## Rate limit

Bucket4j é o padrão:

```java
@Bean
public Bucket loginBucket() {
    return Bucket.builder()
        .addLimit(Bandwidth.classic(5, Refill.intervally(5, Duration.ofMinutes(15))))
        .build();
}
```

## Exemplo prático

> "Faz endpoint Spring Boot pra cadastrar usuário"

ShieldCode entrega:

- `@Valid` no DTO com `@Email`, `@Size`
- Senha hasheada com BCryptPasswordEncoder cost 12
- Sem campo "role" no DTO (usuário não escolhe a role)
- Spring Security configurado
- CORS restrito
- Rate limit no endpoint
- Resposta sem expor senha hash
