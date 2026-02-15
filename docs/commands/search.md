# search

Search topics, posts, and users.

```
discourse search <QUERY>
```

This is a top-level command, not a command group.

## Arguments

| Argument | Description |
|---|---|
| `QUERY` | Search query string |

## Options

| Option | Description |
|---|---|
| `--page` | Page number for paginated results |

## Output

By default, search results display matching topics. If no topics match but posts do, posts are shown instead. Use `-o json` for the full response including all result types.

## Examples

```bash
# Basic search
discourse search "welcome guide"

# Paginate results
discourse search "installation" --page 2

# Get full search results as JSON
discourse search "docker" -o json | jq '.topics[].title'

# Use Discourse search operators
discourse search "status:open category:support"
discourse search "@alice order:latest"
```
