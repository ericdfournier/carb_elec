-- Cast numeric field types

UPDATE cpuc.psps_outages_2013_2023
SET "year" = NULL
WHERE "year" ~ '^[^0-9]+$';

UPDATE cpuc.psps_outages_2013_2023
SET "year" =  regexp_replace("year", '\s+$', '');

ALTER TABLE cpuc.psps_outages_2013_2023
ALTER COLUMN "year" TYPE NUMERIC
USING ("year"::NUMERIC);

--

UPDATE cpuc.psps_outages_2013_2023
SET "total_customers_impacted" = NULL
WHERE "total_customers_impacted" ~ '^[^0-9]+$';

UPDATE cpuc.psps_outages_2013_2023
SET "total_customers_impacted" =  regexp_replace("total_customers_impacted", '\s+$', '');

ALTER TABLE cpuc.psps_outages_2013_2023
ALTER COLUMN "total_customers_impacted" TYPE NUMERIC
USING ("total_customers_impacted"::NUMERIC);

--

UPDATE cpuc.psps_outages_2013_2023
SET "residential_customers" = NULL
WHERE "residential_customers" ~ '^[^0-9]+$';

UPDATE cpuc.psps_outages_2013_2023
SET "residential_customers" = regexp_replace("residential_customers", '\s+$', '');

UPDATE cpuc.psps_outages_2013_2023
SET "residential_customers" = 0
WHERE "residential_customers" = ' 0';

ALTER TABLE cpuc.psps_outages_2013_2023
ALTER COLUMN "residential_customers" TYPE NUMERIC
USING ("residential_customers"::NUMERIC);

--

UPDATE cpuc.psps_outages_2013_2023
SET "commercial.industrial_customers" = NULL
WHERE "commercial.industrial_customers" ~ '^[^0-9]+$';

UPDATE cpuc.psps_outages_2013_2023
SET "commercial.industrial_customers" = regexp_replace("commercial.industrial_customers", '\s+$', '');

ALTER TABLE cpuc.psps_outages_2013_2023
ALTER COLUMN "commercial.industrial_customers" TYPE NUMERIC
USING ("commercial.industrial_customers"::NUMERIC);

--

UPDATE cpuc.psps_outages_2013_2023
SET "medical_baseline_customers" = NULL
WHERE "medical_baseline_customers" ~ '^[^0-9]+$';

UPDATE cpuc.psps_outages_2013_2023
SET "medical_baseline_customers" = regexp_replace("medical_baseline_customers", '\s+$', '');

UPDATE cpuc.psps_outages_2013_2023
SET "medical_baseline_customers" = 0
WHERE "medical_baseline_customers" = ' 0';

ALTER TABLE cpuc.psps_outages_2013_2023
ALTER COLUMN "medical_baseline_customers" TYPE NUMERIC
USING ("medical_baseline_customers"::NUMERIC);

--

UPDATE cpuc.psps_outages_2013_2023
SET "other_customers" = NULL
WHERE "other_customers" ~ '^[^0-9]+$';

UPDATE cpuc.psps_outages_2013_2023
SET "other_customers" = regexp_replace("other_customers", '\s+$', '');

UPDATE cpuc.psps_outages_2013_2023
SET "other_customers" = 0
WHERE "other_customers" = ' 0';

ALTER TABLE cpuc.psps_outages_2013_2023
ALTER COLUMN "other_customers" TYPE NUMERIC
USING ("other_customers"::NUMERIC);

--

UPDATE cpuc.psps_outages_2013_2023
SET "outage_hours" = NULL
WHERE "outage_hours" IN ('NA', 'N/A', '-');

ALTER TABLE cpuc.psps_outages_2013_2023
ALTER COLUMN "outage_hours" TYPE NUMERIC
USING (TRIM("outage_hours")::NUMERIC);

--

UPDATE cpuc.psps_outages_2013_2023
SET "outage_days" = NULL
WHERE "outage_days" IN ('NA', 'N/A', '-');

ALTER TABLE cpuc.psps_outages_2013_2023
ALTER COLUMN "outage_days" TYPE NUMERIC
USING (TRIM("outage_days")::NUMERIC);
