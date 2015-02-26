-- 查询金融测试组所有  没有关联到项目的BUG的issue
SELECT  DISTINCT
				 '' projectName,
				 '' projectCode,
         CONCAT(project.pkey,'-',ji.issuenum) issuekey,
         ji.id issueId,
         ji.SUMMARY,
         cu2.lower_display_name REPORTER,
         cu1.lower_display_name ASSIGNEE,
         ji.PRIORITY,
         priority.pname,
         ist.pname status,
         resolution.pname resolution,
         ji.CREATED,
         ji.UPDATED,
         pv.vname versionName,
         '' OrganizationName
FROM
         jiraissue ji
         LEFT JOIN priority ON ji.PRIORITY=priority.ID
         LEFT JOIN issuestatus ist on ji.issuestatus = ist.ID
         LEFT JOIN resolution ON ji.RESOLUTION = resolution.ID
         LEFT JOIN project project ON ji.PROJECT=project.ID
         LEFT JOIN nodeassociation na ON na.source_node_entity = 'Issue'
         and na.sink_node_entity = 'Version'
         and na.source_node_id = ji.id
         and ( na.association_type = 'IssueFixVersion' || na.association_type = 'IssueVersion')
         LEFT JOIN projectversion pv ON pv.id = na.sink_node_id
         LEFT JOIN ctrip_stage_version_rel csvr ON pv.id = csvr.version_id
         LEFT JOIN cwd_user cu1 on ji.ASSIGNEE =cu1.lower_user_name
         LEFT JOIN cwd_user cu2 on ji.REPORTER =cu2.lower_user_name
         INNER JOIN customfieldvalue cfv ON ji.ID = cfv.ISSUE
         AND cfv.CUSTOMFIELD = 10100
				 AND cfv.STRINGVALUE = 10021
WHERE
         ji.issuetype=1
         AND (pv.ID is NULL || csvr.ID is NULL)
         AND ji.REPORTER in (SELECT lower_user_name FROM cwd_user cu LEFT JOIN cwd_membership cms ON cu.ID = cms.child_id where cms.parent_id = 29988)
         AND cfv.CUSTOMFIELD = 10100
				 AND cfv.STRINGVALUE = 10021
         GROUP BY ji.id
         ORDER BY ji.CREATED DESC;
