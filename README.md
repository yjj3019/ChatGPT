# TaskForge

엔지니어링·문서 작업·증거 기반 완료를 위한 **작업 지침 팩**입니다. Codex 앱에서는 GitHub marketplace 플러그인으로 설치하고, ChatGPT에서는 Project Instructions로 사용할 수 있습니다. 모델 가중치나 숨은 추론을 학습·복사하거나 자동 교차 세션 기억을 만들지 않습니다.

Codex용 TaskForge를 적용한 새 대화는 Sol 총괄·Luna 탐색/검증·Astra 조건부 검토를 기본 정책으로 사용합니다. 사용자가 모델을 명시적으로 선택하면 그 대화에서는 3모델 위임을 해제하고 선택한 모델·추론 수준을 유지합니다. 새 대화에서 TaskForge를 적용하면 기본 정책으로 돌아갑니다. 같은 대화 재개나 앱 재시작만으로는 초기화하지 않습니다. 설치는 사용자 설정·역할·메모리를 자동 변경하지 않습니다. 배포 원칙은 [배포 표준](docs/distribution-standard.md)을 참고하세요.

**언어:** 한국어 | [English](README.en.md)

## 설치 방식 선택

| 환경·목적 | 사용할 방식 |
|---|---|
| **Codex 앱 — 기본 설치** | 아래 marketplace 절차로 `taskforge` 플러그인 설치 |
| ChatGPT Project | `CHATGPT.md`를 Project Instructions에 넣고 필요한 `docs/` 파일 제공 |
| 다른 스킬형 호스트·기존 설치 방식 | 아래 Python 설치기로 `chatgpt-transfer/` 복사 |
| 저장소 개발·워크스페이스 규칙 적용 | 저장소를 열고 루트 `AGENTS.md`의 실제 적용 여부 확인 |
| 원샷 복사/붙여넣기 | `docs/chatgpt-5.5-all-in-one-instructions.md` 사용 |

진입점은 하나를 선택합니다. marketplace 플러그인과 Python 설치본을 함께 사용하면 같은 팩이 중복 검색될 수 있습니다.

## Codex 앱 marketplace 설치·삭제·업데이트

Codex CLI가 필요합니다. `codex plugin --help`와 `codex plugin marketplace --help`에서 아래 명령을 지원하는지 먼저 확인합니다. marketplace 이름은 `yjj3019`, 플러그인 이름은 `taskforge`입니다. `taskforge@yjj3019`에서 `@` 앞은 플러그인, 뒤는 marketplace 식별자입니다. GitHub 기반 marketplace이며, 공개 플러그인 디렉터리의 심사·등록과는 별도입니다.

### 설치

터미널에서 저장소를 marketplace로 등록하고 플러그인을 설치합니다. 저장소를 직접 클론하거나 Python 설치기를 실행할 필요는 없습니다.

```text
codex plugin marketplace add yjj3019/ChatGPT --ref main
codex plugin add taskforge@yjj3019
```

Codex 앱을 다시 시작하고 새 채팅에서 사용합니다. 요청 예: “TaskForge를 적용해 이 코드를 검토해줘.” 플러그인은 자기 설치 경로의 `AGENTS.md`와 필요한 가이드를 읽으며, 사용자의 작업 폴더를 팩 저장소로 바꾸지 않습니다.

### 설치 상태 확인

```text
codex plugin list --marketplace yjj3019 --json
```

설치 목록·버전을 확인하고 앱의 Plugins에서도 설치 상태를 확인합니다. 설치 파일이 존재하는 것과 실제 모델이 지침을 선택·준수하는 것은 별도 검증입니다.

### 업데이트

검증한 Windows CLI의 캐시 교체 오류를 피하도록 **제거 → marketplace 갱신 → 재설치** 순서를 사용합니다. 각 명령의 성공을 확인한 뒤 다음 명령을 실행합니다.

```text
codex plugin remove taskforge@yjj3019
codex plugin marketplace upgrade yjj3019
codex plugin add taskforge@yjj3019
```

갱신 중에는 팩이 일시적으로 미설치 상태입니다. 네트워크 갱신이 실패하면 연결을 복구한 뒤 갱신·설치를 다시 실행합니다. 완료 후 설치 상태를 확인하고 앱을 다시 시작해 새 채팅을 엽니다.

### 플러그인 삭제

```text
codex plugin remove taskforge@yjj3019
```

이 플러그인의 설치 설정·캐시를 제거합니다. 기존 Python 설치본과 Git 클론은 삭제하지 않습니다.

### marketplace 등록 해제 — 선택 사항

플러그인을 삭제한 뒤 이 marketplace도 더 이상 사용하지 않을 때 실행합니다.

```text
codex plugin marketplace remove yjj3019
```

### 확인한 범위

Windows의 Codex CLI `0.162.0-alpha.17.2`, 별도 임시 설정·캐시에서 실제 GitHub URL의 등록·설치·재설치 갱신·삭제와 로컬 시험용 버전·문서 내용 갱신을 확인했습니다. 설치 상태로 marketplace를 갱신할 때는 기존 캐시 교체가 액세스 거부로 실패했고, 위 재설치 순서는 성공했습니다. 실제 앱 화면 표시와 모델 행동은 별도 검증 대상입니다.

