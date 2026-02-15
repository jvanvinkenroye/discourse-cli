# groups

Manage groups.

```
discourse groups <subcommand>
```

## Subcommands

### list

List all groups.

```bash
discourse groups list
```

### get

Get a group by name.

```bash
discourse groups get moderators
```

| Argument | Description |
|---|---|
| `NAME` | Group name |

### get-by-id

Get a group by numeric ID.

```bash
discourse groups get-by-id 42
```

| Argument | Description |
|---|---|
| `GROUP_ID` | Group ID |

### create

Create a new group.

```bash
discourse groups create --name "beta-testers" --full-name "Beta Testers" --visibility-level 2
```

| Option | Required | Description |
|---|---|---|
| `--name` | Yes | Group name |
| `--full-name` | No | Full display name |
| `--bio-raw` | No | Group bio (Markdown) |
| `--visibility-level` | No | Visibility level (integer) |
| `--primary-group` | No | Set as primary group for members |

### update

Update a group.

```bash
discourse groups update 42 --full-name "Senior Beta Testers"
```

| Argument | Description |
|---|---|
| `GROUP_ID` | Group ID (integer) |

| Option | Description |
|---|---|
| `--name` | Group name |
| `--full-name` | Full display name |
| `--bio-raw` | Group bio |
| `--visibility-level` | Visibility level |

### delete

Delete a group. Prompts for confirmation unless `--yes` is passed.

```bash
discourse groups delete 42 --yes
```

| Argument | Description |
|---|---|
| `GROUP_ID` | Group ID (integer) |

| Option | Description |
|---|---|
| `--yes` | Skip confirmation prompt |

### members

List members of a group.

```bash
discourse groups members moderators
```

| Argument | Description |
|---|---|
| `NAME` | Group name |

### add-members

Add members to a group.

```bash
discourse groups add-members 42 --usernames "alice,bob,charlie"
```

| Argument | Description |
|---|---|
| `GROUP_ID` | Group ID (integer) |

| Option | Required | Description |
|---|---|---|
| `--usernames` | Yes | Comma-separated usernames to add |

### remove-members

Remove members from a group.

```bash
discourse groups remove-members 42 --usernames "charlie"
```

| Argument | Description |
|---|---|
| `GROUP_ID` | Group ID (integer) |

| Option | Required | Description |
|---|---|---|
| `--usernames` | Yes | Comma-separated usernames to remove |

## Examples

```bash
# Create a group and add members
discourse groups create --name "project-alpha" --full-name "Project Alpha Team"
discourse groups add-members 42 --usernames "alice,bob"

# List members as JSON
discourse groups members moderators -o json | jq '.[].username'

# Remove a member
discourse groups remove-members 42 --usernames "bob"
```
