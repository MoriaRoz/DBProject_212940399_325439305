ALTER TABLE patient
ADD COLUMN gender CHAR(1),
ADD COLUMN address VARCHAR (30),
ADD COLUMN phone INTEGER,
ADD COLUMN is_disabled CHAR(1),
ADD COLUMN medical_equipment VARCHAR (20);

ALTER TABLE volunteer
ADD COLUMN city_of_residence VARCHAR(30),
ADD FOREIGN KEY (city_of_residence) REFERENCES city(name);

CREATE TABLE driver (
  volunteer_id INT PRIMARY KEY,
  license_number INTEGER,
  night_avail CHAR(1),
  FOREIGN KEY (volunteer_id) REFERENCES volunteer(volunteer_id)
);

CREATE TABLE transport_assistant (
  volunteer_id INT PRIMARY KEY,
  has_medical_training CHAR(1),
  FOREIGN KEY (volunteer_id) REFERENCES volunteer(volunteer_id)
);

CREATE TABLE vehicle (
  vehicle_id SERIAL PRIMARY KEY,
  license_plate INTEGER,
  type VARCHAR(20),
  capacity INTEGER
);

CREATE TABLE destination (
  destination_name VARCHAR(35) PRIMARY KEY,
  destination_address VARCHAR(50) PRIMARY KEY,
  destination_type VARCHAR(20),
  destination_city VARCHAR(30),
  FOREIGN KEY (destination_city) REFERENCES city(name)
);

CREATE TABLE ride (
  ride_id SERIAL PRIMARY KEY,
  pickup_time TIME,
  destination_name VARCHAR(35),
  destination_address VARCHAR(50),
  vehicle_id INT,
  driver_id INT,
  assistant_id INT,
  volunteering_id INT,
  FOREIGN KEY (destination_name) REFERENCES destination(destination_name),
FOREIGN KEY (  destination_address) REFERENCES destination(  destination_address),
  FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id),
  FOREIGN KEY (driver_id) REFERENCES driver(volunteer_id),
  FOREIGN KEY (assistant_id) REFERENCES transport_assistant(volunteer_id),
  FOREIGN KEY (volunteering_id) REFERENCES volunteering(volunteering_id)
);