-- 所有金融测试（功能）组下的成员名称
SELECT
  lower_display_name '组员'
FROM cwd_user cu
	LEFT JOIN cwd_membership cms ON cu.ID = cms.child_id
	where cms.parent_id = 29988