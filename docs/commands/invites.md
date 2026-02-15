# invites

Manage invitations.

```
discourse invites <subcommand>
```

## Subcommands

### create

Create an invite link or send an invite email.

```bash
discourse invites create --email alice@example.com
discourse invites create --max-redemptions 10 --group-names "beta-testers" --expires-at "2026-03-01"
```

| Option | Description |
|---|---|
| `--email` | Email address to invite |
| `--skip-email` | Create link only, don't send email |
| `--custom-message` | Custom invite message |
| `--max-redemptions` | Maximum number of redemptions allowed |
| `--topic-id` | Topic to invite to |
| `--group-names` | Comma-separated group names to add invitee to |
| `--expires-at` | Expiry date (ISO format) |

### bulk

Create multiple invites at once.

```bash
discourse invites bulk --email "emails.txt" --group-names "newcomers"
```

| Option | Description |
|---|---|
| `--email` | Email list (one per line in file) |
| `--group-names` | Comma-separated group names |
| `--custom-message` | Custom message |

## Examples

```bash
# Invite a user to the forum
discourse invites create --email new-user@example.com --custom-message "Welcome!"

# Create a reusable invite link
discourse invites create --skip-email --max-redemptions 50 --expires-at "2026-06-01"

# Invite users to a specific group
discourse invites create --email alice@example.com --group-names "beta-testers,moderators"
```
