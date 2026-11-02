USE advertising_analytics;
-- Weighted overall KPIs; rates are fractions, ROAS a multiplier.
SELECT SUM(impressions) AS impressions,
 SUM(clicks) AS clicks,
 SUM(conversions) AS conversions,
 SUM(cost) AS cost,
 SUM(revenue) AS revenue,
 SUM(sale_amount) AS sale_amount,
 CAST(SUM(clicks) AS DECIMAL(30,12))/NULLIF(SUM(impressions),0) AS ctr,
 CAST(SUM(conversions) AS DECIMAL(30,12))/NULLIF(SUM(clicks),0) AS conversion_rate,
 CAST(SUM(cost) AS DECIMAL(30,12))/NULLIF(SUM(clicks),0) AS cpc,
 CAST(SUM(cost) AS DECIMAL(30,12))/NULLIF(SUM(conversions),0) AS cpa,
 CAST(SUM(revenue) AS DECIMAL(30,12))/NULLIF(SUM(cost),0) AS roas,
 SUM(revenue)-SUM(cost) AS profit_loss FROM campaign_performance;
-- Month-over-month absolute changes, first month undefined.
SELECT *,cost-LAG(cost) OVER (ORDER BY reporting_month) AS spend_change,
 revenue-LAG(revenue) OVER (ORDER BY reporting_month) AS revenue_change
FROM vw_monthly_kpis ORDER BY reporting_month;
SELECT *,RANK() OVER (ORDER BY revenue DESC) AS revenue_rank FROM vw_ad_group_kpis ORDER BY revenue DESC;
SELECT *,RANK() OVER (ORDER BY profit_loss DESC) AS profit_rank FROM vw_ad_group_kpis ORDER BY profit_loss DESC;
SELECT * FROM vw_ad_group_kpis WHERE profit_loss<0 ORDER BY profit_loss;
-- Illustrative screening thresholds, not statistical significance or causal evidence.
SELECT * FROM vw_ad_group_kpis WHERE cost>=1000 AND clicks>=1000 ORDER BY roas DESC;
SELECT * FROM vw_ad_group_kpis WHERE cost>=1000 AND conversions>=100 ORDER BY cpa;
-- Above portfolio CTR but below portfolio conversion rate, with meaningful volume.
WITH overall AS (SELECT CAST(SUM(clicks) AS DECIMAL(30,12))/NULLIF(SUM(impressions),0) AS ctr,
 CAST(SUM(conversions) AS DECIMAL(30,12))/NULLIF(SUM(clicks),0) AS cvr FROM campaign_performance)
SELECT a.* FROM vw_ad_group_kpis a CROSS JOIN overall o
WHERE a.ctr>o.ctr AND a.conversion_rate<o.cvr AND a.clicks>=1000 ORDER BY a.cost DESC;
SELECT * FROM vw_ad_group_kpis WHERE cost>=1000 AND roas<1 ORDER BY profit_loss;
