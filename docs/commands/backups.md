# backups

Manage backups.

```
discourse backups <subcommand>
```

## Subcommands

### list

List all backups.

```bash
discourse backups list
```

### create

Create a new backup.

```bash
discourse backups create
discourse backups create --no-uploads
```

| Option | Default | Description |
|---|---|---|
| `--with-uploads` / `--no-uploads` | `--with-uploads` | Include uploads in the backup |

### send-email

Send a download link email for a specific backup.

```bash
discourse backups send-email backup-2026-02-15.tar.gz
```

| Argument | Description |
|---|---|
| `FILENAME` | Backup filename |

## Examples

```bash
# List available backups
discourse backups list

# Create a backup without uploads (faster)
discourse backups create --no-uploads

# Send download link for a backup
discourse backups send-email backup-2026-02-15.tar.gz
```
