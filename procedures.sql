use petvet_system;

drop procedure if exists schedule_view;
DELIMITER $$
create procedure schedule_view(vet_id_p int, selection int, date_p date)
   begin
   if selection = 1 then
		SELECT * from appointment
        where vet_id = vet_id_p and appointment_date = curdate();
	elseif selection = 2 then
		select * from appointment
        where vet_id = vet_id_p and appointment_date between curdate() and curdate() + interval 7 day;
	else
		select * from appointment
        where vet_id = vet_id_p and appointment_date = date_p;
	end if;
    
    end $$
DELIMITER ;

drop procedure if exists patient_search;
DELIMITER $$
create procedure patient_search(IN pet_id_p int, IN pet_name varchar(32), IN vet_id_p int)
	begin
    
    if pet_id_p = 0 then
		select p.name, p.age, p.gender, p.weight, p.owner_id, 
			   mr.diagnosis, mr.treatment, mr.visit_date,
               md.name as medicine, md.cost, md.how_to_use from pet p
			left join medical_record mr on mr.pet_id = p.pet_id
            left join appointment ap on ap.pet_id = p.pet_id
            left join prescription pr on ap.appointment_id = pr.appointment_id
            left join medication md using (medication_id)
            where p.name = pet_name and 
                  ap.vet_id = vet_id_p;
	else
		select p.name, p.age, p.gender, p.weight, p.owner_id, 
			   mr.diagnosis, mr.treatment, mr.visit_date,
               md.name as medicine, md.cost, md.how_to_use from pet p
			left join medical_record mr on mr.pet_id = p.pet_id
            left join appointment ap on ap.pet_id = p.pet_id
            left join prescription pr on ap.appointment_id = pr.appointment_id
            left join medication md using (medication_id)
            where p.pet_id = pet_id_p and 
                  ap.vet_id = vet_id_p;
	end if;
    
	end $$
DELIMITER ;

drop procedure if exists create_new_record;
DELIMITER $$
create procedure create_new_record(IN pet_id_p int, IN vet_id_p int, IN diagnosis_p varchar(64), IN treatment_p varchar(1000))
	begin
    declare relation_exists int;
	select count(*) into relation_exists from pet_vet where pet_id_p = pet_id and vet_id_p = vet_id;
    if relation_exists = 0 then
		insert into pet_vet (pet_id, vet_id) value (pet_id_p, vet_id_p);
    end if;
    
	insert into medical_record (pet_id, vet_id, visit_date, diagnosis, treatment) value (pet_id_p, vet_id_p, curdate(), diagnosis_p, treatment_p);
    end $$
DELIMITER ;

call create_new_record(1, 1, "something", "something");
select count(*) from pet_vet where 1 = pet_id and 1 = vet_id;

drop procedure if exists update_record;
DELIMITER $$
create procedure update_record(IN record_id_p int, IN diagnosis_p varchar(100), IN treatment_p varchar(100))
	begin
    if diagnosis_p = "" then
		update medical_record
			set treatment = treatment_p
            where record_id = record_id_p;
	elseif treatment_p = "" then
		update medical_record
			set diagnosis = diagnosis_p
            where record_id = record_id_p;
	else
		update medical_record
			set diagnosis = diagnosis_p and treatment = treatment_p
            where record_id = record_id_p;
    end if;
    
	end $$
DELIMITER ;

drop procedure if exists update_profile;
DELIMITER $$
create procedure update_profile(IN vet_id_p int, IN name_p varchar(64), IN phone_p varchar(16), IN email_p varchar(32), IN specialization_p varchar(64))
	begin
    
    if name_p != "" then
		update veterinarian
			set name = name_p
            where vet_id = vet_id_p;
	elseif phone_p != "" then
		update veterinarian
			set phone=phone_p
            where vet_id = vet_id_p;
	elseif email_p != "" then
		update veterinarian
			set email=email_p
            where vet_id = vet_id_p;
	elseif specialization_p != "" then
		update veterinarian
			set specialization=specialization_p
            where vet_id = vet_id_p;
	end if;
    
    end $$
DELIMITER ;