# Advertising Campaign Performance Dashboard

A portfolio analytics project investigating which paid-search ad groups return advertising spend and where controlled optimization experiments may help. Built for ads and sponsorships analyst applications; this retail paid-search dataset does not measure sponsorship or game advertising performance.

**Current status:** Python validation, MySQL reporting scripts, Tableau CSV exports, and analysis are complete locally. Live MySQL 9.4.0 imports, SQL queries, reporting views, and KPI reconciliation are verified; the Tableau workbook/publication remains pending. See [progress](reports/progress.md).

## Verified findings

Across 190 observations, 40 ad groups, and five months: spend **635,372**, revenue **561,960**, advertising loss **73,412**, CTR **34.56%**, conversion rate **10.38%**, and ROAS **0.884×**. October alone was profitable. The highest group profit came from a group spending only 44, so it is weak evidence for scaling. See [business insights](reports/business_insights.md) for campaign comparisons and limitations.

## Source and definitions

[Kaggle: Shopping Mall Paid Search Campaign Dataset](https://www.kaggle.com/datasets/marceaxl82/shopping-mall-paid-search-campaign-dataset). 

The [source author's sharing post](https://www.reddit.com/r/datascienceproject/comments/xtjliu) describes a real anonymized US shopping-mall paid-search campaign in 2021. The raw file has month names but no year; the existing notebook assigns 2021, consistent with that post. The Kaggle page's primary dictionary was not retrievable during this work.

Revenue and sale_amount remain separate. The project interprets revenue as commission income and sale_amount as underlying sales, but this interpretation and currency require primary dictionary confirmation. ROAS always uses the source Revenue field, never Sale Amount. Profit means revenue less advertising cost, before overhead. Check source licensing before redistributing data.

## Workflow and model

Python, pandas, NumPy, MySQL 8, SQL, Jupyter, and prepared Tableau Public inputs. Original work remains in `notebooks/data_cleaning.ipynb`; it reads the 12-column raw CSV, retains source ratios, recalculates metrics, and creates the 19-column cleaned CSV. `scripts/reporting.py` independently reconstructs that logic and compares every field. The notebook assumes its working directory is notebooks/; the scripts work from any directory.

The reporting model is one fact table, `advertising_analytics.campaign_performance`, at ad-group/month grain. Primary key: `(ad_group, reporting_month)`; binary text collation preserves exact source names. Text uses VARCHAR, month uses DATE, counts use BIGINT UNSIGNED, and monetary/ratio fields use DECIMAL. Undefined ratios permit NULL. Dates represent month starts. The 190 observations cover 190 of 200 possible combinations; absent combinations are not fabricated zeros. Two aggregate views expose month and ad-group grains, and one detail view supports exports.

| KPI | Definition |
|---|---|
| Impressions, clicks, conversions, spend, revenue | SUM of corresponding raw measure |
| CTR | SUM(clicks) / SUM(impressions) |
| Conversion rate | SUM(conversions) / SUM(clicks) |
| CPC | SUM(cost) / SUM(clicks) |
| CPA | SUM(cost) / SUM(conversions) |
| ROAS | SUM(revenue) / SUM(cost) |
| Ad profit/loss | SUM(revenue) − SUM(cost) |

SQL uses NULLIF for zero denominators. Rates are fractions displayed as percentages; ROAS is a multiplier. Never average row percentages. Seven rows have undefined CPA. Maximum supplied/recalculated differences are 0.005 CTR, 0.25 conversion rate, 0.286667 CPC, and 0.499 profit. Source KPIs are retained for audit only.

## Reproduce locally

From the repository root, with Python 3.10+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/reporting.py
.venv/bin/python scripts/import_mysql.py --dry-run
.venv/bin/python -m unittest discover -s tests -v
```

Exports: `tableau/tableau_campaign_month.csv` (190 rows), `tableau/tableau_monthly_kpis.csv` (5), and `tableau/tableau_ad_group_kpis.csv` (40). Local checks and totals are recorded in [validation.json](reports/validation.json). CSV floating-point artifacts below a cent can appear in aggregate sale amount; MySQL stores monetary data in fixed-point DECIMAL.

For MySQL 8.0.16+ (CHECK enforcement), execute `sql/01_create_tables.sql` in Workbench with a schema-creation account. Create a separate local account with SELECT/INSERT/UPDATE privileges on this database. Copy `.env.example` to `.env` and set credentials; never commit `.env`. Then run:

```sh
.venv/bin/python scripts/import_mysql.py
```

The importer validates CSV first, maps missing ratios to SQL NULL, upserts matching keys in one transaction, checks every stored column against the CSV, and commits only if all 190 rows match. Existing unrelated rows cause rollback rather than deletion. No passwords are embedded. Schema creation and view creation are separate DDL operations, not part of this transaction. Existing incompatible schemas must be reviewed manually; CREATE IF NOT EXISTS does not migrate tables.

In Workbench run `sql/04_reporting_views.sql`, then `sql/02_data_validation.sql` and `sql/03_kpi_analysis.sql`. Validation expects monthly counts 38/38/38/37/39 and totals matching validation.json. Analysis includes profit/revenue rankings, volume-screened efficiency comparisons, engagement/conversion screening, and LAG month-over-month changes. The default 1,000 spend screen is an explicit analyst choice, not statistical significance.

No MySQL client/server or connector was available during implementation: dry run passed, but no database import, SQL execution, or view parity has been claimed. After executing on MySQL, retain results in reports/ and reconcile view totals to the exported summaries. Tableau exports are derived directly from the validated CSV and do not depend on a live server.

## Tableau dashboard

Use the detail CSV for all interactive sheets. Do not join different aggregate grains. The planned dashboard includes six KPI cards, spend vs revenue, monthly ROAS, best/worst groups by profit, a CTR/conversion scatter plot, efficiency comparison, month/group filters, and evidence-based recommendations.

Follow [build guide and calculated fields](tableau/dashboard_build_guide.md). This includes formatting, layouts, filter/ranking behavior, QA totals, and publication steps using embedded extracts.

Dashboard URL: pending actual Tableau Public publication.

Screenshots: pending actual workbook creation; add images under images/ after verification.

[Resume bullets](reports/resume_bullets.md) describe verified work without claiming Tableau construction. No GitHub remote was supplied and this folder was not an initialized Git repository; review dataset licensing and staged files before initializing and publishing to your chosen repository.

## Audit and notebook reproduction

See [PROJECT_AUDIT.md](PROJECT_AUDIT.md) for tested scope and outstanding work. Run `.venv/bin/python tests/audit_project.py` to execute the notebook code in an isolated copy, independently reconcile Decimal KPIs and all exports, test 200 month/group selections, and write `reports/audit_evidence.json`. It does not connect to MySQL. Run Python without `-O`; current validation uses assertions.

For interactive notebook work, install Jupyter separately (`.venv/bin/python -m pip install notebook ipykernel`), launch `.venv/bin/python -m notebook` from `notebooks/`, and select the project environment. Jupyter is optional for the command-line pipeline. The audited existing environment uses Python 3.9.6; a fresh Python 3.10+ environment and full dependency installation have not been verified here. The existing environment is missing mysql-connector-python and python-dotenv; install requirements before attempting a real import. The account used to create reporting views also needs CREATE VIEW and source-table SELECT privileges.

## Verified local MySQL execution — October 22, 2026

The earlier implementation-time availability notes above are historical. MySQL 9.4.0 is installed and running locally. Both database dependencies are now installed. `scripts/verify_mysql.py` completed successfully: two imports verified all 190 records, all SQL scripts executed, nine analytical result sets returned, all 45 summary-view rows reconciled to independent CSV totals, and seven NULL CPA values were confirmed. See [server evidence](reports/mysql_validation.json) and the latest [audit](PROJECT_AUDIT.md). All three regression tests and pip check pass. MySQL 8.x compatibility and fresh-server initialization have not been separately executed.
