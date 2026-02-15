# posts

Manage posts.

```
discourse posts <subcommand>
```

## Subcommands

### list

List latest posts across all topics.

```bash
discourse posts list
discourse posts list --before 500
```

| Option | Description |
|---|---|
| `--before` | List posts before this post ID (for pagination) |

### get

Get a post by ID.

```bash
discourse posts get 42
```

| Argument | Description |
|---|---|
| `POST_ID` | Post ID |

### create

Create a new post (reply to a topic).

```bash
discourse posts create --topic-id 123 --raw "Great discussion!"
discourse posts create --topic-id 123 --raw "I agree with you." --reply-to 2
```

| Option | Required | Description |
|---|---|---|
| `--topic-id` | No | Topic ID to reply to |
| `--raw` | Yes | Post content (Markdown) |
| `--reply-to` | No | Post number to reply to within the topic |

### update

Update a post's content.

```bash
discourse posts update 42 --raw "Updated content here." --edit-reason "Fixed typo"
```

| Argument | Description |
|---|---|
| `POST_ID` | Post ID |

| Option | Description |
|---|---|
| `--raw` | New post content |
| `--edit-reason` | Reason for the edit |

### delete

Delete a post. Prompts for confirmation unless `--yes` is passed.

```bash
discourse posts delete 42 --yes
discourse posts delete 42 --force --yes
```

| Argument | Description |
|---|---|
| `POST_ID` | Post ID (integer) |

| Option | Description |
|---|---|
| `--force` | Force destroy (permanent deletion) |
| `--yes` | Skip confirmation prompt |

### lock

Lock or unlock a post to prevent editing.

```bash
discourse posts lock 42 --locked
discourse posts lock 42 --unlocked
```

| Argument | Description |
|---|---|
| `POST_ID` | Post ID |

| Option | Required | Description |
|---|---|---|
| `--locked` / `--unlocked` | Yes | Lock or unlock the post |

### replies

Get replies to a specific post.

```bash
discourse posts replies 42
```

| Argument | Description |
|---|---|
| `POST_ID` | Post ID |

## Examples

```bash
# Reply to a topic
discourse posts create --topic-id 123 --raw "Thanks for sharing!"

# Edit a post with a reason
discourse posts update 42 --raw "Corrected version." --edit-reason "Fixed formatting"

# Get replies as JSON
discourse posts replies 42 -o json

# Lock a staff post
discourse posts lock 42 --locked
```
