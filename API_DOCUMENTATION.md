# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

All endpoints (except registration and token obtain) require JWT authentication.

Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

### Endpoints

#### 1. Register User
**POST** `/api/users/register/`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "EDITOR"
}
```

**Roles:** `ADMIN`, `EDITOR`, `READER`

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "EDITOR",
  "is_active": true
}
```

---

#### 2. Obtain JWT Token
**POST** `/api/token/`

Get access and refresh tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "EDITOR",
    "is_active": true
  }
}
```

---

#### 3. Refresh Token
**POST** `/api/token/refresh/`

Get a new access token using refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Articles

### 4. List Articles
**GET** `/api/articles/`

Get paginated list of articles (10 per page).

**Query Parameters:**
- `status` (optional): Filter by status (`draft`, `published`, `archived`)
- `page` (optional): Page number

**Response:** `200 OK`
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/articles/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Article Title",
      "status": "published",
      "author_email": "user@example.com",
      "created_at": "2025-10-02T12:00:00Z",
      "published_at": "2025-10-02T13:00:00Z"
    }
  ]
}
```

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/articles/?status=published"
```

---

### 5. Create Article
**POST** `/api/articles/`

Create a new article.

**Permissions:**
- Admin: ✅
- Editor: ✅
- Reader: ❌

**Request Body:**
```json
{
  "title": "My Article Title",
  "content": "This is the article content...",
  "status": "draft"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "My Article Title",
  "content": "This is the article content...",
  "status": "draft",
  "author": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "EDITOR",
    "is_active": true
  },
  "created_at": "2025-10-02T12:00:00Z",
  "updated_at": "2025-10-02T12:00:00Z",
  "published_at": null
}
```

**Example:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Article","content":"Content here","status":"draft"}' \
  "http://localhost:8000/api/articles/"
```

---

### 6. Get Article Detail
**GET** `/api/articles/{id}/`

Get details of a specific article.

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "My Article Title",
  "content": "This is the article content...",
  "status": "published",
  "author": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "EDITOR",
    "is_active": true
  },
  "created_at": "2025-10-02T12:00:00Z",
  "updated_at": "2025-10-02T12:00:00Z",
  "published_at": "2025-10-02T13:00:00Z"
}
```

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/articles/1/"
```

---

### 7. Update Article
**PUT** `/api/articles/{id}/`

Update an existing article.

**Permissions:**
- Admin: ✅ (all articles)
- Editor: ✅ (own articles only)
- Reader: ❌

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content...",
  "status": "published"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content...",
  "status": "published",
  "author": {...},
  "created_at": "2025-10-02T12:00:00Z",
  "updated_at": "2025-10-02T14:00:00Z",
  "published_at": "2025-10-02T14:00:00Z"
}
```

**Example:**
```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated","content":"New content","status":"published"}' \
  "http://localhost:8000/api/articles/1/"
```

---

### 8. Delete Article
**DELETE** `/api/articles/{id}/`

Delete an article.

**Permissions:**
- Admin: ✅ (all articles)
- Editor: ✅ (own articles only)
- Reader: ❌

**Response:** `204 No Content`

**Example:**
```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/articles/1/"
```

---

## Users

### 9. Get Current User
**GET** `/api/users/me/`

Get details of the authenticated user.

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "EDITOR",
  "is_active": true
}
```

---

### 10. List All Users
**GET** `/api/users/`

List all users (Admin only).

**Permissions:**
- Admin: ✅
- Editor: ❌
- Reader: ❌

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "EDITOR",
    "is_active": true
  }
]
```

---

## Permission Matrix

| Action | Admin | Editor | Reader |
|--------|-------|--------|--------|
| Create Article | ✅ | ✅ | ❌ |
| Read All Articles | ✅ | ✅ | ✅ |
| Update Own Article | ✅ | ✅ | ❌ |
| Update Any Article | ✅ | ❌ | ❌ |
| Delete Own Article | ✅ | ✅ | ❌ |
| Delete Any Article | ✅ | ❌ | ❌ |
| Manage Users | ✅ | ❌ | ❌ |

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Caching

The article list endpoint is cached for 15 minutes to improve performance. Cache is automatically invalidated when:
- A new article is created
- An article is updated
- An article is deleted
