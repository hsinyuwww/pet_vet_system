CREATE DATABASE petvet_system;
USE petvet_system;

CREATE TABLE Owner (
    owner_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE Veterinarian (
    vet_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    specialization VARCHAR(100)
);

CREATE TABLE Pet (
    pet_id INT PRIMARY KEY AUTO_INCREMENT,
    owner_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    gender ENUM('Male', 'Female', 'Unknown') NOT NULL,
    weight DECIMAL(5,2),
    FOREIGN KEY (owner_id) REFERENCES Owner(owner_id)
        ON DELETE CASCADE ON UPDATE CASCADE 				-- If the owner leaves the system, the pet leaves the system as well.
);

CREATE TABLE Medical_record (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    pet_id INT NOT NULL,
    vet_id INT NOT NULL,
    visit_date DATE NOT NULL,
    diagnosis TEXT NOT NULL,
    treatment TEXT NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES Pet(pet_id)
        ON DELETE CASCADE ON UPDATE CASCADE,			-- The medical records are deleted if the pet is deleted.
    FOREIGN KEY (vet_id) REFERENCES Veterinarian(vet_id)
        ON DELETE RESTRICT ON UPDATE CASCADE			-- The medical records always stay in the system as long as the pet is in the system.
);

CREATE TABLE Pet_Vet (
    pet_id INT,
    vet_id INT,
    PRIMARY KEY (pet_id, vet_id),
    FOREIGN KEY (pet_id) REFERENCES Pet(pet_id)
        ON DELETE CASCADE ON UPDATE CASCADE,			-- If a pet is gone, this relationship no longer holds.
    FOREIGN KEY (vet_id) REFERENCES Veterinarian(vet_id)
        ON DELETE CASCADE ON UPDATE CASCADE				-- Same reasoning as above.
);

CREATE TABLE Service (
	service_id INT PRIMARY KEY AUTO_INCREMENT,
    description VARCHAR(200) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    duration TIME NOT NULL
);

CREATE TABLE Appointment (
	appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_date DATE NOT NULL,
    appoinment_time TIME NOT NULL,
    appointment_status ENUM('Scheduled', 'Completed', 'Cancelled', 'No-Show') NOT NULL DEFAULT 'Scheduled',
    pet_id INT NOT NULL,
	vet_id INT NOT NULL,
    service_id INT NOT NULL,
    owner_id INT NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES Pet(pet_id)
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (vet_id) REFERENCES Veterinarian(vet_id)
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (owner_id) REFERENCES Owner(owner_id)
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (service_id) REFERENCES Service(service_id)
		ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Bill (
	bill_id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_status ENUM('Pending', 'Paid', 'Refunded', 'Failed') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
		ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Medication (
	medication_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    how_to_use VARCHAR(100) NOT NULL
);

CREATE TABLE Prescription (
	prescription_id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT NOT NULL,
    medication_id INT NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (medication_id) REFERENCES Medication(medication_id)
		ON DELETE CASCADE ON UPDATE CASCADE
);

-- Sample data for PetVet System
-- Insert Owners
INSERT INTO Owner (name, email, phone, address) VALUES
('John Smith', 'john.smith@email.com', '+1-555-0101', '123 Main St, Boston, MA'),
('Emma Wilson', 'emma.w@email.com', '+1-555-0102', '456 Oak Ave, Boston, MA'),
('Michael Brown', 'michael.b@email.com', '+1-555-0103', '789 Pine Rd, Cambridge, MA'),
('Sarah Johnson', 'sarah.j@email.com', '+1-555-0104', '321 Elm St, Somerville, MA'),
('David Lee', 'david.lee@email.com', '+1-555-0105', '654 Maple Dr, Brookline, MA'),
('Jennifer Adams', 'jen.adams@email.com', '+1-555-0106', '111 Beach Rd, Boston, MA'),
('Robert Taylor', 'rob.taylor@email.com', '+1-555-0107', '222 River St, Cambridge, MA'),
('Lisa Martinez', 'lisa.m@email.com', '+1-555-0108', '333 Lake Ave, Brookline, MA'),
('James Wilson', 'james.w@email.com', '+1-555-0109', '444 Forest Dr, Somerville, MA'),
('Patricia Chen', 'pat.chen@email.com', '+1-555-0110', '555 Hill St, Boston, MA'),
('Thomas Baker', 'tom.baker@email.com', '+1-555-0111', '666 Valley Rd, Cambridge, MA'),
('Mary Johnson', 'mary.j@email.com', '+1-555-0112', '777 Mountain Ave, Brookline, MA'),
('Kevin Patel', 'kevin.p@email.com', '+1-555-0113', '888 Ocean Dr, Boston, MA'),
('Amanda White', 'amanda.w@email.com', '+1-555-0114', '999 Sky St, Somerville, MA'),
('Richard Lee', 'richard.l@email.com', '+1-555-0115', '101 Star Ave, Cambridge, MA');

-- Insert Veterinarians
INSERT INTO Veterinarian (name, phone, email, specialization) VALUES
('Dr. Lisa Anderson', '+1-555-0201', 'dr.anderson@petvet.com', 'General Practice'),
('Dr. James Wilson', '+1-555-0202', 'dr.wilson@petvet.com', 'Surgery'),
('Dr. Maria Garcia', '+1-555-0203', 'dr.garcia@petvet.com', 'Dermatology'),
('Dr. Robert Chen', '+1-555-0204', 'dr.chen@petvet.com', 'Cardiology'),
('Dr. Emily White', '+1-555-0205', 'dr.white@petvet.com', 'General Practice'),
('Dr. Sarah Palmer', '+1-555-0206', 'dr.palmer@petvet.com', 'Orthopedics'),
('Dr. Michael Zhang', '+1-555-0207', 'dr.zhang@petvet.com', 'Internal Medicine'),
('Dr. Rachel Green', '+1-555-0208', 'dr.green@petvet.com', 'General Practice'),
('Dr. David Kim', '+1-555-0209', 'dr.kim@petvet.com', 'Dentistry'),
('Dr. Jessica Brown', '+1-555-0210', 'dr.brown@petvet.com', 'Emergency Care'),
('Dr. Christopher Lee', '+1-555-0211', 'dr.lee@petvet.com', 'Neurology'),
('Dr. Ashley Rodriguez', '+1-555-0212', 'dr.rodriguez@petvet.com', 'Oncology'),
('Dr. William Taylor', '+1-555-0213', 'dr.taylor@petvet.com', 'General Practice'),
('Dr. Elizabeth Chen', '+1-555-0214', 'dr.chen.e@petvet.com', 'Surgery'),
('Dr. Daniel Martinez', '+1-555-0215', 'dr.martinez@petvet.com', 'Dermatology');

-- Insert Services
INSERT INTO Service (description, cost, duration) VALUES
('Regular Checkup', 50.00, '00:30:00'),
('Vaccination', 75.00, '00:20:00'),
('Surgery - Minor', 200.00, '01:00:00'),
('Surgery - Major', 500.00, '02:00:00'),
('Dental Cleaning', 150.00, '01:00:00'),
('X-Ray', 125.00, '00:45:00'),
('Laboratory Tests', 100.00, '00:30:00'),
('Grooming - Basic', 45.00, '01:00:00'),
('Grooming - Full', 80.00, '02:00:00'),
('Emergency Visit', 150.00, '00:45:00'),
('Ultrasound', 175.00, '00:45:00'),
('Blood Work', 90.00, '00:30:00'),
('Microchip Implant', 45.00, '00:20:00'),
('Eye Examination', 85.00, '00:45:00'),
('Allergy Testing', 200.00, '01:00:00'),
('Physical Therapy', 120.00, '01:00:00'),
('Behavior Consultation', 95.00, '01:00:00');

-- Insert Medications
INSERT INTO Medication (name, cost, how_to_use) VALUES
('AmoxiPet 250mg', 25.00, 'One tablet twice daily with food'),
('DermaCure Shampoo', 30.00, 'Apply weekly during bath, leave for 5 minutes'),
('HeartGuard Plus', 40.00, 'One tablet monthly'),
('PainAway 50mg', 35.00, 'One tablet daily for pain'),
('FleaGuard', 45.00, 'Apply monthly to back of neck'),
('MultiVit Plus', 20.00, 'One tablet daily with food'),
('JointFlex 500mg', 50.00, 'One tablet daily with food'),
('EarClear Drops', 25.00, '3 drops in affected ear twice daily'),
('ProbioticPlus', 30.00, 'Mix with food once daily'),
('UriCare 250mg', 35.00, 'One tablet twice daily'),
('AllerStop 10mg', 40.00, 'One tablet daily'),
('EyeBright Drops', 28.00, '1-2 drops in affected eye three times daily'),
('CalmingAid', 45.00, 'One treat as needed for anxiety'),
('DentalFresh', 22.00, 'Add to water daily'),
('InflamAway 100mg', 38.00, 'One tablet daily for inflammation'),
('DigestEase', 32.00, 'Mix with food twice daily');

-- Insert Pets
INSERT INTO Pet (owner_id, name, age, gender, weight) VALUES
(1, 'Max', 5, 'Male', 25.50),
(1, 'Luna', 3, 'Female', 15.75),
(2, 'Bella', 2, 'Female', 8.20),
(3, 'Charlie', 4, 'Male', 30.00),
(4, 'Milo', 1, 'Male', 12.40),
(5, 'Bailey', 3, 'Female', 18.90),
(6, 'Rocky', 2, 'Male', 28.30),
(7, 'Daisy', 4, 'Female', 16.80),
(8, 'Cooper', 1, 'Male', 9.50),
(9, 'Molly', 5, 'Female', 23.40),
(10, 'Tucker', 3, 'Male', 31.20),
(11, 'Sadie', 2, 'Female', 14.60),
(12, 'Duke', 6, 'Male', 27.90),
(13, 'Ruby', 1, 'Female', 11.30),
(14, 'Oscar', 4, 'Male', 19.70),
(15, 'Coco', 3, 'Female', 13.40),
(15, 'Kai', 8, 'Male', 19.60);

-- Insert Medical Records
INSERT INTO Medical_record (pet_id, vet_id, visit_date, diagnosis, treatment) VALUES
(1, 1, '2024-11-20', 'Annual checkup', 'Regular vaccination'),
(2, 1, '2024-11-21', 'Minor skin irritation', 'Prescribed anti-inflammatory medication'),
(3, 3, '2024-11-22', 'Dermatitis', 'Prescribed medicated shampoo and oral medication'),
(4, 2, '2024-11-23', 'Sprain in left leg', 'Rest and anti-inflammatory medication'),
(5, 5, '2024-11-24', 'Routine vaccination', 'Administered core vaccines'),
(6, 4, '2024-11-25', 'Heart murmur detected', 'Prescribed heart medication and scheduled follow-up'),
(8, 6, '2024-11-26', 'Limping in right hind leg', 'Prescribed pain medication and rest'),
(9, 7, '2024-11-26', 'Digestive issues', 'Special diet and probiotics'),
(10, 8, '2024-11-26', 'Dental checkup', 'Professional cleaning scheduled'),
(11, 9, '2024-11-27', 'Eye infection', 'Prescribed eye drops'),
(12, 10, '2024-11-27', 'Allergic reaction', 'Antihistamine prescribed'),
(13, 6, '2024-11-27', 'Annual wellness check', 'All clear, vaccines updated'),
(14, 7, '2024-11-27', 'Ear infection', 'Ear drops and cleaning'),
(15, 8, '2024-11-27', 'Urinary tract infection', 'Antibiotics prescribed'),
(16, 9, '2024-11-27', 'Obesity consultation', 'Diet plan provided'),
(17, 10, '2024-11-27', 'Arthritis symptoms', 'Anti-inflammatory medication');

-- Insert Pet-Vet Relationships
INSERT INTO Pet_Vet (pet_id, vet_id) VALUES
(1, 1),
(2, 1),
(3, 3),
(4, 2),
(5, 5),
(6, 4),
(7, 5),
(8, 6),
(9, 7),
(10, 8),
(11, 9),
(12, 10),
(13, 6),
(14, 7),
(15, 8),
(16, 9),
(17, 10);

-- Insert Appointments
INSERT INTO Appointment (appointment_date, appoinment_time, appointment_status, pet_id, vet_id, service_id, owner_id) VALUES
('2024-11-28', '09:00:00', 'Completed', 1, 1, 1, 1),
('2024-11-28', '10:00:00', 'Completed', 3, 3, 2, 2),
('2024-11-28', '14:00:00', 'No-Show', 4, 2, 3, 3),
('2024-11-29', '09:30:00', 'Completed', 2, 1, 2, 1),
('2024-11-29', '11:00:00', 'Cancelled', 5, 5, 1, 4),
('2024-11-29', '15:00:00', 'No-Show', 6, 4, 6, 4),
('2024-11-30', '10:00:00', 'Scheduled', 7, 5, 5, 5),
('2024-11-30', '13:00:00', 'Scheduled', 8, 6, 8, 6),
('2024-11-30', '14:00:00', 'Scheduled', 9, 7, 9, 7),
('2024-11-30', '15:00:00', 'Scheduled', 10, 8, 10, 8),
('2024-12-01', '09:00:00', 'Scheduled', 11, 9, 11, 9),
('2024-12-01', '10:00:00', 'Cancelled', 12, 10, 12, 10),
('2024-12-01', '11:00:00', 'Scheduled', 13, 6, 13, 11),
('2024-12-01', '13:00:00', 'Scheduled', 14, 7, 14, 12),
('2024-12-01', '14:00:00', 'Scheduled', 15, 8, 15, 13),
('2024-12-02', '09:00:00', 'Scheduled', 16, 9, 16, 14),
('2024-12-02', '10:00:00', 'Scheduled', 17, 10, 17, 15);

-- Insert Bills
INSERT INTO Bill (appointment_id, total_amount, payment_status) VALUES
(1, 50.00, 'Paid'),
(2, 75.00, 'Paid'),
(3, 200.00, 'Failed'),
(4, 75.00, 'Paid'),
(5, 50.00, 'Refunded'),
(6, 125.00, 'Failed'),
(7, 150.00, 'Pending'),
(8, 200.00, 'Pending'),
(9, 120.00, 'Paid'),
(10, 95.00, 'Pending'),
(11, 45.00, 'Paid'),
(12, 80.00, 'Refunded'),
(13, 150.00, 'Pending'),
(14, 175.00, 'Paid'),
(15, 90.00, 'Failed'),
(16, 45.00, 'Paid'),
(17, 85.00, 'Pending');

-- Insert Prescriptions
INSERT INTO Prescription (appointment_id, medication_id, dosage, start_date, end_date) VALUES
(2, 1, '1 tablet twice daily', '2024-11-28', '2024-12-05'),
(3, 4, '1 tablet daily', '2024-11-28', '2024-12-12'),
(4, 1, '1 tablet twice daily', '2024-11-29', '2024-12-06'),
(6, 3, '1 tablet monthly', '2024-11-29', '2025-11-29'),
(8, 7, '1 tablet daily', '2024-11-30', '2024-12-14'),
(9, 8, '2 tablets daily', '2024-11-30', '2024-12-07'),
(10, 9, '1 tablet twice daily', '2024-11-30', '2024-12-14'),
(11, 10, '1 tablet daily', '2024-12-01', '2024-12-15'),
(12, 11, '1 tablet as needed', '2024-12-01', '2024-12-31'),
(13, 12, '2 drops three times daily', '2024-12-01', '2024-12-08'),
(14, 13, '1 treat as needed', '2024-12-01', '2025-01-01'),
(15, 14, 'Mix with water daily', '2024-12-01', '2024-12-31'),
(16, 15, '1 tablet daily', '2024-12-02', '2024-12-16'),
(17, 16, 'Mix with food twice daily', '2024-12-02', '2024-12-16');
