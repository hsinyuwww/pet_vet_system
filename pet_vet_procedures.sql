USE petvet_system;

-- Owner Profile Management
DELIMITER $$
CREATE PROCEDURE sp_verify_owner(IN p_owner_id INT)
BEGIN
    SELECT owner_id, name FROM Owner 
    WHERE owner_id = p_owner_id;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_get_owner_profile(IN p_owner_id INT)
BEGIN
    DECLARE owner_exists INT;
    
    SELECT COUNT(*) INTO owner_exists
    FROM Owner WHERE owner_id = p_owner_id;
    
    IF owner_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Owner ID not exist';
    ELSE
        SELECT name, email, phone, address 
        FROM Owner 
        WHERE owner_id = p_owner_id;
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_update_owner_profile(
    IN p_owner_id INT,
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_phone VARCHAR(20),
    IN p_address TEXT
)
BEGIN
    DECLARE email_exists INT;
    IF p_name IS NULL OR p_email IS NULL OR p_phone IS NULL OR p_address IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'All fields are required';
    END IF;
    SELECT COUNT(*) INTO email_exists
    FROM Owner 
    WHERE email = p_email AND owner_id != p_owner_id;
    
    IF email_exists > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Email already exists';
    END IF;
    
    UPDATE Owner 
    SET name = p_name,
        email = p_email,
        phone = p_phone,
        address = p_address
    WHERE owner_id = p_owner_id;
    
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Owner not found';
    END IF;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_get_owner_pets(IN p_owner_id INT)
BEGIN
    DECLARE owner_exists INT;
    
    SELECT COUNT(*) INTO owner_exists
    FROM Owner WHERE owner_id = p_owner_id;
    
    IF owner_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Owner ID not exist';
    ELSE
        SELECT p.*, mr.last_visit FROM Pet p
        LEFT JOIN (SELECT pet_id, MAX(visit_date) as last_visit FROM Medical_record
        GROUP BY pet_id ) mr ON p.pet_id = mr.pet_id
        WHERE p.owner_id = p_owner_id;
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_add_pet(
    IN p_owner_id INT,
    IN p_name VARCHAR(50),
    IN p_age INT,
    IN p_gender ENUM('Male', 'Female', 'Unknown'),
    IN p_weight DECIMAL(5,2)
)
BEGIN
    DECLARE owner_exists INT;
    
    -- Input validation
    IF p_name IS NULL OR p_age IS NULL OR p_gender IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'These fields cannot be null';
    END IF;
    
    IF p_age < 0 OR p_age > 30 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'The age is invalid';
    END IF;
    
    IF p_weight <= 0 OR p_weight > 100 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'The weight is invalid';
    END IF;
    
    IF p_gender NOT IN ('Male', 'Female', 'Unknown') THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Gender must be Male, Female, or Unknown';
    END IF;
    
    SELECT COUNT(*) INTO owner_exists
    FROM Owner WHERE owner_id = p_owner_id;
    
    IF owner_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Owner is not found';
    END IF;
    
    INSERT INTO Pet (owner_id, name, age, gender, weight)
    VALUES (p_owner_id, p_name, p_age, p_gender, p_weight);
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_remove_pet(
    IN p_owner_id INT,
    IN p_pet_id INT
)
BEGIN
    DECLARE pet_exists INT;
    
    SELECT COUNT(*) INTO pet_exists
    FROM Pet 
    WHERE pet_id = p_pet_id AND owner_id = p_owner_id;
    
    IF pet_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Pet not found or does not belong to this owner';
    END IF;
    
    DELETE FROM Pet WHERE pet_id = p_pet_id AND owner_id = p_owner_id;
