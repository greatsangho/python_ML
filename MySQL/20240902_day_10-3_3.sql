CREATE DEFINER=`root`@`localhost` PROCEDURE `ifProc3`(in p_emp_no int)
BEGIN
	declare hireDate date; -- 입사일
    declare curDate date; -- 현재 날짜
    declare days int; -- 근무한 일수
    
    select hire_date into hireDate
	from employees.employees
	where emp_no = p_emp_no;
    set curDate = current_date(); -- 현재 날짜
    set days = datediff(curdate, hiredate);
    if (days/365) >= 5 then -- 입사한지 5년이 지났으면
		select concat('입사한지 ',days, '일이 지났습니다.');
	else
		select concat('입사한지 ',days, '일밖에 안되었습니다..');
	end if;
    
END