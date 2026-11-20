"""同步个人主页中的 GitHub 指标、论文列表与文档描述。"""

from __future__ import annotations

import json
import re
import subprocess
import urllib.request
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "github-projects.json"
INDEX_PATH = REPO_ROOT / "index.html"
README_EN_PATH = REPO_ROOT / "README.md"
README_CN_PATH = REPO_ROOT / "README-CN.md"

GITHUB_REPOS_URL = "https://api.github.com/users/Eriemon/repos?per_page=100&type=owner"
ORCID_WORKS_URL = "https://pub.orcid.org/v3.0/0009-0000-9034-6811/works"
ORCID_WORK_DETAIL_URL = "https://pub.orcid.org/v3.0/0009-0000-9034-6811/work/{put_code}"

PUBLICATIONS_START_MARKER = "<!-- PUBLICATIONS-LIST:START -->"
PUBLICATIONS_END_MARKER = "<!-- PUBLICATIONS-LIST:END -->"

DAC_HIGHLIGHT_TITLE = "🏆 Optimized Time-dependent Hamiltonian Evolution Quantum Solver for Power System Transient Computations"

VENUE_OVERRIDES_BY_TITLE = {
    DAC_HIGHLIGHT_TITLE.removeprefix("🏆 "): "Design Automation Conference (DAC) 2026 • CCF-A Conference",
    "Acc-VQLS: Accelerated Variational Quantum Linear Solver for VSC Simulation": "ACM Transactions on Quantum Computing, 2026",
    "Design of A Universal LVDS-based 4K@60Hz Video Processing Development Platform": "CSTIC, 2026",
    "Fine-grained data integration for high throughput and bandwidth-efficient computation on FPGAs": "Integration, 2026",
    "FPGA Implemented Quantum Approximate Optimization Algorithm for MaxCut Acceleration": "ICFPT, 2025",
    "FPGA Accelerated Large-Scale State-Space Equations for Multi-Converter Systems": "Electronics, 2025",
    "A Real-Time Simulation Model With Constant Admittance Matrix for Multiple Grid-Connected Converters System": "IEEE Transactions on Power Electronics, 2025",
    "Scalable and Real-Time Power System Simulation Based on Heterogeneous CPU-FPGA Co-operation": "ISCAS, 2025",
    "Precision Analysis and Hardware Acceleration for Large-Scale Quantum Fourier Transformation on Modern FPGAS": "CSTIC, 2025",
    "FPGA Accelerated Adaptive LDPC-based Quantum Error Correction by Bitwise Pipeline Parallelism": "ISCAS, 2025",
    "An Efficient ML-based Hardware Trojan Localization Framework for RTL Security Analysis": "MLCAD, 2024",
    "MSDF-SGD: Most-Significant Digit-First Stochastic Gradient Descent for Arbitrary-Precision Training": "FPL, 2023",
    "A Novel Schematic Placement and Routing Algorithm for FPGAs": "ISEDA, 2023",
    "FAPN: Face Alignment Propagation Network for Face Video Super-Resolution": "ACCV Workshops, 2023",
}


@dataclass(frozen=True)
class GithubProjectMetrics:
    """保存单个项目卡片要展示的 GitHub 指标。"""

    name: str
    stars: int
    forks: int
    clones14d: int


@dataclass(frozen=True)
class OrcidWork:
    """保存 ORCID 论文条目生成卡片所需的字段。"""

    title: str
    authors: list[str]
    venue: str
    year: int
    month: int
    day: int
    pdf_url: str
    doi_url: str


# 用户确认的 FPT 2026 已接收论文；尚无公开 DOI/PDF。
FIBO_WORK = OrcidWork(
    title="Fibo: A Role-Orchestrated Agentic Reasoning Framework for Autonomous FPGA RTL Design",
    authors=["Jiyuan Liu", "Fangtian Gu", "Yongming Tang", "He Li"],
    venue="FPT 2026 · Accepted",
    year=2026,
    month=0,
    day=0,
    pdf_url="",
    doi_url="",
)


