# admin

Admin operations for user management (suspend, silence, activate, etc.).

```
discourse admin <subcommand>
```

## Subcommands

### activate

Activate a user.

```bash
discourse admin activate 42
```

| Argument | Description |
|---|---|
| `USER_ID` | User ID (integer) |

### deactivate

Deactivate a user.

```bash
discourse admin deactivate 42
```

| Argument | Description |
|---|---|
| `USER_ID` | User ID (integer) |

### suspend

Suspend a user. Prompts for confirmation unless `--yes` is passed.

```bash
discourse admin suspend 42 --until 2026-06-01 --reason "policy violation"
```

| Argument | Description |
|---|---|
| `USER_ID` | User ID (integer) |

| Option | Required | Description |
|---|---|---|
| `--until` | Yes | Suspension end date (`YYYY-MM-DD`) |
| `--reason` | Yes | Reason for suspension |
| `--message` | No | Message sent to the user |
| `--yes` | No | Skip confirmation prompt |

### silence

Silence a user. Prompts for confirmation unless `--yes` is passed.

```bash
discourse admin silence 42 --until 2026-04-01 --reason "spam"
```

| Argument | Description |
|---|---|
| `USER_ID` | User ID (integer) |

| Option | Required | Description |
|---|---|---|
| `--until` | Yes | Silence end date (`YYYY-MM-DD`) |
| `--reason` | Yes | Reason for silencing |
| `--message` | No | Message sent to the user |
| `--yes` | No | Skip confirmation prompt |

### anonymize

Anonymize a user. **This cannot be undone.** Prompts for confirmation unless `--yes` is passed.

```bash
discourse admin anonymize 42 --yes
```

| Argument | Description |
|---|---|
| `USER_ID` | User ID (integer) |

| Option | Description |
|---|---|
| `--yes` | Skip confirmation prompt |

### log-out

Log a user out of all sessions.

```bash
discourse admin log-out 42
```

| Argument | Description |
|---|---|
| `USER_ID` | User ID (integer) |

### refresh-gravatar

Refresh a user's Gravatar image.

```bash
discourse admin refresh-gravatar alice
```

| Argument | Description |
|---|---|
| `USERNAME` | Username |

## Examples

```bash
# Suspend a user for a month
discourse admin suspend 42 --until 2026-03-15 --reason "repeated violations" --message "Please review our community guidelines."

# Silence and then activate a user
discourse admin silence 42 --until 2026-02-28 --reason "cooling off" --yes
discourse admin activate 42

# Force log out a compromised account
discourse admin log-out 42
```