[공식 패키징 안내](https://developers.openai.com/plugins/build/plugins?install-scope=workspace), [공식 관리 명령](https://learn.chatgpt.com/docs/developer-commands#codex-plugin) (확인일 2026-10-15).

## 이전 플러그인에서 전환

기존 `chatgpt-transfer@yjj3019-chatgpt` 설치 사용자만 실행합니다. 이름 변경은 자동 업데이트되지 않으므로 이전 플러그인과 marketplace 등록을 제거한 뒤 새 이름으로 설치합니다. 각 명령의 성공을 확인하고 다음 명령을 실행합니다. 저장소 URL은 그대로입니다.

```text
codex plugin remove chatgpt-transfer@yjj3019-chatgpt
codex plugin marketplace remove yjj3019-chatgpt
codex plugin marketplace add yjj3019/ChatGPT --ref main
codex plugin add taskforge@yjj3019
```

전환 중에는 플러그인이 일시적으로 미설치 상태입니다. 실패하면 남은 단계를 복구 후 실행하고, 완료하면 앱을 다시 시작해 새 채팅에서 TaskForge를 사용합니다. 기존 Python 설치기는 호환성을 위해 `chatgpt-transfer/` 이름을 유지합니다.

## ChatGPT Project에서 사용

1. 저장소의 `CHATGPT.md`를 Project Instructions에 넣습니다.
2. 작업에 필요한 `docs/` 파일만 프로젝트 지식으로 제공합니다.
3. 선택한 가이드에 실제로 접근할 수 있는지 확인합니다.

전체 transfer 가이드와 all-in-one은 대체 진입점입니다. 일반 사용에서 함께 쌓아 읽지 않습니다. 붙여넣기 절차가 필요하면 로컬 클론에서 `python3 scripts/install_pack.py --print-chatgpt`를 실행합니다.

## 기존 Python 설치 방식 — 다른 스킬형 호스트용

Claude / Grok / Cursor / AGENTS 호환 호스트 등에 팩을 파일로 복사할 때 사용합니다. Codex CLI도 감지 대상에 포함되지만, Codex 앱의 기본 설치는 위 marketplace 방식입니다.

```bash
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
python3 scripts/install_pack.py --auto
```

- `--dest` — 설치할 스킬 루트 직접 지정
- `--with-tests` — 평가 기준·테스트 파일도 포함
- `--dry-run` — 쓰기 없이 대상과 충돌 확인
- `--check` — Python 설치본의 파일 무결성 확인; 테스트 파일이 있으면 구조 검증도 실행
- `--force` — 기존 팩 전체 교체; 사용자 추가 파일까지 교체하므로 먼저 백업

동일한 설치는 건너뛰고 사용자 파일을 보존합니다. 변경·누락·구형 설치는 기본적으로 덮어쓰지 않습니다. 같은 대상에 동시에 설치하지 마세요. 이 설치기의 `--check`는 marketplace 설치 상태나 배포자 인증을 검증하지 않습니다.

Python 방식에서 marketplace로 전환할 때는 기존 설치 대상과 사용자 추가 파일을 확인·백업한 뒤, 이전 `chatgpt-transfer/` 팩만 별도로 정리합니다. marketplace 명령은 이전 Python 설치본을 자동으로 제거하지 않습니다.

소스 ZIP은 `python scripts/validate_framework.py`로 검사합니다. 원본에서 `install_pack.py --check`의 소스 검사 모드를 쓰려면 Git 체크아웃이 필요합니다. ZIP 소스도 Python 방식으로 설치할 수 있습니다.

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

플러그인 배포 내용을 바꾸면 루트 `plugin.json`의 버전도 올립니다.

Codex용 기본 구성은 [세션 기준 3모델 설정 가이드](docs/codex-three-model-setup.md)를 따릅니다. 실제 역할 사용에는 계정의 모델 접근과 호스트 역할 등록이 필요합니다. 지침만으로 실행 중인 메인 모델을 바꾸거나 모든 UI 모델 선택을 감지할 수는 없습니다. 수동 선택이 호스트에 표시되지 않으면 **“이 대화에서는 선택한 모델만 사용해”**라고 요청하세요. 명시적으로 다시 켜려면 **“TaskForge 3모델 구성을 다시 활성화해”**라고 요청하세요. 권한·설정 변경은 별도 승인과 검증을 거칩니다. ChatGPT 및 기존 Python 설치 진입점은 현재 모델 유지 정책을 따릅니다.

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
- 행동 평가 루브릭: `tests/Scorecard.md`, `tests/GoldenTest-015.md` … `tests/GoldenTest-040.md`

구조 검사는 실제 ChatGPT/Codex 행동 시험을 실행하지 않습니다. 라우팅에 참고한 공식 원칙(속도·정확도 이득의 증명은 아님): [AGENTS.md 발견](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [선택적 스킬 로딩](https://learn.chatgpt.com/docs/build-skills), [지침 명확성](https://developers.openai.com/api/docs/guides/latest-model) (확인일 2026-09-06).

## 라이선스

[MIT License](LICENSE).