# 用户补充的 ICCD 2026 论文；已接收；不推测 DOI 或 PDF。
HIFA_WORK = OrcidWork(
    title="HiFA: Hierarchical Data Integrated FPGA Accelerator for Block-wise Quantum Circuit Simulation",
    authors=["Kai Chen", "Jiyuan Liu", "He Li"],
    venue="ICCD 2026 · Accepted",
    year=2026,
    month=0,
    day=0,
    pdf_url="",
    doi_url="",
)

def fetch_json(url: str, *, accept: str = "application/json") -> Any:
    """拉取公开 JSON 数据。"""

    headers = {
        "Accept": accept,
        "User-Agent": "EriemonHomepageSync/1.0",
    }

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def read_text(path: Path) -> str:
    """读取 UTF-8 文本文件。"""

    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    """写入 UTF-8 文本文件。"""

    path.write_text(content, encoding="utf-8", newline="\n")


def load_existing_project_state() -> list[str]:
    """读取既有项目卡片的展示顺序。"""

    existing_data = json.loads(read_text(DATA_PATH))
    return [project["name"] for project in existing_data["projects"]]


def build_github_projects_json() -> tuple[dict[str, Any], int]:
    """同步 GitHub 项目指标并生成 JSON 数据。"""

    # gh 复用本机登录；不在源码或公开数据中保存凭据。
    pages = json.loads(subprocess.check_output(
        ["gh", "api", "--paginate", "--slurp", GITHUB_REPOS_URL], text=True, encoding="utf-8"
    ))
    repos_payload = [repo for page in pages for repo in page]
    project_order = load_existing_project_state()

    # 只统计当前账号名下的非 fork 仓库。
    owner_repos = [repo for repo in repos_payload if not repo.get("fork") and not repo.get("private")]

    # 为后续按既定顺序重排卡片数据建立名称索引。
    repo_by_name = {repo["name"]: repo for repo in owner_repos}

    missing_names = [name for name in project_order if name not in repo_by_name]
    if missing_names:
        raise RuntimeError(
            f"> ERR: [Python] GitHub 返回结果缺少既有项目卡片：{', '.join(missing_names)}"
        )

    project_metrics_list: list[GithubProjectMetrics] = []

    # 按既有顺序构造卡片指标，保证页面项目排序稳定。
    for project_name in project_order:
        repo = repo_by_name[project_name]

        clones = json.loads(subprocess.check_output(
            ["gh", "api", f"repos/Eriemon/{project_name}/traffic/clones"], text=True, encoding="utf-8"
        ))
        # 克隆数查询失败会中止同步，不将旧值冒充当前窗口。
        project_metrics = GithubProjectMetrics(
            name=project_name,
            stars=int(repo["stargazers_count"]),
            forks=int(repo["forks_count"]),
            clones14d=int(clones["count"]),
        )
        project_metrics_list.append(project_metrics)

    # 统计页面顶部使用的仓库数与总星标数。
    repositories_count = len(owner_repos)
    stars_count = sum(int(repo["stargazers_count"]) for repo in owner_repos)

    # 组装写回前端读取的数据文件。
    github_projects_data = {
        "summary": {
            "projects": len(project_metrics_list),
            "repositories": repositories_count,
            "stars": stars_count,
        },
        "projects": [
            {
                "name": project.name,
                "stars": project.stars,
                "forks": project.forks,
                "clones14d": project.clones14d,
            }
            for project in project_metrics_list
        ],
    }

    # 返回前端数据文件和总仓库数，供 README 同步说明使用。
    return github_projects_data, repositories_count


def parse_numeric_date(summary: dict[str, Any]) -> tuple[int, int, int]:
    """提取排序用的年月日整数。"""

    publication_date = summary.get("publication-date") or {}

    year = int((publication_date.get("year") or {}).get("value") or 0)
    month = int((publication_date.get("month") or {}).get("value") or 0)
    day = int((publication_date.get("day") or {}).get("value") or 0)

    # 返回元组供倒序排序。
    return year, month, day


