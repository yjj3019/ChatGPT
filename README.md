# TaskForge for ChatGPT

ChatGPT와 Codex에서 코드 검토, 운영 분석, 문서 작업을 돕는 **작업 지침 팩**입니다.
필요한 가이드만 선택하고, 확인한 근거와 검증 범위에 맞춰 결과를 보고하도록 안내합니다.

한국어 | [English](README.en.md) · [배포 원칙](docs/distribution-standard.md) · [라이선스](LICENSE)

## 시작하기

### Codex 앱

`codex plugin --help`와 `codex plugin marketplace --help`에서 명령 지원을 확인한 뒤 실행합니다.

```text
codex plugin marketplace add yjj3019/ChatGPT --ref main
codex plugin add taskforge-for-chatgpt@yjj3019
```

앱을 다시 시작하고 다음처럼 요청하세요.

> TaskForge for ChatGPT를 적용해 이 코드를 검토해줘.

```text
codex plugin list --marketplace yjj3019 --json
```

설치 목록에서 버전을, 앱의 플러그인 화면(`Plugins`)에서 활성 상태를 확인합니다. 이 저장소는 GitHub 기반 마켓플레이스이며 공개 플러그인 디렉터리의 심사·등록과는 별도입니다.

## 업데이트·삭제

기존 플러그인 설정과 캐시 안의 사용자 변경분을 먼저 백업합니다. **마켓플레이스 갱신 성공을 확인한 뒤에만** 제거·재설치를 진행하고, 완료 후 설치된 버전을 확인하세요.

```text
codex plugin marketplace upgrade yjj3019
```

갱신이 성공한 경우에만 다음을 순서대로 실행합니다.

```text
codex plugin remove taskforge-for-chatgpt@yjj3019
codex plugin add taskforge-for-chatgpt@yjj3019
codex plugin list --marketplace yjj3019 --json
```

갱신 실패 시 기존 설치를 유지합니다. 일부 Windows 명령줄 도구(CLI)에서는 설치 중인 캐시 교체가 실패할 수 있습니다. 이때도 복구 가능한 백업 없이 먼저 제거하지 마세요. 재설치 실패 시 보관한 이전 버전으로 복구하고 설치·활성 상태를 확인합니다.

플러그인만 삭제하려면 `codex plugin remove taskforge-for-chatgpt@yjj3019`를 사용합니다. 이 마켓플레이스를 더 이상 사용하지 않을 때만 `codex plugin marketplace remove yjj3019`로 등록도 해제합니다. Python 복사본과 Git 클론은 별도로 관리합니다.

## 다른 환경에서 사용

### ChatGPT 프로젝트

1. [CHATGPT.md](CHATGPT.md)를 프로젝트 지침(`Project Instructions`)에 넣습니다.
2. 작업에 필요한 `docs/` 파일만 프로젝트 지식으로 제공합니다.
3. 선택한 가이드에 실제로 접근할 수 있는지 확인합니다.

전체 참고 문서와 [원샷 지침](docs/chatgpt-5.5-all-in-one-instructions.md)은 대체 진입점입니다. 일반 사용에서는 진입점 하나와 관련 가이드 1–2개만 사용합니다.

<details>
<summary>Python 설치 — 다른 스킬형 호스트</summary>

Python 3.11+와 표준 라이브러리를 사용합니다. Claude·Grok·Cursor·AGENTS 호환 호스트 등에 파일로 복사할 때 선택합니다.

```bash
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
python3 scripts/install_pack.py --auto
```

| 옵션 | 용도 |
|---|---|
| `--dest <경로>` | 대상 스킬 루트 지정. `--auto`와 함께 사용 불가 |
| `--with-tests` | 테스트·평가 자료 포함 |
| `--dry-run` | 쓰기 없이 대상과 충돌 확인 |
| `--check` | Python 설치본 무결성 확인 |
| `--force` | 사용자 추가 파일을 포함한 팩 전체 교체. 먼저 백업 필요 |

같은 대상에는 순차적으로 설치하세요. 동일 설치는 건너뛰며, 변경된 설치는 기본적으로 덮어쓰지 않습니다. `--check`는 마켓플레이스 상태나 배포자 인증을 검증하지 않습니다.

마켓플레이스 설치와 Python 복사본을 동시에 활성화하면 중복 검색될 수 있습니다. 전환할 때는 기존 팩을 백업하고 모든 활성 스킬 폴더 밖에 보관하세요.

</details>

<details>
<summary>이전 플러그인·구 ID에서 전환</summary>

### 3.0 이름·ID 전환

