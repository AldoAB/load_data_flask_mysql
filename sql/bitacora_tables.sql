-- Creación de la tabla jobs_log
CREATE TABLE jobs_log (
  id int(11) DEFAULT NULL,
  job varchar(100) DEFAULT NULL,
  inserted_by varchar(100) DEFAULT CURRENT_USER(),
  inserted_at datetime DEFAULT CURRENT_TIMESTAMP()
);

-- Creación de la tabla departments_log
CREATE TABLE departments_log (
  id int(11) DEFAULT NULL,
  department varchar(100) DEFAULT NULL,
  inserted_by varchar(100) DEFAULT CURRENT_USER(),
  inserted_at datetime DEFAULT CURRENT_TIMESTAMP()
);

-- Creación de la tabla hired_employees_log
CREATE TABLE hired_employees_log (
  id int(11) DEFAULT NULL,
  name varchar(100) DEFAULT NULL,
  datetime varchar(100) DEFAULT NULL,
  department_id int(11) DEFAULT NULL,
  job_id int(11) DEFAULT NULL,
  inserted_by varchar(100) DEFAULT CURRENT_USER(),
  inserted_at datetime DEFAULT CURRENT_TIMESTAMP()
);

-- Creación del trigger para la tabla jobs
CREATE TRIGGER bitacora_jobs
AFTER INSERT ON jobs
FOR EACH ROW
BEGIN
  INSERT INTO jobs_log (id, job, inserted_by, inserted_at)
  VALUES (NEW.id, NEW.job, CURRENT_USER(), NOW());
END;

-- Creación del trigger para la tabla departments
CREATE TRIGGER bitacora_departments
AFTER INSERT ON departments
FOR EACH ROW
BEGIN
  INSERT INTO departments_log (id, department, inserted_by, inserted_at)
  VALUES (NEW.id, NEW.department, CURRENT_USER(), NOW());
END;

-- Creación del trigger para la tabla hired_employees
CREATE TRIGGER bitacora_employees
AFTER INSERT ON hired_employees
FOR EACH ROW
BEGIN
  INSERT INTO hired_employees_log (id, name, datetime, department_id, job_id, inserted_by, inserted_at)
  VALUES (NEW.id, NEW.name, NEW.datetime, NEW.department_id, NEW.job_id, CURRENT_USER(), NOW());
END;