def normalize_text(value: str | None) -> str:
    """统一清理 ORCID 返回文本中的空白字符。"""

    normalized_text = (value or "").replace("\xa0", " ")
    normalized_text = re.sub(r"\s+", " ", normalized_text)
    return normalized_text.strip()


def build_orcid_doi_url(external_ids: list[dict[str, Any]]) -> str:
    """优先使用 ORCID 中的 DOI 链接，没有则自行补全。"""

    for external_id in external_ids:
        if external_id.get("external-id-type") != "doi":
            continue

        doi_url = normalize_text((external_id.get("external-id-url") or {}).get("value"))
        if doi_url:
            return doi_url

        doi_value = normalize_text(external_id.get("external-id-value"))
        if doi_value:
            return f"https://doi.org/{doi_value}"

    raise RuntimeError("> ERR: [Python] ORCID 论文条目缺少 DOI，当前脚本无法为页面生成稳定链接")


def build_pdf_url(detail_payload: dict[str, Any], doi_url: str) -> str:
    """仅保留明确的 PDF 地址，不将 DOI 或索引页误标为 PDF。"""

    raw_pdf_url = normalize_text((detail_payload.get("url") or {}).get("value"))
    if re.search(r"\.pdf(?:[?#]|$)|/doi/(?:e?pdf)/", raw_pdf_url, re.IGNORECASE):
        return raw_pdf_url
    return ""


def build_publication_venue(title: str, journal_title: str, year: int) -> str:
    """生成页面要展示的 venue 文本。"""

    if title in VENUE_OVERRIDES_BY_TITLE:
        return VENUE_OVERRIDES_BY_TITLE[title]

    if journal_title:
        return f"{journal_title}, {year}"

    raise RuntimeError(f"> ERR: [Python] 无法确定论文会议信息：{title}")


def build_authors_list(detail_payload: dict[str, Any]) -> list[str]:
    """提取 ORCID 明细中的作者列表。"""

    contributors = ((detail_payload.get("contributors") or {}).get("contributor") or [])
    authors: list[str] = []

    # 逐个提取 ORCID 中登记的作者显示名。
    for contributor in contributors:
        credit_name = normalize_text((contributor.get("credit-name") or {}).get("value"))
        if credit_name:
            authors.append(credit_name)

    if not authors:
        raise RuntimeError("> ERR: [Python] ORCID 论文条目缺少作者列表")

    # 返回页面排版要使用的作者顺序。
    return authors


def build_orcid_works() -> list[OrcidWork]:
    """拉取 ORCID works 并生成页面卡片数据。"""

    works_payload = fetch_json(ORCID_WORKS_URL)
    works_group = works_payload.get("group") or []
    orcid_works: list[OrcidWork] = []
    seen_dois: set[str] = set()

    # 逐个读取明细，补全作者、链接和期刊信息。
    for work_group in works_group:
        work_summary = (work_group.get("work-summary") or [{}])[0]
        put_code = work_summary.get("put-code")
        if not put_code:
            raise RuntimeError("> ERR: [Python] ORCID 返回的 works 缺少 put-code")

        year, month, day = parse_numeric_date(work_summary)
        detail_payload = fetch_json(ORCID_WORK_DETAIL_URL.format(put_code=put_code))

        # 清洗标题，避免 HTML 中混入不稳定空白。
        title = normalize_text(
            (((detail_payload.get("title") or {}).get("title") or {}).get("value"))
        )
        authors = build_authors_list(detail_payload)

        # 生成页面展示用的 venue 文本。
        journal_title = normalize_text((detail_payload.get("journal-title") or {}).get("value"))
        venue = build_publication_venue(title, journal_title, year)

        external_ids = ((detail_payload.get("external-ids") or {}).get("external-id") or [])
        doi_url = build_orcid_doi_url(external_ids)
        pdf_url = build_pdf_url(detail_payload, doi_url)

        # 累积页面所需的字段，后续统一排序并生成 HTML。
        orcid_work = OrcidWork(
            title=title,
            authors=authors,
            venue=venue,
            year=year,
            month=month,
            day=day,
            pdf_url=pdf_url,
            doi_url=doi_url,
        )
        doi_key = doi_url.lower().replace("http://", "https://").replace("dx.doi.org/", "doi.org/").rstrip("/")
        if doi_key not in seen_dois:
            orcid_works.append(orcid_work)
            seen_dois.add(doi_key)

    for manual_work in (FIBO_WORK, HIFA_WORK):
        if not any(normalize_text(work.title).casefold() == manual_work.title.casefold() for work in orcid_works):
            orcid_works.append(manual_work)

    # Fibo、HiFA、MSDF-BP、DAC 优先，其余保持日期倒序。
    orcid_works.sort(
        key=lambda work: (
            normalize_text(work.title).casefold() == FIBO_WORK.title.casefold(),
            normalize_text(work.title).casefold() == HIFA_WORK.title.casefold(),
            work.title.startswith("MSDF-BP:"),
            work.title == DAC_HIGHLIGHT_TITLE.removeprefix("🏆 "),
            work.year, work.month, work.day, work.title,
        ),
        reverse=True,
    )

    # 返回后续用于生成 Publications 区块的有序条目。
    return orcid_works


