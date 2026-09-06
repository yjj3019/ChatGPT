# ChatGPT·Codex 전이 팩

엔지니어링·문서 작업·증거 기반 완료를 위한 **모델 비의존** 작업 지침입니다. 이 저장소는 **지침과 라우팅**을 바꾸며, 모델 가중치나 숨은 추론을 학습·복사하지 않습니다. 세션 간 자동 기억도 만들지 않습니다.

**English:** [README.md](README.md)

## AI 에이전트용 (저장소 URL만 있을 때)

```bash
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
python3 scripts/install_pack.py --auto
# 다음: Codex → 이 저장소를 워크스페이스로 연다 (AGENTS.md 로드)
# ChatGPT → CHATGPT.md를 Project Instructions에 붙여넣기; 필요 시 docs/ 첨부
```

- `python3 scripts/install_pack.py --auto` — Claude / Codex / Grok / Cursor / AGENTS 호스트를 감지해 각 스킬 루트에 `chatgpt-transfer/`로 복사
- `python3 scripts/install_pack.py --print-chatgpt` — ChatGPT Project Instructions 붙여넣기 절차 (웹은 완전 자동화 불가)
- `python3 scripts/install_pack.py --check` — 설치 파일 확인 + `validate_framework.py` 실행
- `python3 scripts/install_pack.py --help` — `--dest`, `--with-tests`, `--dry-run` 등

Codex 권장 경로: **이 클론을 워크스페이스로 열어** 루트의 `AGENTS.md`가 로드되게 합니다. 스킬 복사는 `~/.agents/skills` 등에서 팩을 찾는 호스트용입니다. 이미 있는 더 높은 우선순위 워크스페이스 규칙은 유지하세요.

## 이 팩이 하는 일 / 하지 않는 일

| 하는 일 | 하지 않는 일 |
|---|---|
| 선택 로딩이 있는 얇은 ChatGPT·Codex 진입점 | 파인튜닝·가중치 학습·CoT 증류 |
| 모델 공통 Context Budget + Model-Invariant Floor | 모든 모델이 동일 성능을 낸다는 보장 |
| sync / validate / measure / 골든 테스트 유지보수 도구 | 자동 교차 세션 기억·비밀 저장 |
| 권고형 모델 라우팅 (`gpt-6-astra` … `gpt-5.4-mini`) | 호스트 모델 가용성 확인의 대체 |

## 진입점 하나 고르기

| 용도 | 진입 |
|---|---|
| ChatGPT Project | `CHATGPT.md`를 Project Instructions에 넣고, 관련 `docs/`를 프로젝트 지식으로 제공 |
| Codex | **이 저장소에서** Codex를 시작해 `AGENTS.md`를 로드 |
| 원샷 복사/붙여넣기 | 저장소를 붙일 수 없을 때 `docs/chatgpt-5.5-all-in-one-instructions.md` (Core + 코딩/제안/블로그) |
| 스킬형 호스트 | `--auto` 후 설치된 `chatgpt-transfer/` (`SKILL.md` + `AGENTS.md`) |

세션 시작 시 선택한 진입을 읽습니다. 진입점은 작업을 **가장 작은** 관련 가이드로 보냅니다. 단순 작업은 Core만 사용합니다. 전체·단독 가이드는 대안이며 매 작업에 쌓는 층이 아닙니다.

## Context Budget + Model-Invariant Floor

**Context Budget (일반 사용):** Core + 매핑된 가이드 1–2개, 또는 작업 섹션 1개 + 도메인 섹션 1개. 전체 transfer 가이드·all-in-one·패턴 뱅크·모든 `docs/codex-*.md`를 **미리 로드하지 마세요**.

**Model-Invariant Floor** (`docs/chatgpt-codex-model-routing.md`): `gpt-6-astra` … `gpt-5.4-mini`와 무관하게:

1. 동일한 Core + Operational Integrity (증거·완료·권한·비밀 금지).
2. 동일한 Context Budget — 약한/강한 모델에 문서를 더 쏟아 “보정”하지 않음.
3. 동일한 Task Loading Map / Intent Classifier.
4. 동일한 출력 계약 (`[unverified]`, 최소 완전 변경, 가짜 완료 금지).
5. 막히면: **모델을 상향** (`mini` → `luna` → `terra` → `sol` → `astra`); 무관한 지침을 **늘리지 않음**.

