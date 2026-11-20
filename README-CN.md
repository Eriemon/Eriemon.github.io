<p align="center">
  <a href="README.md">English</a>
  <span>&nbsp;|&nbsp;</span>
  <a href="README-CN.md"><strong>中文</strong></a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-1f6feb"></a>
  <a href="https://Eriemon.github.io"><img alt="GitHub Pages" src="https://img.shields.io/badge/GitHub%20Pages-live-16a34a"></a>
  <img alt="Stack" src="https://img.shields.io/badge/stack-HTML%20%7C%20CSS%20%7C%20JS-f59e0b">
  <img alt="Default Style" src="https://img.shields.io/badge/default-Natural-22c55e">
</p>

<h1 align="center">Jiyuan Liu 个人学术主页</h1>

<p align="center">
  一个用于展示研究方向、学术论文、精选项目和最新动态的双语 GitHub Pages 学术主页。
</p>

## 项目简介

本仓库用于维护 [Eriemon.github.io](https://Eriemon.github.io)，即 Jiyuan Liu 的个人学术主页。主页展示 AI-量子-FPGA协同计算研究方向、19 项论文（含已接收论文），以及一个 GitHub 项目概览区：展示精选项目，全部 10 个公开非 Fork 仓库累计 422 个 Stars，并为每个仓库显示星标、Fork 和当前近 14 天克隆次数。

站点采用纯静态实现：只包含 HTML、CSS 和 JavaScript，便于审阅、维护和通过 GitHub Pages 直接部署。

## 功能特性

- 支持英文和中文双语切换。
- 默认使用 Natural 风格，并保留 Academic 风格切换。
- 支持 Light/Dark 主题切换，并在浏览器本地保存偏好。
- 适配桌面端与移动端访问。
- 包含论文、项目、新闻、经历、获奖和联系方式等模块。
- 无后端、无构建依赖，适合 GitHub Pages 静态部署。

## 页面模块

| 模块 | 内容 |
| --- | --- |
| About | 研究简介、实验室信息、编程语言和技术技能。 |
| Publications | 19 篇学术论文，Fibo（FPT 2026，已接收）居首，HiFA（ICCD 2026，已接收）第二，MSDF-BP（ITC-Asia 2026）第三，DAC 2026 第四，其余条目按 ORCID 同步生成。 |
| Projects | 展示精选项目；全部公开非 Fork 仓库共 10 个，刷新卡片 Stars、Forks 和 14 天 Clones 指标。 |
| News | 2026年12月FPT受邀报告、11月ICCD、7月DAC与CCF Chip报告，以及原有新闻。 |
| Experience | 教育经历与科研/工作经历时间线。 |
| Contact | 邮箱、LinkedIn、GitHub、ORCID、Google Scholar 等公开联系方式。 |

## 项目结构

| 路径 | 说明 |
| --- | --- |
| `index.html` | 主页内容与双语翻译字典。 |
| `style-natural.css` | 默认 Natural 视觉风格。 |
| `style-academic.css` | 可切换的 Academic 视觉风格。 |
| `script.js` | 主题、风格、语言切换与滚动动画等交互逻辑。 |
| `dac2026.html` | DAC 2026 论文详情页。 |
| `scripts/sync_homepage_data.py` | 同步 GitHub 指标、重建基于 ORCID 的论文列表，并更新 README 中的数量描述。 |
| `images/` | 站点使用的个人照片与研究图片。 |

## 本地预览

在仓库根目录运行：

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

然后访问：

```text
http://127.0.0.1:8765/
```

发布前建议检查：

```powershell
git diff --check
```

## 维护方式

使用以下命令刷新主页数据：

```powershell
python scripts/sync_homepage_data.py
```

数据来源：

- GitHub 官方公开 API：同步仓库数、Stars 和 Forks。
- ORCID 官方公开 API：同步论文标题、作者、期刊/会议信息与 DOI 链接。

说明：

- 需要已登录且可读取仓库流量的 gh CLI。刷新 Clones (14d)，总 Stars 包含全部公开非 Fork 仓库。
- Fibo（FPT 2026，已接收）、HiFA（ICCD 2026）在 ORCID 收录前人工补录；Fibo、HiFA、MSDF-BP、DAC 优先，其余按日期倒序。全部渲染成功后才写文件。

## 部署方式

本项目面向 GitHub Pages，静态文件可直接从发布分支提供服务，无需额外构建步骤。主页地址为：

[https://Eriemon.github.io](https://Eriemon.github.io)

## 隐私与范围

本仓库是公开静态主页。请不要提交私人草稿、访问令牌、本机路径、未公开个人信息，或不属于站点内容的生成文件。外部链接应指向可公开访问、适合访客查看的学术主页、项目页面或联系方式。

## 联系方式

- LinkedIn：[Eriemon](https://www.linkedin.com/in/eriemon)

- 邮箱：[erie@seu.edu.cn](mailto:erie@seu.edu.cn)
- GitHub：[@Eriemon](https://github.com/Eriemon)
- ORCID：[0009-0000-9034-6811](https://orcid.org/0009-0000-9034-6811)
- Google Scholar：[Jiyuan Liu](https://scholar.google.com/citations?user=0-PQi3AAAAAJ)

## 引用

引用元数据见 [CITATION.cff](CITATION.cff)。BibTeX 风格示例如下：

```bibtex
@software{liu_2026_eriemon_homepage,
  author = {Liu, Jiyuan},
  title = {Eriemon.github.io: A Personal Academic Homepage},
  year = {2026},
  url = {https://github.com/Eriemon/Eriemon.github.io},
  license = {Apache-2.0}
}
```

## 许可证

本项目采用 [Apache License 2.0](LICENSE) 许可证。
