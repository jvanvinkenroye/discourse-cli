# api

Generic API access to any Discourse endpoint. Use this when a dedicated command doesn't exist or you need full control over the request.

```
discourse api <METHOD> <PATH> [options]
```

This is a top-level command, not a command group.

## Arguments

| Argument | Description |
|---|---|
| `METHOD` | HTTP method: `GET`, `POST`, `PUT`, `DELETE`, `PATCH` |
| `PATH` | API endpoint path (e.g. `/site.json`) |

## Options

| Option | Description |
|---|---|
| `-p`, `--param` | Query parameter as `key=value`. Repeatable. |
| `-d`, `--data` | JSON request body (inline string or `@filename`) |
| `--list` | List all available API endpoints |

## Usage

### Simple GET request

```bash
discourse api GET /site.json
```

### GET with query parameters

```bash
discourse api GET /admin/users.json -p page=1 -p show_emails=true
```

### POST with inline JSON body

```bash
discourse api POST /posts.json -d '{"raw": "Hello world!", "topic_id": 123}'
```

### POST with JSON body from file

```bash
discourse api POST /posts.json -d @payload.json
```

### List all endpoints

```bash
discourse api --list
```

This reads the OpenAPI specification bundled with the project and lists all available endpoints with their HTTP methods, paths, and descriptions.

## Examples

```bash
# Get site settings
discourse api GET /site.json -o json | jq '.default_locale'

# Create a post via raw API
discourse api POST /posts.json -d '{"raw": "New post content", "topic_id": 42}'

# Fetch admin dashboard stats
discourse api GET /admin/dashboard.json

# Update a site setting
discourse api PUT /admin/site_settings/title.json -d '{"title": "My Forum"}'

# Delete with parameters
discourse api DELETE /admin/users/99.json -d '{"delete_posts": true}'

# Paginate through users
discourse api GET /admin/users/list/active.json -p page=0
discourse api GET /admin/users/list/active.json -p page=1
```
