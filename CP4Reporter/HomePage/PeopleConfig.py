# -*- coding:utf-8 -*-
__author__ = 'kiven'

def peopleConfig(pType):
    result = []
    # 案例问题BUG经办人员列表
    if pType == 'case_bug':
        result = ['cx陈星','syq孙友青','tcq唐超群','vyhy杨宏宇','wwy吴伟怡']
    elif pType == 'soa':
        result = ['vyj俞晶']
    elif pType =='server':
        result = ['vgl郭亮','vgzm桂之明','cd曹丹','zft张方涛','vzxs张学圣','vlgr李广瑞','sj施建']
    return result
