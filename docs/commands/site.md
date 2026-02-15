# site

Site information and settings.

```
discourse site <subcommand>
```

## Subcommands

### info

Get basic site information (title, description, version, etc.).

```bash
discourse site info
```

### full

Get the full site configuration including all settings, categories, trust levels, and more.

```bash
discourse site full
```

!!! tip
    The `full` command returns a large amount of data. Use `-o json` with `jq` to extract specific fields.

## Examples

```bash
# Show site name and version
discourse site info

# Get site version from JSON
discourse site info -o json | jq '.version'

# Export full site configuration
discourse site full -o json > site-config.json

# List all trust levels
discourse site full -o json | jq '.trust_levels'
```
