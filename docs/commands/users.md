# users

Manage users.

```
discourse users <subcommand>
```

## Subcommands

### list

List users (admin endpoint).

```bash
discourse users list
discourse users list --flag staff --order username --asc
```

| Option | Description |
|---|---|
| `--flag` | Filter by flag: `active`, `new`, `staff`, `suspended`, `blocked`, `suspect` |
| `--order` | Sort order field |
| `--asc` | Sort ascending |
| `--page` | Page number |
| `--show-emails` | Show email addresses |
| `--email` | Filter by email |
| `--ip` | Filter by IP address |

### get

Get user details by username.

```bash
discourse users get alice
```

| Argument | Description |
|---|---|
| `USERNAME` | Username to look up |

### get-by-id

Get user details by numeric ID (admin endpoint).

```bash
discourse users get-by-id 42
```

| Argument | Description |
|---|---|
| `USER_ID` | User ID (integer) |

### create

Create a new user. Prompts for password if not provided.

```bash
discourse users create --name "Alice" --email alice@example.com --username alice --password secret
```

| Option | Required | Description |
|---|---|---|
| `--name` | Yes | Display name |
| `--email` | Yes | Email address |
| `--username` | Yes | Username |
| `--password` | Yes | Password (prompted if omitted) |
| `--active` / `--no-active` | No | Activate immediately |
| `--approved` / `--no-approved` | No | Approve immediately |

### update

Update a user.

```bash
discourse users update alice --name "Alice Smith"
```

| Argument | Description |
|---|---|
| `USERNAME` | Username to update |

| Option | Description |
|---|---|
| `--name` | New display name |

### delete

Delete a user (admin endpoint). Prompts for confirmation unless `--yes` is passed.

```bash
discourse users delete 42 --yes
discourse users delete 42 --delete-posts --block-email
```

| Argument | Description |
|---|---|
| `USER_ID` | User ID (integer) |

| Option | Description |
|---|---|
| `--delete-posts` | Also delete the user's posts |
| `--block-email` | Block the user's email |
| `--block-urls` | Block the user's URLs |
| `--block-ip` | Block the user's IP |
| `--yes` | Skip confirmation prompt |

### emails

Get a user's email addresses (admin endpoint).

```bash
discourse users emails alice
```

| Argument | Description |
|---|---|
| `USERNAME` | Username |

### update-username

Change a user's username.

```bash
discourse users update-username alice --new-username alice_smith
```

| Argument | Description |
|---|---|
| `USERNAME` | Current username |

| Option | Required | Description |
|---|---|---|
| `--new-username` | Yes | New username |

### update-email

Change a user's email.

```bash
discourse users update-email alice --email new@example.com
```

| Argument | Description |
|---|---|
| `USERNAME` | Username |

| Option | Required | Description |
|---|---|---|
| `--email` | Yes | New email address |

### reset-password

Send a password reset email.

```bash
discourse users reset-password alice
```

| Argument | Description |
|---|---|
| `LOGIN` | Username or email |

### actions

List user actions.

```bash
discourse users actions alice --filter 1
```

| Argument | Description |
|---|---|
| `USERNAME` | Username |

| Option | Required | Description |
|---|---|---|
| `--filter` | Yes | Action type filter (e.g. `1` for likes) |
| `--offset` | No | Offset (default: 0) |

### by-external-id

Get user by external ID.

```bash
discourse users by-external-id ext-12345
```

| Argument | Description |
|---|---|
| `EXTERNAL_ID` | External ID |

### public

List the public user directory.

```bash
discourse users public --period monthly --order likes_received
```

| Option | Required | Description |
|---|---|---|
| `--period` | Yes | Time period: `daily`, `weekly`, `monthly`, `quarterly`, `yearly`, `all` |
| `--order` | Yes | Sort by: `likes_received`, `likes_given`, `topic_count`, `post_count`, `topics_entered`, `posts_read`, `days_visited` |
| `--asc` | No | Sort ascending |
| `--page` | No | Page number |

## Examples

```bash
# List active users
discourse users list --flag active

# Get user details as JSON
discourse users get alice -o json

# Create and activate a user
discourse users create --name "Bob" --email bob@example.com --username bob --active

# Delete user and block their email
discourse users delete 42 --delete-posts --block-email --yes

# Find user by external SSO ID
discourse users by-external-id sso-abc123
```
