# Project audit — October 21, 2026

## Live MySQL verification — October 22, 2026: PASS

This result supersedes earlier NOT TESTED entries for local MySQL below; earlier sections remain historical records.

| Component | Status | Evidence | Issues | Required Action |
|---|---|---|---|---|
| Authenticated local connection | PASS | Project account connected to MySQL Community Server 9.4.0 using private environment configuration | Sandbox TCP attempt failed with error 2003/OS error 1; approved outside-sandbox retry succeeded | None for local connection |
| Schema/table execution | PASS | Existing 01_create_tables.sql executed successfully | Existing schema was created manually before verification; IF NOT EXISTS path was exercised | Fresh-database initialization and MySQL 8.x compatibility remain untested |
| Import and idempotency | PASS | Two committed imports, each comparing all 190 rows and every column against cleaned CSV | Connector emitted a fetchwarnings API deprecation warning | Optional future API modernization; no observed failure |
| SQL validation | PASS | 190 rows, 40 groups, five months; correct monthly counts; zero duplicate, invalid-count/cost, or inconsistent-KPI exception rows | None observed | None |
| Analytical queries | PASS | All nine analytical result sets executed, including LAG, RANK and optimization screens | None observed | None |
| Reporting views | PASS | 45 monthly/ad-group view rows matched independent Decimal calculations; detail view count 190 | None observed | None |
| Overall KPI reconciliation | PASS | Every overall measure/ratio matches CSV Decimal calculations within 1e-9 | None observed | None |
| Undefined ratios | PASS | Seven SQL NULL CPA values verified | None observed | None |
| Regression checks | PASS | All three unit tests pass after database execution; pip check reports no broken requirements | Current Python remains 3.9.6 | Recommended fresh Python 3.10+ reproduction remains separate |

Actual server results are saved in reports/mysql_validation.json, including version, validation output and all analytical query results. Verified totals: impressions 2,674,699; clicks 924,503; conversions 95,996; spend 635,372; revenue 561,960; CTR 0.3456474915495164; conversion rate 0.1038352498585727; CPC 0.6872579104664885; CPA 6.6187341139214134; ROAS 0.8844582386381521; profit/loss −73,412. No credential values were printed or committed. No cleaning pipeline or source records were changed.

The local MySQL portion is now verified. This does not certify execution against MySQL 8.x, an initially empty server, forced-error rollback behavior, or Tableau workbook/publication, which remain outside this successful run.

## MySQL follow-up — October 22, 2026

This section supersedes the October 21 environment/MySQL availability findings below. The earlier audit is retained as historical evidence.

| Component | Status | Evidence | Issues | Required Action |
|---|---|---|---|---|
| Installed MySQL discovery | PASS | macOS 15.7.3 arm64; `/usr/local/mysql/bin/mysql --version` and mysqld report 9.4.0; Oracle launch daemon and socket exist | Client absent from PATH; local version is 9.4, not target 8 | Use full client path; test 8.x compatibility separately if required |
| Server responsiveness | PASS | Outside-sandbox mysqladmin TCP probe received Access denied for root@localhost using password NO | This proves response, not authenticated access; mysqladmin exit 0 alone is not a database test | Authenticate using administrator/project account |
| Project Python MySQL dependencies | PASS | Installed mysql-connector-python 9.4.0 and python-dotenv 1.2.1 in existing .venv; pip check passes | Initial sandbox pip download failed DNS; approved outside-sandbox retry succeeded | No dependency action required |
| Private connection configuration | NOT TESTED | Created .env template mode 0600; existing .gitignore excludes it; .env.example preserved | Password remains replace_me, no working credentials configured | Complete account setup in reports/mysql_setup.md |
| Authenticated database connection | NOT TESTED | Root no-password probe was rejected; user requested administrator-login help | Administrator login/account creation remains manual | Try password-prompt login or existing Workbench connection; do not disclose passwords |
| Schema creation/import/live SQL/views/KPI comparisons | NOT TESTED | No authorized database session established | Cannot execute required server checks | Configure credentials and run verifier |
| Live verification workflow | NOT TESTED | Added scripts/verify_mysql.py; invocation exits 1 with configuration-required message before connecting | No server-backed verification or mysql_validation.json generated | Run after .env setup; review actual results |
| Regression tests and dry run | PASS | 3 unit tests pass; importer dry run validates 190 rows; pip check finds no broken dependencies | No live MySQL coverage in these tests | Repeat after live run |

