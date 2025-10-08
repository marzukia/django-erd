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

