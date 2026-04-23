# Data Dictionary

Generate comprehensive Markdown documentation from your Django models.

## Basic Usage

```bash
python manage.py generate_data_dictionary -o docs/data_dictionary.md
```

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `-a APPS` | Filter by specific apps | `-a shopping,polls` |
| `-o OUTPUT` | Output file path | `-o docs/dictionary.md` |

## Output Structure

The data dictionary includes:

- **Model Overview**: Description and database table name
- **Field Details**: Type, constraints, nullability
- **Relationships**: Foreign keys, many-to-many relationships
- **Help Text**: Documentation from field definitions
- **Meta Options**: Ordering, verbose names, unique_together

## Example Output

```markdown
# Data Dictionary

## Customer

**Table:** `auth_customer`

### Fields

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| id | bigint | Yes | Yes | Auto-incrementing primary key |
| first_name | varchar(100) | Yes | No | Customer's first name |
| last_name | varchar(100) | Yes | No | Customer's last name |
| email | varchar(254) | Yes | Yes | Email address (unique) |

### Relationships

- **Orders**: One-to-many relationship with Order model

## Order

**Table:** `sales_order`

### Fields

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| id | bigint | Yes | Yes | Auto-incrementing primary key |
| customer | bigint | Yes | No | Reference to Customer |
| order_date | datetime | Yes | No | Date and time of order |
| total | decimal(10,2) | Yes | No | Order total amount |

### Relationships

- **Customer**: Many-to-one relationship to Customer model
```

## Integration with Documentation

### MkDocs

1. Generate dictionary:
   ```bash
   python manage.py generate_data_dictionary -o docs/data_dictionary.md
   ```

2. Add to mkdocs.yml:
   ```yaml
   nav:
     - Data Dictionary: data_dictionary.md
   ```

### GitHub Wiki

1. Generate dictionary
2. Copy content to GitHub Wiki pages
3. Update on each model change

## Best Practices

- Generate data dictionary alongside ERDs
- Include in API documentation
- Update on every model change (add to CI/CD)
- Filter by app for modular documentation

## Comparison: ERD vs Data Dictionary

| Aspect | ERD | Data Dictionary |
|--------|-----|-----------------|
| **Format** | Visual diagram | Structured text |
| **Best For** | Quick overview | Detailed reference |
| **Content** | Models, relationships | Field properties, constraints |
| **Use Case** | Design reviews | Technical documentation |
