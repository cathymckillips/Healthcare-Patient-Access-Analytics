SELECT

100.0*

SUM(
CASE
WHEN FinalStatus
LIKE 'Approved%'
THEN 1
ELSE 0
END
)

/

COUNT(*)

AS ApprovalRate

FROM PriorAuthorizations;