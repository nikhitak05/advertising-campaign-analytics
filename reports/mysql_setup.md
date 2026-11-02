# Local MySQL setup — macOS Apple Silicon

## Detected on October 22, 2026

macOS 15.7.3, arm64. Oracle MySQL Community Server/client **9.4.0** are installed under `/usr/local/mysql-9.4.0-macos15-arm64`, with `/usr/local/mysql` pointing to that installation. A launch daemon is configured at `/Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist`. TCP port 3306 responded with an authentication error outside the sandbox. **No server installation or restart is needed.** MySQL 8-specific compatibility still requires testing against an 8.x server; the available local server is 9.4.

The client is not on PATH. Use its full path below. No system software was installed. Project packages mysql-connector-python 9.4.0 and python-dotenv 1.2.1 were installed in the existing .venv.

## Required administrator action

From a local terminal, open the existing server using your administrator password at the interactive prompt:

```sh
MYSQL_HISTFILE=/dev/null /usr/local/mysql/bin/mysql --protocol=TCP --host=127.0.0.1 --port=3306 --user=root --password
```

If you do not know the administrator password, use your existing MySQL Workbench administrator connection or recover it using Oracle's documented procedure. Do not reinstall, reinitialize the data directory, or reset passwords blindly. Tell the assistant you need administrator-login help; do not paste a password into chat.

Run these statements in that interactive client, replacing the example password with a unique strong password locally. The account has privileges only on this project database and only from the local host:

```sql
CREATE USER 'advertising_user'@'localhost' IDENTIFIED BY 'REPLACE_WITH_A_UNIQUE_STRONG_PASSWORD';
GRANT SELECT, INSERT, UPDATE, CREATE, CREATE VIEW, SHOW VIEW, DROP
ON advertising_analytics.* TO 'advertising_user'@'localhost';
```

CREATE allows the project schema/table to be initialized; DROP is needed for replacing existing views. No script drops a table. Do not rerun CREATE USER if the account already exists; inspect its existing configuration instead. An administrator may instead create the schema and views, then grant only SELECT/INSERT/UPDATE to the importer; verification's object-creation steps will then need the administrator account.

A private `.env` with mode 0600 has been created from `.env.example`. Open it in your editor and replace `MYSQL_PASSWORD=replace_me` with the same project-account password. For special characters, use python-dotenv quoting, e.g. single quotes around values containing # or spaces; escape quotes as needed. Keep host 127.0.0.1, port 3306, database advertising_analytics, and user advertising_user. `.env` is ignored by the existing .gitignore. No credentials belong in source files, shell command arguments, reports, or chat.

## Execute and verify

From the repository root:

```sh
.venv/bin/python scripts/verify_mysql.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
```

The verifier connects with environment variables (or .env defaults), runs the existing schema, imports all rows twice to check idempotency, creates reporting views, executes all validation and analytical SQL statements, and compares all overall KPIs and 45 summary rows to independently calculated Decimal CSV totals at 1e-9 tolerance. It also checks 190 detail-view rows and seven NULL CPA values. The importer compares every table column on both imports. Successful runs write actual server version and query results to reports/mysql_validation.json. No success report is written before checks complete. DDL commits independently; an interrupted run may leave created schema/views, and completed imports persist.

Network access from the assistant sandbox may require a separate execution approval. A missing password is a separate issue from sandbox network access.

If the server later stops, use the existing Oracle installation's service controls; do not install a second server. Oracle documents its macOS [launch daemon](https://dev.mysql.com/doc/refman/9.4/en/macos-installation-launchd.html). Installation instructions are unnecessary for this machine because the server is already present and responding.
