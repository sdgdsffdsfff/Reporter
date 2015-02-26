-- BUG标签为空的BUG
SELECT
*
FROM
jiraissue ji
LEFT JOIN cwd_user cu ON ji.REPORTER = cu.lower_user_name
RIGHT JOIN cwd_membership cms ON cu.ID = cms.child_id
and cms.parent_id = 29988
LEFT JOIN label ON ji.id = label.issue
WHERE
label.LABEL = 'no' AND ji.issuetype=1;