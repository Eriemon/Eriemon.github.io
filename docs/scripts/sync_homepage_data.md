# 主页数据同步

目标：复用原有 Python 标准库脚本刷新静态页面，无运行时后端。

## 入口与边界

运行 `python scripts/sync_homepage_data.py`。需要 Python 3.10+、已登录的 gh CLI 和仓库 traffic 读取权限；不保存凭据。不更改远程仓库。

- `build_github_projects_json`：分页读取全部公开非 Fork 仓库；Projects 为现有六张卡片，Repositories 与总 Stars 按全部公开非 Fork 仓库计算。卡片顺序取自原 JSON，Clones (14d) 为 API 当次窗口 count。
- `build_orcid_works`：读取 ORCID 0009-0000-9034-6811，规范化 DOI 去重；未收录 Fibo 时补入 `FIBO_WORK`。Fibo、HiFA、DAC 优先，其余日期倒序。
- Fibo 元数据由用户确认：2026、FPT 2026、Accepted，作者 Jiyuan Liu、Fangtian Gu、Yongming Tang、He Li；无 DOI/PDF。不以会议月份推测发表日期。
- `render_orcid_card`：统一生成论文卡片，无链接不生成按钮；`render_dac_highlight_card` 复用该函数添加详情入口和边线。
- `build_pdf_url`：只接受明确 PDF 地址；DOI 和索引页不充作 PDF。
- `update_index_html`、`update_readme_en/cn` 返回字符串；`main` 获取、校验并渲染全部内容后再写入 JSON、HTML、两份 README。

API 或模板渲染失败在写入前终止，保留现有文件；不声称多个文件的磁盘写入具有事务性。News、LinkedIn 和研究简介位于受管论文区外，不被同步覆盖。

## 验证

`python -m unittest discover -s tests/homepage_sync -v`

对应测试说明见 `../tests/homepage_sync/test_sync_homepage_data.md`。

## HiFA 与首篇标记修正

用户补充 HiFA（ICCD 2026），作者 Kai Chen、Jiyuan Liu、He Li；复用 OrcidWork 人工补录，无 DOI/PDF，不推测接收状态。顺序固定为 Fibo、HiFA、DAC、其余论文。DAC 渲染函数只保留详情页入口，蓝线由列表函数统一加到首篇。

## 后续内容修订

HiFA 已由用户确认 Accepted；MSDF-BP 使用 ORCID 正式元数据，不新增人工论文副本。排序固定 Fibo、HiFA、MSDF-BP、DAC，其余日期倒序。项目展示顺序取自缩减后的六项 JSON 清单；总仓库与总 Stars 口径保持不变。

`render_orcid_card()` 按规范化标题匹配 `FIBO_WORK.title` 后生成 Fibo 的 Page 链接，人工补录与 ORCID 记录共用该逻辑。
