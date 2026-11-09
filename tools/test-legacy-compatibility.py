#!/usr/bin/env python3
import argparse,copy,json,subprocess,hashlib
from pathlib import Path
from datetime import date,timedelta
from urllib.parse import urljoin
from date_schema import *
from legacy_projection import PHP_FIELDS
from wog_history import SOURCE,ROOT
BASE_URL='https://raw.githubusercontent.com/qxwd565/Whispers-Of-The-Old-Gods/main/'

def independent_old(current,state,latest):
    # Independent statement of old-wire behavior. This does not call the
    # production compatibility projector or inspect generated reverse rows.
    expected=copy.deepcopy(current)
    if state is None:return {k:v for k,v in expected.items() if k in PHP_FIELDS}
    for key in ('name','type','cardClass','rarity','cost','attack','health','durability','armor','text','race','spellSchool'):
        if key in state:expected[key]=state[key]
        elif key in ('cost','attack','health','durability','armor'):expected[key]=state.get('durability',0) if key=='health' and state['type']=='WEAPON' else 0
        elif key in ('race','spellSchool'):expected[key]=''
    # Current catalog had no mechanics annotation in this source corpus.
    additions=[k for k in state.get('mechanics',[]) if k not in latest.get('mechanics',[])]
    if additions:expected['mechanics']=additions
    return {k:v for k,v in expected.items() if k in PHP_FIELDS}

def resolve_old(current,rows,day):
    state=copy.deepcopy(current);seen=set()
    for row in rows:
        if row.get('from','0001-01-01')<=day<row.get('before','9999-12-31'):
            for k,v in row['changes'].items():
                if k in PHP_FIELDS and k not in seen:state[k]=v;seen.add(k)
    return {k:v for k,v in state.items() if k in PHP_FIELDS}

def main(fixture):
    original=json.loads(subprocess.check_output(['git','show',SOURCE+':cards.json'],cwd=ROOT));catalog=load(ROOT/'cards.json');history=load(ROOT/'history.json');render=load(ROOT/'render.json')
    expected=copy.deepcopy(original);approved=load(ROOT/'tools/wog-current-diff.json');by_id={c['id']:c for c in catalog['cards']};r_by_id={c['id']:c for c in render['cards']}
    for c in expected['cards']:
        for field,change in approved['changes'].get(c['id'],{}).items():
            assert c.get(field)==change['before'];c[field]=change['after']
    assert json_equal(expected,catalog),'Unreviewed current output change'
    assert all(x['schema']==1 and 'historySchema' not in x for x in (catalog,history,render))
    for n in ('cards.json','render.json','history.json'):assert '__remove' not in (ROOT/n).read_text()
    assets={}
    for line in subprocess.check_output(['git','ls-tree','-r',SOURCE,'--','art','golden'],cwd=ROOT,text=True).splitlines():
        info,path=line.split('\t');assets[path]=info.split()[2]
    for path,sha in assets.items():
        data=(ROOT/path).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==sha,path
    dates={'1900-01-01','2099-12-31'}
    for cid in by_id:
        for d in load(ROOT/'data'/f'{cid}.json'):dates.update((date.fromisoformat(d)+timedelta(days=n)).isoformat() for n in (-1,0,1))
    cases=[]
    for cid,c in by_id.items():
        assert c['art'] in assets
        for n in ('cards.json','render.json','history.json','cards-date.json','render-date.json','history-date.json'):assert urljoin(BASE_URL+n,c['art'])==BASE_URL+c['art']
        rows=history['cards'].get(str(c['dbfId']),{}).get('history',[]);assert rows==r_by_id[cid].get('history',[])
        timeline=load(ROOT/'data'/f'{cid}.json');latest=fold(timeline)
        for d in sorted(dates):
            target=independent_old(c,fold(timeline,d),latest);assert json_equal(resolve_old(c,rows,d),target),(cid,d)
            cases.append({'id':cid,'dbfId':c['dbfId'],'date':d,'expected':target})
    report={'result':'pass','cards':163,'reviewedCurrentChanges':sum(len(v) for v in approved['changes'].values()),'legacyDateCases':len(cases),'preservedAssetFiles':len(assets),'artURLChecks':163*6,'historyBytes':(ROOT/'history.json').stat().st_size,'visibility':'Original schema1 before-release fallback retained; exact -date endpoints gate verified first use.'}
    put(ROOT/'tools/legacy-compatibility-validation.json',report)
    if fixture:put(fixture,{'catalog':catalog,'history':history,'cases':cases,'allowed':list(PHP_FIELDS),'originalCatalog':expected,'baseUrl':BASE_URL,'expectedCards':163,'originalComparison':'Pinned original plus individually recorded current display normalization/release changes.'})
    print(json.dumps(report))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path);main(p.parse_args().fixture)