def format_author_name(author_name: str) -> str:
    """为页面作者列表添加必要的强调样式。"""

    safe_author_name = escape(author_name)
    normalized_author_key = re.sub(r"\s+", "", author_name).lower()
    highlighted_author_keys = {
        "jiyuanliu",
        "liu,j.",
        "liu,j",
        "liu,jiyuan",
    }

    if normalized_author_key in highlighted_author_keys:
        return f"<strong>{safe_author_name}</strong>"

    return safe_author_name


def render_orcid_card(work: OrcidWork) -> str:
    """渲染单条 ORCID 论文卡片。"""

    authors_html = ", ".join(format_author_name(author) for author in work.authors)
    title_html = escape(work.title)
    venue_html = escape(work.venue)
    pdf_url = escape(work.pdf_url, quote=True)
    doi_url = escape(work.doi_url, quote=True)
    links = []
    if pdf_url:
        links.append(f'<a href="{pdf_url}" class="pub-link" target="_blank" rel="noopener noreferrer">PDF</a>')
    if doi_url:
        links.append(f'<a href="{doi_url}" class="pub-link" target="_blank" rel="noopener noreferrer">DOI</a>')

    return f"""                <article class="pub-card" data-year="{work.year}">
                    <div class="pub-year">{work.year}</div>
                    <div class="pub-content">
                        <div class="pub-header">
                            <h3 class="pub-title">{title_html}</h3>
                            <div class="pub-links">
                                {" ".join(links)}
                            </div>
                        </div>
                        <p class="pub-authors">{authors_html}</p>
                        <p class="pub-venue">{venue_html}</p>
                    </div>
                </article>"""


def render_dac_highlight_card(work: OrcidWork) -> str:
    """复用普通卡片，保留 DAC 的详情页入口。"""

    card = render_orcid_card(work)
    return card.replace('<div class="pub-links">', '<div class="pub-links"><a href="dac2026.html" class="pub-link">Page</a>', 1)


def render_publications_block(orcid_works: list[OrcidWork]) -> str:
    """每篇论文只渲染一次，保留已排序的 Fibo、HiFA、MSDF-BP、DAC 优先顺序。"""

    cards = "\n\n".join(
        render_dac_highlight_card(work)
        if work.title == DAC_HIGHLIGHT_TITLE.removeprefix("🏆 ") else render_orcid_card(work)
        for work in orcid_works
    )
    return cards.replace('class="pub-card"', 'class="pub-card" style="border-left: 3px solid #667eea;"', 1)


