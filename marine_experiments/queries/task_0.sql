SELECT
    s.subject_id,
    s.subject_name,
    s.species_id,
    s.date_of_birth
FROM 
    subject AS s
WHERE
    s.subject_name LIKE '%o%';    