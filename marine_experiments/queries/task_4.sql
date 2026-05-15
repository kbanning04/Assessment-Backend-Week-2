SELECT
    sp.species_name,
    e.experiment_id,
    sp.is_predator,
CASE
    WHEN sp.is_predator = 't' THEN e.score * 1.2
ELSE
    e.score * 1
END AS score
FROM
    subject AS sb
JOIN  
    species AS sp
    USING (species_id)
JOIN 
    experiment AS e
    USING (subject_id)
ORDER BY
    e.score DESC;
