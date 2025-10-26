# 🔐 Traditional Authentication Flow (Email/Password)

This document describes the traditional authentication flow using email and password in the Descubre Boyacá application.

## Registration Diagram

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant F as Frontend
    participant B as Backend (FastAPI)
    participant DB as Database

    Note over U,DB: USER REGISTRATION
    
    U->>F: Complete registration form
    Note right of U: - Email<br/>- Password<br/>- Full Name
    
    F->>F: Validate fields (frontend)
    
    F->>B: POST /api/v1/auth/register
    Note right of F: {<br/>  email,<br/>  password,<br/>  full_name<br/>}
    
    activate B
    
    B->>B: Validate data (Pydantic)
    Note right of B: - Valid email<br/>- Password >= 8 chars<br/>- Full name >= 2 chars
    
    B->>DB: Check if email exists
    activate DB
    DB-->>B: User not found
    deactivate DB
    
    alt Email already exists
        B-->>F: 409 Conflict<br/>UserAlreadyExistsException
        F-->>U: "Email already registered"
    else Email available
        B->>B: Hash password with bcrypt<br/>(cost factor = 12)
        
        B->>B: Create User entity
        Note right of B: - ID (ULID)<br/>- email<br/>- hashed_password<br/>- full_name<br/>- role = "user"<br/>- is_active = true<br/>- auth_provider = "email"<br/>- created_at
        
        B->>DB: Save user
        activate DB
        DB-->>B: User created
        deactivate DB
        
        B-->>F: 201 Created
        Note left of B: {<br/>  user: {...},<br/>  message: "User registered successfully"<br/>}
        deactivate B
        
        F-->>U: "Registration successful"
        F->>F: Redirect to login
    end
```

## Login Diagram

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant F as Frontend
    participant B as Backend (FastAPI)
    participant DB as Database

    Note over U,DB: LOGIN
    
    U->>F: Enter email and password
    
    F->>B: POST /api/v1/auth/login
    Note right of F: {<br/>  email,<br/>  password<br/>}
    
    activate B
    
    B->>DB: Find user by email
    activate DB
    DB-->>B: User found
    deactivate DB
    
    alt User not found
        B-->>F: 401 Unauthorized<br/>InvalidCredentialsException
        F-->>U: "Invalid credentials"
    else User found
        B->>B: Verify password<br/>bcrypt.verify(password, hash)
        
        alt Invalid password
            B-->>F: 401 Unauthorized<br/>InvalidCredentialsException
            F-->>U: "Invalid credentials"
        else Valid password
            B->>B: Verify is_active = true
            
            alt Inactive user
                B-->>F: 403 Forbidden<br/>UserInactiveException
                F-->>U: "Account deactivated"
            else Active user
                B->>B: Generate Access Token (JWT)
                Note right of B: Payload:<br/>- sub (user_id)<br/>- email<br/>- role<br/>- exp: 30 min
                
                B->>B: Generate Refresh Token (JWT)
                Note right of B: Payload:<br/>- sub (user_id)<br/>- exp: 7 days
                
                B-->>F: 200 OK
                Note left of B: {<br/>  access_token,<br/>  refresh_token,<br/>  token_type: "bearer",<br/>  user: {...}<br/>}
                deactivate B
                
                F->>F: Save tokens<br/>(localStorage/cookies)
                
                F-->>U: Redirect to dashboard
            end
        end
    end
```

## Protected Resource Access Diagram

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant F as Frontend
    participant B as Backend (FastAPI)
    participant DB as Database

    Note over U,DB: ACCESS PROTECTED ENDPOINT
    
    U->>F: Access protected page
    
    F->>F: Get access_token<br/>(localStorage)
    
    F->>B: GET /api/v1/auth/me<br/>Authorization: Bearer <token>
    
    activate B
    
    B->>B: Extract token from header
    
    alt No token present
        B-->>F: 401 Unauthorized
        F->>F: Redirect to login
    else Token present
        B->>B: Decode and validate JWT
        Note right of B: Verify:<br/>- Valid signature<br/>- Not expired<br/>- Correct structure
        
        alt Invalid or expired token
            B-->>F: 401 Unauthorized
            F->>F: Try refresh token
        else Valid token
            B->>B: Extract user_id from token
            
            B->>DB: Find user by ID
            activate DB
            DB-->>B: User found
            deactivate DB
            
            alt User doesn't exist
                B-->>F: 401 Unauthorized
                F->>F: Redirect to login
            else User exists and active
                B-->>F: 200 OK
                Note left of B: {<br/>  user: {<br/>    id,<br/>    email,<br/>    full_name,<br/>    role,<br/>    ...<br/>  }<br/>}
                deactivate B
                
                F-->>U: Show protected content
            end
        end
    end
