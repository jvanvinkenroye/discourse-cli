# categories

Manage categories.

```
discourse categories <subcommand>
```

## Subcommands

### list

List all categories.

```bash
discourse categories list
discourse categories list --include-subcategories
```

| Option | Description |
|---|---|
| `--include-subcategories` | Include subcategories in the listing |

### get

Get a category by ID.

```bash
discourse categories get 5
```

| Argument | Description |
|---|---|
| `CATEGORY_ID` | Category ID (integer) |

### create

Create a new category.

```bash
discourse categories create --name "Announcements" --color "0088CC" --text-color "FFFFFF"
```

| Option | Required | Description |
|---|---|---|
| `--name` | Yes | Category name |
| `--color` | No | Category color (hex, without `#`) |
| `--text-color` | No | Text color (hex, without `#`) |
| `--slug` | No | Category slug |
| `--parent-category-id` | No | Parent category ID (for subcategories) |

### update

Update a category.

```bash
discourse categories update 5 --name "News & Announcements" --color "FF0000"
```

| Argument | Description |
|---|---|
| `CATEGORY_ID` | Category ID (integer) |

| Option | Required | Description |
|---|---|---|
| `--name` | Yes | Category name |
| `--color` | No | Category color (hex) |
| `--text-color` | No | Text color (hex) |
| `--slug` | No | Category slug |
| `--parent-category-id` | No | Parent category ID |

### topics

List topics in a specific category.

```bash
discourse categories topics general 5
```

| Argument | Description |
|---|---|
| `SLUG` | Category slug |
| `CATEGORY_ID` | Category ID (integer) |

## Examples

```bash
# List all categories with subcategories
discourse categories list --include-subcategories

# Create a subcategory
discourse categories create --name "Bug Reports" --parent-category-id 5 --color "CC0000"

# Get category details as JSON
discourse categories get 5 -o json

# Browse topics in a category
discourse categories topics announcements 3
```
