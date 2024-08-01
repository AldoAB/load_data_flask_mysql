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


