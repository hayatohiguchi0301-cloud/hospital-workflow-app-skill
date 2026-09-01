"""Validate the minimum structure and safety properties of a generated app."""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

REQUIRED = ("app.py", "db.py", "起動.bat", "requirements.txt", "README.md")
FORBIDDEN_PATTERNS = {
    "SQLを文字列補間しています": re.compile(r"(?:execute|executemany)\s*\(\s*f[\"']", re.I),
    "ハードコードされたWindows絶対パスがあります": re.compile(r"[A-Za-z]:\\\\(?:Users|Program Files|Windows)\\", re.I),
    "ハードコードされた秘密情報の可能性があります": re.compile(r"(?:password|api_key|secret)\s*=\s*[\"'][^\"']+[\"']", re.I),
}


def validate(project: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED:
        if not (project / name).is_file():
            errors.append(f"必須ファイルがありません: {name}")
    for path in project.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        try:
            ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            errors.append(f"Python構文エラー: {path.name}:{exc.lineno} {exc.msg}")
        for message, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path.name}: {message}")
    req = project / "requirements.txt"
    if req.exists() and "streamlit" not in req.read_text(encoding="utf-8").lower():
        errors.append("requirements.txt に streamlit がありません")
    readme = project / "README.md"
    if readme.exists():
        body = readme.read_text(encoding="utf-8")
        for term in ("streamlit run", "Python", "バックアップ", "別PC"):
            if term.lower() not in body.lower():
                errors.append(f"README.md に必要な説明がありません: {term}")
    launcher = project / "起動.bat"
    if launcher.exists():
        body = launcher.read_text(encoding="utf-8", errors="replace").lower()
        launcher_terms = {
            'cd /d "%~dp0"': "実行場所をアプリのフォルダへ固定する処理",
            ".venv\\scripts\\python.exe": "プロジェクト専用Python環境",
            "-m pip install -r requirements.txt": "依存パッケージの導入処理",
            "-m streamlit run": "Streamlitの起動処理",
        }
        for term, label in launcher_terms.items():
            if term not in body:
                errors.append(f"起動.bat に必要な処理がありません: {label}")
    return errors


def main() -> int:
    project = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(project)
    if errors:
        print("[NG] プロジェクト検証に失敗しました")
        for error in errors:
            print(f"- {error}")
        return 1
    print("[OK] 必須構成・構文・基本安全チェックを通過しました")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
