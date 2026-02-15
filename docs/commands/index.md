# Commands Overview

Discourse CLI organizes commands into groups by resource type. Every data command supports the `-o` / `--output` option (see [Output Formats](../output-formats.md)).

## Global Options

These options are available on the root `discourse` command and apply to all subcommands:

| Option | Description |
|---|---|
| `--profile` / `-p` | Named config profile to use |
| `--url` | Discourse instance URL (overrides config) |
| `--api-key` | API key (overrides config) |
| `--api-username` | API username (overrides config) |
| `--version` | Show version and exit |
| `--help` | Show help and exit |

## Command Groups

| Group | Description |
|---|---|
| [config](config.md) | Manage CLI configuration and profiles |
| [users](users.md) | User management (list, get, create, update, delete) |
| [admin](admin.md) | Admin operations (suspend, silence, activate, anonymize) |
| [topics](topics.md) | Topic management (list, create, status, timer, invite) |
| [posts](posts.md) | Post management (list, get, create, update, delete, lock) |
| [categories](categories.md) | Category management (list, get, create, update, topics) |
| [groups](groups.md) | Group management (list, get, create, members) |
| [tags](tags.md) | Tag and tag group management |
| [badges](badges.md) | Badge management (list, create, update, delete) |
| [search](search.md) | Full-text search across topics and posts |
| [messages](messages.md) | Private messages (inbox, sent, create) |
| [notifications](notifications.md) | Notification management |
| [backups](backups.md) | Backup management |
| [invites](invites.md) | Invitation management |
| [site](site.md) | Site information and settings |
| [uploads](uploads.md) | File uploads |
| [api](api.md) | Generic API access to any endpoint |
