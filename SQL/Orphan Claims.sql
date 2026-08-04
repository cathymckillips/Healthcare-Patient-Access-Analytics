SELECT
*
FROM Claims c
LEFT JOIN PriorAuthorizations pa
ON c.PriorAuthorizationID=pa.PriorAuthorizationID
WHERE pa.PriorAuthorizationID IS NULL;