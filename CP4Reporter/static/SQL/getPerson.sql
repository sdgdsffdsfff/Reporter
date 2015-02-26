-- 获取个人BUG统计
SELECT
	cu.lower_display_name REPORTER,
	CASE ji.issuestatus
		WHEN 1 THEN 'Open'
		WHEN 3 THEN 'In progress'
		WHEN 6 THEN 'Closed'
		WHEN 5 THEN 'Resolved'
	END AS 'status'
FROM
	jiraissue ji
	LEFT JOIN cwd_user cu ON ji.REPORTER = cu.lower_user_name
	RIGHT JOIN cwd_membership cms ON cu.ID = cms.child_id
	and cms.parent_id = 29988
WHERE 
	ji.issuetype=1