#!/usr/bin/env python3
"""定时休息提醒：按固定工作间隔提醒休息，并在休息结束时提示继续。

仅使用 Python 3 标准库，终端输出 + 系统响铃，无图形界面。
用法见 ``python3 rest_reminder.py --help``。
"""

from __future__ import annotations

import argparse
import math
import sys
import time

WORK_MESSAGE = "该休息了，离开屏幕 1 分钟"
REST_DONE_MESSAGE = "休息结束，可以继续"


def _minutes_to_seconds(minutes: float) -> float:
    return minutes * 60.0


def _format_minutes(minutes: float) -> str:
    """把分钟数格式化成便于阅读的形式（整数不带小数点）。"""
    return str(int(minutes)) if float(minutes).is_integer() else f"{minutes:g}"


def _positive_minutes(text: str) -> float:
    """argparse 类型：接受大于 0 的有限分钟数。"""
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"不是有效数字：{text!r}") from None
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError("必须是大于 0 的分钟数")
    return value


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rest_reminder.py",
        description="定时休息提醒：每工作一段时间提醒你休息，休息结束后提示继续。",
    )
    parser.add_argument(
        "--interval",
        type=_positive_minutes,
        default=45.0,
        metavar="分钟",
        help="工作间隔（分钟，默认 45）",
    )
    parser.add_argument(
        "--rest",
        type=_positive_minutes,
        default=1.0,
        metavar="分钟",
        help="休息时长（分钟，默认 1）",
    )
    return parser


def _bell() -> None:
    """发送终端响铃字符（写到 stderr，不干扰标准输出内容）。"""
    sys.stderr.write("\a")
    sys.stderr.flush()


def _print_line(message: str) -> None:
    print(message, flush=True)


def _sleep_until(deadline: float) -> None:
    """休眠到 monotonic 时钟的指定时刻，避免长时间累计漂移。"""
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return
        time.sleep(remaining)


def _countdown(duration: float, label: str = "休息倒计时") -> None:
    """显示倒计时，直到 duration 秒结束。"""
    deadline = time.monotonic() + duration
    interactive = sys.stdout.isatty()
    last_shown = None
    line_width = 0
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            seconds = math.ceil(remaining)
            if seconds != last_shown:
                line = f"{label}：剩余 {seconds} 秒"
                if interactive:
                    line_width = max(line_width, len(line))
                    sys.stdout.write("\r" + line)
                else:
                    sys.stdout.write(line + "\n")
                sys.stdout.flush()
                last_shown = seconds
            time.sleep(min(0.1, remaining))
    finally:
        if interactive and line_width:
            # 覆盖并清除倒计时行，让后续输出（包括 Ctrl+C 退出）从行首开始。
            sys.stdout.write("\r" + " " * line_width + "\r")
            sys.stdout.flush()


def _notify(message: str) -> None:
    _print_line(message)
    _bell()


def run(interval_minutes: float, rest_minutes: float) -> None:
    """运行提醒循环：工作 interval 分钟，提醒后休息 rest 分钟，如此往复。"""
    interval = _minutes_to_seconds(interval_minutes)
    rest = _minutes_to_seconds(rest_minutes)
    _print_line(
        "定时休息提醒已启动：每工作 "
        f"{_format_minutes(interval_minutes)} 分钟提醒一次，"
        f"休息 {_format_minutes(rest_minutes)} 分钟。按 Ctrl+C 退出。"
    )
    next_reminder = time.monotonic() + interval
    while True:
        _sleep_until(next_reminder)
        _notify(WORK_MESSAGE)
        _countdown(rest)
        _notify(REST_DONE_MESSAGE)
        next_reminder = time.monotonic() + interval


def main(argv: list[str] | None = None) -> int:
    try:
        args = _build_parser().parse_args(argv)
        run(args.interval, args.rest)
    except KeyboardInterrupt:
        _print_line("已退出定时休息提醒。")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
