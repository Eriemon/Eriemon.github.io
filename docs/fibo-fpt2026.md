# Fibo 宣传页

`fibo-fpt2026.html` 是 FPT 2026 已接收论文 Fibo 的英文介绍页。页面按 DAC 2026 详情页排列。Abstract 照录经作者授权的主稿摘要，随后展示论文框架总图和原图注，再播放宣传视频。视频后的 Affiliations 沿用 DAC 详情页的信息框，单位和作者角色依据 Fibo 主稿署名。返回链接定位到 `index.html#publications`。

播放器直接读取 `videos/Fibo-FPT26.mp4`，由访问者点击播放。替换同名视频即可更新内容；如果更改文件名或画幅，请同步更新 HTML 中的路径或视频尺寸。本地检查视频拖动时使用支持 HTTP Range 请求的静态服务器。

框架图 `images/fibo-framework-overview.png` 由论文工程内的 `figures/fig-framework-overview.pdf` 全页等比渲染，点击图片可查看原尺寸。
