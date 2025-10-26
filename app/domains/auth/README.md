# Authentication Module

This module provides comprehensive authentication and authorization for the Descubre Boyacá backend, supporting both **email/password** and **Google OAuth2** authentication methods.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Google OAuth Setup](#-google-oauth-setup)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)

---

## ✨ Features

- ✅ **Email/Password Authentication**
  - User registration with password hashing (bcrypt)
  - Login with JWT token generation
  - Password verification

- ✅ **Google OAuth2 Authentication**
  - One-click Google sign-in
  - Automatic user creation/linking
  - Email verification from Google

- ✅ **JWT Token Management**
  - Access tokens (short-lived, 30 minutes)
  - Refresh tokens (long-lived, 7 days)
  - Token verification and validation

- ✅ **Authorization**
  - Role-based access control (ADMIN, USER, GUEST)
  - Protected endpoint decorators
  - Current user injection

- ✅ **Security**
  - Bcrypt password hashing (12 rounds)
  - JWT with HS256 algorithm
  - Secure token storage and validation

---

## 🏗️ Architecture

The authentication module follows **Clean Architecture** and **DDD** principles:

```
auth/
├── domain/              → Domain Layer (Pure business logic)
│   ├── entities/        → User, Token, PasswordHash, OAuthProfile
│   ├── interfaces/      → Repository and Service contracts
│   ├── value_objects/   → Credentials (immutable)
│   ├── enums/           → UserRole, AuthProvider
│   └── exceptions/      → Domain-specific exceptions
│
├── models/              → Infrastructure Layer (ORM)
│   └── user.py          → UserModel (SQLModel)
│
├── repositories/        → Infrastructure Layer (Persistence)
│   └── user.py          → UserRepository
│
├── services/            → Application Layer (Business logic)
│   ├── password.py      → Password hashing/verification
│   ├── token.py         → JWT creation/verification
│   ├── google_oauth.py  → Google OAuth2 flow
│   └── auth.py          → Main auth service
│
├── schemas/             → Presentation Layer (API DTOs)
│   ├── register.py      → Registration schemas
│   ├── login.py         → Login schemas
│   ├── google.py        → Google OAuth schemas
│   ├── token.py         → Token schemas
│   └── user.py          → User response schemas
│
├── routes/              → Presentation Layer (Endpoints)
│   ├── register.py      → POST /auth/register
│   ├── login.py         → POST /auth/login
│   ├── refresh.py       → POST /auth/refresh
│   ├── me.py            → GET /auth/me
│   ├── google_login.py  → GET /auth/google/login
│   └── google_callback.py → GET /auth/google/callback
│
└── dependencies/        → Dependency Injection
    ├── auth.py          → get_current_user(), require_admin()
    ├── sql.py           → Repository and service factories
    └── security.py      → Token and password service factories
```

---

## 🔌 API Endpoints

### Email/Password Authentication

#### `POST /api/v1/auth/register`
Register a new user with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "01HZXXX...",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "auth_provider": "email",
    "profile_picture_url": null,
    "created_at": "2025-10-23T00:00:00Z"
  },
  "message": "User registered successfully"
}
```

#### `POST /api/v1/auth/login`
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "01HZXXX...",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "auth_provider": "email",
    "profile_picture_url": null,
    "created_at": "2025-10-23T00:00:00Z"
  }
}
```

### Google OAuth2 Authentication

#### `GET /api/v1/auth/google/login`
Get Google authorization URL to redirect user.

**Response (200 OK):**
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...",
  "message": "Redirect user to this URL for Google authentication"
}
```

#### `GET /api/v1/auth/google/callback?code={authorization_code}`
Handle Google OAuth callback and authenticate user.

**Query Parameters:**
- `code`: Authorization code from Google

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "01HZXXX...",
    "email": "user@gmail.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "auth_provider": "google",
    "profile_picture_url": "https://lh3.googleusercontent.com/...",
    "created_at": "2025-10-23T00:00:00Z"
  }
}
```

### Token Management

#### `POST /api/v1/auth/refresh`
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### User Information

#### `GET /api/v1/auth/me`
Get current authenticated user information.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "01HZXXX...",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "auth_provider": "email",
    "profile_picture_url": null,
    "created_at": "2025-10-23T00:00:00Z"
  }
}
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-change-in-production-min-32-characters-long
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Google OAuth2 Configuration
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```

### Generate JWT Secret Key

```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -base64 32
```

---

## 🔧 Google OAuth Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google+ API** (or **People API**)

### Step 2: Create OAuth 2.0 Credentials

1. Navigate to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Choose **Web application**
4. Configure:
   - **Name**: Descubre Boyacá Backend
   - **Authorized JavaScript origins**: 
     - `http://localhost:8000` (development)
     - `https://yourdomain.com` (production)
   - **Authorized redirect URIs**:
     - `http://localhost:8000/api/v1/auth/google/callback` (development)
     - `https://yourdomain.com/api/v1/auth/google/callback` (production)

