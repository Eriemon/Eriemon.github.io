# 主页同步回归测试

代码：`tests/homepage_sync/test_sync_homepage_data.py`。

使用标准库 unittest 和 mock 替换网络边界。覆盖 Fibo 补录与远程合并、DAC 单次渲染、空链接隐藏、全部公开仓库总 Stars、克隆数更新、渲染失败不写入、重复生成一致和手工内容保留。文件操作使用临时目录，不覆盖工作区。

执行：`python -m unittest discover -s tests/homepage_sync -v`。

新增回归：HiFA 作者和会议正确，排在 Fibo 之后；蓝线只在首篇。手工正文保留比较统一换行符，兼容 Windows CRLF。

新增 ORCID MSDF-BP 排序回归：Fibo、HiFA、MSDF-BP、DAC；HiFA 会议字段包含 Accepted。

已有 Fibo 补录与合并测试同时检查两种数据来源各生成一个 Page 链接，并验证目标 HTML 文件存在。
