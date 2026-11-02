# Advertising Campaign Performance Dashboard

Status: data and build specification prepared; no Tableau workbook or publication exists yet.

Use `tableau_campaign_month.csv` as the single dashboard data source so both filters operate consistently. Set reporting_month to Date; impressions, clicks, and conversions to whole numbers; monetary measures to decimals. All measures are additive except ratios. Keep source_* fields hidden from report authors. Empty CPA values are NULL, not zero.

The monthly (5 rows) and ad-group (40 rows) exports are independent summary QA sources. Do not join them to the detail source or each other. They cannot support both filters correctly. Use the detail source for every interactive sheet.

Create these calculated fields (bracket names refer to the CSV column names):

```text
CTR = IF SUM([impressions]) = 0 THEN NULL ELSE SUM([clicks])/SUM([impressions]) END
Conversion Rate = IF SUM([clicks]) = 0 THEN NULL ELSE SUM([conversions])/SUM([clicks]) END
CPC = IF SUM([clicks]) = 0 THEN NULL ELSE SUM([cost])/SUM([clicks]) END
CPA = IF SUM([conversions]) = 0 THEN NULL ELSE SUM([cost])/SUM([conversions]) END
ROAS = IF SUM([cost]) = 0 THEN NULL ELSE SUM([revenue])/SUM([cost]) END
Profit = SUM([revenue])-SUM([cost])
```

Use distinct names such as `Weighted CTR` if Tableau detects a collision with an imported field. Never average the imported row ratios. Format rates as percentages (2 decimals), ROAS as a decimal with × suffix, and spend/revenue/profit as source currency units without an unverified currency symbol.

Build a fixed 1440×1100 dashboard with white background, navy text, teal revenue/profit, slate spend, and rust losses. Use an 8–16 px spacing grid, descriptive subtitles, and accessible labels in addition to color.

1. Header and reporting-month/ad-group filters (multiple selection); apply filters to all sheets using this data source.
2. Six KPI cards: SUM(cost), SUM(revenue), SUM(conversions), Weighted CTR, Weighted ROAS, Profit. Label the last card “Ad profit / loss”; explain that overhead is excluded.
3. Monthly spend vs revenue: continuous month on Columns; Measure Values SUM(cost) and SUM(revenue) on Rows, two colored lines and end labels. Sort months chronologically.
4. Monthly ROAS: month and Weighted ROAS line, with reference line at 1×.
5. Top profit groups: ad_group rows, Profit horizontal bars, descending; include only positive profit, show at most 10. Under these data only small groups qualify; display spend and conversions in tooltips.
6. Largest losses: ad_group rows, Profit bars ascending, negative groups only, at most 10.
7. Engagement vs conversion: Weighted CTR on x, Weighted Conversion Rate on y, ad_group on Detail, SUM(cost) on Size, Profit on Color. Tooltips include spend, conversions, CPA, and ROAS. Add portfolio benchmarks only if they respond correctly to the active filters; label any fixed benchmarks.
8. Efficiency: ad_group rows and Weighted ROAS columns, 1× reference line; show spend and conversion counts. Offer a minimum-spend parameter default 1,000 and clearly identify it as an analyst-selected screen, not a confidence threshold.
9. Footer: 3–5 findings from reports/business_insights.md, period, source, and limitations. Static findings must say “Full July–November portfolio; does not update with filters.”

For top/bottom sheets, make the date and group filters context filters before adding Top N sets, or use table-calculation rank filters after aggregation. Verify ranks update with selections. Keep all-group efficiency optional so the minimum-spend screen does not hide groups from the whole dashboard.

QA before publishing: no filters must show spend 635,372; revenue 561,960; conversions 95,996; CTR 34.56%; ROAS 0.884×; profit −73,412. October alone must show 78,256 spend, 79,303 revenue, 1,047 profit. Choose a zero-conversion record and confirm CPA is blank. Test month and group together, clear filters, and check totals again. No selection should create duplicate rows or silently zero-fill missing groups.

Connect the local CSV in Tableau Public, build sheets, assemble dashboard, and save the workbook. Publish using the user's Tableau Public account with an embedded data extract. View the published URL while signed out to confirm it needs no private MySQL connection. Capture overview and filtered screenshots into images/ and add the actual URL to README only after publication. Confirm source redistribution terms before committing datasets or publishing extracts.
