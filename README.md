# Volunteer Management System - Ezer Mizion  

Moria Rozenfeld & Tehila Shraga  
**System:** Ezer Mizion  
**Unit:** Volunteer Division  

## Table of Contents  
- [Introduction](#introduction)  
- [Entity Relationship Diagram (ERD)](#entity-relationship-diagram-erd)  
- [Data Structure Diagram (DSD)](#data-structure-diagram-dsd)
- [Insert data to table](#insert-data-to-table)
- [Backup and Restore](#Backup-and-Restore)
- [Queries](#Queries)  

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
### Import Files:  
![image](https://github.com/user-attachments/assets/c62f508e-ad13-4eaa-a757-0952ed72bc88)
![image](https://github.com/user-attachments/assets/a647b170-4214-4169-b5bb-e11e75ee75d4)     

### Pyhton:  
![image](https://github.com/user-attachments/assets/6ea79551-7cfc-4262-ac53-983d3f4a37c6)  
![image](https://github.com/user-attachments/assets/4a789652-3df1-4343-ad58-5dc1175e8d5e)  

### Mockaroo:
![patient_mockaroo](Stage%20A/mockarooFiles/patient_mockaroo.png)  

## Backup and Restore  
![image](https://github.com/user-attachments/assets/92392fcb-11e0-49d6-8c3e-8ad70c355d6d)
![image](https://github.com/user-attachments/assets/f2469c7d-23c9-46a8-9bc1-c4e63720f723)


## Queries  
### Select queries:
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
  

### Update queries:
#### 1. The query updates volunteers to be inactive if they have not participated in a volunteer or event in the past year. 
##### before:  
![image](https://github.com/user-attachments/assets/1cb18d47-76fd-4ae0-bb1a-b174115c04e1)  
##### running:  
![image](https://github.com/user-attachments/assets/2fadc990-b5c2-4acf-905e-f35e51bd3d94)  
##### after:  
![image](https://github.com/user-attachments/assets/1d55aa46-9a58-4f4a-8a49-204755d88e78)   
  

#### 2. The query updates that for events that take place in the north or south, it is impossible to come with a companion, so the plus one will be FALSE.
##### before:  
![image](https://github.com/user-attachments/assets/3206a3e1-95ea-405e-8622-6044b62931f0)  
##### running:  
![image](https://github.com/user-attachments/assets/6cee5c1d-562b-423a-ab99-6dd51c6a2faa)  
##### after:  
![image](https://github.com/user-attachments/assets/9b51a9d9-8fb2-433a-9a7f-9c855aebe6b5)  
  
#### 3. The query updates that volunteers under the age of 18 cannot volunteer on the evening shift, but only on the morning shift.
##### before:  
![image](https://github.com/user-attachments/assets/1431b391-5bc4-4ba5-b922-fafe198b0ce1)  
##### running:  
![image](https://github.com/user-attachments/assets/9841b41d-3cf4-465d-b2a8-47ea567737d0)  
##### after:  
![image](https://github.com/user-attachments/assets/941e040d-273e-4d2e-8e82-892ea182d7aa)  
  

### Delete queries
1. 
 b:![image](https://github.com/user-attachments/assets/7c53f25e-97b5-47d2-a1ad-93da84b3fb6d)

   Q:
![image](https://github.com/user-attachments/assets/7f7097d6-ac6f-431a-b692-4311af9cfa29)
![image](https://github.com/user-attachments/assets/14160a1e-b320-4747-8c27-ccf22777d782)
![image](https://github.com/user-attachments/assets/84e635d0-ff0d-40d5-a9c6-a715496535c6)
![image](https://github.com/user-attachments/assets/31174d4c-72f2-43ac-93cc-b5967ce24668)

   A:
   ![image](https://github.com/user-attachments/assets/1fb6e158-180d-4076-ba47-2a58018d74b2)

2. b:![image](https://github.com/user-attachments/assets/895c7bc7-6cf5-4166-a483-562685bc4ed8)

   q:![image](https://github.com/user-attachments/assets/41c2f990-31b3-48de-842e-5d2ab2ced2c8)

   a:<img width="388" alt="image" src="https://github.com/user-attachments/assets/c6855ede-96ca-49c6-af0d-d4dcd181dc8b" />

3.
b:![image](https://github.com/user-attachments/assets/99e93c6c-fa23-4a7e-b5cf-57c2fe55cf74)
q:![image](https://github.com/user-attachments/assets/cabf596a-6ce5-4965-b4ed-4f0c2fd8d2b4)

a:![image](https://github.com/user-attachments/assets/842f834c-b61c-48ce-a949-a11b7dda2748)

