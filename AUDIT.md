# Whispers of the Old Gods: dated card history

Checked on 2026-11-09. Immutable source cards and catalogue are pinned to
`36969f9ade690085ac3d01f886dbd357644921e4`. The source-card content is unchanged
in `dd44a5837431e778d9696af560ce62d027e6cf74`; its four additional `frame/`
resources are preserved. The newest checked HearthSim source is
`31b034c26f24b8a66ece845ffd03c1ca397b9a02` (37.0.2.256589).

## Result and scope

All 163 existing original IDs remain present: 134 collectible cards and 29
noncollectible options, generated minions, forms and hero-power records. Each
card starts with its full 2016-04-27 Korean ordinary constructed-use state,
even when its values still match today. Later entries contain sparse changes.
There are 254 later card changes across 130 cards. Original/Core/reprint IDs
are not interchangeable, and prefix similarity is not ownership evidence.

Two sibling API families are built from the same canonical data. The original
`cards.json`, `render.json` and `history.json` retain schema 1 and the pinned
PHP consumer's wire conventions. The three `-date.json` endpoints retain
exact typed field presence, explicit removals and verified first-use gating.
No card IDs, DBF IDs, artwork paths or existing assets are removed or replaced.

## Principal corrections

- Silithid Swarmer gains Beast on 2016-07-13. Three generated slime costs
  change from 1 to 2 on 2016-08-10.
- Call of the Wild changes from 8 to 9 on 2016-10-04, then returns to 8 on
  2020-03-18.
- Three original minions gain Elemental on 2017-04-05; Hallazeal gains it
  separately on 2017-07-11.
- Six Choose One option costs change from zero to their parent spell costs
  on 2019-05-15. They are distinct original records, not deleted duplicates.
- The 27 applicable original spells gain spell schools on 2021-03-26.
  Combined Druid of the Claw (`OG_044a`) changes from 4/6 Charge to 5/6 Rush
  that day, then to 6 mana and 7/9 on 2023-04-05.
- Stand Against Darkness changes from 5 to 4 on 2022-08-17. Seven original
  minions gain Undead on 2022-11-30, and `OG_221` gains Draenei on 2024-10-30.
- The original 27.2 changes apply on 2023-08-23, not the later Caverns of Time
  release. These include Cho'gall, Hallazeal and both Twin Emperors, as well as
  the other archived original-ID buffs and wording changes.
- `OG_282` changes from 9 to 6 on 2023-08-23, then to 7 on 2023-09-29.
  Fandral gains its sixth health on 2025-03-19.
- Dated Korean wording, four card-name changes and the formal Elusive keyword
  are included. Elusive is dated 2024-03-12, not backfilled into launch text.

The old current catalogue changes only through added first-use metadata and
78 display-normalized texts: 40 newline-only changes and 38 native layout or
numeric-marker changes. Each difference is enumerated in
`tools/wog-current-diff.json`. Display newlines use exactly `<br></br>`; the
original source strings are retained unchanged in the archive evidence.

## Evidence and verification

`tools/wog-archive-evidence.json` records 167 pinned client archives and all
27,221 original-ID observations. Lossless shared states retain raw Korean and
English strings, numeric tags, distinct referenced tags, source commits,
complete XML SHA-256 and reconstructed-card-map SHA-256. The sample includes
all 124 intermediate tagged builds within intervals that showed changes in
the initial 43-build sample. Exact effective Korean dates are sourced
separately in `tools/wog-korean-source-audit.json` and
`tools/wog-effective-dates.json`; archive observation is not a release date.

Validation scripts cover:

- All 163 immutable per-card originals, catalogue membership and original
  `data/history.json`, verified against the pinned Git source.
- Full timeline and reverse-history replay, with 13,529 global date cases
  across 83 boundary days, plus literal high-risk card/date fixtures.
- Presence, zero, false, null, empty lists and removals, type-appropriate
  stats, future canonical edits and keyword changes.
- 883 unchanged artwork/golden assets and 978 sibling-endpoint relative URL
  resolutions. Weapon durability decoding is checked across the archive's
  HEALTH/DURABILITY storage change, without inventing a gameplay change.
- Idempotent builds and 333 byte-identical files regenerated from a clean
  checkout of the original source, with an explicit failure when that source
  is missing. CI uses full Git history and does not run the old writer.

All 167 retained XML files were independently re-extracted and their full
SHA-256 values verified, reproducing 27,221 card observations with no missing
local archive. The unchanged pinned PHP 8.5.12 import/replay test passed
163 imports and 13,530 checks.

Machine-readable validation reports accompany the scripts. Exact XML
re-extraction can be run with `tools/extract-wog-archives.py --archive-dir
<archive-directory> --require-all`; it verifies hashes before comparing each
card observation. The pinned, unchanged PHP consumer is tested separately;
this is offline import/replay evidence, not a claim about a live site's UI.

## Limits

Noncollectible rarity history remains explicitly qualified for 29 records.
Changes between absent and zero client rarity tags do not prove the visible
rarity or its effective date. The installed value is retained with that
qualification rather than assigned invented historical changes.

The selected archive coverage has no unresolved dated display/spec transition
other than the separately qualified rarity question. It is not an exhaustive
claim about every live build: equal-ended, unsampled intervals could contain
transient changes. Baselines therefore remain partially verified, available
by default and rejectable by strict consumers, rather than silently hidden.

Game-engine behavior with unchanged printed specs is retained separately in
`tools/wog-behavior-audit.json`, not invented as a freeform gameplay field.
This includes Yogg's 2016 stop-casting change, the separate 2016-10-21 Overload
correction, its 2020 revert, Nat's 2019 probability correction, the 2025 Evolve
mana cap, and the scoped 2024 C'Thun-family generation restriction. These
functional rules are not replayed by the display-spec schema, and unproven
membership in the scoped rule is not inferred from ID prefixes.

Schema 1 necessarily loses some exact presence and type semantics. Those
losses are documented in `tools/legacy-compatibility-losses.json`; the exact
canonical data and schema-2 history transport retain them. No plugin,
database or live website change is part of this audit.
