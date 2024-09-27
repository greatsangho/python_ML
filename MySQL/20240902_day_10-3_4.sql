CREATE DEFINER=`root`@`localhost` PROCEDURE `ifProc4`(in p_jumsu int)
BEGIN
	declare hakjum varchar(2);
	if p_jumsu >=90 then
		set hakjum = 'A';
	elseif p_jumsu >=80 then
		set hakjum = "B";
	elseif p_jumsu >=80 then
		set hakjum = "C";
	elseif p_jumsu >=80 then
		set hakjum = "D";
	else
		set hakjum = "F";
	end if;        
    select concat('점수==>',p_jumsu) as 'jumsu', concat('학점==>',hakjum) as 'hakjum';
END