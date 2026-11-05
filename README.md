# GitHub Research Skill

面向 Codex 等兼容 Agent 的 GitHub 调研工作流：从需求出发发现与比较仓库、核查项目声明、寻找可复用代码，并记录结论的证据与边界。

## 适合什么任务

- 寻找符合实际输入、平台和许可证约束的开源项目。
- 比较候选项目，核对 README、代码、Issue 和版本等证据。
- 判断一个项目能力是否有依据，或识别适合进一步验证的需求缺口。

此 Skill 做只读研究，不替代代码审查、部署、安装或运行第三方软件。它不能保证覆盖 GitHub 上全部项目。

## 安装与使用

```bash
npx -y skills add zseissol-debug/github-research-workflow-skill
```

需要 Node.js、npm、网络与支持 Skill 的 Agent；使用时按安装器提示选择目标。示例：“使用 github-research，比较适合 macOS 的本地图片去重开源工具，并核对许可证。”

可选采集脚本使用 Python 3 标准库访问 GitHub API；配置 `GITHUB_TOKEN` 或 `GH_TOKEN` 可使用用户自己的授权额度，未配置时受匿名 API 限制。不要把凭据写入报告或仓库。

本次安装验证使用 `skills` 1.7.4；该版本声明需要 Node.js 22.20.0 或更高。

## 来源与许可

由仓库维护者根据实际调研需求从零制作并持续迭代；当前版本为 0.5.12。代码与文档使用 [MIT 许可证](LICENSE)。历史调研案例和私人记录不在此仓库内。
