-- select "Hello";
select cast('2024-09-02 09:16:15.232' as datetime) as 'DATE';  -- date, time, datetime으로 변환, 별칭주기

use sqldb;

set @myVar1 = 5;
set @myVar2 = 3;
set @myVar3 = 3.25;
set @myVar4 = "가수이름";

select @myVar1;
select @myVar2 + @myvar3;
desc usertbl;

select @myvar4, name from usertbl where height > 180;

select cast(avg(amount) as signed integer) as '평균 구매 개수' from buytbl;
select convert(avg(amount), signed integer) as '평균 구매 개수' from buytbl;

select avg(amount) as '평균 구매 개수' from buytbl;

-- cast
select cast(avg(amount) as signed integer) as '평균 구매 개수' from buytbl; -- 정수로 반올림 하여 반환함

-- convert
select convert(avg(amount), signed integer) as '평균 구매 개수' from buytbl;

select
concat(cast(price as char(10)),
' X ',
cast(amount as char(4)), '=') as '단가x수량',price*amount as '구매액'
from buytbl;

select '100' + '200';
select concat('100','200');
select concat(100, '200');
select 1 > 'mega'; -- 0
select 123123123 = '123123123mega';
select 0 = 'mega123123123'; -- 0
set @age = 15;
select @age;
select if (@age>19, '성인', '미성년');

select ifnull(null,'null입니다');

select
num, userid, prodname,
ifnull(groupname, '기타') as groupname,
price,
amount
from buytbl;

select case 2
		when 1 then '일'
		when 2 then '이'
		else '일과 이가 아닌 그 밖의 모든 것'
    end as 'case 연습';
    
select
prodname,
case 
	when price > 100 then '비싸다'
				else '살만하네'
end as '구매여부'
from buytbl;

-- 항목을 위로 올려서 전달하고 싶을 때, sql로 처리하는 것이 처리하기 더 간단하고 빠름
select
sum(case when prodname='운동화' then price*amount else 0 end) as '운동화',
sum(case when prodname='노트북' then price*amount else 0 end) as '노트북',
sum(case when prodname='모니터' then price*amount else 0 end) as '모니터',
sum(case when prodname='청바지' then price*amount else 0 end) as '청바지',
sum(case when prodname='메모리' then price*amount else 0 end) as '메모리',
sum(case when prodname='책' then price*amount else 0 end) as '책'
from
	buytbl;

select concat_ws('/','10','20','30');

select * from buytbl;

select
userid, ifnull(groupname,'기타') as groupname, prodname
from buytbl;

select
concat_ws(',', userid,prodname, ifnull(groupname,'기타')) as '임시'
from buytbl;

select elt(2, '한', '둘', '셋');

select format(125.3215,1);  -- 소숫점 자리

select insert('abcdef', 1, 3, '@@@'); -- 시작위치 1부터, 3개, 대체

select left('abcdef', 3);
select right('abcdef', 3);

select lpad('한글',5,'#'), rpad('한글',5,'#');

select substring('동해물과백두산이',3,2);

select abs(-25);
select ceiling(4.2), floor(4.7), round(4.725,2);

select insert('abcdef', 1, 3, repeat('@',3));

use sqldb;
drop table pivottest;
create table pivotTest
(
	id int auto_increment primary key,
	uname varchar(3),
	season varchar(2),
    amount int
);
    
insert into pivotTest values
(null, '윤종신', '봄', 20),(null, '윤종신', '여름', 20),(null, '윤종신', '가을', 20),
(null, '윤종신', '겨울', 20),(null, '윤종', '봄', 20),(null, '윤종', '봄', 20),
(null, '윤신', '봄', 20),(null, '윤종신', '봄', 20),(null, '윤종신', '봄', 20),
(null, '윤종', '봄', 20),(null, '종신', '겨울', 20),(null, '종신', '가을', 20)
;

select
uname,
sum(if(season = '봄', amount,0)) as '봄',
sum(if(season = '여름', amount,0)) as '여름',
sum(if(season = '가을', amount,0)) as '가을',
sum(if(season = '겨울', amount,0)) as '겨울'
from pivotTest group by uname;

select
uname,
sum(case when season = '봄' then amount else 0 end) as '봄',
sum(case when season = '여름' then amount else 0 end) as '여름',
sum(case when season = '가을' then amount else 0 end) as '가을',
sum(case when season = '겨울' then amount else 0 end) as '겨울'
from pivottest
group by uname;

create table testtbl1
(
id int,
username varchar(45),
age int
);
insert into testtbl1(id,username) values(1,'설현');
insert into testtbl1(username,age, id) values('하니',26,2);
select * from testtbl1;

