SELECT
    sb.subject_id,
    sb.subject_name,
    sp.species_name,
    to_char(sb.date_of_birth, 'YYYY-MM') AS date_of_birth
FROM 
    subject AS sb
JOIN
    species AS sp
    ON (sb.species_id = sp.species_id)
ORDER BY date_of_birth DESC;

