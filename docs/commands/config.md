# config

Manage Discourse CLI configuration and profiles.

```
discourse config <subcommand>
```

## Subcommands

### init

Create configuration file interactively.

```bash
discourse config init
discourse config init --profile staging
```

| Option | Description |
|---|---|
| `--profile` | Profile name to create (e.g. `staging`). Creates a named profile. |

Prompts for URL, API key, and API username. If a config file already exists and no profile is specified, asks for confirmation before overwriting.

### show

Show current configuration with masked API key.

```bash
discourse config show
discourse config show --profile production
```

| Option | Description |
|---|---|
| `--profile` | Profile name to show |

### validate

Validate configuration by testing the connection to the Discourse instance.

```bash
discourse config validate
discourse config validate --profile staging
```

| Option | Description |
|---|---|
| `--profile` | Profile name to validate |

### list

List all configured profiles.

```bash
discourse config list
```

Shows all profile names with the default profile marked.

### use

Set the default profile.

```bash
discourse config use production
```

| Argument | Description |
|---|---|
| `NAME` | Profile name to set as default |

## Examples

```bash
# Initial setup
discourse config init

# Add a staging profile
discourse config init --profile staging

# Verify connection
discourse config validate

# Switch between profiles
discourse config use staging
discourse config list
```
