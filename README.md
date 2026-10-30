# JSP-SKILL · 视频剪辑包装库

个人视频包装工作库与 `ai-video-packaging` Skill 备份。

## 内容

- [包装库](包装库/)：54 个独立包装模板，包含标题、关键词、字幕、组合界面与解释元素，以及本地预览、原片片段、参数、素材和字体。
- [包装目录](包装库/目录.md) / [拆解表](包装库/包装拆解表.md)：编号、场景与参考来源。
- [ai-video-packaging Skill](skills/ai-video-packaging/SKILL.md)：建库、按稿选包装、渲染透明素材、达芬奇时间线制作与音效对齐流程。

库内案例仍使用 R01–R54 编号，目录中的待评审状态按原文件保留。具体项目使用和修改不等于所有模板均已完成正式入库评审。

## 打开包装库

1. 下载仓库 ZIP 并解压，或克隆此仓库。
2. Windows 安装 Python 3，并确保 `python` 或 `py` 命令可用。
3. 双击 `包装库/打开包装库.cmd`，自动启动本地服务并打开浏览器。
4. 地址为 `http://127.0.0.1:8769/index.html`。重启电脑后再次双击入口即可。

也可在终端运行：

```sh
python -m http.server 8769 --bind 127.0.0.1 --directory 包装库
```

GitHub 文件页不会直接运行本地 HTML 预览。浏览器中的评审意见保存在该浏览器本地，不会自动提交 GitHub；可在页面导出评审 JSON。

## 安装 Skill

将 `skills/ai-video-packaging` 整个文件夹复制到对应工具的 skills 目录。例如 Codex 使用 `~/.codex/skills/ai-video-packaging`。安装后开启新会话以加载。

Skill 是供 AI 阅读的工作流说明；本地视频处理、浏览器渲染和达芬奇连接仍需相应运行环境。

## 重新渲染

浏览已有预览只需 Python。重新渲染模板还需要 Node.js、Playwright、ffmpeg、Chrome，以及部分分析脚本所需的 Python 包。

复制 `包装库/tools/runtime.example.json` 为同目录 `runtime.json`，填写本机路径后运行：

```sh
cd 包装库
node tools/render_all.cjs R13
```

`runtime.json`、日志、原始长视频、本期项目素材和成片输出不上传。`sources/sources.json` 保留来源信息，原视频路径统一写为可在本机配置的 `local_sources/Vxx.mp4`；历史分析脚本重跑前需按实际素材修改路径。

## 作者与许可

Skill 由 **大象学长**（全网同名）开源，原始出处：
https://q52zkkpo8s.feishu.cn/wiki/CmwewoJnmibaRrkWcNec3FPfnRf

原 Skill 文档、模板和代码按 **CC BY-NC 4.0** 分享，具体条款见 [原始 LICENSE](skills/ai-video-packaging/LICENSE)。本仓库保留作者署名，不代表原作者认可这些改动。

参考视频片段、照片等来自用户提供的参考材料，权利归原权利人；不因收录到本仓库而被重新授权。字体许可见 [fonts/OFL.txt](包装库/fonts/OFL.txt)。详见 [NOTICE](NOTICE.md)。