def replace_between_markers(source_text: str, replacement_body: str) -> str:
    """只替换受管标记之间的内容。"""

    managed_pattern = re.compile(
        rf"({re.escape(PUBLICATIONS_START_MARKER)})(.*)({re.escape(PUBLICATIONS_END_MARKER)})",
        re.DOTALL,
    )

    if not managed_pattern.search(source_text):
        raise RuntimeError("> ERR: [Python] index.html 缺少 Publications 受管标记")

    replacement_text = (
        f"{PUBLICATIONS_START_MARKER}\n"
        f"{replacement_body}\n"
        f"                {PUBLICATIONS_END_MARKER}"
    )

    # 只替换标记之间的正文，不影响区块外的手写结构。
    return managed_pattern.sub(replacement_text, source_text, count=1)


def update_stat_fallback(index_html: str, stat_name: str, stat_value: int) -> str:
    """更新首页统计兜底值。"""

    stat_pattern = re.compile(
        rf'(<span class="stat-number" data-stat="{re.escape(stat_name)}">)(\d+)(</span>)'
    )

    if not stat_pattern.search(index_html):
        raise RuntimeError(f"> ERR: [Python] index.html 缺少 {stat_name} 统计定位")

    # 替换 HTML fallback 值，保证离线或数据加载失败时仍显示正确数字。
    return stat_pattern.sub(rf"\g<1>{stat_value}\g<3>", index_html, count=1)


def update_project_card_fallbacks(index_html: str, github_projects_data: dict[str, Any]) -> str:
    """更新每张项目卡片的兜底指标。"""

    for project in github_projects_data["projects"]:
        project_name = re.escape(project["name"])
        card_pattern = re.compile(
            rf'(<div class="project-card" data-project="{project_name}">.*?<div class="project-metrics">)(.*?)(</div>)',
            re.DOTALL,
        )

        card_match = card_pattern.search(index_html)
        if not card_match:
            raise RuntimeError(f"> ERR: [Python] index.html 缺少项目卡片：{project['name']}")

        metrics_block = card_match.group(2)

        # 逐项覆盖卡片里的 fallback 指标，确保脚本未加载时也能显示最新值。
        for metric_name in ("stars", "forks", "clones14d"):
            metric_pattern = re.compile(
                rf'(<strong data-metric="{metric_name}">)(\d+)(</strong>)'
            )
            if not metric_pattern.search(metrics_block):
                raise RuntimeError(
                    f"> ERR: [Python] 项目卡片 {project['name']} 缺少 {metric_name} 指标定位"
                )

            metrics_block = metric_pattern.sub(
                rf"\g<1>{int(project[metric_name])}\g<3>",
                metrics_block,
                count=1,
            )

        index_html = (
            index_html[: card_match.start(2)]
            + metrics_block
            + index_html[card_match.end(2) :]
        )

    # 返回已经同步所有项目兜底指标的 HTML。
    return index_html


def update_index_html(github_projects_data: dict[str, Any], orcid_works: list[OrcidWork]) -> str:
    """更新首页中的统计兜底值与论文区块。"""

    index_html = read_text(INDEX_PATH)
    publications_count = len(orcid_works)
    summary = github_projects_data["summary"]

    # 先更新顶部四个兜底数字。
    index_html = update_stat_fallback(index_html, "publications", publications_count)
    index_html = update_stat_fallback(index_html, "projects", int(summary["projects"]))
    index_html = update_stat_fallback(index_html, "repositories", int(summary["repositories"]))
    index_html = update_stat_fallback(index_html, "stars", int(summary["stars"]))
    index_html = update_project_card_fallbacks(index_html, github_projects_data)

    publications_html = render_publications_block(orcid_works)
    index_html = replace_between_markers(index_html, publications_html)

    # 清理替换过程中可能遗留的行尾空格，保证 diff 检查通过。
    index_html = re.sub(r"[ \t]+\n", "\n", index_html)
    return index_html


def ensure_readme_script_row(readme_text: str, row_text: str) -> str:
    """确保 README 项目结构中包含同步脚本说明。"""

    if row_text in readme_text:
        return readme_text

    anchor = "| `images/` |"
    if anchor not in readme_text:
        raise RuntimeError("> ERR: [Python] README 缺少项目结构锚点，无法插入脚本说明")

    # 在静态资源目录之前插入同步脚本路径说明。
    return readme_text.replace(anchor, f"{row_text}\n{anchor}", 1)


