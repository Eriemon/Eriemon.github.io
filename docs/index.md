# 主页内容维护

目标：以现有双语静态页面展示 AI-量子-FPGA协同计算研究、论文、项目和公开联系信息。

- `index.html` 保存默认英文正文与 `translations.en/zh`；同一信息须同时更新三处。
- 技能为嵌入式系统开发、FPGA开发、SoC设计、Agent开发、量子算法。
- News 顺序：2026-12 FPT 邀请、2026-11 ICCD、2026-07 DAC、2026-07 CCF Chip，再接原有新闻。12 月事件在 2026-11-20 以将来时表述。
- LinkedIn：用户提供的 https://www.linkedin.com/in/eriemon，置于现有学术链接与联系区。
- `PUBLICATIONS-LIST` 标记内的论文与所有指标由同步脚本生成，勿只改生成内容。
- 复用原有卡片、翻译字典、CSS 与交互，不增加前端依赖。

预览：`python -m http.server 8765 --bind 127.0.0.1`。

## 本次验收（2026-11-20）

- 真实同步：17项论文（含Fibo已接收论文）、9张项目卡片、10个公开非Fork仓库、422 Stars。
- unittest：5项通过；git diff --check 通过。
- 浏览器：1440px、390px，中英文×两种风格×明暗主题共16种组合无横向溢出；控制台无错误。
- 核对 Fibo 首位、News 四条顺序、技能与研究方向、两个 LinkedIn 入口，以及 DAC 详情作者顺序。

## 本次修正

Contact 桌面端四个链接同行；四条新增 News 的会议名和报告主题加粗，原有 DAC 新闻中的 CCF-A 加粗。论文蓝线位于首篇 Fibo，第二篇补入 HiFA（ICCD 2026）。论文统计随实际唯一条目更新。

修正后验收：真实同步生成18项论文；6项回归测试通过。1024px、1440px 两种风格和中英文下 Contact 均同行；390px 保持原有手机布局，无水平溢出。浏览器核对首三篇 Fibo、HiFA、DAC，只有首篇蓝线；News 会议名、主题与 CCF-A 为 strong。

## 六项目与论文更新

HiFA（ICCD 2026）状态为 Accepted。MSDF-BP 从 ORCID 234086832 获取，DOI 为 10.1109/itc-asia71864.2026.11710883。首四篇固定 Fibo、HiFA、MSDF-BP、DAC。移除主页仓库、github-management、搭建指南三张项目卡片，保留六张，桌面三列两行；总仓库数和总 Stars 仍按全部公开非 Fork 仓库计算。

本轮验收：真实同步19项论文、6张项目卡片；7项回归通过。浏览器确认 HiFA Accepted、MSDF-BP 作者及 DOI 元数据、首四篇顺序；1024/1440px 两种风格均两行，390px 无横向溢出。
