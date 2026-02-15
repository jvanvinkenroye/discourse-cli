# Configuration

Discourse CLI supports layered configuration from multiple sources with a clear priority chain.

## Priority Order

Configuration is resolved in this order (highest priority first):

1. **CLI flags** (`--url`, `--api-key`, `--api-username`)
2. **Environment variables** (`DISCOURSE_URL`, `DISCOURSE_API_KEY`, etc.)
3. **Config file** (`~/.config/discourse-cli/config.yaml` or platform equivalent)

## Interactive Setup

```bash
# Create a default configuration
discourse config init

# Create a named profile
discourse config init --profile staging
```

The `init` command prompts for URL, API key, and API username, then saves to the config file.

## Config File Formats

The config file is stored at the platform-specific config directory (e.g. `~/.config/discourse-cli/config.yaml` on Linux/macOS).

### Flat Format (simple)

For a single Discourse instance:

```yaml
url: https://forum.example.com
api_key: your-api-key-here
api_username: system
timeout: 30
default_output: auto
```

### Profile Format (multiple instances)

For managing multiple Discourse instances:

```yaml
default_profile: production
profiles:
  production:
    url: https://forum.example.com
    api_key: prod-api-key
    api_username: system
    timeout: 30
    default_output: auto
  staging:
    url: https://staging.example.com
    api_key: staging-api-key
    api_username: system
```

## Profile Resolution

When using profile-based config, the active profile is determined by:

1. `--profile` / `-p` CLI flag
2. `DISCOURSE_PROFILE` environment variable
3. `default_profile` key in config file
4. `"default"` as final fallback

```bash
# Use a specific profile
discourse -p staging users list

# Set the default profile
discourse config use production

# List all profiles
discourse config list
```

## Environment Variables

| Variable | Config Key | Description |
|---|---|---|
| `DISCOURSE_URL` | `url` | Discourse instance URL |
| `DISCOURSE_API_KEY` | `api_key` | API key |
| `DISCOURSE_API_USERNAME` | `api_username` | API username (default: `system`) |
| `DISCOURSE_TIMEOUT` | `timeout` | Request timeout in seconds (default: `30`) |
| `DISCOURSE_DEFAULT_OUTPUT` | `default_output` | Default output format (`auto`/`json`/`table`) |
| `DISCOURSE_PROFILE` | -- | Profile name to use |

```bash
# Override with environment variables
export DISCOURSE_URL=https://forum.example.com
export DISCOURSE_API_KEY=your-key
discourse users list
```

## Config Options

| Key | Required | Default | Description |
|---|---|---|---|
| `url` | Yes | -- | Discourse instance base URL |
| `api_key` | Yes | -- | API key for authentication |
| `api_username` | No | `system` | Username for API requests |
| `timeout` | No | `30` | HTTP request timeout (seconds) |
| `default_output` | No | `auto` | Output format: `auto`, `json`, or `table` |

## Auto-Migration

When you create the first named profile on a flat config file, the existing flat configuration is automatically migrated into a `default` profile. No manual migration is needed.

```bash
# Start with flat config
discourse config init
# Writes: url, api_key, api_username (flat)

# Add a profile -- flat config auto-migrates to profile format
discourse config init --profile staging
# Now config.yaml has: profiles.default (old flat) + profiles.staging (new)
```

## Validate Configuration

Test the connection to verify your configuration works:

```bash
discourse config validate
discourse config validate --profile staging
```

## Show Current Config

Display the resolved configuration (API key is masked):

```bash
discourse config show
discourse config show --profile production
```
