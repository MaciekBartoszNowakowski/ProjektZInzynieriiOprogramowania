# Thesis component - endpoints

### POST /thesis/add

Adding thesis by authenticated supervisor.

**Request Schema:**

```json
{
  "thesis_type": "string", (required)
  "name": "string", (required)
  "description": "string", (optional)
  "max_students": "number", (optional, default=1, must be positive)
  "language": "string", (optional, default="English")
  "tags": [
    "string"
  ]
}
```

**Response Schema:**

Returns confirmation the thesis was added successfully.

```json
{
  "detail": "New thesis added successfully."
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a supervisor
- 400 Bad Request - one of the following:
- - supervisor id is invalid (not found in the database),
- - wrong thesis type,
- - supervisor does not have title required to supervise specific thesis type (e. g. has a Master title and wants to create phd thesis),
- - supervisor has already used his limit for given thesis type (adding next one would cause exceeding the limit),
- - given `max_students` value is nonpositive,
- - not all tags are of a correct type (`common.models.Tag`)

### PUT /thesis/update/{id}

Updating specific thesis (given by id) by supervisor who added it.

**Request Schema:**

```json
{
  "name": "string", (required)
  "description": "string", (optional, if not given stays the same)
  "max_students": "number", (optional, if not given stays the same, must be positive)
  "status": "string", (required)
  "language": "string" (optional, if not given stays the same)
  "tags": [
    "string"
  ]
}
```

**Response Schema:**

Thesis after the update.

```json
{
  "id": "number",
  "supervisor_id": "number",
  "thesis_type": "string",
  "name": "string",
  "description": "string",
  "max_students": "number",
  "status": "string",
  "language": "string",
  "tags": [
    "string"
  ]
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a supervisor
- 400 Bad Request - one of the following:
- - supervisor id is invalid (not found in the database),
- - thesis id is invalid (not found in the database),
- - thesis was not added by requesting supervisor,
- - wrong thesis status,
- - given `max_students` value is nonpositive,
- - not all tags are of a correct type (`common.models.Tag`)

### DELETE /thesis/delete/{id}

Deleting thesis given by id by supervisor who originally added it.

**Request Schema:**

No request body required.

**Response Schema:**

Thesis that has just been deleted.

```json
{
  "id": "number",
  "supervisor_id": "number",
  "thesis_type": "string",
  "name": "string",
  "description": "string",
  "max_students": "number",
  "status": "string",
  "language": "string",
  "tags": [
    "string"
  ]
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a supervisor
- 400 Bad Request - one of the following:
- - supervisor id is invalid (not found in the database),
- - thesis id is invalid (not found in the database),
- - thesis was not added by requesting supervisor.

### GET /thesis/available

Displays all theses available for students to apply (with status: APP_OPEN).

**Request Schema:**

No request body required.

**Response Schema:**

All available theses list.

```json
[
  {
    "url": "string", (url to specific thesis, containing its id - compare below)
    "supervisor_id": "number",
    "thesis_type": "string",
    "name": "string",
    "description": "string",
    "max_students": "number",
    "language": "string",
    "tags": [
      "string"
    ]
  },
  // ... more theses
]
```

### GET /thesis/available/{id}

Like above, but displays more specific info about thesis (supervisor info) for thesis given by id.

**Request Schema:**

No request body required.

**Response Schema:**

```json
{
  "id": "number",
  "supervisor_id": {
    "user": {
      "email": "string",
      "first_name": "string",
      "last_name": "string",
      "academic_title": "string",
      "description": "string",
      "department": "number",
      "department_name": "string",
      "tags": [
        "string"
      ]
    }
  },
  "thesis_type": "string",
  "name": "string",
  "description": "string",
  "max_students": "number",
  "language": "string",
  "tags": [
    "string"
  ]
}
```

**Errors**:
- 404 Not Found - if no thesis with given id exists.

### GET /thesis/my-topics

Displays *all* thesis present in the system for an authenticated supervisor.

**Request Schema:**

No request body required.

**Response Schema:**

Theses list.

```json
[
  {
    "id": "number",
    "thesis_type": "string",
    "name": "string",
    "description": "string",
    "max_students": "number",
    "status": "string",
    "language": "string",
    "tags": [
      "string"
    ]
  },
  // ... more theses
]
```

**Errors**:
- 403 Forbidden: when authenticated user is not a supervisor
- 400 Bad Request: when supervisor id is invalid (not found in the database)

*Not exactly an error, but other than 200 OK:*
- 204 No Content: if supervisor has no theses in the system.

### GET /common/search-topics/[QUERY]

#### Query parameters:
- first_name (optional) - default None (example: `first_name=Bogdan`) 
- last_name (optional) - default None (example: `last_name=Bogdanowski`)
- academic_title (optional) - default None (example: `academic_title=doctor`)
- tags (optional) - default None (example: `tags=AI&tags=Math`)
- department (optional) - default None (values: string matching department name from database)
- thesis_type (optional) - default None (example: `thesis_type=engineering`)
- language (optional) - default None (example: `language=English`)
- limit (optional) - default 10 (example: `limit=5`)
- offset (optional) - default 0 (example: `offset=2`)

**Response schema:**

All available theses that comply with query parameters. For no parameters given it is equivalent to response of `GET /thesis/available`.

```json
[
  {
    "url": "string",
    "supervisor_id": "number",
    "thesis_type": "string",
    "name": "string",
    "description": "string",
    "max_students": "number",
    "language": "string",
    "tags": [
      "string"
    ]
  },
  // ... more theses
]
```
