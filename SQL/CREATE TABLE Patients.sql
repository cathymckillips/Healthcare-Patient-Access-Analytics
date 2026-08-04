CREATE TABLE Patients
(
    PatientID VARCHAR(10) PRIMARY KEY,
    BirthYear INT,
    AgeAtEnrollment INT,
    Gender VARCHAR(25),
    State CHAR(2),
    Diagnosis VARCHAR(50),
    InsurancePlan VARCHAR(50),
    PayerType VARCHAR(25),
    EnrollmentDate DATE
);