update testtbl1
set age = 30
where username = '하니'
;

update testtbl1
set age = 15
where username = '하니';

select *
from testtbl1;

select
*
from
(
select
userid, sum(price*amount) totalprice
from buytbl group by userid
-- having sum(price*amount) > 1000
) as T
where T.totalprice > 1000  -- totalprice라는 이름은 서브쿼리 안에서 아직 나오지 않아 사용 불가능함
;

with T(a,b) -- 값 2개를 얼라이어스를 준다
as
(
select
userid, sum(price*amount) totalprice
from buytbl group by userid
)
select * from T where T.b > 1000  -- totalprice라는 이름은 서브쿼리 안에서 아직 나오지 않아 사용 불가능함
;

-- 서브쿼리, with 구문, pivot을 위한 case when... / if

use employees;
select * from employees.titles;
-- 타이틀의 종류
select count(distinct(title)) from employees.titles;
-- 타이틀의 개수
select title, count(title) as count from employees.titles group by title;

select count(*) from employees.titles;

--
select
userid, sum(price*amount) totalprice
from buytbl group by userid
having totalprice > 1000;

use sqldb;
select * from usertbl;
select * from buytbl;

-- iner join
select
u.name,
-- case when u.mobbile1 is null then '-'
-- 	else concat_ws('-',u.mobile1, u.mobile2)
--     end as mobile,
if( concat_ws('-',u.mobile1, u.mobile2) = '', '-', concat_ws('-',u.mobile1, u.mobile2)) mobile,
if(u.mobile1 is null,'-',concat(u.mobile1,'-',left(mobile2,4),'-',right(mobile2,4) ) ) mobile,u.mdate,
b.prodname,
-- if(b.groupName is null, '기타', b.groupname) groupname,
ifnull(b.groupname, '-') groupname,
b.price*b.amount as totlaprice
from usertbl u
	join buytbl b -- inner join
		on u.userid = b.userid
;

select
left(mobile2, 4),
right(mobile2, 4),
mobile2
from usertbl;

use employees;
select
e.emp_no, birth_date, concat_ws(first_name, '-', last_name) name,
if(gender='M','남자','여자') gender, 
title, hire_date
from employees e
	join titles t
		on e.emp_no = t.emp_no
where t.to_date = '9999-01-01'
order by hire_date
;
-- 현재 재직중인 상태의 직원 정보를 출력(emp_no, birth_date, first_name - last_name, gender, title, hire_date)

use sqldb;
select *
from usertbl u
	left join buytbl b
		on u.userId = b.userId
        ;
        
select *
from buytbl b
	left join usertbl u
		on b.userid = u.userid
        ;

with newuser -- with 절은 처음만 써주면 됨
as
(        
select *
from usertbl limit 2
),
newbuy
as
(
select *
from buytbl limit 2
)
select * 
from newuser cross join newbuy;

drop table if exists A;
drop table if exists B;


create table A
(
	id int,
    name_a varchar(45)
);
create table B
(
	id int,
    name_b varchar(45)
);

insert into A values
(1,'abc'),(2,'def'),(3,'ghi'),(4,'jkl');

insert into B values
(2,'aaaaaaaa'),(3,'bbbbbb'),(5,'11111111'),(6,'22222222');

-- 교집합
select * from A join B 
	on A.id = B.id;
    
-- 합집합
select * from A left join B
	on A.id = B.id
union
select * from A right join B
	on A.id = B.id;
    
-- 차집합
select * from A left join B
	on A.id = B.id
    where B.id is null;

-- usertbl, buytbl userid가 JYP인 사용자가 구매한 정보를 모두 출력 -  INNER JOIN
select *
from usertbl u
	join buytbl b
		on u.userid = b.userid
			where u.userid = 'JYP';
            
-- 구매이력이 있는 사용자와 구매내역을 전부 출력하는데, num 정렬
select *
from usertbl u
	join buytbl b
		on u.userid = b.userid
			order by b.num;
            
-- 구매한 고객의 아이디 이름 제퓸종류, 주소, 연락처를 출력하고 변호순으로 정렬
select u.userid, u.name, b.prodname, u.addr, concat(u.mobile1, u.mobile2) as '연락처'
from usertbl u
	join buytbl b
		on u.userid = b.userid
			order by b.num;
----------------------------
-- inner join과 같은 효과
select
u.userid, u.name, u.addr
from usertbl u
where exists(
	select * from
		buytbl b
        where u.userid = b.userid
);
