"""
README 인덱스 자동 업데이트 스크립트

저장소 내 모든 TIL Markdown 파일을 탐색하여 README.md의 인덱스 섹션을
카테고리별로 최신화합니다.
"""

import re
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).resolve().parents[2]
README_PATH = REPO_ROOT / "README.md"

# README에서 인덱스 섹션을 구분하는 마커
INDEX_START = "<!-- TIL-INDEX-START -->"
INDEX_END = "<!-- TIL-INDEX-END -->"

# 카테고리 표시 이름 매핑
CATEGORY_LABELS: dict[str, str] = {
    "language": "🖥️ Language",
    "framework": "🛠️ Framework",
    "database": "🗄️ Database",
    "devops": "⚙️ DevOps",
    "algorithm": "📐 Algorithm",
    "network": "🌐 Network",
    "security": "🔒 Security",
    "tools": "🔧 Tools",
    "etc": "📂 Etc",
}


def collect_til_files() -> dict[str, list[Path]]:
    """카테고리별로 TIL Markdown 파일을 수집합니다."""
    categories: dict[str, list[Path]] = {}
    for md_file in sorted(REPO_ROOT.rglob("*.md")):
        # README 자체와 .github 내 파일 제외
        if md_file.name == "README.md" or ".github" in md_file.parts:
            continue
        category = md_file.parent.name
        categories.setdefault(category, []).append(md_file)
    return categories


def extract_title(md_file: Path) -> str:
    """Markdown 파일의 첫 번째 H1 제목을 추출합니다."""
    try:
        for line in md_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return md_file.stem


def build_index(categories: dict[str, list[Path]]) -> str:
    """카테고리별 인덱스 Markdown 문자열을 생성합니다."""
    lines: list[str] = [
        INDEX_START,
        "",
        f"*마지막 업데이트: {date.today().isoformat()}*",
        "",
    ]

    if not categories:
        lines.append("*아직 등록된 TIL이 없습니다. 첫 번째 학습 메모를 등록해 보세요!*")
        lines.append("")
    else:
        for category, files in sorted(categories.items()):
            label = CATEGORY_LABELS.get(category, f"📁 {category.capitalize()}")
            lines.append(f"## {label}")
            lines.append("")
            for md_file in sorted(files, reverse=True):
                title = extract_title(md_file)
                rel_path = md_file.relative_to(REPO_ROOT).as_posix()
                lines.append(f"- [{title}]({rel_path})")
            lines.append("")

    lines.append(INDEX_END)
    return "\n".join(lines)


def update_readme(new_index: str) -> None:
    """README.md의 인덱스 섹션을 업데이트합니다."""
    readme_text = README_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(INDEX_START) + r".*?" + re.escape(INDEX_END),
        re.DOTALL,
    )

    if pattern.search(readme_text):
        updated = pattern.sub(new_index, readme_text)
    else:
        # 마커가 없으면 파일 끝에 추가
        updated = readme_text.rstrip() + "\n\n" + new_index + "\n"

    README_PATH.write_text(updated, encoding="utf-8")
    print("README.md 인덱스가 업데이트되었습니다.")


def main() -> None:
    categories = collect_til_files()
    new_index = build_index(categories)
    update_readme(new_index)


if __name__ == "__main__":
    main()
