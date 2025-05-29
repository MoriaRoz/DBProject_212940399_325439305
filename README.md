# Volunteer Management System - Ezer Mizion  

Moria Rozenfeld & Tehila Shraga  
**System:** Ezer Mizion  
**Unit:** Volunteer Division  

## Table of Contents  
- [Introduction](#introduction)  
- [Entity Relationship Diagram (ERD)](#entity-relationship-diagram-erd)  
- [Data Structure Diagram (DSD)](#data-structure-diagram-dsd)
- [Insert data to table](#insert-data-to-table)
  - [Import CSV Files](#Import-CSV-Files)
  - [Pyhton](#Pyhton)
  - [Mockaroo](#Mockaroo)
- [Backup and Restore](#Backup-and-Restore)
- [Queries](#Queries)
    - [Select queries](#Select-queries)
    - [Update queries](#Update-queries)
    - [Delete queries](#Delete-queries)
- [Constraint](#Constraint)
- [Rollback & Commit](#Rollback-&-Commit)
    - [Rollback](#Rollback)
    - [Commit](#Commit)
- [Integration](#Integration)
    - [Reverse-Engineering Algorithm](#Reverse-Engineering-Algorithm)
    - [new ERD](#new-ERD)
    - [new DSD](#new-DSD)
    - [Integrated ERD](#Integrated-ERD)
    - [Integrated DSD](#Integrated-DSD)
    - [Decisions](#Decisions)
    - [Integration process](#Integration-process)
- [Views](#Views)

## Introduction  
Ezer Mitzion's volunteer management system is used to manage and organize volunteers, volunteer activities with patients, and events intended for volunteers.  
The system records information about volunteers, the various volunteering activities, patients, events, cities across the country, and the areas of volunteering that take place in the organization.

#### Main functionality
* Manage volunteers and their activity status.  
* Assign volunteers to specific volunteering tasks.  
* Record and track patient-volunteer interactions.  
* Organize and manage volunteer events.  
* Log volunteering sessions with details (date, duration, report).  

## Entity Relationship Diagram (ERD)  
![ERD](Stage%20A/ERD.png)
## Data Structure Diagram (DSD)  
![DSD](Stage%20A/DSD.png)

## Insert data to table 
### Import CSV Files  
![image](https://github.com/user-attachments/assets/c62f508e-ad13-4eaa-a757-0952ed72bc88)
![image](https://github.com/user-attachments/assets/a647b170-4214-4169-b5bb-e11e75ee75d4)     

### Pyhton  
![image](https://github.com/user-attachments/assets/6ea79551-7cfc-4262-ac53-983d3f4a37c6)  
![image](https://github.com/user-attachments/assets/4a789652-3df1-4343-ad58-5dc1175e8d5e)  

### Mockaroo  
![patient_mockaroo](Stage%20A/mockarooFiles/patient_mockaroo.png)  

## Backup and Restore  
![image](https://github.com/user-attachments/assets/92392fcb-11e0-49d6-8c3e-8ad70c355d6d)
![image](https://github.com/user-attachments/assets/f2469c7d-23c9-46a8-9bc1-c4e63720f723)


## Queries  
### Select queries
##### 1. The query displays the volunteer hours of each volunteer by month.  
![image](https://github.com/user-attachments/assets/e6df3705-355e-4be5-aa78-bda997b9967f)   
  
#### 2. The query displays the average number of attendees at events by city.
![image](https://github.com/user-attachments/assets/58890d29-3073-4e5b-a39d-bbe9bce907f7)  
  
#### 3. The query displays the average volunteer hours for each age group among the groups: 16-18,19-25,26-40,41-60,60+
![image](https://github.com/user-attachments/assets/85a6b61c-d1dc-4022-98b2-f8d5f2a73130)
![image](https://github.com/user-attachments/assets/4f922844-e771-4023-8d57-dfc281bcc6f4)  
  
#### 4. The query displays all volunteers who have a birthday in the current month and calculates their age.
![image](https://github.com/user-attachments/assets/cff77f20-381b-4e90-9eec-81eac89a3ae1)  

#### 5. The query displays the 50 outstanding volunteers of the past year, that is, the 50 volunteers who volunteered the most volunteer hours.
![image](https://github.com/user-attachments/assets/e672c367-a4f4-4f7b-beeb-57c1cd556e05)  

#### 6. The query displays the number of active volunteers in each region.
![image](https://github.com/user-attachments/assets/f6692d91-7462-4a6f-8cb7-2cd342988c33)  

#### 7. The query displays the patients who have not visited them in the past year.
![image](https://github.com/user-attachments/assets/418c1db7-0394-466f-bc5c-24fcdc0970e1)  

#### 8. The query displays the average number of participants in events, by event type and by year.
![image](https://github.com/user-attachments/assets/b5de30c0-216e-4ba6-bb2d-272292e89c81)  
  

### Update queries
#### 1. The query updates volunteers to be inactive if they have not participated in a volunteer or event in the past year.   
before:    
![image](https://github.com/user-attachments/assets/1cb18d47-76fd-4ae0-bb1a-b174115c04e1)   
running:  
![image](https://github.com/user-attachments/assets/2fadc990-b5c2-4acf-905e-f35e51bd3d94)   
after:    
![image](https://github.com/user-attachments/assets/1d55aa46-9a58-4f4a-8a49-204755d88e78)   
  

#### 2. The query updates that for events that take place in the north or south, it is impossible to come with a companion, so the plus one will be FALSE.
before:  
![image](https://github.com/user-attachments/assets/3206a3e1-95ea-405e-8622-6044b62931f0)  
running:  
![image](https://github.com/user-attachments/assets/6cee5c1d-562b-423a-ab99-6dd51c6a2faa)  
after:  
![image](https://github.com/user-attachments/assets/9b51a9d9-8fb2-433a-9a7f-9c855aebe6b5)  
  
#### 3. The query updates that volunteers under the age of 18 cannot volunteer on the evening shift, but only on the morning shift.
before:  
![image](https://github.com/user-attachments/assets/1431b391-5bc4-4ba5-b922-fafe198b0ce1)  
running:  
![image](https://github.com/user-attachments/assets/9841b41d-3cf4-465d-b2a8-47ea567737d0)  
after:  
![image](https://github.com/user-attachments/assets/941e040d-273e-4d2e-8e82-892ea182d7aa)  
  

### Delete queries
#### 1. The query deletes all volunteers who have not participated in volunteering and events in the last two years.  
before:  
![image](https://github.com/user-attachments/assets/7c53f25e-97b5-47d2-a1ad-93da84b3fb6d)  
running:  
![image](https://github.com/user-attachments/assets/7f7097d6-ac6f-431a-b692-4311af9cfa29)  
![image](https://github.com/user-attachments/assets/14160a1e-b320-4747-8c27-ccf22777d782)  
![image](https://github.com/user-attachments/assets/84e635d0-ff0d-40d5-a9c6-a715496535c6)  
![image](https://github.com/user-attachments/assets/31174d4c-72f2-43ac-93cc-b5967ce24668)  
after:  
![image](https://github.com/user-attachments/assets/1fb6e158-180d-4076-ba47-2a58018d74b2)  

#### 2. The query deletes all patients over the age of 120.  
before:  
![image](https://github.com/user-attachments/assets/895c7bc7-6cf5-4166-a483-562685bc4ed8)  
running:  
![image](https://github.com/user-attachments/assets/41c2f990-31b3-48de-842e-5d2ab2ced2c8)  
after:   
![image](https://github.com/user-attachments/assets/c6855ede-96ca-49c6-af0d-d4dcd181dc8b)  

#### 3. The query deletes events that were more than 5 years ago.  
before:   
![image](https://github.com/user-attachments/assets/99e93c6c-fa23-4a7e-b5cf-57c2fe55cf74)  
running:  
![image](https://github.com/user-attachments/assets/cabf596a-6ce5-4965-b4ed-4f0c2fd8d2b4)  
after:  
![image](https://github.com/user-attachments/assets/842f834c-b61c-48ce-a949-a11b7dda2748)   

## Constraint
### 1. The constraint requires that the patients entered into the table be those with a birth date in the past and not in the future.
ALTER TABLE Patient  
ADD CONSTRAINT chk_patient_birthday  
CHECK (Birthday <= CURRENT_DATE);    
![image](https://github.com/user-attachments/assets/b4561de3-c313-42c2-8e96-c10489159be4)

### 2. The constraint requires that the volunteer's phone number to be entered must not be null.
ALTER TABLE Volunteer  
ALTER COLUMN Phone SET NOT NULL;  
![image](https://github.com/user-attachments/assets/c456f8ee-33d8-4672-9ba5-f79781e7b383)

### 3. The constraint inserts a morning shift-M as the default if no shift was inserted.
ALTER TABLE Volunteering_Participation  
ALTER COLUMN Shift SET DEFAULT 'M';  
![image](https://github.com/user-attachments/assets/a11be685-d5cc-4b13-ae96-f64e78cdcbc2)
![image](https://github.com/user-attachments/assets/f27b9f4e-8e76-4446-bed1-184ecaa420e4)
   

## Rollback & Commit
### Rollback
![image](https://github.com/user-attachments/assets/a246ddc2-37bc-4258-91e7-3cb9c7575176)
![image](https://github.com/user-attachments/assets/fdbd04f8-2088-4745-abb2-0ac58913da4f)

### Commit
![image](https://github.com/user-attachments/assets/a246ddc2-37bc-4258-91e7-3cb9c7575176)
![image](https://github.com/user-attachments/assets/a18ed9a1-92df-433c-b370-6cdbcd9abcea)  

## Integration
### Reverse-Engineering Algorithm
- A table that contains only a primary key without foreign keys:
  → This is a regular entity.
- A table whose primary key contains more than one attribute and none of the attributes is a foreign key:
  → This is a regular entity with a composite key.
- A table that contains a primary key and in addition to it a foreign key:
  → This is a regular entity with a 1:N (one-to-many) relationship to the referenced entity.
- A table where the primary key consists of only two foreign keys:
  → This is a table representing a many-to-many relationship between two entities.
- A table that contains a foreign key that is also the only primary key:
  → This is either a weak entity or an inheritance child.
 - A table that has a foreign key referencing itself:
  → This represents a recursive relationship.  
### new ERD  
![newERD](Stage%20C/newERD.png)
### new DSD
![newDSD](Stage%20C/newDSD.png)
### Integrated ERD
![integratedERD](Stage%20C/integratedERD.png)  
### Integrated DSD
![integratedDSD](Stage%20C/integratedDSD.png)  

### Decisions
- We will keep the following entities without changes: city, event, volunteering, and kindOfVol, along with their existing relationships.  
- In the original ERD, we will add the following attributes to the patient entity: gender, address, phone_number, is_disabled, and medical_equipment.
- We will add the attribute city to the volunteer entity as a foreign key referencing the city entity.
- We will create inheritance for volunteer and add two new entities:
    - driver(volunteer_id, license_number, night_avail)
    - transport_assistant(volunteer_id, has_medical_training)
- The existing relationships will remain connected to the base volunteer entity.
- We will add the following new entities, the relationships between these entities will remain as in the new ERD.:
    - destination(destination_name, destination_address, destination_type, destination_city), Note: destination_city is a foreign key referencing the city table.
    - vehicle(vehicle_id, license_plate, type, capacity)
- We will create an inheritance for volunteering and add a new entity:
    - ride(volunteering_id, pickup_time, vehicle_id, driver_id, assistant_id, destination_name, destination_address) where vehicle_id, driver_id, assistant_id, destination_name, destination_address are foreign keys.
- We will remove the relationship between ride and patient because patient is connected to volunteering.

### Integration process
* Part 1 – Expanding the Patient Entity
    - Using the ALTER TABLE command, we add the following properties to the Patient entity: gender, address, phone_number, is_disabled, medical_equipment.
    - Using the INSERT INTO command, we add the data from the Patient table from the backup we received.
    - To the data we already have in the Patient table, we add the missing fields by importing a CSV file as in the first stage of the project.
![image](https://github.com/user-attachments/assets/678c062b-a4ed-452e-b024-79de697b5526)

* Part 2 – Expanding the Volunteer Table
    - Using the ALTER TABLE command, we add the field city_of_residence to the Volunteer entity.
    - Using the INSERT INTO command, we add the data from the Volunteer table from the backup.
    - To the data we already have in the Volunteer table, we add the missing field by importing a CSV file as in the first stage of the project.
![image](https://github.com/user-attachments/assets/8f2e3693-5f8f-43a4-b7c8-09788a1263d2)

* Part 3 – Creating Inheritance for Volunteer
   - Using the CREATE TABLE command, we create two new tables to represent subtypes of volunteer:
       * driver(volunteer_id, license_number, night_avail)
       * transport_assistant(volunteer_id, has_medical_training)
   - Using the INSERT INTO command, we add the data from the tables from the backup.
![image](https://github.com/user-attachments/assets/eafa1b8b-e599-49f9-95f5-18c4d047f7bb)
![image](https://github.com/user-attachments/assets/89bcff7d-8bb7-4156-91ca-7804d504517c)

* Part 4 – Creating the Destination Table
   - Using the CREATE TABLE command, we create a new table destination(destination_name, destination_address, destination_type, destination_city).
   - We define the destination_city attribute as a foreign key that references the city table.
   - Using the INSERT INTO command, we add the data from the destination table from the backup.
   - In the original table, the city was part of destination_address after the comma, so we ran an update query to break the city into a separate column.
![image](https://github.com/user-attachments/assets/d01934bc-88d8-42c5-8e43-5969e87a8b95)
![image](https://github.com/user-attachments/assets/2e826afc-1e48-447b-8fff-015106474a5c)

* Part 5 – Creating a vehicle table
   - Using the CREATE TABLE command, we create a new table vehicle(vehicle_id, license_plate, type, capacity).
   - Using the INSERT INTO command, we add the data of the vehicle table from the backup.
![image](https://github.com/user-attachments/assets/ab810582-0a7d-44fe-8988-b2ede25e2fbb)

* Part 6 – Creating an inheritance for volunteering
   - Using the CREATE TABLE command, we create a new table ride(volunteering_id, pickup_time, destination_name, destination_address, vehicle_id, driver_id, assistant_id) which is an extension of volunteering.
   - Using the INSERT INTO command, we add the data of the trips table from the backup. The keys of trips and volunteering are of the same type and overlap, so for the ride_id column we inserted what was in the ride_id column.
   - All fields except pickup_time are declared as foreign keys that refer to their corresponding tables.
![image](https://github.com/user-attachments/assets/21528761-0305-4d64-b3e9-bd0e34a867b9)
![image](https://github.com/user-attachments/assets/f99f93ed-5444-4351-9465-1ee2d39b4e7b)

## Views
### view_volunteer_participation:
This view displays the participation of each volunteer in volunteering activities, including their contact details, activity type, date, and report.
![image](https://github.com/user-attachments/assets/e7d369ed-2673-4f80-a72e-27196126d159)
- Query 1:
  Returns how many volunteering activities were performed by type.
  ![image](https://github.com/user-attachments/assets/c8517c2d-c774-4df8-b856-bdc94f85f3fc)

- Query 2:
  Lists volunteers who participated in at least 3 volunteering activities, sorted by their participation count.
  ![image](https://github.com/user-attachments/assets/db26e278-6fd7-4e7e-a9e4-ada818c30e90)

### view_rides_schedule:
This view combines ride details with volunteering information, including date, pickup time, destination, vehicle, driver, and medical assistant.
![image](https://github.com/user-attachments/assets/60aca2fb-adcc-4bf4-bcfc-b49923984f4e)
![image](https://github.com/user-attachments/assets/8c330ad9-e5dd-4142-84c4-95ce4bae0d28)
- Query 1:
   Shows all rides that were completed without a medical assistant, including the driver’s name and phone number.
  ![image](https://github.com/user-attachments/assets/db8fbc67-6e5a-42ae-a0b1-d1621c3d9826)

- Query 2:
  Counts the number of rides that took place per month and year.
  ![image](https://github.com/user-attachments/assets/a873cc3e-32d4-4c50-8d97-9e51b6a88943)