```

## Refresh Token Diagram

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant F as Frontend
    participant B as Backend (FastAPI)

    Note over U,B: RENEW ACCESS TOKEN
    
    F->>F: Detect expired access_token
    Note right of F: 401 error in request
    
    F->>F: Get refresh_token<br/>(localStorage)
    
    alt No refresh_token
        F->>F: Redirect to login
    else Has refresh_token
        F->>B: POST /api/v1/auth/refresh
        Note right of F: {<br/>  refresh_token<br/>}
        
        activate B
        
        B->>B: Validate refresh_token
        Note right of B: Verify:<br/>- Valid signature<br/>- Not expired<br/>- Correct structure
        
        alt Invalid/expired refresh token
            B-->>F: 401 Unauthorized<br/>InvalidTokenException
            deactivate B
            F->>F: Delete tokens
            F->>F: Redirect to login
            F-->>U: "Session expired"
        else Valid refresh token
            B->>B: Extract user_id
            
            B->>B: Generate new access_token
            Note right of B: New token with<br/>exp: now + 30 min
            
            B-->>F: 200 OK
            Note left of B: {<br/>  access_token,<br/>  token_type: "bearer"<br/>}
            deactivate B
            
            F->>F: Save new access_token
            
            F->>F: Retry original request
            Note right of F: With new token
            
            F-->>U: Continue navigation
        end
    end
```

## Traditional Authentication Endpoints

### `POST /api/v1/auth/register`

**Description**: Registers a new user with email and password.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Validations**:
- Email: Valid format (RFC 5322)
- Password: Minimum 8 characters, maximum 100
- Full Name: Minimum 2 characters, maximum 255

**Response** (201 Created):
```json
{
  "user": {
    "id": "01JXXXXXXXXX",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "auth_provider": "email",
    "profile_picture_url": null,
    "created_at": "2024-10-26T10:30:00Z"
  },
  "message": "User registered successfully"
}
```

**Errors**:
- `409 Conflict`: Email already registered (UserAlreadyExistsException)
- `422 Unprocessable Entity`: Invalid data

### `POST /api/v1/auth/login`

**Description**: Authenticates a user and generates JWT tokens.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "01JXXXXXXXXX",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "auth_provider": "email",
    "created_at": "2024-10-26T10:30:00Z"
  }
}
```

**Errors**:
- `401 Unauthorized`: Invalid credentials (InvalidCredentialsException)
- `403 Forbidden`: Deactivated user (UserInactiveException)

### `GET /api/v1/auth/me`

**Description**: Gets current authenticated user information.

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "01JXXXXXXXXX",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "auth_provider": "email",
    "created_at": "2024-10-26T10:30:00Z"
  }
}
```

**Errors**:
- `401 Unauthorized`: Invalid or expired token

### `POST /api/v1/auth/refresh`

**Description**: Renews access token using a valid refresh token.

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors**:
- `401 Unauthorized`: Invalid or expired refresh token

## Security

### Password Hashing

- **Algorithm**: bcrypt
- **Cost Factor**: 12 (2^12 = 4096 rounds)
- **Salt**: Automatically generated by bcrypt
- **Hash Time**: ~300-500ms (intentional to prevent brute force)

### JWT Tokens

#### Access Token
- **Purpose**: Authenticate API requests
- **Expiration**: 30 minutes (configurable)
- **Payload**:
  ```json
  {
    "sub": "01JXXXXXXXXX",
    "email": "user@example.com",
    "role": "user",
    "exp": 1730000000
  }
  ```

#### Refresh Token
- **Purpose**: Obtain new access tokens
- **Expiration**: 7 days (configurable)
- **Payload**:
  ```json
  {
    "sub": "01JXXXXXXXXX",
    "exp": 1730604800
  }
  ```

### Validations

1. ✅ Unique email (unique index in database)
2. ✅ Password minimum 8 characters
3. ✅ bcrypt hash with cost factor 12
4. ✅ JWT tokens signed with HS256
5. ✅ Expiration verification on each request
6. ✅ User must be active (`is_active = true`)

## Differences between Auth Providers

| Aspect | Email/Password | Google OAuth |
|---------|----------------|--------------|
| `auth_provider` | "email" | "google" |
| `hashed_password` | bcrypt hash | null |
| `google_id` | null | Google ID |
| Registration | Manual | Automatic |
| Password | Required | Not applicable |
| Email verification | Required (future) | Google handles it |

### ⚠️ Important

A user **CANNOT** switch between authentication methods:
- If registered with email, cannot use Google OAuth with the same email (email already exists)
- If registered with Google, cannot use traditional login (no password)

## Use Cases

### Successful Registration

1. User completes form
2. Backend validates data
3. Email doesn't exist in DB
4. User is created with hashed password
5. User can login immediately

### Successful Login

1. User enters credentials
2. Backend finds user by email
3. Password matches hash
4. User is active
5. JWT tokens are generated
6. Frontend saves tokens

### Expired Token

1. Frontend tries to access protected resource
2. Backend returns 401 (token expired)
3. Frontend uses refresh token
4. Backend validates refresh token
5. Backend generates new access token
6. Frontend retries original request

### Expired Session

1. Access token expired
2. Refresh token also expired
3. Backend rejects refresh
4. Frontend deletes tokens
5. Frontend redirects to login

## Configuration

### Environment Variables

```bash
# JWT Configuration
JWT_SECRET_KEY=your-very-secure-secret-key-minimum-32-characters
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Hashing
BCRYPT_ROUNDS=12  # Implicit in code
```

### Generate Secret Key

```bash
# Generate a secure 32-byte (256-bit) key
openssl rand -hex 32
```

## Manual Testing

### 1. Register User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. Access Protected Endpoint

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJI..."
```

### 4. Refresh Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJI..."
  }'
```

## References

- [JWT (JSON Web Tokens)](https://jwt.io/)
- [bcrypt Password Hashing](https://en.wikipedia.org/wiki/Bcrypt)
- [OAuth 2.0 vs Traditional Auth](https://auth0.com/intro-to-iam/oauth-2-vs-openid-connect)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
