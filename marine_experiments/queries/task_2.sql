SELECT
    e.experiment_id,
    sb.subject_id,
    sp.species_name AS species,
    e.experiment_date,
    et.type_name AS experiment_type,
    CONCAT(ROUND(((e.score / et.max_score)*100),2), '%') AS score
FROM subject AS sb
JOIN 
    species AS sp
    USING (species_id)
JOIN 
    experiment AS e
    USING (subject_id)
JOIN 
    experiment_type AS et
    USING (experiment_type_id)
ORDER BY experiment_date DESC
;
