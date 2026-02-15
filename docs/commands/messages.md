# messages

Manage private messages.

```
discourse messages <subcommand>
```

## Subcommands

### inbox

List a user's private message inbox.

```bash
discourse messages inbox alice
```

| Argument | Description |
|---|---|
| `USERNAME` | Username |

### sent

List a user's sent private messages.

```bash
discourse messages sent alice
```

| Argument | Description |
|---|---|
| `USERNAME` | Username |

### create

Send a private message.

```bash
discourse messages create --title "Hello" --raw "How are you?" --target-recipients "bob,charlie"
```

| Option | Required | Description |
|---|---|---|
| `--title` | Yes | Message subject |
| `--raw` | Yes | Message content (Markdown) |
| `--target-recipients` | Yes | Comma-separated usernames |

## Examples

```bash
# Check inbox
discourse messages inbox system

# Send a message to multiple users
discourse messages create --title "Meeting" --raw "Let's meet tomorrow." --target-recipients "alice,bob"

# List sent messages as JSON
discourse messages sent admin -o json
```