def ensure_readme_maintenance_section(
    readme_text: str,
    section_title: str,
    section_body: str,
    insert_before_title: str,
) -> str:
    """补充 README 的维护说明章节。"""

    if section_title in readme_text:
        existing_pattern = re.compile(
            rf"{re.escape(section_title)}\n\n.*?(?=\n## |\Z)",
            re.DOTALL,
        )
        return existing_pattern.sub(f"{section_title}\n\n{section_body}\n", readme_text, count=1)

    if insert_before_title not in readme_text:
        raise RuntimeError("> ERR: [Python] README 缺少插入维护章节的锚点")

    # 将维护章节放到部署方式前，便于维护者先看到更新命令。
    return readme_text.replace(
        insert_before_title,
        f"{section_title}\n\n{section_body}\n\n{insert_before_title}",
        1,
    )


def update_readme_en(publications_count: int, repositories_count: int, stars_count: int) -> str:
    """更新英文 README 中的数量描述与维护说明。"""

    readme_text = read_text(README_EN_PATH)

    overview_pattern = re.compile(
        r"This repository powers .*?14-day clone counts\.",
        re.DOTALL,
    )
    overview_replacement = (
        "This repository powers [Eriemon.github.io](https://Eriemon.github.io), "
        "the personal academic homepage of Jiyuan Liu, a PhD student at Southeast University. "
        f"The site presents research interests in AI–Quantum–FPGA Collaborative Computing, "
        f"{publications_count} publications including accepted papers, and a GitHub project snapshot of selected projects from "
        f"{repositories_count} public repositories with {stars_count} total stars together with per-card stars, forks, "
        "and current 14-day clone counts."
    )
    readme_text = overview_pattern.sub(overview_replacement, readme_text, count=1)

    readme_text = re.sub(
        r"\| Publications \| .*? \|",
        f"| Publications | {publications_count} academic publications, including Fibo (FPT 2026, Accepted), followed by HiFA (ICCD 2026, Accepted), MSDF-BP (ITC-Asia 2026), DAC 2026 and the remaining ORCID works. |",
        readme_text,
        count=1,
    )
    readme_text = re.sub(
        r"\| Projects \| .*? \|",
        f"| Projects | Selected project cards; {repositories_count} public non-fork repositories in total. Stars, Forks, and Clones (14d) are refreshed. |",
        readme_text,
        count=1,
    )

    readme_text = ensure_readme_script_row(
        readme_text,
        "| `scripts/sync_homepage_data.py` | Refreshes GitHub metrics, rebuilds the ORCID-driven publication list, and updates README count text. |",
    )

    maintenance_body = (
        "Refresh homepage data with:\n\n"
        "```powershell\n"
        "python scripts/sync_homepage_data.py\n"
        "```\n\n"
        "Data sources:\n\n"
        "- GitHub public API for repository counts, stars, and forks.\n"
        "- ORCID public API for publication titles, authors, venues, and DOI links.\n\n"
        "Notes:\n\n"
        "- Requires authenticated gh CLI access for repository traffic. Clones (14d) values are refreshed; total Stars include all public non-fork repositories.\n"
        "- Fibo (FPT 2026, Accepted) and HiFA (ICCD 2026) are manually supplemented until ORCID contains them; Fibo, HiFA, MSDF-BP, and DAC precede the remaining works. All content is rendered before writing files."
    )
    readme_text = ensure_readme_maintenance_section(
        readme_text,
        "## Maintenance",
        maintenance_body,
        "## Deployment",
    )

    return readme_text


