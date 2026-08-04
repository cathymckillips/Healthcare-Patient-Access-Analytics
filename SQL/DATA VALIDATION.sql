SELECT
PatientID,
COUNT(*)
FROM Patients
GROUP BY PatientID
HAVING COUNT(*)>1;