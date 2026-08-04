SELECT
*
FROM Prescriptions p
LEFT JOIN Providers pr
ON p.ProviderID=pr.ProviderID
WHERE pr.ProviderID IS NULL;