-- creacion de base de datos inicial
create database historical_data;

-- indicar que usaremos la base de datos creada
use historical_data;

-- 1 jobs
CREATE TABLE jobs (
  id int(11) DEFAULT NULL,
  job varchar(100) DEFAULT NULL
);


-- 2 departments
CREATE TABLE departments (
  id int(11) DEFAULT NULL,
  department varchar(100) DEFAULT NULL
);


-- 3 hired_employees
CREATE TABLE hired_employees (
  id int(11) DEFAULT NULL,
  name varchar(100) DEFAULT NULL,
  datetime varchar(100) DEFAULT NULL,
  department_id int(11) DEFAULT NULL,
  job_id int(11) DEFAULT NULL
);

