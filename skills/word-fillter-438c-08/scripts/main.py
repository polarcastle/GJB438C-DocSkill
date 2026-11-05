"""Skill 命令行入口：共享引擎位于仓库根 shared/，模板专属规则位于本目录 rules.py。"""

import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[3] / "shared"
sys.path.insert(0, str(_SHARED))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from strict_word_filler.pipeline import main as _main  # noqa: E402
import rules  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(_main(rules))
