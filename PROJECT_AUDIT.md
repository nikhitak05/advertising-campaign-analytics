# Validation summary

This summary records the tested scope of the data pipeline, MySQL reporting layer, and Tableau dashboard. Machine-readable results are retained under reports/. Tableau checks below are based on the authoring and published screenshots reviewed during dashboard development; the hosted dashboard could not be loaded by the automated web reader during the documentation review.

| Component | Status | Evidence | Issues | Required Action |
|---|---|---|---|---|
| Cleaning and source reconciliation | PASS | All 19 notebook code cells executed in an isolated copy; exported CSV matches the existing cleaned data | Notebook uses notebooks/ as working directory | Follow README instructions |
| Data integrity | PASS | 190 rows; 40 groups; five months; unique keys; valid counts, amounts and dates | Ten group/month combinations absent | Treat absence as missing observations, not zeros |
| Regression tests | PASS | Three tests cover reconciliation, weighted/undefined ratios, and invalid-input rejection | Validation uses assertions | Run without Python -O |
| Independent CSV audit | PASS | Decimal calculations reconcile 190 detail rows, 45 summary rows and 200 filter combinations | Tiny floating-point sale-amount artifacts within tolerance | None |
| MySQL schema and imports | PASS | MySQL 9.4.0; two imports each verified every field of all 190 rows | Fresh-server initialization and 8.x compatibility not separately tested | Rerun verifier on a new deployment |
| MySQL validation and analysis | PASS | Zero validation exceptions; nine analytical result sets; correct monthly counts | Deprecated importer APIs emit a warning | Monitor compatibility when upgrading |
| MySQL reporting views and KPIs | PASS | All 45 summary-view rows and overall KPIs match independent CSV calculations at 1e-9; seven NULL CPA values | None observed | None |
| Tableau exports | PASS | Detail 190 rows; monthly 5; ad-group 40; matching totals and weighted ratios | Summary grains must not be joined to detail | Use detail CSV for interactive reporting |
| Tableau dashboard | PASS | Published dashboard screenshots show KPI cards, six charts, insights and filters; full-period, October, single-group and combined-filter results match | Current hosted view not independently exercised by an automated browser | Verify final published changes interactively |
| Tableau local artifacts | NOT IMPLEMENTED | Published URL is provided in README; no .twb/.twbx or screenshots exist in repository | Repository does not include an offline dashboard copy | Optional download/screenshots |
| Fresh Python environment | NOT TESTED | Existing environment: Python 3.9.6, pandas 2.3.3, NumPy 2.0.2 | New Python 3.10+ setup not separately executed | Repeat README steps for a new environment |
| Source license/currency dictionary | NOT TESTED | Source is attributed; revenue and sale amount remain separate | Currency, commission interpretation and redistribution terms not independently confirmed | Consult original dataset documentation |

## Verification commands

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tests/audit_project.py
.venv/bin/python scripts/verify_mysql.py
.venv/bin/python -m pip check
```

The independent audit runs reporting, importer dry run, regression tests, isolated notebook execution, and Decimal reconciliation. The MySQL verifier requires an authenticated running server and executes the existing schema, imports twice, creates views, and runs all validation and analysis SQL. A saved successful report describes that recorded run, not the current state of a subsequently changed server.

## Recorded evidence

- [Python validation](reports/validation.json): counts, totals, missing ratios and supplied-metric discrepancies.
- [Independent audit](reports/audit_evidence.json): exact totals, filter-comparison counts and SHA-256 hashes.
- [MySQL verification](reports/mysql_validation.json): successful live run on October 22, 2026, server version 9.4.0, query results and summary reconciliation.
- [Tableau implementation and QA](tableau/dashboard_build_guide.md): formulas and observed filter test cases.

Verified totals are 2,674,699 impressions, 924,503 clicks, 95,996 conversions, 635,372 spend, 561,960 revenue, and −73,412 advertising profit/loss. Weighted CTR is 34.564749%, conversion rate 10.383525%, CPC 0.687258, CPA 6.618734, and ROAS 0.884458×.

Monthly row counts are July 38, August 38, September 38, October 37, and November 39. Seven records have zero conversions and undefined CPA. No duplicate keys, negative counts/cost/revenue, invalid reporting dates, or clicks exceeding impressions were found.

The notebook's invalid pandas display option was corrected, negative-revenue validation was added, and SQL numerator casts preserve precision before ratio comparison. Source records and metric definitions were preserved. Forced-error transaction rollback and MySQL 8.x runtime behavior were not separately exercised.
