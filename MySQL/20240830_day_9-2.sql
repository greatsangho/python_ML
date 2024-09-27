-- 데이터베이스 목록 조회
show databases;
-- 데이터베이스 선택(활성화)
use sqldb;
-- 데이터베이스에 있는 테이블 조회
show tables;
-- 테이블 형식을 조회
desc usertbl;
-- 조회 select
select * from usertbl u;
-- 이름이 김경호
select * from usertbl u
where u.name = '김경호';
-- 1970년 이상이고 키가 182이상인 고객
select * from usertbl u
u.birthyear > 1970 and height >= 182;
-- 1970년 이상이거나 키가 182이상인 고객
select * from usertbl where birthyear > 1970 or height >= 182;
-- 키가 180이상이고 183이하인 고객 -> and 연산자 / between 연산자
select * from usertbl where height >= 180 and height <= 183;
select * from usertbl where height between 180 and 183;
-- 지역이 경남이거나 전남이거나 경북인 고객 -> or 연산자 / in 연산자
select * from usertbl where addr = '경남' or addr = '전남' or addr = '경북';
select * from usertbl where addr in ('경남', '전남', '전북');
-- 고객 중에 김씨인 사람들
select * from usertbl where name like '김%';
-- 고객 중에 김경호보다 키가 큰 고객들
select * from usertbl where height > (select height from usertbl where name = '김경호');
-- 고객중에 경남지역에 거주하는 고객의 키의 평균보다 큰 고객들
select * from usertbl where height > (select avg(height) from usertbl where addr = '경남');
-- 고객테이블에서 mData 날자로 정령(오름차순), 내림차순
select * from usertbl u
order by u.mDate desc;

use employees;
show tables;

select emp_no, hire_date from employees 
order by hire_date limit 5;

select * from salaries;

use employees;
-- 연봉이 가장 높은 상위 5명에 대한 사원 정보를 출력
-- select * from employees where emp_no in (
-- 	select emp_no from salaries
-- 	group by emp_no
-- 	order by max(salary) desc
-- ) limit 5;

with temp(emp_no) as -- colom 명
(
select emp_no from salaries
	group by emp_no
	order by max(salary) desc limit 5
)
select * from employees
	where emp_no in (
    select emp_no from temp
    )
;

use sqldb;
select * from usertbl;
-- 각 지역별 최고키
select addr, max(height) from usertbl
group by addr
;