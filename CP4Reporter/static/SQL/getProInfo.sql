SELECT DISTINCT
         cpm.`NAME` projectName,
         ji.SUMMARY,
         cu2.lower_display_name REPORTER,
         cu1.lower_display_name ASSIGNEE,
         ist.pname status,
         ji.CREATED,
				 ji.UPDATED
FROM
         jiraissue ji
         LEFT JOIN priority ON ji.PRIORITY=priority.ID
         LEFT JOIN issuestatus ist on ji.issuestatus = ist.ID
         LEFT JOIN resolution ON ji.RESOLUTION = resolution.ID
         INNER JOIN project project ON ji.PROJECT=project.ID
         INNER JOIN nodeassociation na ON na.source_node_entity = 'Issue'
         and na.sink_node_entity = 'Version'
         and na.source_node_id = ji.id
         and( na.association_type = 'IssueFixVersion' || na.association_type = 'IssueVersion')
         INNER JOIN projectversion pv ON pv.id = na.sink_node_id
         INNER JOIN ctrip_stage_version_rel csvr ON pv.id = csvr.version_id
         INNER JOIN ctrip_stageplan csp ON csvr.STAGE_PLAN_ID = csp.ID AND csp.PROJ_FLAG=1
         INNER JOIN ctrip_projectpm cpm ON csp.PROJECT_PM_ID = cpm.ID
         INNER JOIN ctrip_product product ON cpm.JIRA_PROJECT_ID = product.JIRA_PROJECT_ID
         INNER JOIN ctrip_productline cpl ON product.PRODUCT_LINE_ID = cpl.ID
         INNER JOIN ctrip_organization corg ON cpl.ORGANIZATION_ID =corg.ID
         LEFT JOIN cwd_user cu1 on ji.ASSIGNEE =cu1.lower_user_name
         LEFT JOIN cwd_user cu2 on ji.REPORTER =cu2.lower_user_name
WHERE
         ji.ASSIGNEE in (SELECT lower_user_name FROM cwd_user cu LEFT JOIN cwd_membership cms ON cu.ID = cms.child_id where cms.parent_id = 29988)
         GROUP BY ji.id  -- 按组分类,去重挂在多个版本的下的项目issue
         ORDER BY ji.CREATED DESC;