No system software was installed, no root password was guessed/reset, and no existing server configuration or cleaning pipeline was modified. The first sandbox TCP probe returned error 1 (permission); the approved outside-sandbox probe reached the server and received an authentication denial. Dependencies required an approved network retry. Current blocker is administrator/project credentials, not server installation. User explicitly requested help with administrator login.

Next: run `/usr/local/mysql/bin/mysql --protocol=TCP --host=127.0.0.1 --port=3306 --user=root --password` locally and enter the existing MySQL administrator password at the prompt (not the macOS password unless deliberately configured identically). If unknown, check an existing Workbench connection or the password manager used during MySQL setup. A password reset requires a separate planned maintenance procedure; it was not performed. Account creation, scoped grants, private .env editing, and verifier instructions are in reports/mysql_setup.md. No MySQL completion PASS is claimed.

The local Python/data preparation layer passes the executed checks after fixes. The project is **partially complete**, not an end-to-end verified MySQL/Tableau deliverable. No live MySQL execution or Tableau dashboard verification was possible. Statuses below describe the final state; original failures and fixes are recorded separately.

| Component | Status | Evidence | Issues | Required Action |
|---|---|---|---|---|
| Repository inventory | PASS | Two production Python scripts, one notebook, four SQL files, two test/audit Python files; inventory below | No Git metadata | Initialize/publish only when ready |
| Cleaned data | PASS | 190 rows, 19 columns, 40 ad groups, five months; no duplicate primary keys | Seven NULL CPA values are expected | Preserve NULL semantics |
| Python reporting pipeline | PASS | reporting.py exits 0 and regenerates all exports | Validation uses assert and must run without Python -O | Follow documented command |
| Notebook execution | PASS | All 19 original code cells executed in order after option correction; isolated output equals existing CSV | Jupyter GUI/kernel lifecycle was not exercised | Optional interactive verification |
| Invalid-input handling | PASS | Three unit tests pass, including 15 invalid-input/duplicate subcases | This is selected-case testing, not an exhaustive fuzz test | Retain regression tests |
| Source integrity | PASS | SHA-256 comparison before/after final audit shows no raw, processed, notebook, or Tableau file changes during execution | Notebook was intentionally corrected before these hashes were captured | See audit_evidence.json |
| Independent KPIs | PASS | Decimal arithmetic from CSV strings; row and aggregate reconciliations | Minor binary float representation of sale_amount only | Use monetary formatting; no data correction needed |
| Tableau CSVs | PASS | Detail 190×19; monthly 5×13; ad-group 40×13; schemas, keys, totals, ratios reconcile | Summary exports cannot support both filters independently | Use detail source for interactive dashboard |
| Filter data behavior | PASS | 200 month/group combinations, including 10 absent combinations, reconcile | Actual Tableau filter actions not exercised | Verify workbook filters later |
| MySQL SQL static review | PASS | Schema, constraints, NULLIF, weighted KPIs, three views, LAG/RANK reviewed; decimal casts corrected | Static review does not establish runtime correctness | Execute on MySQL 8.0.16+ |
| MySQL import dry run | PASS | import_mysql.py --dry-run exits 0 with 190 validated records | Does not import connector or connect | Install requirements and configure database |
| Live MySQL schema/import/queries/views | NOT TESTED | No mysql client, connector, dotenv, .env, or MYSQL_* variables; local socket probe returned permission error (1) | No working authorized connection established; socket result does not prove server absence | Configure MySQL; run schema, import, views, validation, analysis |
| SQL vs Python/Tableau numeric comparison | NOT TESTED | No server query outputs exist | Cannot claim SQL output parity | Capture and compare live query/view results with independent totals |
| Environment readiness | FAIL | Python 3.9.6; pandas 2.3.3; NumPy 2.0.2; mysql-connector-python and python-dotenv missing | Current environment does not meet README Python 3.10+ recommendation or all declared packages | Create recommended environment and install requirements |
| Installed dependency consistency | PASS | python -m pip check: No broken requirements found | pip check does not verify requirements.txt is installed | Install declared dependencies |
| Clean-environment reproduction | NOT TESTED | Existing environment executed local checks successfully | No fresh environment/dependency installation attempted | Repeat README steps in Python 3.10+ |
| README/configuration review | PASS | Relative paths, environment example, .env ignore rule, correct SQL execution order; optional notebook steps added | View creator needs CREATE VIEW; documented | Follow README; do not execute SQL files merely in numerical order |
| Credential/path review | PASS | Reviewed project code/config/docs and notebook code; no embedded real credentials or executable machine-specific paths found | Notebook saved output cell 16 contains a historical local path; this is not a runtime dependency. Review is not a comprehensive secret-scanner guarantee | Optionally clear saved outputs before publication |
| Tableau build specification | PASS | tableau/dashboard_build_guide.md contains formulas, six visuals, filters, QA and publishing steps | Specification is not a workbook | Build and verify dashboard |
| Tableau workbook | NOT IMPLEMENTED | No .twb/.twbx files found; only CSVs and guide in tableau/ | No functional dashboard to test | Build workbook in Tableau |
| Tableau Public publication/screenshots | NOT IMPLEMENTED | README has explicit placeholders, no publication evidence or screenshots | No claimed verified public URL | Publish actual extract-backed workbook; verify signed out |
| Business analysis/resume | PASS | reports/business_insights.md and resume_bullets.md match observed totals and avoid claiming Tableau completion | Commission/currency/source license remain unconfirmed | Confirm primary dictionary and redistribution rights |