def update_readme_cn(publications_count: int, repositories_count: int, stars_count: int) -> str:
    """更新中文 README 中的数量描述与维护说明。"""

    readme_text = read_text(README_CN_PATH)

    overview_pattern = re.compile(
        r"本仓库用于维护 .*?近 14 天克隆次数。",
        re.DOTALL,
    )
    overview_replacement = (
        "本仓库用于维护 [Eriemon.github.io](https://Eriemon.github.io)，即 Jiyuan Liu 的个人学术主页。"
        f"主页展示 AI-量子-FPGA协同计算研究方向、{publications_count} 项论文（含已接收论文），"
        f"以及一个 GitHub 项目概览区：展示精选项目，全部 {repositories_count} 个公开非 Fork 仓库累计 {stars_count} 个 Stars，"
        "并为每个仓库显示星标、Fork 和当前近 14 天克隆次数。"
    )
    readme_text = overview_pattern.sub(overview_replacement, readme_text, count=1)

    readme_text = re.sub(
        r"\| Publications \| .*? \|",
        f"| Publications | {publications_count} 篇学术论文，Fibo（FPT 2026，已接收）居首，HiFA（ICCD 2026，已接收）第二，MSDF-BP（ITC-Asia 2026）第三，DAC 2026 第四，其余条目按 ORCID 同步生成。 |",
        readme_text,
        count=1,
    )
    readme_text = re.sub(
        r"\| Projects \| .*? \|",
        f"| Projects | 展示精选项目；全部公开非 Fork 仓库共 {repositories_count} 个，刷新卡片 Stars、Forks 和 14 天 Clones 指标。 |",
        readme_text,
        count=1,
    )

    readme_text = ensure_readme_script_row(
        readme_text,
        "| `scripts/sync_homepage_data.py` | 同步 GitHub 指标、重建基于 ORCID 的论文列表，并更新 README 中的数量描述。 |",
    )

    maintenance_body = (
        "使用以下命令刷新主页数据：\n\n"
        "```powershell\n"
        "python scripts/sync_homepage_data.py\n"
        "```\n\n"
        "数据来源：\n\n"
        "- GitHub 官方公开 API：同步仓库数、Stars 和 Forks。\n"
        "- ORCID 官方公开 API：同步论文标题、作者、期刊/会议信息与 DOI 链接。\n\n"
        "说明：\n\n"
        "- 需要已登录且可读取仓库流量的 gh CLI。刷新 Clones (14d)，总 Stars 包含全部公开非 Fork 仓库。\n"
        "- Fibo（FPT 2026，已接收）、HiFA（ICCD 2026）在 ORCID 收录前人工补录；Fibo、HiFA、MSDF-BP、DAC 优先，其余按日期倒序。全部渲染成功后才写文件。"
    )
    readme_text = ensure_readme_maintenance_section(
        readme_text,
        "## 维护方式",
        maintenance_body,
        "## 部署方式",
    )

    return readme_text


def write_github_projects_json(github_projects_data: dict[str, Any]) -> None:
    """写回前端读取的 GitHub 数据文件。"""

    json_text = json.dumps(github_projects_data, ensure_ascii=False, indent=2)
    write_text(DATA_PATH, f"{json_text}\n")


def main() -> int:
    """执行主页数据同步流程。"""

    github_projects_data, repositories_count = build_github_projects_json()
    orcid_works = build_orcid_works()

    index_html = update_index_html(github_projects_data, orcid_works)

    publications_count = len(orcid_works)
    stars_count = int(github_projects_data["summary"]["stars"])

    readme_en = update_readme_en(publications_count, repositories_count, stars_count)
    readme_cn = update_readme_cn(publications_count, repositories_count, stars_count)

    write_github_projects_json(github_projects_data)
    write_text(INDEX_PATH, index_html)
    write_text(README_EN_PATH, readme_en)
    write_text(README_CN_PATH, readme_cn)

    # 用简短状态输出来汇报同步结果。
    print(f"> INFO: [Python] 已刷新 GitHub 指标文件：{DATA_PATH}")
    print(f"> INFO: [Python] 已重建 Publications 区块，当前页面论文数：{publications_count}")
    print(f"> INFO: [Python] 已更新 README 数量描述，总 Stars：{stars_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
