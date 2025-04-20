# sit-wechat-bot

一个基于 MCP+LangChain 的微信群聊机器人

# 环境准备

```bash
# MacOS/Linux 安装 UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows 安装 UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 激活 Python 环境
uv venv
```

# 架构设计

## Agent

在每个 Windows 节点上有一个微信，每个微信附带有一个 Agent 进程，这个进程用于包装所有的 wcferry 的操作，以便于和微信交互。

配置文件结构：

```yml
logger: <日志相关配置>
wcferry: <WCF相关配置>
http_callback: <接收消息并传递给HTTP CALLBACK>
```

对外提供API接口：

- 发送消息


## Gateway

在中心服务器运行一个Gateway节点，Agent将
