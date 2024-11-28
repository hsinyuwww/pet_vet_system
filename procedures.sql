use petvet_system;

drop procedure if exists schedule_view;
DELIMITER $$
create procedure schedule_view(vet_id_p int, selection int)
   begin
   if selection = 1 then
		SELECT * from appointment
        where vet_id = vet_id_p and appointment_date = curdate();
	elseif selection = 2 then
		select * from appointment
        where vet_id = vet_id_p and appointment_date between curdate() and curdate() + interval 7 day;
	else
		select * from appointment
        where vet_id = vet_id_p;
	end if;
    
    end $$
DELIMITER ;