## Inventory and implementation assessment

- Python: `scripts/reporting.py`, `scripts/import_mysql.py`.
- Notebook: `notebooks/data_cleaning.ipynb` (19 code cells).
- SQL: `01_create_tables.sql`, `02_data_validation.sql`, `03_kpi_analysis.sql`, `04_reporting_views.sql` in sql/.
- Configuration: `.env.example`, `.gitignore`, `requirements.txt`; no actual `.env` present. No environment MYSQL_* names were configured (values were not printed).
- Source: `data/raw/final_shop_6modata.csv` (190×12); cleaned: `data/processed/advertising_campaigns_clean.csv` (190×19).
- Tableau exports: `tableau_campaign_month.csv`, `tableau_monthly_kpis.csv`, `tableau_ad_group_kpis.csv` under tableau/.
- Tests: `tests/test_reporting.py`; repeatable independent audit: `tests/audit_project.py`.
- Evidence/documentation: README.md, reports/validation.json, reports/audit_evidence.json, business_insights.md, progress.md, resume_bullets.md, tableau/dashboard_build_guide.md, this audit.
- Steps 1–2: local data preparation verified after notebook fix. Step 3: scripts implemented, database execution pending. Step 4: exports verified. Step 5: instructions only; workbook/publication missing. Steps 6–7: analysis and portfolio documentation prepared; dashboard evidence and GitHub publication missing.

## Tests executed and actual results

`tests/audit_project.py` runs these commands in the repository root:

```sh
.venv/bin/python scripts/reporting.py
.venv/bin/python scripts/import_mysql.py --dry-run
.venv/bin/python -m unittest discover -s tests -v
```

All exit 0 on final run. Unit tests: **3 passed** (source/output reconciliation, weighted ratios/zero denominators, invalid data rejection). Invalid cases: negative impressions/clicks/conversions/cost/revenue; missing revenue; infinite cost; missing/blank ad group; fractional impressions; clicks exceeding impressions; non-month-start/malformed dates; missing defined CTR; duplicate keys. Existing seven undefined CPA values are accepted; synthetic zero-denominator metrics are NULL, not zero.

The audit executes each notebook code cell in a shared Python namespace with a no-op display callback and captured stdout, using a temporary project copy. This tests its calculations and export, not notebook rendering or an actual Jupyter kernel. All 19 cells complete and the resulting CSV matches the repository export. No source files in the real data directories are overwritten by notebook execution.

The audit independently uses the standard-library csv and Decimal modules, not production aggregation helpers, to calculate KPIs. It checks all 190 row metrics, all 45 summary rows, complete detail-table equality, additive totals at both summary grains, expected columns, unique keys, and 200 combined date/group selections. Monthly reporting dates and group coverage are validated by the pipeline. All checks pass at absolute tolerance 1e-9 (1e-8 for float representation of aggregate measure sums).

All 200 combinations include ten absent observations; empty selections remain empty and are not converted into invented records. No joins are used in exports, and no inflated totals were found. The full detail source supports date and ad-group filters; monthly-only and group-only files do not both support these filters and must not be joined to detail for the interactive dashboard.

`pip check` passes for installed packages; connector and dotenv absence was checked separately. MySQL client lookup and configuration inspection were performed. The localhost:3306 socket probe was denied by the environment; it is not a successful connection test. No live importer invocation, MySQL DDL, SELECT, window query, or view was executed.

## Independent KPI comparison

