<p align="center">
  <a href="README.md"><strong>English</strong></a>
  <span>&nbsp;|&nbsp;</span>
  <a href="README-CN.md">中文</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-1f6feb"></a>
  <a href="https://Eriemon.github.io"><img alt="GitHub Pages" src="https://img.shields.io/badge/GitHub%20Pages-live-16a34a"></a>
  <img alt="Stack" src="https://img.shields.io/badge/stack-HTML%20%7C%20CSS%20%7C%20JS-f59e0b">
  <img alt="Default Style" src="https://img.shields.io/badge/default-Natural-22c55e">
</p>

<h1 align="center">Jiyuan Liu Academic Homepage</h1>

<p align="center">
  A bilingual GitHub Pages academic homepage for research, publications, selected projects, and news.
</p>

## Overview

This repository powers [Eriemon.github.io](https://Eriemon.github.io), the personal academic homepage of Jiyuan Liu, a PhD student at Southeast University. The site presents research interests in high performance computing and FPGA accelerator design, 11 publications, 5 selected GitHub projects with 16 total stars, and recent academic news including QCDAC 2026 and DAC 2026.

The site is intentionally static: it uses plain HTML, CSS, and JavaScript so it can be reviewed easily, deployed through GitHub Pages, and maintained without a build system.

## Features

- Bilingual English and Chinese content switching.
- Natural style as the default visual theme, with an Academic style available from the style toggle.
- Light and dark theme switching with local browser preference persistence.
- Responsive layout for desktop and mobile visitors.
- Publication, project, news, experience, awards, and contact sections.
- GitHub Pages deployment with no runtime backend or package dependency.

## Site Sections

| Section | Purpose |
| --- | --- |
| About | Research profile, lab affiliation, programming languages, and technical skills. |
| Publications | 11 academic publications, including the DAC 2026 paper highlight. |
| Projects | 5 selected repositories: `Github-Homepage-Setup-Guide`, `hls-generator`, `verilog-generator`, `remote-ssh`, and `github-management`. |
| News | Recent academic updates, including QCDAC 2026 in Ningbo, DAC 2026, FPT 2026, HIQC Lab recruitment, and Integration. |
| Experience | Education and research/work experience timeline. |
| Contact | Email, GitHub, ORCID, Google Scholar, and related academic links. |

## Project Map

| Path | Description |
| --- | --- |
| `index.html` | Main single-page homepage content and bilingual translation dictionary. |
| `style-natural.css` | Default Natural visual system. |
| `style-academic.css` | Alternative Academic visual system. |
| `script.js` | Theme/style/language toggles, scroll animation, and UI behavior. |
| `dac2026.html` | Dedicated DAC 2026 paper detail page. |
| `images/` | Local profile and research images used by the site. |

## Local Preview

From the repository root:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8765/
```

Useful checks before publishing:

```powershell
git diff --check
```

## Deployment

The site is designed for GitHub Pages and can be served directly from the repository without a build step. Updates to the published branch are reflected at:

[https://Eriemon.github.io](https://Eriemon.github.io)

## Privacy and Scope

This repository is a public static homepage. Do not commit private drafts, access tokens, local machine paths, unpublished personal data, or generated files that are not part of the site. External links should point only to public academic, project, or contact pages that are intended for visitors.

## Contact

- Email: [erie@seu.edu.cn](mailto:erie@seu.edu.cn)
- GitHub: [@Eriemon](https://github.com/Eriemon)
- ORCID: [0009-0000-9034-6811](https://orcid.org/0009-0000-9034-6811)
- Google Scholar: [Jiyuan Liu](https://scholar.google.com/citations?user=0-PQi3AAAAAJ)

## Citation

Citation metadata is available in [CITATION.cff](CITATION.cff). A BibTeX-style reference is:

```bibtex
@software{liu_2026_eriemon_homepage,
  author = {Liu, Jiyuan},
  title = {{Eriemon.github.io}: A Personal Academic Homepage},
  year = {2026},
  url = {https://github.com/Eriemon/Eriemon.github.io},
  license = {Apache-2.0}
}
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).
