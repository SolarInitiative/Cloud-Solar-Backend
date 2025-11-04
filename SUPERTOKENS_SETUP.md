# SuperTokens Integration Guide

This guide explains how to set up and use SuperTokens for user authentication in the Cloud Solar application.

## Overview

SuperTokens has been integrated to provide robust user authentication with the following features:

- **Email/Password Authentication**: Secure sign up and login
- **Session Management**: Access tokens and refresh tokens with automatic rotation
- **CSRF Protection**: Built-in protection against cross-site request forgery
- **User Identification**: Track and identify users across requests
- **Session Revocation**: Logout functionality with session cleanup
- **Admin Access Control**: Role-based access control for admin endpoints

## Architecture

### Components

1. **SuperTokens Core**: The backend service that manages authentication
2. **SuperTokens Python SDK**: Integrated into your FastAPI application
3. **Your Database**: Stores user information (username, email, location, etc.)
4. **SuperTokens Database**: Stores session and authentication data

### How It Works

1. User signs up via `/auth/signup`
   - User created in SuperTokens
   - User created in your PostgreSQL database
   - Session created and returned as cookies

2. User logs in via `/auth/login`
   - Credentials verified in SuperTokens
   - Session created with user metadata
   - Access token payload includes user info (id, username, email, is_admin)

3. Protected routes use session verification
   - SuperTokens validates the session automatically
   - User information extracted from session payload
   - User data fetched from your database

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install `supertokens-python>=0.29.0` along with other dependencies.

### Step 2: Set Up SuperTokens Core

You have two options:

#### Option A: Local Development with Docker (Recommended)

Run SuperTokens Core locally using Docker:

```bash
docker run -d \
  -p 3567:3567 \
  --name supertokens \
  registry.supertokens.io/supertokens/supertokens-postgresql
```

This starts SuperTokens Core on `http://localhost:3567`.

#### Option B: SuperTokens Managed Service

