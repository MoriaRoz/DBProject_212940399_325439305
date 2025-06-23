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
- [PL/pgSQL programs](#PLpgSQL-programs)
    - [Main 1](#Main-1)
        - [Procedura1- assign assistants to future rides](#Procedura1--assign-assistants-to-future-rides)
        - [Trigger1- limit assistant rides](#Trigger1--limit-assistant-rides)
        - [Function1- volunteer schedule](#Function1--volunteer-schedule)
    - [Main 2](#Main-2)
        - [Procedura2- deactivate inactive volunteers](#Procedura2--deactivate-inactive-volunteers)
        - [Trigger2- prevent inactive responsible](#Trigger2--prevent-inactive-responsible)
        - [Function2- top 10 volunteers of week](#Function2--top-10-volunteers-of-week)
- [Graphical interface](#Graphical-interface)
    - [Tools and technologies](#Tools-and-technologies)
    - [Work step](#Work-step)
    - [App operating instructions](#App-operating-instructions)

## Introduction  
Ezer Mitzion's volunteer management system is used to manage and organize volunteers, volunteer activities with patients, and events intended for volunteers.  
The system records information about volunteers, the various volunteering activities, patients, events, cities across the country, and the areas of volunteering that take place in the organization.

**Main functionality**
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
*Insert:*  
![image](https://github.com/user-attachments/assets/c62f508e-ad13-4eaa-a757-0952ed72bc88)
   
*Table:*  
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
1. **The query displays the volunteer hours of each volunteer by month.**  
![image](https://github.com/user-attachments/assets/e6df3705-355e-4be5-aa78-bda997b9967f)    
   
2. **The query displays the average number of attendees at events by city.**  
![image](https://github.com/user-attachments/assets/58890d29-3073-4e5b-a39d-bbe9bce907f7)   
  
3. **The query displays the average volunteer hours for each age group among the groups: 16-18,19-25,26-40,41-60,60+**  
![image](https://github.com/user-attachments/assets/85a6b61c-d1dc-4022-98b2-f8d5f2a73130)  
![image](https://github.com/user-attachments/assets/4f922844-e771-4023-8d57-dfc281bcc6f4)   
  
4. **The query displays all volunteers who have a birthday in the current month and calculates their age.**  
![image](https://github.com/user-attachments/assets/cff77f20-381b-4e90-9eec-81eac89a3ae1)  
  
5. **The query displays the 50 outstanding volunteers of the past year, that is, the 50 volunteers who volunteered the most volunteer hours.**  
![image](https://github.com/user-attachments/assets/e672c367-a4f4-4f7b-beeb-57c1cd556e05)  
  
6. **The query displays the number of active volunteers in each region.**  
![image](https://github.com/user-attachments/assets/f6692d91-7462-4a6f-8cb7-2cd342988c33)  
  
7. **The query displays the patients who have not visited them in the past year.**  
![image](https://github.com/user-attachments/assets/418c1db7-0394-466f-bc5c-24fcdc0970e1)  
  
8. **The query displays the average number of participants in events, by event type and by year.**  
![image](https://github.com/user-attachments/assets/b5de30c0-216e-4ba6-bb2d-272292e89c81)  
  

### Update queries
1. **The query updates volunteers to be inactive if they have not participated in a volunteer or event in the past year.**
     
   *Before:*   
   ![image](https://github.com/user-attachments/assets/1cb18d47-76fd-4ae0-bb1a-b174115c04e1)
     
   *Running:*   
   ![image](https://github.com/user-attachments/assets/2fadc990-b5c2-4acf-905e-f35e51bd3d94)
     
   *After:*   
   ![image](https://github.com/user-attachments/assets/1d55aa46-9a58-4f4a-8a49-204755d88e78)
     
2. **The query updates that for events that take place in the north or south, it is impossible to come with a companion, so the plus one will be FALSE.**
     
   *Before:*  
   ![image](https://github.com/user-attachments/assets/3206a3e1-95ea-405e-8622-6044b62931f0)
     
   *Running:*  
   ![image](https://github.com/user-attachments/assets/6cee5c1d-562b-423a-ab99-6dd51c6a2faa)
     
   *After:*  
   ![image](https://github.com/user-attachments/assets/9b51a9d9-8fb2-433a-9a7f-9c855aebe6b5)
     
3. **The query updates that volunteers under the age of 18 cannot volunteer on the evening shift, but only on the morning shift.**
     
   *Before:*  
   ![image](https://github.com/user-attachments/assets/1431b391-5bc4-4ba5-b922-fafe198b0ce1)
     
   *Running:*  
   ![image](https://github.com/user-attachments/assets/9841b41d-3cf4-465d-b2a8-47ea567737d0)
     
   *After:*  
   ![image](https://github.com/user-attachments/assets/941e040d-273e-4d2e-8e82-892ea182d7aa)    
    

### Delete queries
1. **The query deletes all volunteers who have not participated in volunteering and events in the last two years.**
     
   *before:*  
   ![image](https://github.com/user-attachments/assets/7c53f25e-97b5-47d2-a1ad-93da84b3fb6d)  
     
   *Running:*  
   ![image](https://github.com/user-attachments/assets/7f7097d6-ac6f-431a-b692-4311af9cfa29)  
   ![image](https://github.com/user-attachments/assets/14160a1e-b320-4747-8c27-ccf22777d782)  
   ![image](https://github.com/user-attachments/assets/84e635d0-ff0d-40d5-a9c6-a715496535c6)  
   ![image](https://github.com/user-attachments/assets/31174d4c-72f2-43ac-93cc-b5967ce24668)  
     
   *After:*  
   ![image](https://github.com/user-attachments/assets/1fb6e158-180d-4076-ba47-2a58018d74b2)  
    
2. **The query deletes all patients over the age of 120.**
     
   *Before:*  
   ![image](https://github.com/user-attachments/assets/895c7bc7-6cf5-4166-a483-562685bc4ed8)
     
   *Running:*  
   ![image](https://github.com/user-attachments/assets/41c2f990-31b3-48de-842e-5d2ab2ced2c8)
      
   *After:*  
   ![image](https://github.com/user-attachments/assets/c6855ede-96ca-49c6-af0d-d4dcd181dc8b)
     
3. **The query deletes events that were more than 5 years ago.**
     
   *Before:*  
   ![image](https://github.com/user-attachments/assets/99e93c6c-fa23-4a7e-b5cf-57c2fe55cf74)
     
   *Running:*  
   ![image](https://github.com/user-attachments/assets/cabf596a-6ce5-4965-b4ed-4f0c2fd8d2b4)
     
   *After:*  
   ![image](https://github.com/user-attachments/assets/842f834c-b61c-48ce-a949-a11b7dda2748)     

## Constraint
1. **The constraint requires that the patients entered into the table be those with a birth date in the past and not in the future.**  
   ALTER TABLE Patient  
   ADD CONSTRAINT chk_patient_birthday  
   CHECK (Birthday <= CURRENT_DATE);
     
   ![image](https://github.com/user-attachments/assets/b4561de3-c313-42c2-8e96-c10489159be4)  

3. **The constraint requires that the volunteer's phone number to be entered must not be null.**  
   ALTER TABLE Volunteer  
   ALTER COLUMN Phone SET NOT NULL;
     
   ![image](https://github.com/user-attachments/assets/c456f8ee-33d8-4672-9ba5-f79781e7b383)  

4. **The constraint inserts a morning shift-M as the default if no shift was inserted.**  
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
    - To the data we already have in the patient table, we add the missing fields using SQL update commands - in the update_patients file in the StageC folder.
![image](https://github.com/user-attachments/assets/678c062b-a4ed-452e-b024-79de697b5526)

* Part 2 – Expanding the Volunteer Table
    - Using the ALTER TABLE command, we add the field city_of_residence to the Volunteer entity.
    - Using the INSERT INTO command, we add the data from the Volunteer table from the backup.
    - To the data we already have in the volunteer table, we add the missing field by using SQL update commands - in the update_volunteers file in the StageC folder.
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
   - Using the INSERT INTO command, we insert the rides table data from the backup. The keys for ride and volunteer are of the same type and overlap, so we will insert the rides only if volunteering_id=ride_id.
   - All fields except pickup_time are declared as foreign keys that refer to their corresponding tables.
![image](https://github.com/user-attachments/assets/21528761-0305-4d64-b3e9-bd0e34a867b9)
![image](https://github.com/user-attachments/assets/f99f93ed-5444-4351-9465-1ee2d39b4e7b)

## Views
### view_volunteer_participation:
This view displays the participation of each volunteer in volunteering activities, including their contact details, activity type, date, and report.
![image](https://github.com/user-attachments/assets/e7d369ed-2673-4f80-a72e-27196126d159)  
  
- *Query 1:*
  Returns how many volunteering activities were performed by type.
    
  ![image](https://github.com/user-attachments/assets/c8517c2d-c774-4df8-b856-bdc94f85f3fc)

- *Query 2:*
  Lists volunteers who participated in at least 3 volunteering activities, sorted by their participation count.
    
  ![image](https://github.com/user-attachments/assets/db26e278-6fd7-4e7e-a9e4-ada818c30e90)

### view_rides_schedule:
This view combines ride details with volunteering information, including date, pickup time, destination, vehicle, driver, and medical assistant.
![image](https://github.com/user-attachments/assets/60aca2fb-adcc-4bf4-bcfc-b49923984f4e)  
![image](https://github.com/user-attachments/assets/8c330ad9-e5dd-4142-84c4-95ce4bae0d28)  
  
- *Query 1:*
   Shows all rides that were completed without a medical assistant, including the driver’s name and phone number.  
  ![image](https://github.com/user-attachments/assets/db8fbc67-6e5a-42ae-a0b1-d1621c3d9826)
    
- *Query 2:*
  Counts the number of rides that took place per month and year.  
  ![image](https://github.com/user-attachments/assets/a873cc3e-32d4-4c50-8d97-9e51b6a88943)  

## PL/pgSQL programs
### Main 1
This program runs Procedure1- assign_assistants which automatically assigns available transportation assistants to future trips based on the city and region where the volunteer lives and the trip is going.  
Assigning a transportation assistant to a trip triggers Trigger1 which checks before updating or assigning a new trip if the assistant does not already have 3 trips on that day.  
The program then runs Function1- volunteer_schedule which displays the weekly schedule of a specific volunteer, including their upcoming volunteer meetings, trips (as a driver or assistant), and events.

Execution steps:
* Call the procedure assign_assistants_to_future_rides() to assign assistants to future trips where no assistant is currently defined.
* Call the function get_volunteer_schedule(volunteer_id) for the volunteer ID 10000101, which returns a refcursor containing all scheduled activities for the next 7 days.
  
***Code***
![main1](https://github.com/user-attachments/assets/23633aea-b4f5-4c59-9170-1c05aa567e21)  
  
***Result of Procedure1- assign_assistants***  
![Result of Procedure1- assign_assistants](https://github.com/user-attachments/assets/f7985d27-e2ed-48ff-8b5e-903f056421bb)  
  
***Results of Function1- volunteer_schedule***  
![Results of Function1- volunteer_schedule](https://github.com/user-attachments/assets/c28b6362-480b-4f62-b176-409d2aabaa89)  
  
***Update database-display future rides***  
![image](https://github.com/user-attachments/assets/dc0b9d53-da86-4236-ae77-c096ebb85c19)  
![image](https://github.com/user-attachments/assets/d86bd366-ea11-40eb-9479-eed202964c11)  

#### Procedura1- assign assistants to future rides
This procedure automatically assigns available transport assistants to future rides that do not yet have an assistant.  
It first attempts to find an assistant from the same city as the ride destination. If no suitable city-based assistant is available, it looks for one from the same area.  
It ensures that:  
- Assistants are active.
- There are no scheduling conflicts with other rides, volunteering, or events.
- Assistants do not exceed the daily ride limit (3 per day, enforced via trigger).
   
If an assignment is successful, a confirmation notice is printed. If no suitable assistant is found, a warning is logged.  
(The code in the StageD folder)  
  
*Before:*  
![image](https://github.com/user-attachments/assets/7c669c38-814e-4b0f-be4b-f32384287261)  
  
*Running:*  
![image](https://github.com/user-attachments/assets/db70b1f2-aeb9-49a3-8e2e-bd6d21eeb6ab)
  
*After:*  
![image](https://github.com/user-attachments/assets/440988af-d068-42af-962a-c8988f052f48)
  

#### Trigger1- limit assistant rides
This trigger function ensures that a transport assistant is not assigned to more than 3 rides on the same day.  
When a new ride is inserted or updated:  
- It checks the ride date using the linked volunteering event.  
- If an assistant is assigned, it counts how many other rides they already have on that date.  
- If the assistant has 3 or more rides, the function raises an exception and blocks the operation.  
  
The associated trigger trg_limit_assistant_rides is activated before any INSERT or UPDATE on the ride table, and enforces this daily ride limit per assistant. 
  
*Code:*   
![image](https://github.com/user-attachments/assets/ede4f1cf-46d1-4b7d-b0a9-ce43f295f91a)  
![image](https://github.com/user-attachments/assets/9607ae9f-9054-4666-809c-62e931b95c31)  
   
#### Function1- volunteer schedule
This function returns a refcursor containing the schedule of a given volunteer (v_id) for the upcoming week.  
It performs the following:  
- Verifies that the volunteer exists and is active.
- Collects all activities scheduled for the next 7 days:
    * Volunteering sessions
    * Rides as a driver
    * Rides as an assistant
    * Events
- If the volunteer has no upcoming activities, a fallback message is included.  
  
Results are returned in a sorted schedule (by date and time) via a cursor named 'schedule_cursor'.  
(The code in the StageD folder)  
  
*Running:*  
![image](https://github.com/user-attachments/assets/a6cd2278-1881-47b5-9a67-224d6cf5288e)  
  
Volunteer with no activities this coming week:  
![image](https://github.com/user-attachments/assets/ba20f897-4d18-4082-8d1b-7f4fdddf1932)  
  
Volunteer not present/active:  
![image](https://github.com/user-attachments/assets/49191562-d0c8-47aa-a01f-7f148363d3d0)  
  
Volunteer with this week's activities:  
![image](https://github.com/user-attachments/assets/ef712310-9d76-4e4a-a04c-09e0529558e6)  
  
### Main 2
This program runs Procedure2- deactivate_inactive_volunteers which updates all volunteers who were not part of a volunteering/trip (as an assistant or driver)/event in the last six months as inactive.  
Changing the Active field of a volunteer runs Trigger2- prevent_inactive_responsible which checks before updating a volunteer if he is responsible for a future event or responsible for a certain type of volunteering and if so does not allow him to be changed to inactive.  
Then, the program runs Function2- top_10_volunteers_of_week which displays the 10 outstanding volunteers of the week, that is, the 10 volunteers with the most activities in the previous week.

Execution steps:
* Call the deactivate_inactive_volunteers() procedure to mark volunteers as inactive if they have not participated in any activity in the last six months.  
* Call to get_top_10_volunteers_of_week() function which returns a refcursor with volunteers ranked by activity count during the last week.

***Code***  
![main2](https://github.com/user-attachments/assets/34939d91-2270-4818-bbfe-0460ed9828fc)  
  
***Result of Procedure2- deactivate_inactive_volunteers***  
![Result of Procedure2- deactivate_inactive_volunteers](https://github.com/user-attachments/assets/7d63063f-2dba-41aa-aae9-500850fbf209)  
  
***Result of Function2- top_10_volunteers_of_week***  
![Result of Function2- top_10_volunteers_of_week](https://github.com/user-attachments/assets/952a4230-78bc-4138-91ef-c2c5962b8aa8)  
  
***Database update - showing inactive volunteers in the last six months***  
![before](https://github.com/user-attachments/assets/f05342da-c014-4ab8-9e22-c0be9c1ad178)  
![after](https://github.com/user-attachments/assets/871d86ea-95db-4cbf-85a9-2b14eb3c14ca)  

#### Procedura2- deactivate inactive volunteers
This procedure scans all active volunteers and deactivates those who haven’t participated in any activity in the past 6 months.  
For each such volunteer, it checks four types of activity:  
- Participation in events (`event_participation`)
- Rides as a driver (`ride.driver_id`)
- Rides as an assistant (`ride.assistant_id`)
- Participation in volunteering (`volunteering_participation`)
  
If none of these have been found in the last six months, the volunteer status is updated to ``F'' (inactive), after a pre-update check trigger is fired that checks if they can be updated without active volunteers.  
A success or error notice is printed for each volunteer to log the result.  
At the end, a summary message confirms the process is complete.  
(The code in the StageD folder)
  
*Before:*  
![image](https://github.com/user-attachments/assets/651ccaff-3182-4bce-bf65-84319f3784fe)
  
*Running:*  
![image](https://github.com/user-attachments/assets/6e8ccaa9-c2c4-40cf-bffd-a5acf94457e6)
![image](https://github.com/user-attachments/assets/73965bcb-f681-44cf-b35c-0a9faf96db01)
  
*After:*  
![image](https://github.com/user-attachments/assets/a410afc2-92e0-453b-b97d-2cddef177047)
  
#### Trigger2- prevent inactive responsible
This trigger function prevents the deactivation of a volunteer if they are still responsible for active roles.  
It runs before updating the volunteer table and blocks the change if:  
- The volunteer is assigned to any future events (as event organizer).
- The volunteer is assigned to one or more volunteering types in kindOfVol.
  
If either condition is met, the trigger raises an exception with a clear message and prevents the update.
The associated trigger trg_prevent_inactive_responsible is fired before any UPDATE on the volunteer table and ensures that no active responsibility is left unmanaged when deactivating a volunteer.

*Code:*  
![image](https://github.com/user-attachments/assets/52e8720f-f4d1-4e86-b2de-7f7d020fed79)  
![image](https://github.com/user-attachments/assets/72bb5f6a-f2b6-4352-8808-4f2271d6054d)  
   
#### Function2- top 10 volunteers of week
This function returns a refcursor pointing to the top 10 most active volunteers in the past 7 days.  
It checks activity across four categories:  
- Participation in volunteering shifts
- Rides as a driver
- Rides as an assistant
- Attendance at events
Each occurrence is counted as one activity.   
The function then:  
- Groups all activity records by volunteer
- Ranks volunteers by their total number of activities (in descending order)
- Returns the top 10 in a cursor named 'top10_cursor'

If no activity is found in the past week, a notice is printed and a single-row result with NULL values is returned.  
Any unexpected error during execution is caught, a notice is printed, and a fallback cursor with NULL fields is returned.  
(The code in the StageD folder)
  
*Running:*  
![image](https://github.com/user-attachments/assets/3b8f6a20-b342-41e9-aa50-54ebc8641819)  

## Graphical interface
### Tools and technologies
  - Programming language: Python
  - User interface construction: HTML, CSS, JavaScript
  - Server: Flask
  - Query language, procedures and functions: SQL and PL/pgSQL
  
### Work steps
  - We created a connection to our database.
  - We created 7 screens using HTML, CSS, JavaScript to display the tables: Volunteering, Volunteers, Trips and Volunteer Participation, plus a home screen, a personal area screen, and a display of a specific volunteer trip.
  - For each screen, we wrote a function in Flask that activates it, including retrieving, creating, deleting and updating data from the database and running queries appropriate for these operations.
  - We also wrote functions that cause the activation of functions and procedures existing in the database from the previous steps.
  - We used try/except to notify the user if there are errors without crashing the entire site.  

### App operating instructions
Each screen has a top bar with the following options:
  - Clicking on the logo on the left will take you to the [Home screen](#Home-screen).
  - Clicking the "Volunteers" button will lead to the [Volunteers screen](#Volunteers-screen)
  - Clicking the "Volunteering" button will lead to the [Volunteering screen](#Volunteering-screen)
  - Clicking the "Rides" button will take you to the [Rides screen](#Rides-screen)

#### Home screen
  - Clicking on the "Personal Area" button will pop up a message to enter a volunteer ID and, if it exists, will lead to the screen [Personal area](#Personal-area)
  - The display of the top 10 volunteers of the week is an implementation of [Function2- top 10 volunteers of week](#Function2--top-10-volunteers-of-week)
  - Clicking the "Volunteers" button will lead to the [Volunteers screen](#Volunteers-screen)
  - Clicking the "Volunteering" button will lead to the [Volunteering screen](#Volunteering-screen)
  - Clicking the "Rides" button will take you to the [Rides screen](#Rides-screen)  
![image](https://github.com/user-attachments/assets/3280002c-f317-4de8-8b09-da90e9d293f3)

#### Personal area
  - After clicking the "personal area" button on the home screen, the following message pops up and if there is a volunteer with the entered ID, the following screen will open.
  
![image](https://github.com/user-attachments/assets/8fd54bdc-c7c3-4d0c-ba96-12151bd99a5c)  

  - The top table displays the volunteer's details with the option to update them.
  - The table below shows the volunteer's schedule for the coming week and is an implementation of [Function1- volunteer schedule](#Function1--volunteer-schedule)
![image](https://github.com/user-attachments/assets/848406e4-ba28-40dc-b0b4-19443495acc2)  

#### Volunteers screen
  - The top table allows you to search for a volunteer by ID
      - Enter ID -> click the search button.
      - After an existing volunteer is found, the fields are filled with their details:
          - To update the volunteer insert the new fields ->clicking the "update" button.
          - To delete the volunteer -> clicking the "delete" button.
      - To add a new volunteer filling in all the details -> clicking the "add" button.
      - To clear the contents of the fields -> clicking the "clear" button.
      - When adding/updating after selecting a role, messages pop up to enter the fields according to the role.
  - The table below shows all volunteers in the database including their driver/assistant classification.
  - Clicking on "Deactivate Inactive Volunteers" button activates the [Procedura2- deactivate inactive volunteers](#Procedura2--deactivate-inactive-volunteers)
  - Clicking on "Deleting Inactive Volunteers" button activates the  [Delete queries](#Delete-queries) 1 which deletes volunteers who have not been active in the last two years.  
![image](https://github.com/user-attachments/assets/b7116621-cc19-4a4b-8c34-ceef9e6944e1)  
***Driver:***  
![image](https://github.com/user-attachments/assets/e000b83b-a49f-4e2b-b053-0714a1c71275)  
![image](https://github.com/user-attachments/assets/548b267b-e16c-4ab2-8828-f0241aa9da81)  
***Assistant:***    
![image](https://github.com/user-attachments/assets/c30e4ab0-0c9f-47f9-8942-be2f3ab18bf7)

#### Volunteering screen
  - The top table allows you to search for a volunteering by date, location and hour
      - Enter date, location and hour -> click the "search" button.
      - After an existing volunteering is found, the fields are filled with the details:
          - To update volunteering insert the new fields -> clicking the "update" button.
          - To delete the volunteering -> clicking the "delete" button.
      - To add a new volunteering filling in all the details -> clicking the "add" button.
      - To clear the contents of the fields -> clicking the "clear" button.
  - The table below shows all volunteering in the database and for each one, whether there is a ride and the participating volunteers:
      - Clicking on the ambulance will lead to [Ride details screen](#Ride-details-screen)
      - Clicking on the X will pop up a question asking if you want to add a ride and if so, it will open [Add ride screen](#Add-ride-screen)
      - Clicking on the kid's drawing will lead to [Volunteer Participation Screen](#Volunteer-Participation-Screen)
![image](https://github.com/user-attachments/assets/7612e7b7-3ffc-491c-a609-1088f9b610cc)

#### Rides screen
  - The top table allows you to search for a ride by destination, driver, pickup time
      - Enter destination, driver, pickup time -> click the "search" button.
      - After an existing ride is found, the fields are filled with their details:
          - To update the ride insert the new fields -> clicking the "update" button.
          - To delete the ride -> clicking the "delete" buttons.
      - To clear the contents of the fields -> clicking the "clear" button.
  - The table below shows all rides in the database.
  - Clicking on "Assign Assistant" button activates the [Procedura1- assign assistants to future rides](#Procedura1--assign-assistants-to-future-rides)
![image](https://github.com/user-attachments/assets/a0627c7f-f702-4bba-828a-5db58f669112)  

#### Volunteer Participation Screen
  - On the left side, a display of volunteering details
  - Clicking the "Back to Volunteering" button will lead to the [Volunteering screen](#Volunteering-screen)
  - Clicking the "Update Shifts" button activates [Update queries](#Update-queries) 3 that volunteers under the age of 18 are only allowed to be on the morning shift.
  - The table displays all volunteers participating in volunteering from the volunteering participation table with their full name, phone number and age.
  - To add a volunteer to volunteering
      - Select an ID, shift -> click the "add" button.
  - To delete a volunteer from volunteering
      - Select the ID -> click the "delete" button.
![image](https://github.com/user-attachments/assets/2e542409-ec92-413f-9da3-2eb09a24a4b9)

#### Ride details screen
  - The top two tables display the ride details with the Date, Hour, City, and Patient ID fields from the Volunteering table associated with the ride.
  - The tables below show:
      - For the driver of the ride - ID, name, phone number
      - For the assistant (if any) - ID, name, phone number
      - For vehicle - ID, license plate, type, and capacity
      - A table showing the volunteers participating in the volunteering and each one's ID, name, and phone number.
  - Clicking the "Back to Volunteering" button will lead to the [Volunteering screen](#Volunteering-screen)
![image](https://github.com/user-attachments/assets/e2c5ede9-f5cb-4dea-bec2-3a59b7265153)  

#### Add ride screen
  - The date, time and location of the volunteering are displayed.
  - You must select a pickup time and address -> Clicking on Search for Available Crew
      - display tables of drivers and vehicles available on the selected date and time.
      - After selecting a vehicle and driver -> "Update selection" button.
          - Add a ride without an assistant ->  click the "Add ride" button.
          - Add a ride with an assistant ->  click the "Add assistant" button.
              -select an assistant and then-> Click the "Add ride" button.
- Clicking the "Back to Volunteering" button will lead to the [Volunteering screen](#Volunteering-screen)

![image](https://github.com/user-attachments/assets/0b31938e-ffb5-4edd-bed0-5cf470fd456a)  

![image](https://github.com/user-attachments/assets/2673c882-3b57-49cf-b304-7a8fc789f66c)  

![image](https://github.com/user-attachments/assets/34bd1174-425d-4eed-922d-00703e54fbaf)
