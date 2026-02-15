# topics

Manage topics.

```
discourse topics <subcommand>
```

## Subcommands

### list

List latest topics.

```bash
discourse topics list
discourse topics list --per-page 50 --order activity --ascending
```

| Option | Description |
|---|---|
| `--order` | Sort order field |
| `--ascending` | Sort ascending |
| `--per-page` | Results per page |

### top

List top topics by time period.

```bash
discourse topics top --period monthly
```

| Option | Description |
|---|---|
| `--period` | Time period: `all`, `yearly`, `quarterly`, `monthly`, `weekly`, `daily` |
| `--per-page` | Results per page |

### get

Get a topic by ID.

```bash
discourse topics get 123
```

| Argument | Description |
|---|---|
| `TOPIC_ID` | Topic ID |

### get-by-external-id

Get a topic by external ID.

```bash
discourse topics get-by-external-id ext-456
```

| Argument | Description |
|---|---|
| `EXTERNAL_ID` | External ID |

### create

Create a new topic.

```bash
discourse topics create --title "Welcome" --raw "Hello everyone!" --category 5
```

| Option | Required | Description |
|---|---|---|
| `--title` | Yes | Topic title |
| `--raw` | Yes | Post content (Markdown) |
| `--category` | No | Category ID |
| `--external-id` | No | External ID |

### update

Update a topic's title or category.

```bash
discourse topics update 123 --title "Updated Title" --category-id 7
```

| Argument | Description |
|---|---|
| `TOPIC_ID` | Topic ID |

| Option | Description |
|---|---|
| `--title` | New title |
| `--category-id` | New category ID |

### delete

Delete a topic. Prompts for confirmation unless `--yes` is passed.

```bash
discourse topics delete 123 --yes
```

| Argument | Description |
|---|---|
| `TOPIC_ID` | Topic ID |

| Option | Description |
|---|---|
| `--yes` | Skip confirmation prompt |

### status

Update topic status (close, archive, pin, visibility).

```bash
discourse topics status 123 --status closed --enabled
discourse topics status 123 --status pinned --enabled --until 2026-03-01
```

| Argument | Description |
|---|---|
| `TOPIC_ID` | Topic ID |

| Option | Required | Description |
|---|---|---|
| `--status` | Yes | Status to change: `closed`, `archived`, `visible`, `pinned` |
| `--enabled` / `--disabled` | Yes | Enable or disable the status |
| `--until` | No | Until date (for pinned topics) |

### timer

Set a topic timer (auto-close, auto-open, etc.).

```bash
discourse topics timer 123 --status-type close --time "2026-03-01 12:00"
```

| Argument | Description |
|---|---|
| `TOPIC_ID` | Topic ID |

| Option | Description |
|---|---|
| `--time` | Timer time |
| `--status-type` | Timer type (e.g. `close`, `open`) |
| `--category-id` | Move to category ID (for category-move timers) |

### invite

Invite a user to a topic by username or email.

```bash
discourse topics invite 123 --user alice
discourse topics invite 123 --email bob@example.com
```

| Argument | Description |
|---|---|
| `TOPIC_ID` | Topic ID |

| Option | Description |
|---|---|
| `--user` | Username to invite |
| `--email` | Email to invite |

### bookmark

Bookmark a topic.

```bash
discourse topics bookmark 123
```

| Argument | Description |
|---|---|
| `TOPIC_ID` | Topic ID |

### notification-level

Set the notification level for a topic.

```bash
discourse topics notification-level 123 --level 3
```

| Argument | Description |
|---|---|
| `TOPIC_ID` | Topic ID |

| Option | Required | Description |
|---|---|---|
| `--level` | Yes | Notification level: `0` (muted), `1` (normal), `2` (tracking), `3` (watching) |

## Examples

```bash
# List top topics of the week
discourse topics top --period weekly

# Create a pinned announcement
discourse topics create --title "Maintenance Window" --raw "Scheduled for Saturday." --category 1
discourse topics status 456 --status pinned --enabled --until 2026-03-01

# Auto-close a topic after a date
discourse topics timer 123 --status-type close --time "2026-04-01"

# Get topic as JSON for scripting
discourse topics get 123 -o json | jq '.title'
```
