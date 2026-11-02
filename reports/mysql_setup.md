# MySQL setup and verification

SQL targets MySQL 8.0.16+ and has been verified on MySQL Community Server 9.4.0. Install and start a compatible server before proceeding. Use MySQL Workbench or the `mysql` client to connect with an administrator account. For Oracle's macOS installation, the client is typically available at `/usr/local/mysql/bin/mysql`.

## Create a project account

Run the following in an administrator session, substituting a unique password locally. Do not save real credentials in SQL files or command-line arguments.

```sql
CREATE USER 'advertising_user'@'localhost'
IDENTIFIED BY 'REPLACE_WITH_A_UNIQUE_STRONG_PASSWORD';

GRANT SELECT, INSERT, UPDATE, CREATE, CREATE VIEW, SHOW VIEW, DROP
ON advertising_analytics.* TO 'advertising_user'@'localhost';
```

Privileges apply only to the project database. CREATE supports initialization; DROP supports CREATE OR REPLACE VIEW. Scripts do not drop tables. If this account already exists, review its configuration rather than rerunning CREATE USER.

For an import-only account, an administrator can create the schema and views separately and grant only SELECT, INSERT, and UPDATE. The full verification script requires the object-creation privileges above.

## Configure the connection

From the repository root:

```sh
cp .env.example .env
chmod 600 .env
```

If `.env` already exists, edit it rather than overwriting it. Set:

```dotenv
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=advertising_user
MYSQL_PASSWORD='REPLACE_WITH_YOUR_PROJECT_ACCOUNT_PASSWORD'
MYSQL_DATABASE=advertising_analytics
```

Use python-dotenv quoting for special characters. Existing environment variables take precedence over `.env`. The file is excluded by .gitignore; `.env.example` contains placeholders only.

## Execute and verify

```sh
.venv/bin/python scripts/verify_mysql.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
```

The verifier:

1. Executes `sql/01_create_tables.sql`.
2. Runs the transactional importer twice to verify repeatability.
3. Executes `sql/04_reporting_views.sql`.
4. Runs `sql/02_data_validation.sql` and `sql/03_kpi_analysis.sql`.
5. Compares overall KPIs and all 45 summary-view rows against independent Decimal calculations at absolute tolerance 1e-9.
6. Checks the 190-row detail view and seven NULL CPA values.

Successful runs write query results and server version to `reports/mysql_validation.json`. Review the command's exit status; a stored report describes its successful run and does not establish that a later run succeeded. DDL commits independently; completed imports persist if a later step fails. Existing incompatible tables are not automatically migrated.

The importer's `fetchwarnings` call and VALUES-based upsert use deprecated APIs on newer versions; the recorded MySQL 9.4.0 run succeeded. Compatibility with another server version requires rerunning the verifier.
