CREATE DEFINER=`root`@`localhost` PROCEDURE `ifProc5`()
BEGIN
	declare emp_no_var int;
	declare hireDate date; -- 입사일
    declare curDate date; -- 현재 날짜
	declare days int; -- 근무한 일수
    declare done int default 0; -- 선언 및 초기화
    
    -- 커서 선언
    declare cursor_emp cursor for
    select emp_no, hire_date
    from employees.employees; -- cursor 순환객체
    -- 커서가 데이터를 찾는 과정에서 더이상 찾을 수 없을 때
    declare continue handler for not found set done = 1;
    set curDate = current_date(); -- 현재 날짜
    
    open cursor_emp;
    -- 순환
    read_loop: loop
		-- 커서가 데이터를 가져오도록 fetch
        fetch cursor_emp into emp_no_var, hireDate;
        if done then
			leave read_loop;
		end if;

		set days = datediff(curdate, hiredate);
		if (days/365) >= 5 then -- 입사한지 5년이 지났으면
			select concat(emp_no_var, ': 입사한지 ',days, '일이 지났습니다.');
		else
			select concat(emp_no_var, ': 입사한지 ',days, '일밖에 안되었습니다..');
		end if;
	end loop;
END