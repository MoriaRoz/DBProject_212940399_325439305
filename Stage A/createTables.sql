CREATE TABLE Volunteer
(
  Volunteer_id INT NOT NULL,
  First_name VARCHAR(20) NOT NULL,
  Last_name VARCHAR(20) NOT NULL,
  Birthday DATE NOT NULL,
  Phone VARCHAR(10) NOT NULL,
  Active CHAR(1) NOT NULL,
  PRIMARY KEY (Volunteer_id)
);

CREATE TABLE KindOfVol
(
  KindOfVol_id INT NOT NULL,
  Type VARCHAR(20) NOT NULL,
  Volunteer_id INT NOT NULL,
  PRIMARY KEY (KindOfVol_id),
  FOREIGN KEY (Volunteer_id) REFERENCES Volunteer(Volunteer_id)
);

CREATE TABLE Patient
(
  Patient_id INT NOT NULL,
  First_name VARCHAR(20) NOT NULL,
  Last_name VARCHAR(20) NOT NULL,
  Birthday DATE NOT NULL,
  PRIMARY KEY (Patient_id)
);

CREATE TABLE City
(
  Name VARCHAR(30) NOT NULL,
  City_id INT NOT NULL,
  Area VARCHAR(20) NOT NULL,
  PRIMARY KEY (Name)
);

CREATE TABLE Volunteering
(
  Date DATE NOT NULL,
  Duration INT NOT NULL,
  Hour INT NOT NULL,
  Report VARCHAR(255) NOT NULL,
  Volunteering_id INT NOT NULL,
  Patient_id INT NOT NULL,
  KindOfVol_id INT NOT NULL,
  Location VARCHAR(30) NOT NULL,
  PRIMARY KEY (Volunteering_id),
  FOREIGN KEY (Patient_id) REFERENCES Patient(Patient_id),
  FOREIGN KEY (KindOfVol_id) REFERENCES KindOfVol(KindOfVol_id),
  FOREIGN KEY (Location) REFERENCES City(Name)
);

CREATE TABLE Volunteering_participation
(
  Volunteer_id INT NOT NULL,
  Volunteering_id INT NOT NULL,
  PRIMARY KEY (Volunteer_id, Volunteering_id),
  FOREIGN KEY (Volunteer_id) REFERENCES Volunteer(Volunteer_id),
  FOREIGN KEY (Volunteering_id) REFERENCES Volunteering(Volunteering_id)
);

CREATE TABLE Event
(
  Event_id INT NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Date Date NOT NULL,
  Volunteer_id INT NOT NULL,
  Location VARCHAR(30) NOT NULL,
  PRIMARY KEY (Event_id),
  FOREIGN KEY (Volunteer_id) REFERENCES Volunteer(Volunteer_id),
  FOREIGN KEY (Location) REFERENCES City(Name)
);

CREATE TABLE Event_participation
(
  Volunteer_id INT NOT NULL,
  Event_id INT NOT NULL,
  PRIMARY KEY (Volunteer_id, Event_id),
  FOREIGN KEY (Volunteer_id) REFERENCES Volunteer(Volunteer_id),
  FOREIGN KEY (Event_id) REFERENCES Event(Event_id)
);
