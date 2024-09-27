drop database if exists testdb;
create database testdb;
USE testdb;
CREATE TABLE stdtbl 
( stdName    VARCHAR(10) NOT NULL PRIMARY KEY,
  addr      CHAR(4) NOT NULL
);
CREATE TABLE clubtbl 
( clubName    VARCHAR(10) NOT NULL PRIMARY KEY,
  roomNo    CHAR(4) NOT NULL
);
CREATE TABLE stdclubtbl
(  num int AUTO_INCREMENT NOT NULL PRIMARY KEY, 
   stdName    VARCHAR(10) NOT NULL,
   clubName    VARCHAR(10) NOT NULL,
FOREIGN KEY(stdName) REFERENCES stdtbl(stdName),
FOREIGN KEY(clubName) REFERENCES clubtbl(clubName)
);
INSERT INTO stdtbl VALUES ('김범수','경남'), ('성시경','서울'), ('조용필','경기'), ('은지원','경북'),('바비킴','서울');
INSERT INTO clubtbl VALUES ('수영','101호'), ('바둑','102호'), ('축구','103호'), ('봉사','104호');
INSERT INTO stdclubtbl VALUES (NULL, '김범수','바둑'), (NULL,'김범수','축구'), (NULL,'조용필','축구'), (NULL,'은지원','축구'), (NULL,'은지원','봉사'), (NULL,'바비킴','봉사');

-- 3개 join 시
select
*
from stdtbl s
	join stdclubtbl sc
		on s.stdname = sc.stdname
	join clubtbl c
		on sc.clubname = c.clubname
order by s.stdname;

-- 개수가 늘어날 수 있음
select s.stdname, s.addr, c.clubname, c.roomno
from stdtbl s
	left join stdclubtbl sc
		on s.stdname = sc.stdname
	left join clubtbl c
		on sc.clubname = c.clubname
;

select *
from stdtbl s
	left join stdclubtbl sc
		on s.stdname = sc.stdname
        ;
-- 직접 연결되어 있지 않은 데이터의 연결

