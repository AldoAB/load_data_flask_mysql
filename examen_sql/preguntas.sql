-- pregunta 1:
select
    d.department                                                            department,
    j.job                                                                          job,
    sum(
        case 
            when he.`datetime` between '2021-01-01' and '2021-03-31' then 1
            else 0
        end)                                                                        Q1,
    sum(
        case 
            when he.`datetime`  between '2021-04-01' and '2021-06-30' then 1
            else 0
        end)                                                                        Q2,
    sum(
        case 
            when he.`datetime`  between '2021-07-01' and '2021-09-30' then 1
            else 0
        end)                                                                        Q3,
    sum(
        case 
            when he.`datetime`  between '2021-10-01' and '2021-12-31' then 1
            else 0
        end)                                                                        Q4
from hired_employees he
    inner join jobs j on he.job_id = j.id
    inner join departments d on he.department_id = d.id
where he.datetime >= '2021-01-01' and he.datetime < '2022-01-01'
group by d.department, j.job
order by d.department, j.job



-- pregunta 2

select 
    d.id identificacion,
    d.department departamento,
    count(he.id) contratado
from hired_employees he
inner join departments d on he.department_id = d.id
where he.datetime >= '2021-01-01' and he.datetime < '2022-01-01'
group by d.id, d.department
having
    count(he.id) > (
        select AVG(num_employees) 
        from ( 
            select 
                department_id, 
                count(*) num_employees 
            from hired_employees 
            where datetime >= '2021-01-01' and datetime < '2022-01-01' 
            group by department_id
        ) AS e)
order by contratado desc;


-- segunda forma:
WITH employees_2021 AS (
    SELECT department_id, COUNT(*) AS total_hired
    FROM hired_employees
    WHERE YEAR(STR_TO_DATE(datetime, '%Y-%m-%dT%H:%i:%s')) = 2021
    GROUP BY department_id
),
mean_hired AS (
    SELECT AVG(total_hired) AS avg_hired
    FROM employees_2021
)
SELECT d.id, d.department, e.total_hired
FROM employees_2021 e
JOIN departments d ON e.department_id = d.id
WHERE e.total_hired > (SELECT avg_hired FROM mean_hired)
ORDER BY e.total_hired DESC;