SELECT pp.*,
       (SELECT MODE() WITHIN GROUP (ORDER BY po."DP02_0123E") 
            FROM census.acs_ca_2019_tr_population AS po 
            WHERE po."GEOID"::NUMERIC = pp.centract) AS population
INTO public.fm3_priority_population_layer
FROM carb.priority_populations_ces4 AS pp;

ALTER TABLE public.fm3_priority_population_layer 
ALTER COLUMN geom TYPE geometry(MultiPolygon, 3310)
USING ST_CurveToLine(geom);

UPDATE public.fm3_priority_population_layer
SET geom = ST_MAKEVALID(geom)
WHERE ST_ISVALID(geom) = False;

SELECT  DISTINCT(centract),
        MODE() WITHIN GROUP (ORDER BY display) AS display,
        MODE() WITHIN GROUP (ORDER BY dac) AS dac,
        MODE() WITHIN GROUP (ORDER BY lowincome) AS lowincome,
        MODE() WITHIN GROUP (ORDER BY nondesignated) AS nondesignated,
        MODE() WITHIN GROUP (ORDER BY bufferlowincome) AS bufferlowincome,
        MODE() WITHIN GROUP (ORDER BY bufferlih) AS bufferlih,
        MODE() WITHIN GROUP (ORDER BY population) AS population,
        ST_Union(geom) AS geom
INTO public.fm3_priority_population_unified
FROM public.fm3_priority_population_layer
GROUP BY centract;

SELECT SUM(population) FROM public.fm3_priority_population_unified;