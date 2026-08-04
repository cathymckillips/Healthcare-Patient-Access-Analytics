BULK INSERT Patients
FROM 'C:\Users\caths\Desktop\Scrip\patients.csv'
WITH
(
FIRSTROW=2,
FIELDTERMINATOR=',',
ROWTERMINATOR='\n'
);