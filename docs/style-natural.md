# Natural 联系链接布局

目标：沿用现有 flex 布局，让桌面端四个 Contact 链接同行。

`.contact-content` 使用可用容器宽度，取消原先过窄的最大宽度；保持现有间距、按钮样式与手机端断点。窄屏沿用响应式堆叠，避免水平溢出。

Projects 桌面固定 `repeat(3, minmax(0, 1fr))`，六项为两行；沿用 <=768px 单列断点。
