# Base PostgreSQL Repository

**Version: v0.1.0**

A Python client library that provides a base repository for the PostgreSQL database.

## Installation

Install the package using pip:

```bash
pip install git+https://${GITHUB_TOKEN}@<repository-url>.git
```

Or install from source:

```bash
git clone <repository-url>
cd postgresql-repository
pip install .
```

## Dependencies

- Python >= 3.7
- asyncpg==0.30.0
- environs==14.3.0

# Usage
```
from postgresql_repository.base_postgresql_repository import BasePostgreSQLRepository


class LeadRepository(BasePostgreSQLRepository):
    def __init__(self, db_connection: DatabaseConnection):
        self._db_connection = db_connection
        super().__init__(db_connection, "Lead", Lead)
```
