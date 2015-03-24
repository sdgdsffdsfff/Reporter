-- 主SQL
SELECT DISTINCT
  project.ID productID,
  project.pname productName,
  cpp.ID projectID,
  cpp.`NAME` projectName,
  CONCAT(project.pkey,'-',ji.issuenum) issuekey,
  cpp.MAIN_STATE,
  ji.*
FROM
  ctrip_product cp
LEFT JOIN project ON cp.JIRA_PROJECT_ID=project.ID
LEFT JOIN ctrip_projectpm cpp ON cp.JIRA_PROJECT_ID=cpp.JIRA_PROJECT_ID
LEFT JOIN ctrip_stageplan csp ON cpp.ID=csp.PROJECT_PM_ID AND csp.PROJ_FLAG=1
LEFT JOIN ctrip_stage_version_rel csvr ON csp.ID=csvr.STAGE_PLAN_ID
LEFT JOIN nodeassociation na ON na.source_node_entity = 'Issue'
AND na.sink_node_entity = 'Version'
AND (na.association_type = 'IssueFixVersion' || na.association_type = 'IssueVersion')
AND na.SINK_NODE_ID=csvr.VERSION_ID
LEFT JOIN jiraissue ji ON na.SOURCE_NODE_ID=ji.ID
WHERE ji.issuetype=1 AND project.ID IN (11300,11301,11302,11303);