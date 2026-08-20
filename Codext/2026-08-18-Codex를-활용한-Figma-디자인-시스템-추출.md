# Codex를 활용한 Figma 디자인 시스템 추출

## 학습 시작

Codex PLUS 요금제를 사용하여 Figma MCP 서버에 연결하고, WANTED Design System의 디자인 토큰을 추출하여 로컬에 디자인 시스템을 구축하는 방법을 학습했습니다. 로그인 페이지 HTML을 구성하는 과정에서 10% 크레딧이 소모되는 문제를 확인했고, 이를 보완하기 위해 디자인 MD 파일과 작업명세서를 Codex에게 작성하도록 요청했습니다.

## 학습 과정

### 1. Figma MCP 연결

- Figma → Account Settings → Personal Access Tokens에서 토큰 발급 (`figd_` 접두어)
- 환경변수 설정: `export FIGMA_TOKEN=***`
- Codex가 Figma MCP 서버의 도구들을 통해 디자인 토큰 추출, CSS/Tailwind 변환, 코드 → Figma 피드백 등 양방향 워크플로우 수행

### 2. WANTED Design System 추출

- Figma Community에서 WANTED Design System 파일 접근
- Codex를 통해 디자인 토큰(색상, 타이포그래피, 스페이싱, 컴포넌트 등) 추출
- 추출한 토큰을 로컬에 저장하여 디자인 시스템 구축

### 3. 작업명세서 작성

- 디자인 MD 파일을 생성하여 WANTED Design System의 구조를 정리했습니다.
- WANTED Design System을 참조한 로그인 HTML 구성을 위한 작업명세서를 작성했습니다.

## 학습 결과

- Codex의 크레딧 소모량이 큼 (10% 소모)
- 디자인 시스템 구축 및 명세서 작성 → 코드 구축 역할분배 필요성 확인

## 다음 단계

- Codex(디자인 + 명세서) → Hermes(구축) 하이브리드 워크플로우로 역할분배 확정
- 향후 동일한 디자인 시스템 기반 페이지 구축 시 이 워크플로우 적용
