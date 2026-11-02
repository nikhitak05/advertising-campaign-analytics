USE advertising_analytics;
CREATE OR REPLACE VIEW vw_monthly_kpis AS
SELECT reporting_month, COUNT(*) AS record_count, SUM(impressions) AS impressions,
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
 SUM(revenue)-SUM(cost) AS profit_loss
FROM campaign_performance GROUP BY reporting_month;

CREATE OR REPLACE VIEW vw_ad_group_kpis AS
SELECT ad_group, COUNT(*) AS record_count, SUM(impressions) AS impressions,
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
 SUM(revenue)-SUM(cost) AS profit_loss
FROM campaign_performance GROUP BY ad_group;
CREATE OR REPLACE VIEW vw_campaign_month AS SELECT * FROM campaign_performance;
