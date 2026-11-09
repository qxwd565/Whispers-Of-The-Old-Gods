# Date-first WoG card data

Each existing data/<original ID>.json stores one complete initial specification at Korean first ordinary constructed-match use (2016-04-27), followed by sparse date-keyed changes. These are original entities, not replacement Core or reprint IDs. Membership and ID/DBF mappings are unchanged.

An omitted field retains its preceding value. `__remove` explicitly removes fields. Zero, false, null, empty strings and arrays are distinct real values. Minions have attack/health, weapons attack/durability, spells and hero powers do not receive combat-stat placeholders. The original zero-cost spells remain zero-cost. The generic replay tests also cover heroes, locations, enchantments, type changes and nested false-versus-zero distinctions.

Plain display newlines are normalized to exactly `<br></br>`. Korean archive text is preserved unchanged in source evidence. Native text-builder markers are decoded only where their display meaning is separately identified. Spell schools and races begin at their verified Korean patch dates, not expansion unlock dates. Client storage migrations, such as neutral class 0 to 12 and weapon durability moving between raw tags, are not gameplay changes.

## Output families

- cards.json, render.json and history.json retain schema 1 and the unchanged installed PHP parser's conventions. They contain no `__remove` or historySchema 2. Old numeric absence sentinels, the weapon health/durability mirror and before-release fallback are intentionally limited to this boundary.
- cards-date.json, render-date.json and history-date.json provide precise canonical states, reverse intervals with explicit removals, release information and current-only field lists. render-date/history-date advertise historySchema 2. Before first use, exact replay returns no card.
- All six bundles are root siblings. Relative art URLs retain their original base.

Edit only canonical per-card data for an evidence-backed future change, then run tools/build-api.py. Both families propagate canonical changes. Metadata does not freeze complete current snapshots over later edits. The legacyMechanicsConvention.canonicalBaseline field means the **latest canonical intrinsic keyword list at migration**, not a launch list: it preserves the old current endpoint's annotation convention while allowing differing historical and future keywords through. The precise family always carries intrinsic owned keywords.

## Evidence and limits

metadata/<ID>.json preserves the exact pinned original wrapper, current catalog entry and source commit. Its historicalEvidence lists build and official-date sources. The source-only data/history.json is retained unchanged and copied to tools/original-date-first-history.json. It is not an additional writable canonical source: its known preload/expansion-date errors and incomplete modern snapshots are superseded by the per-card maps.

The lossless shared-state archive has 167 selected client builds and all 163 original IDs in each. Each raw source XML has an exact commit URL and SHA-256; every reconstructed extracted-card map has its own SHA-256. Raw Tag and ReferencedTag remain separate. The first 43-build sample was expanded with every archived intermediate tag in intervals where that sample showed changes. Intervals whose endpoints looked equal were not exhaustively sampled. This is not a claim to have checked every client build or game-engine rule.

Keyword lists use owned release tags and explicitly reviewed changes. References to Deathrattle, Taunt, Overload, Freeze, or keywords granted to other cards do not confer those abilities. Hallazeal grants Lifesteal to spells; its own new keyword is Spell Damage. Fandral enables Choose One cards but is not itself a Choose One card. Engine AURA/TRIGGER markers are retained only in raw evidence.

Noncollectible rarity tags changed in client archives without adequate evidence of visible rarity changes. Their installed values remain explicitly qualified; no artificial release rarity or dated disappearance is invented. All baselines remain partially verified, and strict historical lookup refuses to upgrade uncertainty into fact. Unresolved effective dates, where any remain, are stored in per-card undatedEvidence rather than assigned invented dates.

Yogg-Saron's 2016 stop-casting rule, October 2016 Overload fix and March 2020 stop-casting revert do not change printed text or these display/stat fields. They are dated separately in tools/wog-behavior-audit.json and are **not** replayable engine rules. No arbitrary freeform gameplay field is fabricated.

## Validation

Run the commands in .github/workflows/validate.yml with full Git history. The migration must have its pinned source commit; missing history fails explicitly. Clean reconstruction starts from that exact commit and byte-compares all canonical data, metadata and six outputs. Tests cover boundary dates, source identity/membership, sparse replay, precise reverse replay, current output changes, raw asset hashes, relative URLs, zero/absence/removal semantics, future canonical propagation and idempotence.

`extract-wog-archives.py --archive-dir <cache>` independently re-extracts retained full XML and verifies the shared evidence. Missing local XML is reported separately, never counted as a fresh re-extraction. The unchanged pinned PHP parser is checked offline; no plugin, site, database or live rendering has been changed or visually certified.
