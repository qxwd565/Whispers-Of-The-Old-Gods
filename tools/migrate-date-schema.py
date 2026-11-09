#!/usr/bin/env python3
"""Reproduce date-first data from immutable published originals and source audits."""
import copy,json,subprocess
from date_schema import *
from wog_history import SOURCE,ROOT,observations,reconstruct

def original(path):
    try:return json.loads(subprocess.check_output(['git','show',SOURCE+':'+path],cwd=ROOT))
    except subprocess.CalledProcessError:raise RuntimeError('Pinned source unavailable; require checkout fetch-depth: 0')

def main():
    catalog=original('cards.json');builds=observations();dates=load(ROOT/'tools/wog-effective-dates.json')['builds'];changed=0
    original_ids={p.stem for p in (ROOT/'data').glob('*.json') if p.stem!='history'}
    assert original_ids=={c['id'] for c in catalog['cards']}
    for current in catalog['cards']:
        cid=current['id'];path=ROOT/'data'/f'{cid}.json';doc=load(path)
        if 'card' not in doc:
            validate_timeline(doc);assert (ROOT/'metadata'/path.name).exists();continue
        pristine=original('data/'+path.name);assert doc==pristine
        assert not (ROOT/'metadata'/path.name).exists()
        timeline,gaps,evidence=reconstruct(current,builds,dates)
        latest=fold(timeline);fields=sorted({k for d in timeline.values() for k in d if k!='__remove'}|{x for d in timeline.values() for x in d.get('__remove',[])})
        meta={'schema':'hscard-date-metadata-1','id':cid,'timezone':'Asia/Seoul',
              'release':{'date':'2016-04-27','status':'verified'},
              'availabilityScope':'Korean ordinary constructed-match use, including generated original entities. Client preload does not count. IDs and ownership are not inferred from prefixes.',
              'baselineStatus':'partially-verified','confidenceNote':'All 163 identities, initial numbers, Korean archive text and card types cross-checked in the launch archive. Noncollectible rarity display and incompletely evidenced wording effective dates remain qualified; not every live build or game-rule effect is replayed.',
              'sourceCommit':SOURCE,'originalSource':pristine,'currentCatalog':current,
              'canonicalFields':fields,'currentOnlyFields':sorted(set(current)-set(fields)-{'releasedAt','releaseStatus'}),
              'historicalEvidence':evidence,'undatedEvidence':gaps,
              'keywordAbilityEvidence':{'source':'tools/wog-ability-policy.json'},
              'legacyMechanicsConvention':{'present':'mechanics' in current,'original':current.get('mechanics',[]),'canonicalBaseline':latest['mechanics']},
              'behaviorEvidence':'tools/wog-behavior-audit.json',
              'sourceHistory':'tools/original-date-first-history.json'}
        if not current['collectible']:
            meta['fieldUncertainty']={'rarity':{'status':'unresolved-historical-display','retainedValue':current['rarity'],'meaning':'Pinned exporter value retained. Exact archive rarity tags, including absence, are observations, not proof of a dated visible rarity change. No common rarity or fake absence is inferred.'}}
        put(ROOT/'metadata'/path.name,meta);put(path,timeline);changed+=1
    put(ROOT/'tools/original-date-first-history.json',original('data/history.json'))
    print(json.dumps({'migrated':changed,'sourceCommit':SOURCE,'cards':len(catalog['cards'])}))
if __name__=='__main__':main()
