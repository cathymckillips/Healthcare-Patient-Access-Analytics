SELECT
Diagnosis,
COUNT(*) AS Patients
FROM Patients
GROUP BY Diagnosis
ORDER BY Patients DESC;