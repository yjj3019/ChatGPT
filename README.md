# ChatGPT·Codex 전이 팩

엔지니어링·문서 작업·증거 기반 완료를 위한 **모델 비의존** 작업 지침입니다. 이 저장소는 **지침과 라우팅**을 바꾸며, 모델 가중치나 숨은 추론을 학습·복사하지 않습니다. 세션 간 자동 기억도 만들지 않습니다.

**언어:** 한국어 | [English](README.en.md)

## AI 에이전트용 (저장소 URL만 있을 때)

```bash
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
python3 scripts/install_pack.py --auto
# 다음: Codex → 이 저장소를 워크스페이스로 연다 (AGENTS.md 적용 여부 확인)
# ChatGPT → CHATGPT.md를 Project Instructions에 붙여넣기; 필요 시 docs/ 첨부
```

- `python3 scripts/install_pack.py --auto` — Claude / Codex / Grok / Cursor / AGENTS 호스트를 감지해 각 스킬 루트에 `chatgpt-transfer/`로 복사
- `python3 scripts/install_pack.py --print-chatgpt` — ChatGPT Project Instructions 붙여넣기 절차 (웹은 완전 자동화 불가)
- `python3 scripts/install_pack.py --check` — 설치 파일 확인 + `validate_framework.py` 실행
- `python3 scripts/install_pack.py --help` — `--dest`, `--with-tests`, `--dry-run` 등

동일한 설치는 건너뛰며 사용자 파일을 보존합니다. 변경·누락되었거나 구형인 설치는 덮어쓰지 않습니다. `--force`는 사용자 추가 파일까지 전체 교체하므로 먼저 백업하세요. `--dry-run`은 쓰기 없이 충돌을 검사하고, `--check`는 로컬 콘텐츠 매니페스트의 무결성을 확인합니다(배포자 인증은 아님). 같은 대상에 설치를 동시에 실행하지 마세요.

소스 ZIP은 `python scripts/validate_framework.py`로 검사하세요. 원본에서 `install_pack.py --check`를 쓰려면 Git 체크아웃이 필요합니다. ZIP 소스도 설치할 수 있습니다.

Codex 권장 경로: **이 클론을 워크스페이스로 열어** 루트의 `AGENTS.md` 적용 여부를 확인합니다. 스킬 복사는 `~/.agents/skills` 등에서 팩을 찾는 호스트용입니다. 이미 있는 더 높은 우선순위 워크스페이스 규칙은 유지하세요.

## 이 팩이 하는 일 / 하지 않는 일

| 하는 일 | 하지 않는 일 |
|---|---|
| 선택 로딩이 있는 얇은 ChatGPT·Codex 진입점 | 파인튜닝·가중치 학습·CoT 증류 |
| 모델 공통 Context Budget + Model-Invariant Floor | 모든 모델이 동일 성능을 낸다는 보장 |
| sync / validate / measure / 골든 테스트 유지보수 도구 | 자동 교차 세션 기억·비밀 저장 |
| 증거 기반 모델·추론 노력 수준 선택 | 호스트 모델 가용성 확인의 대체 |

## 진입점 하나 고르기

| 용도 | 진입 |
|---|---|
| ChatGPT Project | `CHATGPT.md`를 Project Instructions에 넣고, 관련 `docs/`를 프로젝트 지식으로 제공 |
| Codex | **이 저장소에서** Codex를 시작하고 `AGENTS.md` 적용 확인 |
| 원샷 복사/붙여넣기 | 저장소를 붙일 수 없을 때 `docs/chatgpt-5.5-all-in-one-instructions.md` (Core + 코딩/제안/블로그) |
| 스킬형 호스트 | `--auto` 후 설치된 `chatgpt-transfer/` (`SKILL.md` + `AGENTS.md`) |

세션 시작 시 선택한 진입을 읽습니다. 진입점은 작업을 **가장 작은** 관련 가이드로 보냅니다. 단순 작업은 Core만 사용합니다. 전체·단독 가이드는 대안이며 매 작업에 쌓는 층이 아닙니다.

## 설치 후 실제 호스트 확인

