-- 获取金融测试组下的所有组员
SELECT
  cu.lower_display_name,cu.lower_user_name
FROM cwd_user cu
	LEFT JOIN cwd_membership cms ON cu.ID = cms.child_id
	where cms.parent_id IN (SELECT child_id FROM cwd_membership WHERE parent_name = '金融测试组' && membership_type = 'GROUP_GROUP')