![logo](https://github.com/marzukia/django-erd/blob/main/docs/img/logo.png?raw=true)

Django ERD Generator is a command-line tool designed to generate Entity-Relationship Diagrams (ERDs) from Django models. It supports multiple output formats, making it easy to visualise database relationships in different diagramming tools. The generator extracts model definitions, fields, and relationships, converting them into structured representations suitable for use with Mermaid.js, PlantUML, and dbdiagram.io. This tool is useful for understanding database structures, documenting data models, and sharing visual representations with team members.

Supported dialects:
* Mermaid.js
* PlantUML
* dbdiagram.io

## Quickstart

To generate an Entity-Relationship Diagram (ERD) in the desired syntax, use the `generate_erd` command:

```sh
python manage.py generate_erd [-h] [-a APPS] [-d DIALECT] [-o OUTPUT]
```

### Options

| Option | Description |
|--------|------------|
| `-h, --help` | Show the help message and exit. |
| `-a APPS, --apps APPS` | Specify the apps to include in the ERD, separated by commas (e.g., `"shopping,polls"`). If omitted, all apps will be included. |
| `-d DIALECT, --dialect DIALECT` | Set the output format. Supported dialects: `mermaid`, `plantuml`, `dbdiagram`. |
| `-o OUTPUT, --output OUTPUT` | Define the output file path. If omitted, the output is printed to the console. |

### Examples

Generate an ERD for all apps in Mermaid format and print to console:
```sh
python manage.py generate_erd -d mermaid
```

Generate an ERD for `shopping` and `polls` apps in PlantUML format and save to `erd.puml`:
```sh
python manage.py generate_erd -a shopping,polls -d plantuml -o erd.puml
```

### Example Output

```py
from django.db import models


class Customer(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    date_of_birth = models.DateField()


class Product(models.Model):
    sku = models.TextField()
    product_name = models.TextField()
    product_code = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=16, decimal_places=2)
    regions = models.ManyToManyField("Region")


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_total = models.DecimalField(max_digits=16, decimal_places=2)


class Region(models.Model):
    name = models.TextField()
    label = models.TextField()

```

### Mermaid.js

#### Code Output

```
erDiagram
Customer {
  integer id pk
  text first_name
  text last_name
}
Product {
  integer id pk
  text sku
  text product_name
  text product_code
  integer quantity
  decimal price
}
Order {
  integer id pk
  integer customer_id
  integer product_id
  integer quantity
  decimal order_total
}
Region {
  integer id pk
  text name
  text label
}
Product }|--|{ Region: ""
Order }|--|| Customer: ""
Order }|--|| Product: ""
```

#### Rendered Example

![mermaid.js render example](https://github.com/marzukia/django-erd/blob/main/docs/img/examples/mermaid.png?raw=true "Mermaid.js render example")


### PlantUML

#### Code Output

```
@startuml

entity Customer {
  *id: integer
  first_name: text
  last_name: text
}
entity Product {
  *id: integer
  sku: text
  product_name: text
  product_code: text
  quantity: integer
  price: decimal
}
entity Order {
  *id: integer
  customer_id: integer
  product_id: integer
  quantity: integer
  order_total: decimal
}
entity Region {
  *id: integer
  name: text
  label: text
}
Product }|--|{ Region
Order }|--|| Customer
Order }|--|| Product

@enduml
```

#### Rendered Example

![PlantUML render example](https://github.com/marzukia/django-erd/blob/main/docs/img/examples/plantuml.png?raw=true "PlantUML render example")

### dbdiagram.io

#### Code Output

```
Table Customer {
  id "integer" [primary key]
  first_name "text"
  last_name "text"
}
Table Product {
  id "integer" [primary key]
  sku "text"
  product_name "text"
  product_code "text"
  quantity "integer"
  price "decimal"
}
Table Order {
  id "integer" [primary key]
  customer_id "integer"
  product_id "integer"
  quantity "integer"
  order_total "decimal"
}
Table Region {
  id "integer" [primary key]
  name "text"
  label "text"
}
Ref: Product.regions <> Region.id
Ref: Order.customer_id > Customer.id
Ref: Order.product_id > Product.id
```

#### Rendered Example

![dbdiagram render example](https://github.com/marzukia/django-erd/blob/main/docs/img/examples/dbdiagram.png?raw=true "dbdiagram.io render example")

## Data Dictionary Generation

The Data Dictionary feature allows you to generate comprehensive documentation of your Django models in Markdown format. This is particularly useful for maintaining up-to-date documentation of your database schema and sharing it with team members.

### Usage

```bash
python manage.py generate_data_dictionary [options]
```

### Options

- `-a, --apps`: Specify which apps to include in the data dictionary. Multiple apps should be comma-separated (e.g., "shopping,polls"). If not specified, all apps will be included.
- `-o, --output`: The path where the output Markdown file should be saved. If not specified, the output will be printed to stdout.

### Examples

Generate data dictionary for all apps and print to console:
```bash
python manage.py generate_data_dictionary
```

Generate data dictionary for specific apps and save to file:
```bash
python manage.py generate_data_dictionary --apps auth,myapp --output docs/data_dictionary.md
```

The generated data dictionary includes:
- Table of Contents with jump links to each section
- Organized documentation by app
- Detailed model information including fields and relationships
- Field types, constraints, and help text

### Rendered Example

```md
# tests - Data Dictionary

Commit `d3e45c95a2895dc3fe6c1c3629a5753d0e0a58d2`

---

## Table of Contents [#](#toc)

- [Table of Contents](#toc)
- [Modules](#modules)
  - [tests](#tests)
    - [Customer](#Customer)
    - [Product](#Product)
    - [Order](#Order)
    - [Region](#Region)

---

## Modules [#](#modules)

### tests

#### Customer[#](#Customer)

`Customer(id, first_name, last_name)`

| pk | field_name | data_type | related_model | description | nullable | unique | choices | max_length | db_index |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✓ | id | `integer` |  |  |  | ✓ |  |  |  |
|  | first_name | `text` |  |  |  |  |  |  |  |
|  | last_name | `text` |  |  |  |  |  |  |  |

#### Product[#](#Product)

`Product(id, sku, product_name, product_code, quantity, price, regions)`

| pk | field_name | data_type | related_model | description | nullable | unique | choices | max_length | db_index |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✓ | id | `integer` |  |  |  | ✓ |  |  |  |
|  | sku | `text` |  |  |  |  |  |  |  |
|  | product_name | `text` |  |  |  |  |  |  |  |
|  | product_code | `text` |  |  |  |  |  |  |  |
|  | quantity | `integer` |  |  |  |  |  |  |  |
|  | price | `decimal` |  |  |  |  |  |  |  |

#### Order[#](#Order)

`Order(id, customer, product, quantity, order_total)`

| pk | field_name | data_type | related_model | description | nullable | unique | choices | max_length | db_index |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✓ | id | `integer` |  |  |  |  |  |  |  |
|  | customer_id | `integer` | [Customer](#Customer) |  |  |  |  |  | ✓ |
|  | product_id | `integer` | [Product](#Product) |  |  |  |  |  | ✓ |
|  | quantity | `integer` |  |  |  |  |  |  |  |
|  | order_total | `decimal` |  |  |  |  |  |  |  |

#### Region[#](#Region)

`Region(id, name, label)`

| pk | field_name | data_type | related_model | description | nullable | unique | choices | max_length | db_index |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✓ | id | `integer` |  |  |  |  |  |  |  |
|  | name | `text` |  |  |  |  |  |  |  |
|  | label | `text` |  |  |  |  |  |  |  |

```

## **Supported Versions**

This project is tested against the following versions:

- **Python**: `3.8, 3.9, 3.10, 3.11, 3.12`
- **Django**: Latest compatible version based on `tox` dependencies

Ensure you have one of the supported Python versions installed before running tests. You can check your Python version with:
```sh
python --version
```

For testing, tox will automatically create isolated environments for each supported Python version.