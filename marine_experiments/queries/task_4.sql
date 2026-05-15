SELECT
    sp.species_name,
    e.experiment_id,
CASE
    WHEN sp.is_predator = 't'
    THEN 'True'
ELSE
    'False'
END AS is_predator,
CASE
    WHEN is_predator = 'True' 
    THEN 
        e.score * 1.2 
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
    score DESC;
