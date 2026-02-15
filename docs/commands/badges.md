# badges

Manage badges.

```
discourse badges <subcommand>
```

## Subcommands

### list

List all badges.

```bash
discourse badges list
```

### user

List badges awarded to a specific user.

```bash
discourse badges user alice
```

| Argument | Description |
|---|---|
| `USERNAME` | Username |

### create

Create a new badge.

```bash
discourse badges create --name "Contributor" --badge-type-id 3
```

| Option | Required | Description |
|---|---|---|
| `--name` | Yes | Badge name |
| `--badge-type-id` | Yes | Badge type: `1` (gold), `2` (silver), `3` (bronze) |

### update

Update a badge.

```bash
discourse badges update 10 --name "Top Contributor" --badge-type-id 2
```

| Argument | Description |
|---|---|
| `BADGE_ID` | Badge ID (integer) |

| Option | Required | Description |
|---|---|---|
| `--name` | Yes | Badge name |
| `--badge-type-id` | Yes | Badge type ID |

### delete

Delete a badge. Prompts for confirmation unless `--yes` is passed.

```bash
discourse badges delete 10 --yes
```

| Argument | Description |
|---|---|
| `BADGE_ID` | Badge ID (integer) |

| Option | Description |
|---|---|
| `--yes` | Skip confirmation prompt |

## Examples

```bash
# List all badges
discourse badges list

# Check a user's badges
discourse badges user alice -o json | jq '.[].name'

# Create a bronze badge
discourse badges create --name "First Post" --badge-type-id 3

# Upgrade badge to silver
discourse badges update 10 --name "First Post" --badge-type-id 2
```
