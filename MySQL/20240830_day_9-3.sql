drop database if exists bookrental;
create database bookrental;
use bookrental;
create table booktbl(
	book_id int auto_increment not null primary key,
    title varchar(45) not null,
    author varchar(45) not null,
    publish varchar(45) not null
);
create table customertbl(
	customer_id varchar(45) not null primary key,
    customer_name varchar(45) not null
);
create table ordertbl(
    customer_id varchar(45) not null,
    book_id int not null,
    price int not null,
    amount int not null,
    foreign key(book_id) references booktbl(book_id),
    foreign key(customer_id) references customertbl(customer_id)
);
insert into booktbl 
values
(null,'sql','이규영', '플레이데이터'), 
(null,'파이썬1','홍길동1', '플레이데이터'),
(null,'파이썬2','홍길동2', '플레이데이터'),
(null,'파이썬3','홍길동3', '플레이데이터1'),
(null,'파이썬4','홍길동4', '플레이데이터2')
;

insert into customertbl
values
('c001','고객1'), 
('c002','고객2'), 
('c003','고객3'), 
('c004','고객4'), 
('c005','고객5') 
;
select * from booktbl;
-- ordertbl을 채워주세요
insert into ordertbl
values
('c001', 1, 10000, 2),
('c001', 2, 10000, 1),
('c001', 3, 5000, 20),
('c002', 1, 10000, 1),
('c003', 1, 10000, 1),
('c003', 2, 10000, 1)
;