기존 `taskforge@yjj3019`는 새 ID로 자동 업데이트되지 않습니다. 설치 목록·설정·사용자 변경분을 백업하고, 새 ID가 게시됐는지 먼저 확인합니다.

```text
codex plugin marketplace upgrade yjj3019
codex plugin list --marketplace yjj3019 --available --json
codex plugin remove taskforge@yjj3019
codex plugin add taskforge-for-chatgpt@yjj3019
```

새 ID의 설치 가능 여부가 확인된 경우에만 구 ID를 제거합니다. 새 설치가 실패하면 백업한 구 버전을 복구합니다. 모델·권한·역할·메모리 설정은 유지합니다.

더 오래된 `chatgpt-transfer@yjj3019-chatgpt`는 새 마켓플레이스 등록·설치를 확인한 뒤 구 플러그인과 구 등록을 정리합니다. 두 ID를 계속 활성화해 두지 마세요.

Python의 `chatgpt-transfer/`·`taskforge/` 설치는 전체 백업 후 모든 활성 스킬 폴더 밖으로 옮긴 다음 새로 설치합니다. 구 ID가 발견되면 설치기는 `--force`에서도 중단합니다. 이전·새 무결성 목록(`manifest`)을 한 폴더에 합치지 마세요.

특정 2.x 버전으로 되돌리는 상세 명령은 [3.0.6 당시의 전환·복구 기록](https://github.com/yjj3019/ChatGPT/blob/654e954870bd522d7be4aa5d8159b05eeda65add/README.en.md#version-3-migration)에 보존돼 있습니다. 기록에 명시된 버전과 환경을 확인해 사용하세요.

</details>

## 모델과 역할

공식 API 모델의 확인일·단가·한도·추론 수준은 [모델 정보표](docs/openai-api-models.md)에서 확인합니다. 매일 오전 9시(한국시간) 점검은 유지관리자의 로컬 Codex 채팅에 등록된 예약 작업이며, 저장소 설치로 활성화되는 기능은 아닙니다. 모델 정보는 PC에 저장하지 않고 GitHub 연결 도구로 저장소에 직접 갱신합니다. API 목록은 현재 앱에서 사용할 수 있는 모델 목록과 다를 수 있습니다.

| 모드 | 동작 |
|---|---|
| **기본 (`DEFAULT`)** | 현재 모델·추론 수준을 유지합니다. 등록된 `pack_explorer`·`pack_runner`·`pack_reviewer`로 필요한 작업만 분담하고 작은 작업은 메인이 처리합니다. |
| **고정 구성 (`PRESET`)** | Sol·Luna·Astra 고정 구성은 명시적으로 선택하고 지원·접근을 확인한 경우에만 사용합니다. |
| **자동 위임 중지 (`SUSPENDED`)** | 사용자가 모델을 명시적으로 선택하면 해당 대화의 자동 위임을 중단합니다. 상속형 하위 에이전트는 별도 요청한 경우에만 사용합니다. |

대화 재개·압축·앱 재시작은 상태를 초기화하지 않습니다. 새 대화는 기본 모드로 시작하며, 별도 승인한 호스트 전역 고정 구성 정책은 예외입니다. 설치만으로 역할·개인 설정·메모리를 활성화하거나 메인 모델을 전환하지 않습니다. 자세한 기준은 [세션 정책](docs/codex-three-model-setup.md#session-policy)과 [역할 등록](docs/codex-three-model-setup.md#register-default-roles)을 참고하세요.

역할이나 필요한 근거가 없으면 해당 범위를 `Validation Gap`(검증 공백)으로 표시합니다. 기존 대화에서 새 스킬이 보이지 않으면 설치·활성 상태와 새 대화의 인식을 각각 확인하세요. `forceReload`는 디스크 재검색이며 기존 문맥 전체 교체를 보장하지 않습니다. 기존 대화는 보존합니다.

<details>
<summary>설치 후 실제 호스트 확인</summary>

설치 파일이 존재해도 지침이 로드됐다는 뜻은 아닙니다. ChatGPT 프로젝트는 컴퓨터 폴더 접근 권한을 주지 않습니다. 파일을 업로드하거나 허용된 연결로 제공하세요.

1. 사용 환경(ChatGPT 대화, ChatGPT Work, Codex, API), 클라이언트·버전, 인증 방식, 주 작업 폴더(`primary folder`) 또는 `cwd`를 확인합니다.
2. `AGENTS.md`의 실제 출처와 전역·상위 지침, `AGENTS.override.md`를 확인합니다. 합산 기본 32 KiB 제한과 `project_doc_max_bytes`는 [호스트 확인 가이드](docs/codex-operations-rules.md#host-setup-smoke-check)를 참고하세요.
3. 선택한 가이드의 접근·실제 읽기와 필요한 역할의 실행 결과를 확인합니다. 모델·추론 수준은 호스트가 제공하는 실행 근거로 확인합니다.

정적 검사는 스모크 테스트를 대신하지 않습니다. [사용 표면·모델 확인](docs/chatgpt-codex-model-routing.md#verify-the-product-surface) · [Projects 공식 안내](https://learn.chatgpt.com/docs/projects) (관련 안내 확인일: 2026-10-10).

</details>

## 작업별 문서

| 목적 | 가이드 |
|---|---|
| 기본 원칙·검증·완료 보고 | [핵심 원칙](docs/chatgpt-5.5-project-instructions.md) · [실행·검증 원칙](docs/chatgpt-operational-integrity-rules.md) |
| 구현·디버깅·코드 리뷰 | [코딩 규칙](docs/chatgpt-coding-rules.md) |
| 아키텍처·원인 분석·조사·절차서·보안 | [엔지니어링](docs/chatgpt-engineering-task-rules.md) — 해당 섹션만 |
| 인프라·기술 도메인 | [도메인 팩](docs/chatgpt-domain-packs.md) — 해당 섹션만 |
| 회의·발표·요약·PDF 번역·HWPX·한국어 교정 | [지식 작업](docs/chatgpt-knowledge-work-rules.md) |
| 제안서·블로그·오피스 문서 | [제안서](docs/chatgpt-proposal-review-rules.md) · [블로그](docs/chatgpt-blog-rules.md) · [오피스 문서](docs/codex-office-agent-rules.md) |
| 모델·운영·위임 | [모델 선택](docs/chatgpt-codex-model-routing.md) · [운영](docs/codex-operations-rules.md) · [서브에이전트](docs/codex-subagent-rules.md) · [팀 게이트](docs/codex-team-agent-rules.md) |
| 선택형 연동 | [메모리 관리](docs/codex-memories-maintenance.md) · [노션 기록](docs/codex-notion-recording.md) |
| 프롬프트·전체 참고 | [작업 프롬프트](prompts/chatgpt-task-prompts.md) · [프롬프트 가이드](docs/codex-prompt-engineering-rules.md) · [전체 참고](docs/chatgpt-transfer-instructions.md) |

파일명에 있는 `5.5`는 호환용 이름이며 특정 모델을 요구하지 않습니다. 전체 참고 문서와 모든 가이드를 미리 로드하지 마세요.

개선 근거와 과거 기록: [AI-Harness 비교](docs/ai-harness-adoption.md) · [Ponytail 비교](docs/ponytail-adoption.md) · [평가 기준](tests/Scorecard.md) · [호스트 검증 이력](docs/host-verification-2026-10-18.md) · [Windows·Orca 문제 해결](docs/host-troubleshooting.md).

<details>
<summary>저장소 개발·검증</summary>

Python 3.11+와 표준 라이브러리만 필요합니다. 저장소 검사에는 패키지 설치·API 키·모델 호출이 필요 없습니다. 원본 문서를 편집한 뒤 생성 문서를 동기화합니다.

```text
python scripts/sync_runtime.py
python scripts/sync_runtime.py --check
python scripts/validate_framework.py
python -m unittest discover -s tests -p "test_*.py"
python scripts/measure_load.py
python scripts/install_pack.py --check
python scripts/check_release.py --base BASE_COMMIT
```

`BASE_COMMIT`은 실제 변경 전 커밋으로 바꿉니다. 배포 내용 변경 시 `plugin.json` 버전을 올리고, 릴리스에는 정확한 커밋·자동 검증 결과·검증 범위를 함께 기록합니다. 소스 ZIP은 구조 검사로 확인하며, 소스의 설치기 `--check`에는 Git 체크아웃이 필요합니다.

자동 검증(CI) 구성은 Windows·Linux × Python 3.11·3.12입니다. 용량 측정에서 바이트 수를 4로 나눈 값은 실제 토큰 사용량이 아닙니다. 소스 업데이트에서는 [참고 저장소 검토 절차](docs/upstream-review.md)에 따라 Ponytail·Karpathy 변경을 검토합니다. 상시 감시 서비스는 생성하지 않습니다. 공통 지침과 번역 안내의 구분은 [저장소 언어 기준](docs/language-policy.md)을 따릅니다.

</details>

## 라이선스

[MIT License](LICENSE).