END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_owner_appointments;
DELIMITER $$
CREATE PROCEDURE sp_get_owner_appointments(
    IN p_owner_id INT
)
BEGIN
    SELECT a.*, p.name as pet_name, v.name as vet_name, 
           s.description as service_desc, s.cost, b.payment_status 
    FROM Appointment a
    JOIN Pet p ON a.pet_id = p.pet_id
    JOIN Veterinarian v ON a.vet_id = v.vet_id
    JOIN Service s ON a.service_id = s.service_id
    JOIN Bill b ON a.appointment_id = b.appointment_id
    WHERE a.owner_id = p_owner_id
    ORDER BY a.appointment_date, a.appoinment_time;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_schedule_appointment(
  IN p_owner_id INT,
  IN p_pet_id INT,
  IN p_vet_id INT,
  IN p_service_id INT,
  IN p_date DATE,
  IN p_time TIME
)
BEGIN
  DECLARE time_conflict INT;
  DECLARE pet_exists INT;
  DECLARE vet_exists INT;
  DECLARE service_exists INT;
  DECLARE new_appointment_id INT;
  DECLARE service_cost DECIMAL(10,2);
  
  IF p_date < CURDATE() THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Cannot schedule appointments in the past date';
  END IF;
  
  SELECT COUNT(*) INTO pet_exists
  FROM Pet 
  WHERE pet_id = p_pet_id AND owner_id = p_owner_id;
  
  IF pet_exists = 0 THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'This pet does not exist or belong to this owner';
  END IF;
  
  SELECT COUNT(*) INTO vet_exists
  FROM Veterinarian
  WHERE vet_id = p_vet_id;
  
  IF vet_exists = 0 THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid Veterinarian ID';
  END IF;
  
  SELECT COUNT(*) INTO time_conflict FROM Appointment
  WHERE vet_id = p_vet_id
  AND appointment_date = p_date
  AND appoinment_time = p_time
  AND appointment_status IN ('Scheduled', 'Completed', 'No-Show');
  
  IF time_conflict > 0 THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'This time is not available';
  END IF;
  
  SELECT COUNT(*) INTO service_exists FROM Service WHERE service_id = p_service_id;
   IF service_exists = 0 THEN
       SIGNAL SQLSTATE '45000'
       SET MESSAGE_TEXT = 'Invalid Service ID';
   END IF;

  SELECT cost INTO service_cost FROM Service WHERE service_id = p_service_id;
  
  INSERT INTO Appointment (
      appointment_date, appoinment_time, appointment_status, 
      pet_id, vet_id, service_id, owner_id
  ) VALUES (
      p_date, p_time, 'Scheduled', 
      p_pet_id, p_vet_id, p_service_id, p_owner_id
  );
  
  SET new_appointment_id = LAST_INSERT_ID();
  
  INSERT INTO Bill (appointment_id, total_amount, payment_status)
  VALUES (new_appointment_id, service_cost, 'Pending');

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_cancel_appointment(
    IN p_owner_id INT,
    IN p_appointment_id INT
)
BEGIN
    DECLARE appt_status VARCHAR(20);
    DECLARE appt_date DATE;
    DECLARE appt_time TIME;
    
    SELECT a.appointment_status INTO appt_status
    FROM Appointment a
    WHERE a.appointment_id = p_appointment_id 
    AND a.owner_id = p_owner_id
    LIMIT 1;
    
    -- Validate appointment exists and belongs to owner
    IF appt_status IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid Appointment ID or appointment does not belong to this owner';
    END IF;
    
    IF appt_status != 'Scheduled' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Only scheduled appointments can be cancelled';
    END IF;
    
    IF appt_date < CURDATE() OR (appt_date = CURDATE() AND appt_time < CURTIME()) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot cancel past appointments';
    END IF;
    
	UPDATE Appointment 
	SET appointment_status = 'Cancelled'
	WHERE appointment_id = p_appointment_id;
	
	UPDATE Bill
	SET payment_status = 'Refunded'
	WHERE appointment_id = p_appointment_id;

END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_get_pet_medical_records(
    IN p_pet_id INT
)
BEGIN
    SELECT 
        m.visit_date,
        v.name AS veterinarian,
        v.specialization,
        m.diagnosis,
        m.treatment,
        COALESCE(GROUP_CONCAT(DISTINCT CONCAT(med.name, ' - ', pr.dosage)), 'No prescription') AS prescriptions
    FROM Medical_record m
    JOIN Veterinarian v ON m.vet_id = v.vet_id
    LEFT JOIN Appointment a ON m.pet_id = a.pet_id 
    LEFT JOIN Prescription pr ON a.appointment_id = pr.appointment_id
    LEFT JOIN Medication med ON pr.medication_id = med.medication_id
    WHERE m.pet_id = p_pet_id
    GROUP BY m.record_id, m.visit_date, v.name, v.specialization, m.diagnosis, m.treatment
    ORDER BY m.visit_date DESC;
END $$
DELIMITER ;

use petvet_system;


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