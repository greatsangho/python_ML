-- select 열이름
-- from 테이블명;
use employees;

select *
from employees.departments;

select *
from employees;

select first_name
from employees;

select first_name, last_name, gender
from employees;

show databases;
show table status;
show tables;

describe employees;
desc departments;

select *
from employees
-- where gender = 'm';
where hire_date > 1990-01-01;