권고 기본값(가용성 확인 필요): 복잡 → `gpt-6-astra`; 일상 에이전틱 → `gpt-5.6-sol`; 일상 코딩 → `gpt-5.6-terra`; 저비용/빠른 코딩 → `gpt-5.6-luna`; 아주 작은 작업 → `gpt-5.4-mini`.

## 집중 가이드

- `docs/chatgpt-5.5-project-instructions.md` — 작업/출력·노력 규칙 (Core)
- `docs/chatgpt-operational-integrity-rules.md` — 권한·증거·행동·완료
- `docs/chatgpt-coding-rules.md` — 구현·디버깅·리뷰
- `docs/chatgpt-proposal-review-rules.md` / `docs/chatgpt-blog-rules.md` — 문서 계약
- `docs/chatgpt-engineering-task-rules.md` — 아키텍처·RCA·리서치·SOP·프롬프트/보안 리뷰 (**해당 섹션만**)
- `docs/chatgpt-domain-packs.md` — RHEL, OpenShift, Kubernetes, Linux, Ansible, Satellite, EA, AI 인프라, EV (**해당 섹션만**)
- `docs/chatgpt-knowledge-work-rules.md` — 회의·발표·경영 요약
- `docs/chatgpt-codex-model-routing.md` — 날짜가 있는 모델 권고 + Model-Invariant Floor
- `docs/codex-*.md` — Codex 운영·Office·서브에이전트·팀 게이트 (필요할 때만)
- `prompts/chatgpt-task-prompts.md` — 선택적 작업 프롬프트
- `docs/chatgpt-transfer-instructions.md` — 생성되는 전체 참고; 요청 시에만 로드
- `docs/fable5-pattern-bank-for-chatgpt.md` — 선택적 역사 보정 (자동 로드 금지)

파일명에 `5.5`가 있어도 해당 모델을 요구하지 않습니다(호환용 이름).

## 유지보수와 검증

Python 3.11+와 표준 라이브러리만 사용합니다. 저장소 검사에 패키지 설치·API 키·모델 호출은 필요 없습니다.

```text
python scripts/sync_runtime.py
python scripts/sync_runtime.py --check
python scripts/validate_framework.py
python -m unittest discover -s tests -p "test_*.py"
python scripts/measure_load.py
python scripts/install_pack.py --check
```

canonical 원본을 수정한 뒤 `sync_runtime.py`로 배포 문서 세 개를 재생성하세요. sync `--check`는 파일을 쓰지 않습니다. 검증은 생성 문서 일치, 라우팅 대상, 로컬 참조, 필수 Golden Test 계약, 펜스 인식 섹션 파싱, Core 불변식, 문자 예산(`CHATGPT.md` ≤ 8000, `AGENTS.md` ≤ 4000)을 확인합니다. 회귀 테스트는 일회용 형제 복사본을 쓰므로 저장소 부모가 쓰기 가능해야 합니다.

GitHub Actions는 Windows·Linux에서 Python 3.11·3.12로 검사합니다. `measure_load.py`는 정규화된 UTF-8 바이트를 보고하며, bytes/4 추정은 **실제 토큰이 아니며** 호스트/도구 오버헤드는 제외합니다.

## 개선·시뮬레이션 근거

- [5차 개선 리포트](docs/optimization-report-2026-09-06.md) — Core 다이어트, AGENTS 축소, 라우팅, 예산
- [Simulation-10 리포트](docs/simulation-10-report-2026-09-06.md) — context budget, model floor, sync, 펜스 인식 섹션, 불변식 (PR #4/#5/#6/#7 이후)
- 행동 평가 루브릭: `tests/Scorecard.md`, `tests/GoldenTest-015.md` … `tests/GoldenTest-037.md`

구조 검사는 실제 ChatGPT/Codex 행동 시험을 실행하지 않습니다. 라우팅에 참고한 공식 원칙(속도·정확도 이득의 증명은 아님): [AGENTS.md 발견](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [선택적 스킬 로딩](https://learn.chatgpt.com/docs/build-skills), [지침 명확성](https://developers.openai.com/api/docs/guides/latest-model) (확인일 2026-09-06).
