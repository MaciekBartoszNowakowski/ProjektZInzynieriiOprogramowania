# Applications component - endpoints

## Student endpoints

### POST /applications/submit/

Submitting application to thesis by authenticated student.

**Request Schema:**

```json
{
  "thesis_id": "number" (required)
}
```

**Response Schema:**

Created submission with thesis and student details.

```json
{
  "id": "number",
  "student": {
    "index_number": "string",
    "full_name": "string"
  },
  "thesis": {
    "id": "number",
    "name": "string",
    "thesis_type": "string",
    "description": "string",
    "status": "string",
    "language": "string",
    "supervisor_name": "string"
  }
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a student
- 400 Bad Request - one of the following:
  - thesis is not available for applications (status != APP_OPEN)
  - student is already assigned to another thesis
- 404 Not Found: when student or thesis not found in database

### DELETE /applications/cancel/

Canceling student's current application.

**Request Schema:**

No request body required.

**Response Schema:**

```json
{
  "message": "Anulowano zgłoszenie na pracę '{thesis_name}'"
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a student
- 400 Bad Request: when student has no active application
- 404 Not Found: when student not found in database

### GET /applications/status/

Getting student's application status.

**Request Schema:**

No request body required.

**Response Schema:**

If student has submission:
```json
{
  "has_submission": true,
  "submission": {
    "id": "number",
    "student": {
      "index_number": "string",
      "full_name": "string"
    },
    "thesis": {
      "id": "number",
      "name": "string",
      "thesis_type": "string",
      "description": "string",
      "status": "string",
      "language": "string",
      "supervisor_name": "string"
    },
    "status": "string"
  }
}
```

If student has no submission:
```json
{
  "has_submission": false,
  "submission": null,
  "message": "Nie masz aktywnej aplikacji na żadną pracę dyplomową"
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a student
- 404 Not Found: when student not found in database

## Supervisor endpoints

### GET /applications/thesis/{thesis_id}/submissions/

Getting all submissions for specific thesis by supervisor who owns it.

**Request Schema:**

No request body required.

**Response Schema:**

```json
{
  "thesis_id": "number",
  "thesis_name": "string",
  "submissions": [
    {
      "id": "number",
      "student": {
        "index_number": "string",
        "full_name": "string"
      },
      "thesis": {
        "id": "number",
        "name": "string",
        "thesis_type": "string",
        "description": "string",
        "status": "string",
        "language": "string",
        "supervisor_name": "string"
      },
      "status": "string"
    }
  ]
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a supervisor
- 404 Not Found: when supervisor or thesis not found, or thesis doesn't belong to supervisor

### POST /applications/submissions/{submission_id}/accept/

Accepting specific submission by supervisor.

**Request Schema:**

No request body required.

**Response Schema:**

Accepted submission details:
```json
{
  "id": "number",
  "student": {
    "index_number": "string",
    "full_name": "string"
  },
  "thesis": {
    "id": "number",
    "name": "string",
    "thesis_type": "string",
    "description": "string",
    "status": "string",
    "language": "string",
    "supervisor_name": "string"
  },
  "status": "string"
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a supervisor
- 404 Not Found: when supervisor or submission not found, or submission doesn't belong to supervisor's thesis
- 400 Bad Request: when submission has already been resolved (i. e. accepted or rejected) or maximum number of students for this thesis has been accepted

### POST /applications/submissions/{submission_id}/reject/

Rejecting specific submission by supervisor.

**Request Schema:**

No request body required.

**Response Schema:**

```json
{
  "message": "Odrzucono zgłoszenie studenta {student_name}"
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a supervisor
- 404 Not Found: when supervisor or submission not found, or submission doesn't belong to supervisor's thesis
- 400 Bad Request: when submission has already been resolved (i. e. accepted or rejected)

### DELETE /applications/submissions/{submission_id}/remove/

Removing student from thesis (for already accepted submissions).

**Request Schema:**

No request body required.

**Response Schema:**

```json
{
  "message": "Usunięto studenta {student_name} z pracy"
}
```

**Errors**:
- 403 Forbidden: when authenticated user is not a supervisor
- 404 Not Found: when supervisor or submission not found, or submission doesn't belong to supervisor's thesis
- 400 Bad Request: when submission has not been accepted - it has been rejected or is still yet to be resolved
