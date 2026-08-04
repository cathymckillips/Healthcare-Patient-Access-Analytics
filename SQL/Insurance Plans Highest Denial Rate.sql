SELECT
InsurancePlan,
COUNT(*) AS TotalRequests,
SUM(
CASE
WHEN PAStatus='Denied'
THEN 1
ELSE 0
END
) AS Denials
FROM PriorAuthorizations
GROUP BY InsurancePlan;