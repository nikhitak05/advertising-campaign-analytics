# Advertising Campaign Performance Dashboard

An end-to-end analysis of paid-search advertising performance using Python, SQL, MySQL, and Tableau. The project evaluates campaign profitability, compares engagement and conversion efficiency, and identifies opportunities for controlled budget optimization.

**[Explore the interactive Tableau dashboard](https://public.tableau.com/app/profile/nikhita.karthikesan/viz/AdvertisingCampaignAnalytics_17927052239570/Dashboard1)**

## Business question

Which ad groups generate the strongest returns, which underperform, and where should a business investigate changes to its advertising budget?

## Results at a glance

The dataset covers **190 ad-group/month observations**, **40 ad groups**, and **July–November 2021**.

| Metric | Result |
|---|---:|
| Impressions | 2,674,699 |
| Clicks | 924,503 |
| Conversions | 95,996 |
| Advertising spend | 635,372 |
| Revenue | 561,960 |
| Advertising profit / loss | −73,412 |
| Click-through rate | 34.56% |
| Conversion rate | 10.38% |
| Cost per acquisition | 6.62 |
| Return on ad spend | 0.884× |

Monetary values use source currency units. Profit means revenue minus advertising cost, excluding overhead and other business costs.

- **Overall advertising was unprofitable:** revenue fell short of spend by 73,412.
- **October was the only profitable month:** profit was 1,047, with ROAS of 1.013×.
- **The largest-loss group lost 15,022:** `Shop - 1:1 - Mob - [shop coupon]` had high CTR but below-average conversion rate, making tracking and search-intent alignment useful areas to investigate.
- **High ROAS does not establish scalability:** the highest-profit group earned 116 on just 44 spend and 24 conversions. Its small seasonal sample does not justify a large budget increase.

Read the [business analysis](reports/business_insights.md) for campaign comparisons, recommendations, and limitations.

## Dashboard

The Tableau dashboard includes six KPI cards, monthly spend and revenue, monthly ROAS, profitable and loss-making ad-group rankings, an engagement/conversion scatter plot, and a volume-screened ROAS comparison.

Reporting-period and ad-group filters update the charts and weighted KPIs. Profit is green and loss is red, with signed values retained. The business insights section explicitly describes the full period and remains static when filters change.

All interactive sheets use the campaign-month detail export. The ROAS comparison includes only groups with at least 1,000 spend **within the active selection**; this is an analytical screen, not a statistical confidence threshold. Missing ad-group/month combinations are not filled with invented zeros.

See the [Tableau implementation guide](tableau/dashboard_build_guide.md) for formulas and validation examples. The published dashboard uses CSV-based data and does not require access to the local MySQL server.

## Data source and quality

Source: [Shopping Mall Paid Search Campaign Dataset on Kaggle](https://www.kaggle.com/datasets/marceaxl82/shopping-mall-paid-search-campaign-dataset).

The raw file contains 190 rows and 12 columns. Cleaning preserves supplied KPIs under `source_*` names and recalculates reporting metrics from the underlying counts and amounts. The resulting dataset contains 19 columns.

Validation confirms unique ad-group/month keys, valid reporting dates, nonnegative counts/cost/revenue, and clicks no greater than impressions. Seven observations have zero conversions, so CPA is undefined and retained as NULL.

Supplied ratios differ from recalculated metrics: maximum absolute differences are 0.005 for CTR, 0.25 for conversion rate, 0.286667 for CPC, and 0.499 for profit/loss. Reporting consistently uses recalculated metrics.

Revenue and Sale Amount are distinct fields; ROAS uses **Revenue**. Revenue's commission-income interpretation and the currency have not been independently confirmed against a primary data dictionary. The raw file supplies month names without a year; 2021 is consistent with the [dataset author's description](https://www.reddit.com/r/datascienceproject/comments/xtjliu). Dataset licensing and redistribution terms remain governed by the original source; no independent dataset license is asserted here.

## Architecture

```text
Raw CSV → Python cleaning notebook → Validated campaign-month CSV
                                      ├── MySQL fact table → SQL reporting views
                                      └── Tableau exports → Tableau Public dashboard
```

**Tools:** Python, pandas, NumPy, Jupyter, MySQL, SQL, Tableau Public.

The database contains one fact table, `advertising_analytics.campaign_performance`, at ad-group/month grain. Its composite primary key is `(ad_group, reporting_month)`. Counts use integers, monetary amounts and ratios use DECIMAL, and reporting months use DATE. Undefined ratios permit NULL.

Three views expose monthly KPIs, ad-group KPIs, and campaign-month detail. SQL analysis uses weighted aggregation, `NULLIF`, `RANK`, and `LAG` for rankings and monthly comparisons. SQL targets MySQL 8.0.16+ and was executed and verified on **MySQL 9.4.0**; an 8.x server was not separately tested.

## KPI definitions

| KPI | Calculation |
|---|---|
| CTR | SUM(clicks) / SUM(impressions) |
| Conversion rate | SUM(conversions) / SUM(clicks) |
| CPC | SUM(cost) / SUM(clicks) |
| CPA | SUM(cost) / SUM(conversions) |
| ROAS | SUM(revenue) / SUM(cost) |
| Advertising profit / loss | SUM(revenue) − SUM(cost) |

Rates are displayed as percentages, and ROAS as a multiplier. Ratios are calculated from aggregated totals, never by averaging row-level ratios. Zero denominators produce NULL.

## Repository structure

```text
data/raw/                         Source CSV
data/processed/                   Cleaned campaign-month data
notebooks/data_cleaning.ipynb      Inspection and cleaning workflow
scripts/reporting.py              Validation and Tableau exports
scripts/import_mysql.py           Transactional MySQL import
scripts/verify_mysql.py            Live SQL and KPI verification
sql/                              Schema, validation, analysis, and views
tableau/                          Tableau CSVs and implementation guide
reports/                          Business analysis and validation evidence
tests/                            Regression tests and independent audit
PROJECT_AUDIT.md                   Validation scope and results
```

## Reproduce the analysis

Use Python 3.10+ for a new environment. The recorded validation environment used Python 3.9.6, pandas 2.3.3, and NumPy 2.0.2; a fresh environment has not been separately verified.

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/reporting.py
.venv/bin/python scripts/import_mysql.py --dry-run
.venv/bin/python -m unittest discover -s tests -v
```

The reporting script validates the existing cleaned data against the raw-data transformation and writes:

| Export | Grain | Rows |
|---|---|---:|
| tableau/tableau_campaign_month.csv | Ad group × reporting month | 190 |
| tableau/tableau_monthly_kpis.csv | Reporting month | 5 |
| tableau/tableau_ad_group_kpis.csv | Ad group | 40 |

Do not join these different grains in Tableau: use the detail file for interactive reporting and summary files for reconciliation.

To reproduce the cleaning notebook interactively, install `notebook` and `ipykernel`, then launch Jupyter from `notebooks/` using the project environment. The notebook expects that working directory. Command-line scripts resolve paths relative to the repository.

For an independent audit, including notebook execution in an isolated temporary copy:

```sh
.venv/bin/python tests/audit_project.py
```

This reconciles 190 detail rows, 45 summary rows, and 200 month/group selections using Decimal arithmetic. Run validation without Python's `-O` option because the current checks use assertions.

### MySQL

Follow [MySQL setup](reports/mysql_setup.md) to create a scoped account and configure `.env` from `.env.example`. Credentials stay outside version control.

With the server running and credentials configured:

```sh
.venv/bin/python scripts/verify_mysql.py
```

The verifier executes the schema, imports twice, creates views, runs all validation/analytical queries, and compares server results to independent CSV calculations. Alternatively, execute the SQL manually in this order: schema → Python import → reporting views → validation → KPI analysis.

The importer upserts matching keys in one transaction, verifies every stored field, and rolls back on a mismatch. It does not delete unrelated records. DDL operations commit independently, and existing incompatible tables require manual schema review.

## Validation and limitations

The [validation summary](PROJECT_AUDIT.md) records the scope and evidence. Live MySQL verification confirmed 190 rows, 40 groups, five months, zero validation exceptions, nine analytical result sets, and 45 matching summary-view rows. Tableau filter behavior was checked through full-period, October-only, single-group, and combined-filter views.

Only five months of observational data are available, with unequal group coverage and no attribution window, customer lifetime value, or incremental-return measurement. Historical ROAS does not establish how additional budget would perform. Recommendations are candidates for investigation and controlled experiments, not causal conclusions.
