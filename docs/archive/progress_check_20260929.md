> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 2026-09-29 进度检查

状态 TRAIN_BATCH1_PARTIAL。09:41 HKT 开始实查；01:07 自动停止，目前没有本数据项目的运行或排队作业。

Native 预检通过：14 次尝试（含两次历史失败），冻结 12 项均合格；adapter、PL KP 不变性、schema 门禁均通过。

Train：计划448，尝试12，11条有合格 admission 回执且文件/qualification 校验和核对通过，1条失败隔离，436条未尝试。旧45条不计入。失败点 broad_rectangle_000011 的错误是 Observed LF magnitudes at z=6 lie outside the model grid；原始 history 已保留。该错误被归为 schema_provenance_failure，触发系统性停止；需要结合原入口的 LF 数值域失败语义修正分类，不能换点或不记失败。

入库回执存在不等于训练 loader 衔接已完成：qualified_development manifest 仍为0条，缺少入库后 loader 成功记录；data_status 的 manifest 回执链接仍指向生成回执，未指向独立 admission 回执。这一汇总衔接需要修复/验证。不能声称11条已由训练 loader 验收可读。

sacct 实际成本：preflight 34.773333、Train 32.280000、runtime probes 0.003333，总计67.056667 core-hours；当前预留0，非预算耗尽。

Sealed labels 未生成、未读，模型训练和生产 MCMC 未启动。本次检查没有追加提交、重试或改变科学配置。
