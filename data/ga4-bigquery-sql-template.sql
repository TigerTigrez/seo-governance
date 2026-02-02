-- GA4 BigQuery Export Template (no project IDs here)
-- Replace DATASET and TABLE with appropriate views
-- Purpose: Landing pages, sessions, engagement, conversions

WITH sessions AS (
  SELECT
    PARSE_DATE('%Y%m%d', event_date) AS date,
    traffic_source.source AS source,
    traffic_source.medium AS medium,
    traffic_source.name AS campaign,
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key='page_location') AS page,
    user_pseudo_id
  FROM `PROJECT.DATASET.events_*`
  WHERE event_name = 'page_view'
    AND _TABLE_SUFFIX BETWEEN 'YYYYMMDD' AND 'YYYYMMDD'
),
agg AS (
  SELECT
    date, page,
    COUNT(DISTINCT user_pseudo_id) AS users
  FROM sessions
  GROUP BY 1,2
)
SELECT * FROM agg
ORDER BY date DESC, users DESC;
