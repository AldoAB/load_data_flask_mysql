-- 1.
SELECT 
    department,
    job,
    SUM(CASE WHEN quarter = 1 THEN num_employees ELSE 0 END) AS Q1,
    SUM(CASE WHEN quarter = 2 THEN num_employees ELSE 0 END) AS Q2,
    SUM(CASE WHEN quarter = 3 THEN num_employees ELSE 0 END) AS Q3,
    SUM(CASE WHEN quarter = 4 THEN num_employees ELSE 0 END) AS Q4
FROM (
    SELECT 
        d.department AS department,
        j.job AS job,
        QUARTER(he.datetime) AS quarter,
        COUNT(*) AS num_employees
    FROM hired_employees he
    INNER JOIN jobs j ON he.job_id = j.id
    INNER JOIN departments d ON he.department_id = d.id
    WHERE he.datetime >= '2021-01-01' AND he.datetime < '2022-01-01'
    GROUP BY d.department, j.job, QUARTER(he.datetime)
) AS subquery
GROUP BY department, job
ORDER BY department, job;




---2
SELECT 
    d.id AS identificacion,
    d.department AS departamento,
    COUNT(he.id) AS contratado
FROM hired_employees he
JOIN departments d ON he.department_id = d.id
WHERE he.datetime >= '2021-01-01' AND he.datetime < '2022-01-01'
GROUP BY d.id, d.department
HAVING
    COUNT(he.id) > (SELECT AVG(num_employees) FROM (SELECT department_id, COUNT(*) AS num_employees FROM hired_employees WHERE datetime >= '2021-01-01' AND datetime < '2022-01-01' GROUP BY department_id) AS subquery)
ORDER BY contratado DESC;