### Step 3: Copy Credentials

1. Copy the **Client ID** and **Client Secret**
2. Add them to your `.env` file:

```bash
GOOGLE_CLIENT_ID=123456789-abcdefg.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123xyz789
```

### Step 4: Configure OAuth Consent Screen

1. Go to **OAuth consent screen**
2. Fill in required information:
   - **App name**: Descubre Boyacá
   - **User support email**: your-email@example.com
   - **Developer contact email**: your-email@example.com
3. Add scopes:
   - `openid`
   - `email`
   - `profile`
4. Save and continue

---

## 💻 Usage Examples

### Protecting Endpoints

```python
from fastapi import APIRouter, Depends
from app.domains.auth.dependencies import get_current_user, require_admin
from app.domains.auth.domain import User

router = APIRouter()

# Require authentication
@router.get("/protected")
async def protected_endpoint(
    current_user: User = Depends(get_current_user),
):
    return {"message": f"Hello {current_user.full_name}!"}

# Require admin role
@router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin),
):
    # Only admins can access this
    return {"message": "User deleted"}
```

### Optional Authentication

```python
from app.domains.auth.dependencies import get_optional_user

@router.get("/public-or-private")
async def endpoint(
    current_user: User | None = Depends(get_optional_user),
):
    if current_user:
        return {"message": f"Hello {current_user.full_name}!"}
    return {"message": "Hello guest!"}
```

### Using Auth Service Directly

```python
from app.domains.auth.services import AuthService
from app.domains.auth.dependencies import get_auth_service

async def my_function(
    auth_service: AuthService = Depends(get_auth_service),
):
    # Register user
    user = await auth_service.register(
        email="user@example.com",
        password="securepassword",
        full_name="John Doe",
    )
    
    # Login user
    tokens, user = await auth_service.login(
        email="user@example.com",
        password="securepassword",
    )
    
    # Get current user from token
    user = await auth_service.get_current_user(tokens.access_token)
```

---

## 🧪 Testing

### Run All Tests

```bash
# Run all authentication tests
uv run pytest tests/auth/

# Run with coverage
uv run pytest tests/auth/ --cov=app/domains/auth
```

### Test Structure

```
tests/auth/
├── unit/
│   ├── test_password_service.py
│   ├── test_token_service.py
│   └── test_auth_service.py
├── integration/
│   └── test_user_repository.py
└── e2e/
    ├── test_register_endpoint.py
    ├── test_login_endpoint.py
    ├── test_google_oauth.py
    └── test_protected_endpoints.py
```

---

## 🔐 Security Considerations

1. **JWT Secret Key**: 
   - Must be at least 32 characters
   - Use a cryptographically secure random value
   - Never commit to version control
   - Rotate regularly in production

2. **Password Requirements**:
   - Minimum 8 characters
   - Hashed with bcrypt (12 rounds)
   - Never stored in plain text

3. **Token Expiration**:
   - Access tokens: 30 minutes (short-lived)
   - Refresh tokens: 7 days (long-lived)
   - Adjust based on security requirements

4. **HTTPS**:
   - Always use HTTPS in production
   - OAuth redirect URIs must use HTTPS

5. **CORS**:
   - Configure allowed origins appropriately
   - Don't use wildcard `*` in production

---

## 📚 Dependencies

- **python-jose[cryptography]**: JWT encoding/decoding
- **bcrypt**: Password hashing
- **passlib**: Password hashing utilities
- **httpx**: HTTP client for OAuth2

---

## 🚀 Next Steps

- [ ] Add password reset functionality
- [ ] Add email verification
- [ ] Add Facebook OAuth support
- [ ] Add 2FA (Two-Factor Authentication)
- [ ] Add rate limiting for login attempts
- [ ] Add user session management
- [ ] Add OAuth token revocation

---

## 📖 Additional Resources

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth 2.0 RFC](https://datatracker.ietf.org/doc/html/rfc6749)
- [JWT Best Practices](https://datatracker.ietf.org/doc/html/rfc8725)
- [Google OAuth2 Documentation](https://developers.google.com/identity/protocols/oauth2)

