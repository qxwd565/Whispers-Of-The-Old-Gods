#!/usr/bin/env python3
import copy,json,subprocess,hashlib
from pathlib import Path
from datetime import date,timedelta
from collections import Counter
from date_schema import *
from wog_history import SOURCE,ROOT,observations,reconstruct

def require_source_commit(root,commit):
    if subprocess.run(['git','cat-file','-e',commit+':data'],cwd=root,capture_output=True).returncode:raise RuntimeError('Pinned source unavailable; use checkout fetch-depth: 0')
def original(path):return json.loads(subprocess.check_output(['git','show',SOURCE+':'+path],cwd=ROOT))
def reverse(record,day):
    if day<record['releasedAt']:return None
    s=copy.deepcopy(record['current']);s.pop('art',None)
    matches=[e for e in record['history'] if e.get('from','0001-01-01')<=day<e.get('before','9999-12-31')];assert len(matches)<=1
    for event in matches:s=apply(s,event['changes'])
    return s

def main():
    require_source_commit(ROOT,SOURCE);current={c['id']:c for c in original('cards.json')['cards']};precise={c['id']:c for c in load(ROOT/'cards-date.json')['cards']};history=load(ROOT/'history-date.json');assert history['historySchema']==2
    assert set(current)==set(precise)=={p.stem for p in (ROOT/'metadata').glob('*.json')}=={p.stem for p in (ROOT/'data').glob('*.json') if p.stem!='history'} and len(current)==163
    builds=observations();effective=load(ROOT/'tools/wog-effective-dates.json')['builds'];dates={'1900-01-01','2099-12-31'};maps={};events=0;gaps=0;rarity=0
    for cid,c in current.items():
        timeline,meta=read_card(ROOT,cid);maps[cid]=timeline;validate_timeline(timeline)
        assert meta['originalSource']==original('data/'+cid+'.json') and meta['currentCatalog']==c and meta['sourceCommit']==SOURCE
        expected,unknown,provenance=reconstruct(c,builds,effective)
        assert json_equal(timeline,expected) and meta['undatedEvidence']==unknown and meta['historicalEvidence']==provenance
        assert json_equal(fold(timeline),{k:precise[cid][k] for k in meta['canonicalFields'] if k in precise[cid]})
        assert timeline.keys()==dict(sorted(timeline.items())).keys() and next(iter(timeline))=='2016-04-27'
        assert c['dbfId']==builds[0]['cards'][cid]['dbfId']==fold(timeline)['dbfId']
        for d in timeline:dates.update((date.fromisoformat(d)+timedelta(days=n)).isoformat() for n in [-1,0,1])
        for state in [fold(timeline,d) for d in timeline]:
            assert not any(marker in state['text'].replace('<br></br>','') for marker in ['\\n','\n','<br/>','<br>','/n'])
            assert not set(state)&set(CURRENT_ONLY) and '__remove' not in state
        try:resolve(timeline,meta,'2016-04-27',strict=True)
        except UncertainHistory:pass
        else:raise AssertionError('Qualified baseline silently fully verified')
        events+=len(timeline)-1;gaps+=len(unknown);rarity+=bool(meta.get('fieldUncertainty'))
    cases=0
    for cid,timeline in maps.items():
        for d in dates:assert json_equal(fold(timeline,d),reverse(history['cards'][str(current[cid]['dbfId'])],d)),(cid,d);cases+=1
    assert load(ROOT/'data/history.json')==original('data/history.json')==load(ROOT/'tools/original-date-first-history.json')
    report={'result':'pass','cards':163,'preciseGlobalDateCases':cases,'dates':len(dates),'sparseEvents':events,'originalSourceDocuments':163,'qualifiedBaselines':163,'unresolvedEffectiveDateObservations':gaps,'qualifiedNoncollectibleRarity':rarity,'currentTypes':dict(Counter(fold(t)['type'] for t in maps.values())),'archivedBuilds':len(builds),'archivedCardObservations':sum(len(b['cards']) for b in builds)}
    put(ROOT/'tools/date-schema-validation.json',report);print(json.dumps(report))
if __name__=='__main__':main()
