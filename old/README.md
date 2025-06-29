## Build & Deploy (API)
The API is a Python Flask project. To run the API (default port `:5000`) run `flask run` or simply `python3 app.py`.

## Migrations
#### Adding a migration
After schema / model changes within SQLAlchemy code, close the API and run `alembic revision --autogenerate -m "commit message"`, this will create a migration script in `/migrations/versions`.

#### Running a migration
After creating a migration, to synchronize the Database with the Code, run `alembic upgrade head`.

#### Undo a Migration
If the migration has already been run, you can use `alembic downgrade -1` to undo the last 1 migration.

## Database Access
This application uses an isolated borealis postgreSQL database that requires a secure SSH tunnel to access. Environment variables for database access are managed by deployment pipeline.
### CLI / PgAdmin
To create a tunnel with the database in order to connect, use the following commands. Find the port number from the `DATABASE_READONLY_URL` and `DATABASE_URL` environment variables respectively.

Readonly Access:
`heroku borealis-pg:tunnel --app cyther-api --port {PORT}`

Read / Write Access
`heroku borealis-pg:tunnel --app cyther-api {PORT} --write-access`

## Emergency Database Refresh
If something horrible happens I can use this script when within the tunnel to delete all tables except important ones:
```SQL
DO $$ 
DECLARE
    r RECORD;
BEGIN
    PERFORM 'SET session_replication_role = replica';

    -- Loop through all tables in the current schema except for the Users table
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename <> 'user' AND tablename <> 'user_roles') LOOP
        -- Drop each table
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;

    PERFORM 'SET session_replication_role = DEFAULT';
END $$;
```
