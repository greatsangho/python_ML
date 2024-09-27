use bookrental;
select * from booktbl;
select * from customertbl;
-- 한번 이상 구매한 고객 / 한번도 구매하지 않은 리스트를 출력
select * from ordertbl;
select * from customertbl where customer_id not in
(
	select distinct customer_id from ordertbl
	-- from ordertbl
    -- group by customer_id
)
;

-- 각 고객별 구매 횟수
select customer_id, count(*) from ordertbl group by customer_id;