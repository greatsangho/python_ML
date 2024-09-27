CREATE DEFINER=`root`@`localhost` PROCEDURE `ifProc`()
BEGIN
	declare var1 int;
    set var1 = 100;
    if var1 = 100 then
		select '100입니다';
	else
		select '100이 아닙니다';
    end if;
END