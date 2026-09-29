WITH latest AS (
    SELECT lead_id, stage, entered_at,
           ROW_NUMBER() OVER (PARTITION BY lead_id ORDER BY entered_at DESC) AS rn
    FROM lead_stage_history
),
points AS (
    SELECT l.lead_id, l.company_name, l.source, s.stage,
           CASE s.stage WHEN 'New' THEN 10 WHEN 'Contacted' THEN 30
                        WHEN 'Quoted' THEN 55 WHEN 'Won' THEN 100 ELSE 0 END AS stage_points,
           CASE l.source WHEN 'Trade fair' THEN 20 WHEN 'Referral' THEN 15
                         WHEN 'Website' THEN 10 WHEN 'IndiaMART listing' THEN 10
                         WHEN 'Cold call' THEN 5 ELSE 0 END AS source_points,
           CASE WHEN s.entered_at >= DATE '2026-01-06' - 14 THEN 10 ELSE 0 END AS recency_points
    FROM leads AS l
    JOIN latest AS s ON s.lead_id = l.lead_id AND s.rn = 1
)
SELECT lead_id, company_name, source, stage,
       CASE WHEN stage = 'Lost' THEN 0
            ELSE LEAST(stage_points + source_points + recency_points, 100) END AS score
FROM points
ORDER BY lead_id;
