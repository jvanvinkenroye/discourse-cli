# uploads

Manage file uploads.

```
discourse uploads <subcommand>
```

## Subcommands

### create

Create an upload.

```bash
discourse uploads create --type composer
discourse uploads create --type avatar --user-id 42 --synchronous
```

| Option | Required | Description |
|---|---|---|
| `--type` | Yes | Upload type: `avatar`, `profile_background`, `card_background`, `custom_emoji`, `composer` |
| `--user-id` | No | User ID for the upload |
| `--synchronous` | No | Perform a synchronous upload |

### create-multipart

Initiate a multipart upload for large files.

```bash
discourse uploads create-multipart --upload-type composer --file-name "large-file.zip" --file-size 104857600
```

| Option | Required | Description |
|---|---|---|
| `--upload-type` | Yes | Upload type |
| `--file-name` | Yes | File name |
| `--file-size` | Yes | File size in bytes |

### complete-external

Complete an external upload after all parts have been uploaded.

```bash
discourse uploads complete-external --unique-identifier "abc-123-def"
```

| Option | Required | Description |
|---|---|---|
| `--unique-identifier` | Yes | Upload identifier from the create-multipart response |

## Examples

```bash
# Simple upload
discourse uploads create --type composer

# Multipart upload workflow
discourse uploads create-multipart --upload-type composer --file-name "backup.zip" --file-size 52428800
# ... upload parts ...
discourse uploads complete-external --unique-identifier "abc-123"
```
