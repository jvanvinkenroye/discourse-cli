# tags

Manage tags and tag groups.

```
discourse tags <subcommand>
```

## Subcommands

### list

List all tags.

```bash
discourse tags list
```

### get

Get a tag by name, including associated topics.

```bash
discourse tags get python
```

| Argument | Description |
|---|---|
| `NAME` | Tag name |

### groups

List all tag groups.

```bash
discourse tags groups
```

### group-get

Get a tag group by ID.

```bash
discourse tags group-get 3
```

| Argument | Description |
|---|---|
| `GROUP_ID` | Tag group ID |

### group-create

Create a new tag group.

```bash
discourse tags group-create --name "Programming Languages"
```

| Option | Required | Description |
|---|---|---|
| `--name` | Yes | Tag group name |

### group-update

Update a tag group.

```bash
discourse tags group-update 3 --name "Languages"
```

| Argument | Description |
|---|---|
| `GROUP_ID` | Tag group ID |

| Option | Description |
|---|---|
| `--name` | New tag group name |

## Examples

```bash
# List all tags as JSON
discourse tags list -o json | jq '.[].name'

# View topics tagged with "python"
discourse tags get python -o json | jq '.topic_list.topics[].title'

# Manage tag groups
discourse tags groups
discourse tags group-create --name "Frameworks"
discourse tags group-update 5 --name "Web Frameworks"
```
