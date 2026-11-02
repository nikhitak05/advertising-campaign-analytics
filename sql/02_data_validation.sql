USE advertising_analytics;
-- Expected 190, 40, 5. Compare sums against reports/validation.json.
SELECT COUNT(*) AS records, COUNT(DISTINCT ad_group) AS ad_groups,
 COUNT(DISTINCT reporting_month) AS months FROM campaign_performance;
-- Expected July-November: 38,38,38,37,39.
SELECT reporting_month,COUNT(*) AS records FROM campaign_performance GROUP BY reporting_month ORDER BY reporting_month;
-- Each following exception query should return zero rows.
SELECT ad_group,reporting_month,COUNT(*) FROM campaign_performance GROUP BY ad_group,reporting_month HAVING COUNT(*)>1;
SELECT * FROM campaign_performance WHERE impressions<0 OR clicks<0 OR conversions<0 OR cost<0 OR clicks>impressions;
SELECT * FROM campaign_performance WHERE
 ABS(profit_loss-(revenue-cost))>0.000000001
 OR (impressions=0 AND ctr IS NOT NULL)
 OR (impressions<>0 AND (ctr IS NULL OR ABS(ctr-CAST(clicks AS DECIMAL(30,12))/NULLIF(impressions,0))>0.000000001))
 OR (clicks=0 AND conversion_rate IS NOT NULL)
 OR (clicks<>0 AND (conversion_rate IS NULL OR ABS(conversion_rate-CAST(conversions AS DECIMAL(30,12))/NULLIF(clicks,0))>0.000000001))
 OR (clicks=0 AND cpc IS NOT NULL)
 OR (clicks<>0 AND (cpc IS NULL OR ABS(cpc-CAST(cost AS DECIMAL(30,12))/NULLIF(clicks,0))>0.000000001))
 OR (conversions=0 AND cpa IS NOT NULL)
 OR (conversions<>0 AND (cpa IS NULL OR ABS(cpa-CAST(cost AS DECIMAL(30,12))/NULLIF(conversions,0))>0.000000001))
 OR (cost=0 AND roas IS NOT NULL)
 OR (cost<>0 AND (roas IS NULL OR ABS(roas-CAST(revenue AS DECIMAL(30,12))/NULLIF(cost,0))>0.000000001));
SELECT SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(conversions) AS conversions, SUM(cost) AS cost, SUM(revenue) AS revenue, SUM(sale_amount) AS sale_amount FROM campaign_performance;
