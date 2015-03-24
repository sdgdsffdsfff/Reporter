--  统计一个BUG被重新打开的次数
SELECT
ji.id issueId,
COUNT(ji.id) reopenNum
FROM
jiraissue ji,
(
SELECT
*
FROM
os_currentstep
UNION ALL
SELECT
*
FROM
os_historystep
) step
WHERE
ji.WORKFLOW_ID = step.entry_id
AND step.step_id = 5 #表示重新打开问题的step
AND ji.issuetype = 1 AND ji.REPORTER IN (
SELECT
  cu.lower_user_name
FROM cwd_user cu
	LEFT JOIN cwd_membership cms ON cu.ID = cms.child_id
	where cms.parent_id IN (SELECT child_id FROM cwd_membership WHERE parent_name = '金融测试组' && membership_type = 'GROUP_GROUP')
)
GROUP BY ji.ID
ORDER BY COUNT(ji.id) DESC
;