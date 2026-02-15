# Output Formats

Every data command supports the `--output` / `-o` option to control how results are displayed.

## Available Formats

### `auto` (default)

Automatically selects the best format based on context:

- **TTY** (interactive terminal): renders as a rich table
- **Pipe / redirect**: outputs raw JSON

```bash
# Table output in terminal
discourse users list

# JSON output when piped
discourse users list | jq .
```

### `json`

Always outputs formatted JSON, regardless of terminal context. Useful for scripting and data processing.

```bash
discourse users list -o json
```

### `table`

Always renders a rich table, even when output is piped. Uses the [Rich](https://rich.readthedocs.io/) library for formatting.

```bash
discourse users list -o table
```

## Piping with jq

The `auto` format makes it easy to pipe output to `jq` without explicitly specifying `-o json`:

```bash
# Extract usernames
discourse users list | jq '.[].username'

# Count topics
discourse topics list | jq '.| length'

# Pretty-print a specific user
discourse users get alice | jq '.user'

# Filter active admin users
discourse users list | jq '[.[] | select(.admin == true and .active == true)]'
```

## Table Rendering

Table output adapts to the data shape:

- **List of dicts**: columnar table with keys as headers
- **Single dict**: two-column key-value table
- **Simple list**: numbered rows

Nested or complex values are truncated to 80 characters for readability. Use `-o json` when you need the full data.
