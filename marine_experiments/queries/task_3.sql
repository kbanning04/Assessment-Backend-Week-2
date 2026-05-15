SELECT 
    et.type_name,
    sp.species_name,
    ROUND(AVG(e.score), 1) AS average_score 
FROM
    subject AS sb
JOIN  
    species AS sp
    USING (species_id)
JOIN 
    experiment AS e
    USING (subject_id)
JOIN 
    experiment_type AS et
    USING (experiment_type_id)
GROUP BY 
    et.type_name, sp.species_name
HAVING
    AVG(e.score) > 5
ORDER BY 
    average_score DESC;
