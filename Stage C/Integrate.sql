-- Patient:
ALTER TABLE patient
ADD COLUMN gender CHAR(1),
ADD COLUMN address VARCHAR (30),
ADD COLUMN phone INTEGER,
ADD COLUMN is_disabled CHAR(1),
ADD COLUMN medical_equipment VARCHAR (20);

INSERT INTO patient (patient_id, first_name, last_name, birthday, address, is_disabled, gender, medical_equipment, phone)
SELECT Patient_ID, First_Name, Last_Name, Date_of_Birth, Address, Is_Disabled, Gender, Medical_Equipment, Phone_Number
FROM patient_temp;

-- Volunteer:
ALTER TABLE volunteer
ADD COLUMN city_of_residence VARCHAR(30),
ADD FOREIGN KEY (city_of_residence) REFERENCES city(name);

INSERT INTO volunteer (volunteer_id, first_name, last_name, birthday, phone, active, city_of_residence)
SELECT volunteer_id, first_name, last_name, date_of_birth, phone_number, 'Y', city
FROM volunteer_temp;

-- Driver:
CREATE TABLE driver (
  volunteer_id INT PRIMARY KEY,
  license_number INTEGER,
  night_avail CHAR(1),
  FOREIGN KEY (volunteer_id) REFERENCES volunteer(volunteer_id));

INSERT INTO driver (volunteer_id, license_number, night_avail)
SELECT volunteer_id, license_number, night_avail
FROM driver_temp;

-- Transport_assistant:
CREATE TABLE transport_assistant (
  volunteer_id INT PRIMARY KEY,
  has_medical_training CHAR(1),
  FOREIGN KEY (volunteer_id) REFERENCES volunteer(volunteer_id));

INSERT INTO transport_assistant (volunteer_id, has_medical_training)
SELECT volunteer_id, has_medical_training
FROM transport_assistant_temp;

-- Destination:
CREATE TABLE destination (
  destination_name VARCHAR(35) PRIMARY KEY,
  destination_address VARCHAR(50) PRIMARY KEY,
  destination_type VARCHAR(20),
  destination_city VARCHAR(30),
  FOREIGN KEY (destination_city) REFERENCES city(name));

INSERT INTO destination (destination_name, destination_address, destination_type)
SELECT destination_name, destination_address, destination_type
FROM destination_temp;

UPDATE destination
SET
  destination_address = TRIM(SPLIT_PART(destination_address, ',', 1)),
  destination_city = TRIM(SPLIT_PART(destination_address, ',', 2))
WHERE destination_address LIKE '%,%';

-- Vehicle:
CREATE TABLE vehicle (
  vehicle_id SERIAL PRIMARY KEY,
  license_plate INTEGER,
  type VARCHAR(20),
  capacity INTEGER);

INSERT INTO vehicle (vehicle_id, license_plate, type, capacity)
SELECT vehicle_id, license_plate, type, capacity
FROM vehicle_temp;

-- Ride:
CREATE TABLE ride (
  volunteering_id INT PRIMARY KEY,
  pickup_time TIME,
  destination_name VARCHAR(35),
  destination_address VARCHAR(50),
  vehicle_id INT,
  driver_id INT,
  assistant_id INT,
  FOREIGN KEY (volunteering_id) REFERENCES volunteering(volunteering_id),
  FOREIGN KEY (destination_name,destination_address) REFERENCES destination(destination_name, destination_address),
  FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id),
  FOREIGN KEY (driver_id) REFERENCES driver(volunteer_id),
  FOREIGN KEY (assistant_id) REFERENCES transport_assistant(volunteer_id));

INSERT INTO ride (volunteering_id, pickup_time, destination_name, vehicle_id, driver_id, assistant_id)
SELECT ride_id, pickup_time, destination_name, vehicle_id, driver_id, assistant_id
FROM ride_temp
WHERE ride_id IN (SELECT volunteering_id FROM volunteering);