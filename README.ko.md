# iShine

[English](README.md)

AI 커리어 에이전트.

*커리어 정보는 한 번만. 지원할 때마다 맞춤 이력서를.*

[Claude Code](https://claude.ai/claude-code) 기반. [Codex](https://github.com/openai/codex)도 지원합니다.

<!-- TODO: 데모 GIF 추가 예정 -->

## 왜 iShine인가?

매번 공고에 맞게 이력서를 다시 쓰는 건 느리고 반복적이며 실수하기 쉽습니다. 대부분의 사람들은 범용 이력서를 그대로 내거나, 손으로 수작업 맞춤화에 몇 시간을 씁니다.

iShine은 이 힘든 과정을 자동화합니다:

1. **JD 분석** — 핵심 요구사항, 키워드, 신호를 추출합니다
2. **포지셔닝 전략 수립** — 프로필에서 가장 적합한 프로젝트와 수치를 선별합니다
3. **맞춤 이력서 초안 작성** — XYZ 포맷 항목, JD에 맞춘 스킬 섹션
4. **3가지 시뮬레이션 페르소나로 검증** — 채용 매니저, 직무 동료, 리크루터가 각각 초안을 콜드 리뷰합니다
5. **PDF 또는 DOCX로 내보내기**

커리어 데이터는 로컬에 보관됩니다 — AI 모델 API 외에 외부 서버로 전송되는 데이터는 없습니다.

## 스킬

```
JD 입력 → [write] 전략 + 초안 → [validate] 페르소나 리뷰 → [export] PDF/DOCX

유틸리티:  [ingest] 프로필 데이터    [humanizer] AI 말투 정리    [update-preference] 스타일 설정
```

| 스킬 | 기능 |
|------|------|
| **write** | JD 분석 → 포지셔닝 전략 → 맞춤 이력서 초안 |
| **validate** | 기계적 검토 + 3-페르소나 콜드 리뷰 → 종합 → 개선된 v2 |
| **export** | 이력서 또는 커버레터를 PDF / DOCX로 렌더링 |
| **ingest** | 커리어 데이터, 프로젝트 업데이트, 지원 결과를 프로필에 추가 |
| **humanizer** | 텍스트의 AI 말투 패턴을 감지하고 제거 |
| **update-preference** | 세션의 문체, 톤, 스타일 설정 저장 |

### 결과 추적

어느 이력서가 면접으로 이어졌는지 추적합니다. iShine은 지원 결과를 기록하고 결과 패턴을 활용해 향후 초안을 개선합니다 — 유사 직무에서 효과가 있었던 전략을 우선 적용합니다.

## 시작하기

### 1. 설치

[Claude Code](https://claude.ai/claude-code)(또는 [Codex](https://github.com/openai/codex))를 열고 다음과 같이 입력하세요:

> "Clone https://github.com/hosioobo/iShine and set it up for me."

끝입니다. 에이전트가 나머지를 처리합니다 — 클론, 예시 파일 복사, 폴더 구조 생성까지 모두 자동으로 됩니다.

### 2. 프로필 구성

커리어 정보를 대화에 넣어주세요 — 이력서 PDF, LinkedIn 내보내기, 글머리 메모, 무엇이든 괜찮습니다:

> "Here's my background. Organize this into my profile."

iShine이 파싱해서 올바른 파일 구조로 정리해줍니다. 언제든지 추가할 수 있습니다:

> "I just finished a project where I migrated 3 services to Kubernetes and cut deploy time by 40%. Add this."

### 3. 이력서 생성

채용 공고 URL이나 텍스트를 붙여넣으세요:

> "Write a resume for this: https://example.com/jobs/12345"

iShine이 JD를 분석하고, 프로필에서 가장 적합한 경험을 골라 맞춤 이력서 초안을 작성합니다. 그다음 검증을 실행하세요:

> "Validate the draft."

3명의 시뮬레이션 리뷰어(채용 매니저, 리크루터, 직무 동료)가 콜드 리뷰를 진행합니다. iShine이 피드백을 종합해 개선된 v2를 작성합니다.

### 4. 내보내기

> "Export as PDF."

### 요구사항

- [Claude Code](https://claude.ai/claude-code) 또는 [Codex](https://github.com/openai/codex)
- Python 3.9+ with Playwright (PDF/DOCX 내보내기용 — 필요 시 에이전트가 자동 설치합니다)

## 에이전트 호환성

| 에이전트 | 동작 방식 |
|---------|----------|
| **Claude Code** (주요) | `.claude/skills/`의 스킬, `CLAUDE.md`로 오케스트레이션 |
| **Codex** | `.agents/skills/`의 스킬, `AGENTS.md`로 오케스트레이션 |

두 에이전트 모두 동일한 코어를 읽습니다 — 템플릿, 스크립트, 프로필 데이터는 공유됩니다. `.claude/`와 `.agents/` 디렉토리에는 에이전트별 스킬 정의만 들어 있습니다.

## 파일 구조

```
├── CLAUDE.md                # Claude Code 오케스트레이터
├── AGENTS.md                # Codex 오케스트레이터
├── .claude/skills/          # Claude Code 스킬 (정식)
├── .agents/skills/          # Codex 어댑터 스킬
├── templates/               # 이력서 & 커버레터 템플릿 (en + ko)
├── scripts/                 # 내보내기 렌더링 스크립트
├── preferences.example.md   # 스타일 & 톤 설정 (템플릿)
├── index.example.yaml       # 런타임 상태 (템플릿)
└── profile/                 # 커리어 데이터 (gitignore 처리됨)
```

## FAQ

**개발자가 아니어도 사용할 수 있나요?**
네. 모든 작업은 자연어로 이루어집니다. Claude Code를 설치할 수 있다면 iShine을 사용할 수 있습니다.

**영어 외 언어도 지원하나요?**
네. iShine은 대상 언어로 이력서를 네이티브하게 생성합니다. 영어와 한국어 템플릿이 기본 포함됩니다.

**데이터는 어디에 저장되나요?**
모든 커리어 데이터는 로컬 머신의 `profile/`에 저장됩니다. 기본적으로 gitignore 처리되어 있어, 직접 선택하지 않는 한 커밋되거나 업로드되지 않습니다.

**비용은 얼마인가요?**
iShine 자체는 무료 오픈소스입니다. AI 모델을 위한 Claude Code 구독(또는 Codex)이 필요하며, 사용량은 토큰 단위로 각 제공업체를 통해 청구됩니다.

## 라이선스

MIT
