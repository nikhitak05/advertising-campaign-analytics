# Tableau dashboard implementation

[View the published dashboard](https://public.tableau.com/app/profile/nikhita.karthikesan/viz/AdvertisingCampaignAnalytics_17927052239570/Dashboard1)

## Data source

Use `tableau_campaign_month.csv` as the single source for all interactive sheets. Set reporting_month to Date, counts to whole numbers, and monetary measures to decimals. Hide `source_*` fields from reporting. Missing CPA values represent undefined ratios, not zero cost.

The monthly and ad-group CSVs are independent summary datasets for reconciliation. Do not join them to the detail table: different grains can duplicate measures and interfere with filtering.

## Calculated fields

Use the field names as displayed in Tableau. These formulas use its automatically capitalized names.

**Weighted CTR**

```text
IF SUM([Impressions]) = 0 THEN NULL
ELSE SUM([Clicks]) / SUM([Impressions]) END
```

**Weighted Conversion Rate**

```text
IF SUM([Clicks]) = 0 THEN NULL
ELSE SUM([Conversions]) / SUM([Clicks]) END
```

**Weighted CPC**

```text
IF SUM([Clicks]) = 0 THEN NULL
ELSE SUM([Cost]) / SUM([Clicks]) END
```

**Weighted CPA**

```text
IF SUM([Conversions]) = 0 THEN NULL
ELSE SUM([Cost]) / SUM([Conversions]) END
```

**Weighted ROAS**

```text
IF SUM([Cost]) = 0 THEN NULL
ELSE SUM([Revenue]) / SUM([Cost]) END
```

**Ad Profit / Loss**

```text
SUM([Revenue]) - SUM([Cost])
```

**Reporting Period** — a discrete filter that preserves year and month

```text
STR(YEAR([Reporting Month])) + "-" +
RIGHT("0" + STR(MONTH([Reporting Month])), 2)
```

**Profit Status** — for the profit/loss KPI color

```text
IF SUM([Revenue]) - SUM([Cost]) < 0 THEN "Loss"
ELSEIF SUM([Revenue]) - SUM([Cost]) > 0 THEN "Profit"
ELSE "Break-even" END
```

Format rates as percentages, ROAS as a multiplier, and monetary figures without an unverified currency symbol. Never average imported row ratios. Use Profit Status on Color for the KPI; green indicates profit and red loss. Keep label font color inherited from the mark rather than manually overriding it. The scatter plot uses a diverging red/green profit scale centered on zero; retain numerical tooltips for accessibility.

## Dashboard sheets

| Sheet | Configuration |
|---|---|
| Six KPI cards | SUM(Cost), SUM(Revenue), SUM(Conversions), Weighted CTR, Weighted ROAS, Ad Profit / Loss on Text; empty Rows/Columns |
| Monthly Spend vs Revenue | Continuous month on Columns; SUM(Cost) and SUM(Revenue) in Measure Values on Rows; Measure Names on Color; lines |
| Monthly ROAS | Continuous month, Weighted ROAS line, reference line at 1× |
| Top Ad Groups by Profit | Ad Group rows; profit bars; positive profit only; descending sort |
| Largest Ad Group Losses | Ad Group rows; profit bars; negative profit only; ascending sort; scrollable |
| Engagement vs Conversion | Weighted CTR x; Weighted Conversion Rate y; Ad Group on Detail; SUM(Cost) on Size; profit on Color |
| Ad Group ROAS — Spend ≥ 1,000 | Ad Group rows; Weighted ROAS bars descending; SUM(Cost) filter at least 1,000; reference line at 1× |

The minimum-spend screen is limited to the efficiency sheet and applies within the selected dates/groups. It is not a confidence threshold. Full-period data contain five profitable groups and 35 loss-making groups; rankings show the qualifying groups rather than a fixed Top N set. If adding Top N later, validate that ranking responds to the active filters.

## Layout and filters

The desktop dashboard uses a 1440×1500 canvas, with a KPI row, three pairs of charts, and a business insights/footer section. Profit is green, loss red, and spend/revenue have distinct blue/orange lines.

Use Reporting Period and Ad Group as multiple-value dropdown filters. Apply each to all worksheets using the data source. Remove obsolete duplicate date filters rather than leaving hidden restrictions. Keep both filters set to All for the published default view.

Display full ad-group names in tooltips, along with spend, conversions, and profit/ROAS as applicable. Use Fit Width for long group lists and Entire View for KPI cards and the scatter plot. Static business insights must explicitly state that they describe the full July–November portfolio and do not change with filters.

Check device layouts before publishing. A phone-specific layout can stack KPI cards even when the Default layout is horizontal. Verify the intended Default/desktop layout in the published browser view as well as in the authoring application.

## Validation cases

| Selection | Expected results |
|---|---|
| All months and groups | Spend 635,372; revenue 561,960; conversions 95,996; CTR 34.56%; ROAS 0.884×; profit −73,412; scatter 40 marks |
| October, all groups | Spend 78,256; revenue 79,303; conversions 13,312; CTR 35.86%; ROAS 1.013×; profit 1,047 |
| All months, Exact/Mob Black Friday/Cyber Monday group | Spend 44; revenue 160; conversions 24; CTR 7.26%; ROAS 3.636×; profit 116 |
| November, same group | Same figures; one scatter mark; no loss bars; efficiency chart empty because spend is below 1,000 |

The group above is `Shop - Exact - Mob - Black Friday/Cyber Monday`. Single-month line charts naturally show points. Empty filtered charts must not manufacture zero-value records. A zero-conversion selection should leave CPA blank.

## Publication

Publish CSV-based data/extracts so viewers need no MySQL connection. Reset filters and clear selected marks before saving. After changes, overwrite the existing published workbook and verify the desktop layout, dropdown filters, tooltips, and KPI totals in the browser. If available, download a packaged workbook for local versioning. No local workbook or screenshots are currently included in this repository.

Source attribution and metric definitions belong in the footer. Dataset redistribution remains subject to the original source terms.
