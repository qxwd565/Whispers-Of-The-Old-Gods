# Whispers of the Old Gods card API

Canonical Korean-date card history is in `data/<original ID>.json`.
Initial full specifications and later sparse deltas preserve all 163 existing IDs.

- Legacy-compatible outputs: `cards.json`, `render.json`, `history.json`.
- Precise history outputs: `cards-date.json`, `render-date.json`, `history-date.json`.
- Source provenance and confidence: `metadata/`, `tools/wog-korean-source-audit.json`, and `tools/wog-archive-evidence.json`.
- Format, replay, evidence limits and checks: [docs/date-schema.md](docs/date-schema.md).

Run `python3 tools/build-api.py` after evidence-backed canonical edits. Artwork and golden assets are unchanged. No plugin or live site changes are required for the legacy endpoints.


## API 편집 지침 (2026-11-14)

- `cards.json`은 목록/ID, `data/<CARD_ID>.json`은 카드별 최초 사용 및 날짜 이력의 단일 원본입니다. 일반/황금 카드 원화 `art/`·`golden/`, 황금 애니메이션 및 `frame/` 원본 리소스는 그대로 유지합니다.
- `render.json`·`history.json`·`cards-date.json`·`render-date.json`·`history-date.json` 같은 중복 집계는 공개 저장소에 다시 생성·커밋하지 않습니다. 빌드 중 생성되면 검증용 임시 파일입니다.
- 한국 시간 최초 실제 사용일(베타 북미 날짜 환산, 모험 지구 개방, 이벤트 개시)을 적용합니다. 토큰·자식 카드도 포함합니다. 사전 탑재는 사용 가능일로 보지 않고, 오기입 이전 날짜 키는 반드시 삭제합니다.
- 카드별 기록이 아직 비날짜형이면 증거·기존 값을 보존한 뒤 날짜 키 형식으로 별도 검증하여 바꿉니다. 이후 날짜에는 바뀐 필드만 기입하고 표시 줄바꿈은 `<br></br>`를 사용합니다.
- 원본 검증에 필요한 `metadata/`, `tools/`, CI는 무작정 삭제하지 않습니다. 새 schema/호환 파일을 만들거나 황금·프레임 바이너리를 재가공하지 않습니다.
