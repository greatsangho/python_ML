drop database if exists sqldb; -- 조건에 맞으면 삭제(drop)
create database sqldb;
use sqldb; -- 활성화

create table usertbl -- 회원
(
	userID	char(8) not null primary key,
    name	varchar(10) not null,
    birthYear	int not null,
    addr	char(2) not null, -- 지역(서울, 경기,...)
    mobile1	char(3), -- 국번 010 011
    mobile2 char(8), -- 나머지 번호
    height	smallint,
    mDate	date
);

create table buytbl -- 구매
(
	num int auto_increment not null primary key, -- pk는 겹치면 안 됨, 재사용 안 함
    userId	char(8) not null,
    prodName	char(6) not null,
    groupName	char(4), -- 분류
    price	int not null, -- 단가
    amount	smallint not null, -- 수량
    foreign key(userId) references usertbl(userId)
);

INSERT INTO usertbl VALUES('LSG', '이승기', 1987, '서울', '011', '1111111', 182, '2008-8-8');
INSERT INTO usertbl VALUES('KBS', '김범수', 1979, '경남', '011', '2222222', 173, '2012-4-4');
INSERT INTO usertbl VALUES('KKH', '김경호', 1971, '전남', '019', '3333333', 177, '2007-7-7');
INSERT INTO usertbl VALUES('JYP', '조용필', 1950, '경기', '011', '4444444', 166, '2009-4-4');
INSERT INTO usertbl VALUES('SSK', '성시경', 1979, '서울', NULL  , NULL      , 186, '2013-12-12');
INSERT INTO usertbl VALUES('LJB', '임재범', 1963, '서울', '016', '6666666', 182, '2009-9-9');
INSERT INTO usertbl VALUES('YJS', '윤종신', 1969, '경남', NULL  , NULL      , 170, '2005-5-5');
INSERT INTO usertbl VALUES('EJW', '은지원', 1972, '경북', '011', '8888888', 174, '2014-3-3');
INSERT INTO usertbl VALUES('JKW', '조관우', 1965, '경기', '018', '9999999', 172, '2010-10-10');
INSERT INTO usertbl VALUES('BBK', '바비킴', 1973, '서울', '010', '0000000', 176, '2013-5-5');
INSERT INTO buytbl VALUES(NULL, 'KBS', '운동화', NULL   , 30,   2);
INSERT INTO buytbl VALUES(NULL, 'KBS', '노트북', '전자', 1000, 1);
INSERT INTO buytbl VALUES(NULL, 'JYP', '모니터', '전자', 200,  1);
INSERT INTO buytbl VALUES(NULL, 'BBK', '모니터', '전자', 200,  5);
INSERT INTO buytbl VALUES(NULL, 'KBS', '청바지', '의류', 50,   3);
INSERT INTO buytbl VALUES(NULL, 'BBK', '메모리', '전자', 80,  10);
INSERT INTO buytbl VALUES(NULL, 'SSK', '책'    , '서적', 15,   5);
INSERT INTO buytbl VALUES(NULL, 'EJW', '책'    , '서적', 15,   2);
INSERT INTO buytbl VALUES(NULL, 'EJW', '청바지', '의류', 50,   1);
INSERT INTO buytbl VALUES(NULL, 'BBK', '운동화', NULL   , 30,   2);
INSERT INTO buytbl VALUES(NULL, 'EJW', '책'    , '서적', 15,   1);
INSERT INTO buytbl VALUES(NULL, 'BBK', '운동화', NULL   , 30,   2);

-- 각각 테이블의 전체값 조회
select *
from usertbl;
select *
from buytbl;

select *
from usertbl
where name = '김경호' or name = '이승기';

select *
from usertbl
where name in('이승기', '김경호');

select userId, Name
from usertbl
where birthyear >= 1970 or height >=182;

select name, addr
from usertbl
where addr in('경남','전남','전북');

select name, height
from usertbl
where name like '%김%';

select *
from usertbl
where height between 180 and 183;

-- 김경호 보다 키가 크거나 같은 사람
-- 1. 김경호의 키를 조회 (ex 180)
-- 사용자 테이블에서 키가 180 이상인 데이터
select name, height
from usertbl
where height >= (select height from usertbl where name = '김경호'); -- 여러값을 보내지 않도록 주의

-- any(서브쿼리), some(서브쿼리), in(데이터) / all(서브쿼리)
select name, height
from usertbl
-- where addr = '경남';
-- where height in (173, 170);
where height >= any(select height from usertbl where addr = '경남'); -- 173보다 크거나 같고, or 170보다 크거나 같은 사람
-- where height >= all(select height from usertbl where addr = '경남'); -- 173보다 크거나 같고, and 170보다 크거나 같은 사람

-- 경남에 사는 회원의 키값과 같은 회원들을 전부 출력 in
select name, height
from usertbl
where height = any(select height from usertbl where addr = '경남');

select name, height
from usertbl
order by height DESC, name asc; -- 정렬은 기본이 오름차순

select *
from usertbl
order by addr, mDate desc;

select * from usertbl
where mDate >= '2010-01-01'
order by addr, mDate desc;

-- distinct 중복제거
select distinct addr from usertbl;
-- limit 5 상위 5개만 출력
select * from usertbl limit 5; -- select * from usertbl limit 0,5;
select * from usertbl limit 2,5;

-- 테이블 복사
create table buytbl2
(
select * from buytbl
);
select * from buytbl2;

-- buytbl3 buytbl의 userid, prodname 만을 가지는 새로운 테이블 복사
create table buytbl3
(
select userid, prodname from buytbl
);
select * from buytbl3;

select * from buytbl;
-- group by 통계
select
userid, sum(amount) 
from buytbl 
group by userid;

select userid, sum(amount) as 'total_amount' 
from buytbl 
group by userid 
order by sum(amount) desc;

select num, groupname, sum(price*amount) as total_price
from buytbl
group by groupName, num;
-- with rollup;

select num, groupname, sum(price*amount) as total_price
from buytbl
group by groupName, num
with rollup;
;

-- having
-- 사용자별 총 구매액
-- userid, 총 구매액
select userid, sum(price*amount) as total_price
from buytbl
group by userid
having sum(price*amount) >= 1000
order by sum(price*amount)
;

-- 데이터 추가
select * from buytbl2;
drop table buytbl3;
drop table buytbl2;
create table buytbl3 like buytbl; -- 구조만 복사
select * from buytbl3;

-- 데이터 추가
insert into  buytbl3(select * from buytbl where prodname = '모니터');
select * from buytbl3;

-- 데이터 삭제
-- delete from 테이블 where 조건
delete from buytbl3 where prodname = '모니터';

-- 구매액 총합이 1000 이상인 고객 정보를 추출
-- 추출한 고객정보를 데이터로 하는 새로운 테이블 생성
select *, price*amount as total_count from buytbl order by userid;

select
userid, sum(price*amount) as total_count_per_user
from buytbl
group by userid
having sum(price*amount)>=1000;
-- BBK, KBS
create table usertbl2(
    select * from usertbl where userid in (
        select
        userid
        from buytbl
        group by userid
        having sum(priceamount) >= 1000
    )
);
select * from buytbl2;
