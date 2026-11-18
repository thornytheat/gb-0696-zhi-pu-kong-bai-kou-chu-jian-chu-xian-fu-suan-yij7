# 质谱字段与规则

sample_id保留前导零。kind取standard、blank、sample、control。area与internal_area为峰面积。level为标样浓度，单位支持ug/L、mg/L、ng/L；统一为ug/L。dilution必须大于0。

每批每检测项至少3个独立浓度点。最小二乘使用Decimal，分母为零拒绝；斜率非正拒绝。空白取同批同项的浓度中位数。净浓度允许为负；不能提前截零。稀释后检出限=0.05×倍数。控制样相对误差超过20%阻断。超过标曲响应范围优先于其他质控判断。

重复编号相同内容标DUPLICATE，不同内容标KEY_CONFLICT。采信包括标曲和空白，最终样品数不等于输入采信数。行数对账独立于样品结果数。

同一批次同一分析项内sample_id唯一；相同样品编号可在不同分析项或批次中复用。
