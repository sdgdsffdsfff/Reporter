-- 查询金融测试组所有  项目集下为BUG的issue
SELECT DISTINCT
				 cpm.`NAME` projectName,
				 cpm.`CODE` projectCode,
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
         corg.`NAME` OrganizationName
FROM
         jiraissue ji
         LEFT JOIN priority ON ji.PRIORITY=priority.ID
         LEFT JOIN issuestatus ist on ji.issuestatus = ist.ID
         LEFT JOIN resolution ON ji.RESOLUTION = resolution.ID
         INNER JOIN project project ON ji.PROJECT=project.ID
         INNER JOIN nodeassociation na ON na.source_node_entity = 'Issue'
         and na.sink_node_entity = 'Version'
         and na.source_node_id = ji.id
         and ( na.association_type = 'IssueFixVersion' || na.association_type = 'IssueVersion')
         INNER JOIN projectversion pv ON pv.id = na.sink_node_id
         INNER JOIN ctrip_stage_version_rel csvr ON pv.id = csvr.version_id
         INNER JOIN ctrip_stageplan csp ON csvr.STAGE_PLAN_ID = csp.ID AND csp.PROJ_FLAG=0
         INNER JOIN ctrip_projectpmset cpm ON csp.PROJECT_PM_ID = cpm.ID
         INNER JOIN ctrip_product product ON cpm.JIRA_PROJECT_ID = product.JIRA_PROJECT_ID
         INNER JOIN ctrip_productline cpl ON product.PRODUCT_LINE_ID = cpl.ID
         INNER JOIN ctrip_organization corg ON cpl.ORGANIZATION_ID =corg.ID
         LEFT JOIN cwd_user cu1 on ji.ASSIGNEE =cu1.lower_user_name
         LEFT JOIN cwd_user cu2 on ji.REPORTER =cu2.lower_user_name
         INNER JOIN customfieldvalue cfv ON ji.ID = cfv.ISSUE
WHERE
         ji.issuetype=1
         AND ji.REPORTER in (SELECT lower_user_name FROM cwd_user cu LEFT JOIN cwd_membership cms ON cu.ID = cms.child_id where cms.parent_id = 29988)
         AND cfv.CUSTOMFIELD = 10100
				 AND cfv.STRINGVALUE = 10021
         GROUP BY ji.id
         ORDER BY ji.CREATED DESC;
