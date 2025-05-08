# PI Endpoints Documentation

This document describes the available API endpoints, including their request and response schemas and error messages.

## Authentication

### POST /auth/login

Authenticates a user using either email or username and password.

**Request Schema:**

Option 1 - Email authentication:
```json
{
  "email": "string",
  "password": "string"
}
```

Option 2 - Username authentication:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response Schema:**

Returns access and refresh tokens (not necessery, because also in cookies)upon successful authentication, along with basic user information.

```json
{
  "access": "string",
  "refresh": "string",
  "user": {
    "pk": "number",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
  }
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```

### POST /auth/token/refresh

This endpoint is intended for refreshing an authentication token.

**Request Schema:**

```json
{
  "email": "string",
  "password": "string"
}
```

OR

```json
{
  "username": "string",
  "password": "string"
}
```

**Response Schema:**

```json
{
  "access": "string",
  "refresh": "string",
  "user": {
    "pk": "number",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
  }
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```

### POST /auth/logout

Logs out the currently authenticated user, invalidating their tokens.

**Request Schema:**

No request body required.

**Response Schema:**

```json
{
  "detail": "string"
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```

### POST /auth/password/change

Allows the currently authenticated user to change their password.

**Request Schema:**

```json
{
  "new_password1": "string",
  "new_password2": "string"
}
```

**Response Schema:**

```json
{
  "detail": "string"
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```

### POST /auth/password/reset

Initiates the password reset process by sending an email containing a reset link to the user.

**Request Schema:**

```json
{
  "email": "string"
}
```

**Response Schema:**

```json
{
  "detail": "string"
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```

### POST /reset/{token}

This endpoint is part of the password reset workflow, accessed via a link sent in an email.

**Request Schema:**

No request body required (token is passed in the URL path).

**Response:**

The response redirects to a page to set the new password.

**Error Response:**
```json
{
  "detail": "string"
}
```

## Users

### GET/PUT/PATCH /users/me

Retrieves or updates details for the currently authenticated user. The response structure depends on the user's role.

**Request Schema (GET):**

No request body required.

**Request Schema (PUT/PATCH):**

User profile data to update.

**Response Schema:**

If user role is **Supervisor**:

```json
{
  "user": {
    "id": "number",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "academic_title": "string",
    "role": "string",
    "description": "string",
    "department": "number",
    "tags": []
  },
  "bacherol_limit": "number",
  "engineering_limit": "number",
  "master_limit": "number",
  "phd_limit": "number"
}
```

If user role is **Student**:

```json
{
  "user": {
    "id": "number",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "academic_title": "string",
    "role": "string",
    "description": "string",
    "department": "number",
    "tags": []
  },
  "index_number": "number"
}
```

If user role is **Coordinator** or **Admin**:

```json
{
  "id": "number",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "academic_title": "string",
  "role": "string",
  "description": "string",
  "department": "number",
  "tags": []
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```

### GET/PUT /users/me/tags

Retrieves or modifies the tags associated with the current user.

**Request Schema (GET):**

No request body required.

**Request Schema (PUT):**

```json
{
  "to_add": [
    "list of tags ids"
  ],
  "to_remove": [
    "list of tags ids"
  ]
}
```

**Response Schema:**

Returns an array containing the current list of tags for the user.

```json
[
  {
    "id": "number",
    "name": "string"
  },
  // ... more tag objects
]
```

**Error Response:**
```json
{
  "detail": "string"
}
```

### GET /users

Retrieves a list of all users.

**Request Schema:**

No request body required.

**Response Schema:**

Returns an array of user objects with limited details.

```json
[
  {
    "url": "string",
    "academic_title": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "role": "string"
  },
  // ... more user objects
]
```

**Error Response:**
```json
{
  "detail": "string"
}
```

### POST /users/create

Creates a new user in the system. Requires coordinator permissions.

**Request Schema:**

```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "academic_title": "string",
  "role": "string",
  "department": "number",
  "index_number": "number",  // only for students
  "bacherol_limit": "number", // only for supervisors
  "engineering_limit": "number", // only for supervisors
  "master_limit": "number", // only for supervisors
  "phd_limit": "number" // only for supervisors
}
```

**Response Schema:**

For a student:
```json
{
  "user": {
    "id": "number",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "academic_title": "string",
    "role": "string",
    "description": "string",
    "department": "number",
    "tags": []
  },
  "index_number": "number"
}
```

For a supervisor:
```json
{
  "user": {
    "id": "number",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "academic_title": "string",
    "role": "string",
    "description": "string",
    "department": "number",
    "tags": []
  },
  "bacherol_limit": "number",
  "engineering_limit": "number",
  "master_limit": "number",
  "phd_limit": "number"
}
```

**Error Responses:**

Validation error:
```json
{
  "detail": "string"
}
```

Permission error:
```json
{
  "detail": "string"
}
```

Server error:
```json
{
  "detail": "string"
}
```

### GET /users/{id}

Retrieves detailed information for a specific user identified by their ID in the URL path.

**Request Schema:**

No request body required. The user ID is part of the URL (e.g., `/users/123`).

**Response Schema:**

```json
{
  "id": "number",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "academic_title": "string",
  "role": "string",
  "description": "string",
  "department": "number",
  "tags": []
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```

## Tags

### GET /tags

Retrieves a list of all available tags in the system.

**Request Schema:**

No request body required.

**Response Schema:**

Returns an array of tag objects with their ID and name.

```json
[
    {
        "id": "number",
        "name": "string"
    },
    // more
]
```

**Error Response:**
```json
{
  "detail": "string"
}
```


### GET/PUT/PATCH /common/department/

Retrieves or modifies the department associated with coordinator.

**Request Schema (GET):**

No request body required.

**Request Schema (PUT/PATCH):**

```json
{
  "name": "string",
  "description": "string"
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```


### GET /users/coordinator-view/

Retrieves a list of managable users on coordinator's department.

**Request Schema (GET):**

No request body required.


**Error Response:**
```json
{
  "detail": "string"
}
```

### GET/PUT/PATCH /users/coordinator-view/{id}

Retrieves or modifies the user in coordinator's department.

**Request Schema (GET):**

No request body required.

**Request Schema (PUT/PATCH):**

```json
{
  "academic_title": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "role": "string",
  "is_active": "bool"
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```