1. Sign up at [https://supertokens.com](https://supertokens.com)
2. Create a new app
3. Get your connection URI and API key
4. Update `.env` with your credentials

### Step 3: Configure Environment Variables

The `.env` file has been updated with SuperTokens configuration:

```env
# SuperTokens Configuration
SUPERTOKENS_CONNECTION_URI=http://localhost:3567
API_DOMAIN=http://localhost:8000
WEBSITE_DOMAIN=http://localhost:3000
API_BASE_PATH=/auth
WEBSITE_BASE_PATH=/auth
COOKIE_DOMAIN=
COOKIE_SAME_SITE=lax
COOKIE_SECURE=false
```

**Production Settings:**
- Set `SUPERTOKENS_CONNECTION_URI` to your production SuperTokens URL
- Set `API_DOMAIN` to your backend domain (e.g., `https://api.yourdomain.com`)
- Set `WEBSITE_DOMAIN` to your frontend domain (e.g., `https://yourdomain.com`)
- Set `COOKIE_DOMAIN` to your domain (e.g., `.yourdomain.com`)
- Set `COOKIE_SECURE=true` for HTTPS
- Set `COOKIE_SAME_SITE=none` if frontend and backend are on different domains

### Step 4: Run the Application

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication Endpoints

#### 1. Sign Up
```http
POST /auth/signup
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "location": "New York"
}
```

**Response:**
- Creates user in both SuperTokens and your database
- Returns user information
- Sets session cookies automatically

#### 2. Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePassword123!"
}
```

**Response:**
- Validates credentials
- Creates new session
- Returns user info and sets cookies

#### 3. Get Current User (Auth Router)
```http
GET /auth/me
```

**Headers:**
- Cookies are automatically sent by the browser
- Or use: `Authorization: Bearer <access_token>`

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "location": "New York",
  "is_admin": false,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### 4. Logout
```http
POST /auth/logout
```

**Response:**
- Revokes the session
- Clears cookies
- Returns success message

### User Endpoints

#### 1. Get Current User (User Router)
```http
GET /user/me
```

Same as `/auth/me` - returns current user information.

#### 2. Get User Profile
```http
GET /user/profile
```

Returns complete user profile information.

#### 3. Admin Test Endpoint
```http
GET /user/admin/test
```

**Requirements:** User must have `is_admin=true`

**Response:**
```json
{
  "status": "OK",
  "message": "Admin access granted",
  "admin": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

## Using Protected Routes

### In Your Code

To protect a route, use the authentication dependencies:

```python
from fastapi import APIRouter, Depends
from app.core.auth_dependencies import get_current_user, get_current_admin_user
from app.models.models import User

router = APIRouter()

# Requires authenticated user
@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}!"}

# Requires admin user
@router.get("/admin-only")
async def admin_route(admin_user: User = Depends(get_current_admin_user)):
    return {"message": f"Admin access granted to {admin_user.username}"}
```

### Available Dependencies

1. **`get_current_user`**: Requires valid session, returns authenticated user
2. **`get_current_admin_user`**: Requires admin user, returns admin user
3. **`get_optional_session()`**: Optional authentication (session can be None)

## Session Management

### How Sessions Work

1. **Access Token**: Short-lived token (default: 1 hour) sent with each request
2. **Refresh Token**: Long-lived token used to get new access tokens
3. **Automatic Refresh**: SuperTokens SDK handles token refresh automatically

### Session Data

The access token payload includes:
```json
{
  "user_id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "is_admin": false
}
```

This data is available in protected routes via the session object.

## Frontend Integration

### Using with React/Vue/Angular

1. **Sign Up:**
```javascript
const response = await fetch('http://localhost:8000/auth/signup', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include', // Important: sends cookies
  body: JSON.stringify({
    username: 'johndoe',
    email: 'john@example.com',
    password: 'password123',
    full_name: 'John Doe',
    location: 'New York'
  })
});
```

2. **Login:**
```javascript
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({
    username: 'johndoe',
    password: 'password123'
  })
});
```

3. **Accessing Protected Routes:**
```javascript
const response = await fetch('http://localhost:8000/user/me', {
  method: 'GET',
  credentials: 'include' // Sends session cookies
});
```

4. **Logout:**
```javascript
const response = await fetch('http://localhost:8000/auth/logout', {
  method: 'POST',
  credentials: 'include'
});
```

### Important Frontend Notes

- Always include `credentials: 'include'` in fetch requests
- SuperTokens handles token refresh automatically
- Session cookies are httpOnly and secure (in production)

## Security Features

### Built-in Protection

1. **CSRF Protection**: Automatic CSRF token validation
2. **Secure Cookies**: httpOnly, secure (HTTPS), sameSite flags
3. **Token Rotation**: Access tokens automatically rotated
4. **Session Theft Detection**: Detects and prevents session hijacking
5. **Password Security**: Handled by SuperTokens with best practices

### Best Practices

1. Always use HTTPS in production (`COOKIE_SECURE=true`)
2. Set appropriate `COOKIE_DOMAIN` for your domain
3. Use strong passwords (enforce in frontend)
4. Regularly rotate your `SUPERTOKENS_API_KEY`
5. Monitor SuperTokens Core logs for suspicious activity

## Troubleshooting

### Common Issues

#### 1. "Connection refused" to SuperTokens Core

**Solution:** Make sure SuperTokens Core is running:
```bash
docker ps | grep supertokens
```

If not running, start it:
```bash
docker start supertokens
```

#### 2. CORS errors in browser

**Solution:** Update CORS settings in [main.py](app/main.py):
```python
allow_origins=["http://localhost:3000", "https://yourdomain.com"]
```

#### 3. "User not found in session"

**Solution:**
- Make sure you're logged in
- Check that cookies are being sent (`credentials: 'include'`)
- Verify session hasn't expired

#### 4. Import errors for supertokens_python

**Solution:** Install the package:
```bash
pip install supertokens-python>=0.29.0
```

## Migration from Old JWT System

The old JWT authentication system has been kept for backward compatibility but is no longer used by the new endpoints.

### What Changed

1. **`/auth/signup`**: Now creates SuperTokens session
2. **`/auth/login`**: Returns session cookies instead of JWT token
3. **`/auth/me`**: Now uses SuperTokens session verification
4. **`/user/me`**: Updated to use SuperTokens sessions

### Deprecated

The following are no longer used:
- `OAuth2PasswordBearer` scheme
- Manual JWT token creation in `/auth/login`
- `decode_access_token` function in user routes

## Database Schema

SuperTokens Core manages its own tables for sessions and authentication. Your application's User table remains unchanged:

```sql
User Table:
- id (Primary Key)
- username (Unique)
- email (Unique)
- hashed_password
- full_name
- location
- location_of_asset
- is_admin
- is_active
- created_at
- updated_at
```

## Additional Resources

- [SuperTokens Documentation](https://supertokens.com/docs)
- [SuperTokens Python SDK](https://supertokens.com/docs/emailpassword/quick-setup/backend)
- [FastAPI Integration Guide](https://supertokens.com/docs/emailpassword/quick-setup/backend/fastapi)

## Support

For issues or questions:
1. Check the [SuperTokens GitHub Issues](https://github.com/supertokens/supertokens-core/issues)
2. Visit the [SuperTokens Discord Community](https://supertokens.com/discord)
3. Review the [FAQ](https://supertokens.com/docs/faq)
