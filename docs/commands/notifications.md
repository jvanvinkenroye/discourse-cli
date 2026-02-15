# notifications

Manage notifications.

```
discourse notifications <subcommand>
```

## Subcommands

### list

List notifications for the current API user.

```bash
discourse notifications list
```

### mark-read

Mark notifications as read. Without `--id`, marks all notifications as read.

```bash
# Mark all as read
discourse notifications mark-read

# Mark a specific notification
discourse notifications mark-read --id 456
```

| Option | Description |
|---|---|
| `--id` | Specific notification ID. Omit to mark all as read. |

## Examples

```bash
# List unread notifications
discourse notifications list -o json | jq '[.[] | select(.read == false)]'

# Mark all notifications as read
discourse notifications mark-read
```