| KPI | Independent value | Python/report and Tableau exports | Live SQL |
|---|---:|---|---|
| Impressions | 2,674,699 | Match | NOT TESTED |
| Clicks | 924,503 | Match | NOT TESTED |
| Conversions | 95,996 | Match | NOT TESTED |
| Spend | 635,372 | Match | NOT TESTED |
| Revenue | 561,960 | Match | NOT TESTED |
| CTR | 0.3456474915495164 (34.564749%) | Match | NOT TESTED |
| Conversion rate | 0.1038352498585727 (10.383525%) | Match | NOT TESTED |
| CPC | 0.6872579104664885 | Match | NOT TESTED |
| CPA | 6.6187341139214134 | Match | NOT TESTED |
| ROAS | 0.8844582386381521× | Match | NOT TESTED |
| Profit/loss | −73,412 | Match | NOT TESTED |
| Underlying sale amount (separate from revenue) | 12,049,074.31 | Match within float tolerance | NOT TESTED |

Ratios use summed numerators and denominators. Overall values are reconciled from additive measures in each summary export, never by averaging exported ratios. Exact Decimal results and hashes are retained in reports/audit_evidence.json. Monthly record counts are July 38, August 38, September 38, October 37, November 39. No negative counts, cost, or revenue, missing required measures, nonfinite required measures, invalid dates, or excessive clicks occur in the existing cleaned data.

Supplied-vs-recalculated metric discrepancies remain documented source-quality findings: maximum absolute differences 0.005 CTR, 0.25 conversion rate, 0.286667 CPC, and 0.499 profit/loss. These are not discrepancies between the verified recalculated outputs. sale_amount's binary float total is 12049074.309999999 versus exact 12049074.31; difference is below tolerance.

## Issues fixed and rerun results

1. **Notebook runtime failure:** initial direct execution stopped in cell 0 with pandas OptionError for `display.max_width`. Changed that option only to `display.width`. All 19 cells subsequently ran and produced an identical cleaned CSV. Saved notebook outputs were not regenerated.
2. **SQL ratio precision:** static review found integer/low-scale division could round ratios before comparison at 1e-9 tolerance. Added `CAST(... AS DECIMAL(30,12))` to numerator expressions in analysis, validation, and reporting views. This is supported by MySQL's [precision arithmetic documentation](https://dev.mysql.com/doc/refman/8.0/en/precision-math-expressions.html). Server execution remains NOT TESTED; Python tests do not verify this SQL fix.
3. **Negative revenue guard:** added revenue to nonnegative cleaned-input checks. New mutation tests verify rejection along with missing/invalid values. All three unit tests pass.
4. **Reproduction documentation gaps:** added optional notebook installation/launch steps, assertion-mode requirement, current environment mismatch, audit command, and CREATE VIEW privilege requirement to README. No packages were installed or claimed installed.

Raw data, processed data, and all three Tableau exports were unchanged by the audit regeneration (SHA-256 verified). No metric definitions or source records were changed.

## Remaining manual steps and limits

1. Create Python 3.10+ environment, install requirements, and repeat checks; optionally install notebook/ipykernel for interactive use. A requirements installation and actual GUI notebook run remain untested.
2. Configure an authorized MySQL 8.0.16+ server/account; copy .env.example to .env and populate credentials. Execute schema first, then real importer, then reporting views, validation, and analysis. Use an account with view-creation privileges for the views.
3. Confirm table count 190, groups 40, months 5 and monthly counts; retain SQL validation output. Compare all SQL summary rows and KPIs to audit_evidence.json/Tableau exports within 1e-9. Test import reruns/rollback, SQL NULL handling, and actual views on server. No database-level tests have passed yet.
4. Build the Tableau workbook from detail data, verify sheets, filters, weighted formulas, top/bottom ranking, and empty selections in the GUI. Publish an embedded extract to Tableau Public, verify signed out, and add real URL/screenshots.
5. Confirm source license, commission interpretation, and currency before public data publication. Initialize/review Git and publish to the intended GitHub destination.

Additional implementation limits: production validators currently use assert (disabled with -O); README now explicitly requires normal execution. MySQL upsert uses VALUES(column), which is deprecated on recent MySQL 8 versions and should be exercised on the chosen server; no unsupported runtime behavior is claimed. Database scripts do not automatically migrate incompatible existing tables. Audit credential review is scoped to project files, not account/server security. Existing notebook outputs may be stale even though its corrected code and exported data now reconcile.