설치 파일이 존재해도 지침이 로드됐다는 뜻은 아닙니다. ChatGPT Project 자체는 컴퓨터 폴더 접근 권한을 주지 않습니다. 관련 파일은 업로드하거나 허용된 연결로 제공하세요. [Projects 공식 안내](https://learn.chatgpt.com/docs/projects) (확인일 2026-10-10).

1. 사용 표면(Chat, ChatGPT Work, Codex, API), 클라이언트·버전, 인증 방식을 기록합니다. 로컬 작업은 primary folder 또는 `cwd`도 확인합니다.
2. Codex 사용 시 적용 중인 `AGENTS.md`의 실제 출처와 전역·상위 지침, `AGENTS.override.md`를 확인합니다. 합산 기본 32 KiB 제한과 `project_doc_max_bytes` 설정은 [운영 가이드](docs/codex-operations-rules.md#host-setup-smoke-check)를 참고하세요.
3. 현재 세션에서 선택한 가이드 하나의 접근 가능 여부와 관련 섹션을 읽었는지 확인합니다. 확인되지 않으면 로드 성공으로 보고하지 않습니다.

이는 사용자가 해당 호스트에서 수행할 확인 절차입니다. 저장소 정적 검사는 실제 호스트·모델 스모크 테스트를 대신하지 않습니다. 모델 선택 전에는 [모델 가이드](docs/chatgpt-codex-model-routing.md#verify-the-product-surface)의 가용 모델·노력 수준·도구·권한을 확인하세요.

## Context Budget + Model-Invariant Floor

**Context Budget (일반 사용):** Core + 매핑된 가이드 1–2개, 또는 작업 섹션 1개 + 도메인 섹션 1개. 전체 transfer 가이드·all-in-one·패턴 뱅크·모든 `docs/codex-*.md`를 **미리 로드하지 마세요**.

**Model-Invariant Floor** (`docs/chatgpt-codex-model-routing.md`): 모든 모델에서:

1. 동일한 Core + Operational Integrity (증거·완료·권한·비밀 금지).
2. 동일한 Context Budget — 약한/강한 모델에 문서를 더 쏟아 “보정”하지 않음.
3. 동일한 Task Loading Map / Intent Classifier.
4. 동일한 출력 계약 (`[unverified]`, 최소 완전 변경, 가짜 완료 금지).
5. 막히면 먼저 원인을 확인합니다. 증거나 권한 부족을 모델의 역량 한계로 보지 않으며, 무관한 지침을 **늘리지 않습니다**.

기본적으로 현재 세션의 모델과 추론 노력 수준을 유지합니다. 작업 증거로 필요성이 확인되고, 호스트가 지원하며, 권한이 허용할 때만 변경합니다. `docs/chatgpt-codex-model-routing.md`를 따르며, 고정 모델 목록이나 자동 상향 순서를 적용하지 않습니다.

## 집중 가이드

- `docs/chatgpt-5.5-project-instructions.md` — 작업/출력·노력 규칙 (Core)
- `docs/chatgpt-operational-integrity-rules.md` — 권한·증거·행동·완료
- `docs/chatgpt-coding-rules.md` — 구현·디버깅·리뷰
- `docs/chatgpt-proposal-review-rules.md` / `docs/chatgpt-blog-rules.md` — 문서 계약
- `docs/chatgpt-engineering-task-rules.md` — 아키텍처·RCA·리서치·SOP·프롬프트/보안 리뷰 (**해당 섹션만**)
- `docs/chatgpt-domain-packs.md` — RHEL, OpenShift, Kubernetes, Linux, Ansible, Satellite, EA, AI 인프라, EV (**해당 섹션만**)
- `docs/chatgpt-knowledge-work-rules.md` — 회의·발표·경영 요약
- `docs/chatgpt-codex-model-routing.md` — 현재 모델 유지 기본값·증거 기반 변경·Model-Invariant Floor
- `docs/codex-*.md` — Codex 운영·Office·서브에이전트·팀 게이트 (필요할 때만)
- `prompts/chatgpt-task-prompts.md` — 선택적 작업 프롬프트
- `docs/chatgpt-transfer-instructions.md` — 생성되는 전체 참고; 요청 시에만 로드
- `docs/fable5-pattern-bank-for-chatgpt.md` — 선택적 역사 보정 (자동 로드 금지)

파일명에 `5.5`가 있어도 해당 모델을 요구하지 않습니다(호환용 이름).

## 유지보수와 검증

Codex Memories 설정·모델 업데이트 시 [Memories 유지보수 가이드](docs/codex-memories-maintenance.md)를 선택적으로 읽으세요. 기본 예시는 모델명을 생략하며, 필요한 override만 설치 버전·지원 키·메모리 역할별 접근을 확인한 뒤 적용합니다. 미지원 override의 제거·기본값 재검증, 오류별 중단, 설정 복원과 메모리 상태 복원의 차이를 설명합니다. 팩 설치는 실제 사용자 설정이나 메모리를 변경하지 않습니다. 정적 검사와 실제 호스트 시험은 별도로 보고합니다.

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

병렬 리뷰는 읽기 전용으로 진행합니다. 리뷰어에게 범위와 수용 기준, 정확한 리비전 또는 diff와 관련 파일을 제공합니다. 각 검증 명령에는 실행 위치, 종료 코드, 성공·실패 근거를 포함하고, 실행하지 못한 검사는 이유를 남깁니다. 누락·오래됨·불충분한 검증은 `Validation Gap`으로, 실제 실패한 검사는 FAIL로 보고합니다. 상위 에이전트가 수정과 집중 재검증을 맡고, 새 근거로 지적 사항을 정리합니다. 리뷰를 재귀적으로 반복하지 않습니다. 자세한 기준은 `docs/codex-subagent-rules.md`와 `docs/codex-team-agent-rules.md`를 참고하세요.

GitHub Actions는 Windows·Linux에서 Python 3.11·3.12로 검사합니다. `measure_load.py`는 정규화된 UTF-8 바이트를 보고하며, bytes/4 추정은 **실제 토큰이 아니며** 호스트/도구 오버헤드는 제외합니다.

## 개선·시뮬레이션 근거

- [5차 개선 리포트](docs/optimization-report-2026-09-06.md) — Core 다이어트, AGENTS 축소, 라우팅, 예산
- [Simulation-10 리포트](docs/simulation-10-report-2026-09-06.md) — context budget, model floor, sync, 펜스 인식 섹션, 불변식 (PR #4/#5/#6/#7 이후)
- 행동 평가 루브릭: `tests/Scorecard.md`, `tests/GoldenTest-015.md` … `tests/GoldenTest-038.md`

구조 검사는 실제 ChatGPT/Codex 행동 시험을 실행하지 않습니다. 라우팅에 참고한 공식 원칙(속도·정확도 이득의 증명은 아님): [AGENTS.md 발견](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [선택적 스킬 로딩](https://learn.chatgpt.com/docs/build-skills), [지침 명확성](https://developers.openai.com/api/docs/guides/latest-model) (확인일 2026-09-06).
