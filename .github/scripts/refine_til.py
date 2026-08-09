"""
AI TIL 정제 스크립트

GitHub Issue로 제출된 학습 메모를 OpenAI API를 사용해 표준화된 Markdown 문서로
변환하고, 검토용 Pull Request를 자동으로 생성합니다.
"""

import os
import re
import sys
from datetime import date
from pathlib import Path

from github import Github
from openai import OpenAI

# ── 환경 변수 ─────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ISSUE_NUMBER = int(os.environ["ISSUE_NUMBER"])
ISSUE_TITLE = os.environ["ISSUE_TITLE"]
ISSUE_BODY = os.environ["ISSUE_BODY"]
REPO_NAME = os.environ["REPO"]

# ── 상수 ──────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """\
당신은 개발자의 학습 메모를 표준화된 TIL(Today I Learned) 문서로 정제하는 전문 AI입니다.

다음 규칙을 반드시 준수하세요:
1. 기술적 사실 관계를 검증하고 오류가 있으면 바로잡아 주세요.
2. 아래 Markdown 템플릿 구조를 정확히 따르세요.
3. 코드 예시는 반드시 언어 태그를 포함한 코드 블록으로 작성하세요.
4. 내용은 한국어로 작성하되, 기술 용어는 영어 원문을 병기하세요.
5. 참고 자료 섹션에는 신뢰할 수 있는 공식 문서 링크를 포함하세요.
6. 출력은 Markdown 본문만 반환하고 다른 텍스트는 포함하지 마세요.

## 템플릿

# {주제}

> **한 줄 요약**: {핵심 내용을 한 문장으로}

## 개요

{2~4문장으로 개념 소개}

## 핵심 내용

{주요 개념, 원리, 동작 방식 설명}

## 코드 예시

```{언어}
{동작 가능한 예시 코드}
```

## 주의사항 / 트레이드오프

{알아두어야 할 제한사항이나 trade-off}

## 참고 자료

- [공식 문서]({url})
"""

USER_PROMPT_TEMPLATE = """\
다음 학습 메모를 TIL 문서로 정제해 주세요.

**제목**: {title}
**메모 내용**:
{body}
"""


def parse_category(body: str) -> str:
    """이슈 본문에서 카테고리를 추출합니다."""
    match = re.search(r"### 카테고리[^\n]*\n+([a-z]+)", body)
    if match:
        return match.group(1)
    print("⚠️  카테고리를 감지하지 못했습니다. 기본값 'etc'로 설정합니다.")
    return "etc"


def parse_topic(body: str) -> str:
    """이슈 본문에서 주제를 추출하고 ASCII 전용 슬러그로 변환합니다."""
    match = re.search(r"### 주제[^\n]*\n+(.+)", body)
    topic = match.group(1).strip() if match else ISSUE_TITLE.replace("[TIL]", "").strip()

    # ASCII 범위 문자만 유지하여 파일 경로/브랜치 이름 호환성을 보장합니다.
    ascii_topic = topic.encode("ascii", errors="ignore").decode()
    slug = re.sub(r"[^a-z0-9\s-]", "", ascii_topic.lower())
    slug = re.sub(r"\s+", "-", slug).strip("-")
    # ASCII 변환 결과가 비어 있으면 이슈 번호를 fallback으로 사용합니다.
    return slug or f"til-{ISSUE_NUMBER}"


def refine_with_ai(title: str, body: str) -> str:
    """OpenAI API를 통해 학습 메모를 TIL 문서로 정제합니다."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(title=title, body=body),
            },
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def create_pr(repo, branch_name: str, file_path: str, content: str) -> None:
    """TIL 문서 초안을 포함하는 Pull Request를 생성합니다."""
    default_branch = repo.default_branch
    source = repo.get_branch(default_branch)

    # 브랜치 생성
    repo.create_git_ref(
        ref=f"refs/heads/{branch_name}",
        sha=source.commit.sha,
    )

    # 파일 커밋
    repo.create_file(
        path=file_path,
        message=f"docs: TIL 초안 생성 - {ISSUE_TITLE} [#{ISSUE_NUMBER}]",
        content=content,
        branch=branch_name,
    )

    # PR 생성
    pr_body = (
        f"## ✅ TIL 문서 검토 체크리스트\n\n"
        f"이 PR은 AI 에이전트가 자동 생성한 TIL 문서 초안입니다. "
        f"아래 항목을 직접 검토 후 승인해 주세요.\n\n"
        f"**원본 이슈:** closes #{ISSUE_NUMBER}\n\n"
        f"---\n\n"
        f"### 검토 항목\n\n"
        f"- [ ] 기술적 사실 관계가 정확한가?\n"
        f"- [ ] 코드 예시가 올바르게 동작하는가?\n"
        f"- [ ] 내용이 충분히 이해 가능하도록 설명되어 있는가?\n"
        f"- [ ] 카테고리 및 파일 경로가 적절한가?\n\n"
        f"---\n\n"
        f"> README 인덱스는 이 PR이 **Merge된 후** 자동으로 업데이트됩니다.\n\n"
        f"> 승인(Merge) 후 해당 TIL 문서가 자동으로 저장소에 기록됩니다."
    )
    repo.create_pull(
        title=f"[TIL 초안] {ISSUE_TITLE}",
        body=pr_body,
        head=branch_name,
        base=default_branch,
    )


def main() -> None:
    category = parse_category(ISSUE_BODY)
    topic_slug = parse_topic(ISSUE_BODY)
    today = date.today().isoformat()

    print(f"카테고리: {category}, 주제 슬러그: {topic_slug}")

    # AI 정제
    print("AI 정제 중...")
    refined_content = refine_with_ai(ISSUE_TITLE, ISSUE_BODY)

    # 파일 경로 결정
    file_path = f"{category}/{today}-{topic_slug}.md"
    branch_name = f"til/{today}-{topic_slug}"

    # GitHub API
    gh = Github(GITHUB_TOKEN)
    repo = gh.get_repo(REPO_NAME)

    print(f"PR 생성 중... 파일: {file_path}")
    create_pr(repo, branch_name, file_path, refined_content)
    print("완료!")


if __name__ == "__main__":
    main()
