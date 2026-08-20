# Codex를 활용한 Figma 디자인 시스템 추출

## Context

Codex PLUS 요금제를 사용하여 Figma MCP 서버를 통해 WANTED Design System의 디자인 토큰을 추출하고, 로컬에 디자인 시스템을 구축함. 간단한 로그인 페이지 HTML 구성 시 10% 크레딧 소모 문제 발생. 이를 커버하기 위해 디자인 MD 파일과 작업명세서 작성을 Codex에게 요청.

## Core

### Figma MCP 연결

- Figma → Account Settings → Personal Access Tokens에서 토큰 발급 (`figd_` 접두어)
- 환경변수 설정: `export FIGMA_TOKEN=***`
- Codex가 Figma MCP 서버의 도구들을 통해 디자인 토큰 추출, CSS/Tailwind 변환, 코드 → Figma 피드백 등 양방향 워크플로우 수행

### WANTED Design System 추출

- Figma Community에서 WANTED Design System 파일 접근
- Codex를 통해 디자인 토큰(색상, 타이포그래피, 스페이싱, 컴포넌트 등) 추출
- 로컬에 디자인 시스템 구축

### 작업명세서 작성

- 디자인 MD 파일 생성
- WANTED Design System을 참조한 로그인 HTML 구성을 위한 작업명세서 작성

## Insight

- Codex의 크레딧 소모가 큼 (10% 소모)
- 디자인 시스템 구축 및 명세서 작성 → 코드 구축 역할분배 필요성 확인
- Codex(디자인+명세서) → Hermes(구축) 하이브리드 워크플로우 결정
