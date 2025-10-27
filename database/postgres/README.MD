# postgres (init scripts)

This folder is intended for SQL and shell scripts that the official Postgres Docker image will run at container initialization.

Key points
- Place files here that should be executed by the image's entrypoint (they are copied/mounted into `/docker-entrypoint-initdb.d`).
- Supported file types: `.sql`, `.sql.gz`, `.sh` (shell scripts). Files are executed in alphanumeric order.
- Scripts run only when the database cluster is empty (first container start for a volume).
- Ensure scripts are readable and, for `.sh`, executable.

Recommended filenames
- Prefix with an order number if execution order is important, e.g. `01-create-db.sql`, `02-schema.sql`, `10-seed-data.sql`.

Example SQL (`01-create-db.sql`)
```sql
CREATE USER app_user WITH PASSWORD 'change_me';
CREATE DATABASE app_db OWNER app_user;
```

Example docker-compose volume mapping
```yaml
services:
    db:
        image: postgres:15
        volumes:
            - ./postgres:/docker-entrypoint-initdb.d
        environment:
            POSTGRES_PASSWORD: example
```

Notes
- Avoid including secrets in repository files; use environment variables or Docker secrets.
- If re-running initialization is required, remove the Postgres data volume so the entrypoint runs again.
- Keep scripts idempotent when possible.