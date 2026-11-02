# dsh-superagent-demo

Sandbox repository for dsh-superagent.

Requests are made by commenting `@<agent login> <request>` on an issue.

## 定时休息提醒 CLI

`rest_reminder.py` 是一个只依赖 Python 3 标准库的终端休息提醒工具：每工作 45 分钟提醒你离开屏幕休息 1 分钟，休息结束后提示可以继续。终端输出提醒文字并响铃，没有图形界面。

### 用法

```bash
python3 rest_reminder.py
```

启动后会输出提示并响铃；按 `Ctrl+C` 可随时干净退出。

### 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--interval` | `45` | 工作间隔，单位为分钟 |
| `--rest` | `1` | 休息时长，单位为分钟 |

两个参数都接受大于 0 的整数或小数（小数便于快速体验）。

示例：

```bash
# 每 25 分钟提醒一次，休息 5 分钟
python3 rest_reminder.py --interval 25 --rest 5

# 快速体验：每 6 秒提醒一次，休息 3 秒
python3 rest_reminder.py --interval 0.1 --rest 0.05
```
