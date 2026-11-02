-- MySQL 8.0.16+; CHECK constraints enforced. Existing tables are never dropped.
CREATE DATABASE IF NOT EXISTS advertising_analytics CHARACTER SET utf8mb4;
USE advertising_analytics;
CREATE TABLE IF NOT EXISTS campaign_performance (
  `ad_group` VARCHAR(255) COLLATE utf8mb4_bin NOT NULL,
  `month` VARCHAR(12) NOT NULL,
  `impressions` BIGINT UNSIGNED NOT NULL,
  `clicks` BIGINT UNSIGNED NOT NULL,
  `conversions` BIGINT UNSIGNED NOT NULL,
  `cost` DECIMAL(20,2) NOT NULL,
  `revenue` DECIMAL(20,2) NOT NULL,
  `sale_amount` DECIMAL(20,2) NOT NULL,
  `source_ctr` DECIMAL(24,12) NULL,
  `source_conversion_rate` DECIMAL(24,12) NULL,
  `source_cpc` DECIMAL(24,12) NULL,
  `source_profit_loss` DECIMAL(24,12) NULL,
  `ctr` DECIMAL(24,12) NULL,
  `conversion_rate` DECIMAL(24,12) NULL,
  `cpc` DECIMAL(24,12) NULL,
  `cpa` DECIMAL(24,12) NULL,
  `roas` DECIMAL(24,12) NULL,
  `profit_loss` DECIMAL(20,2) NOT NULL,
  `reporting_month` DATE NOT NULL,
  PRIMARY KEY (ad_group, reporting_month),
  CHECK (cost >= 0),
  CHECK (clicks <= impressions),
  CHECK (DAY(reporting_month) = 1)
) ENGINE=InnoDB;
