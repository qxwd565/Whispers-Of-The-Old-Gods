#!/usr/bin/env python3
"""Future canonical edits propagate; immutable source is never a frozen fallback."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,json
from date_schema import load,put
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='wog-future-',dir='/tmp') as tmp:
    root=Path(tmp)
    for name in ('tools','data','metadata'):shutil.copytree(r/name,root/name)
    shutil.copy2(r/'cards.json',root/'cards.json');original=(r/'cards.json').read_bytes();p=root/'data/OG_034.json';timeline=load(p)
    timeline['2090-01-01']={'cost':0,'attack':0,'text':'','mechanics':['TAUNT']};put(p,timeline)
    subprocess.run([sys.executable,str(root/'tools/build-api.py')],check=True,capture_output=True)
    for filename in ('cards.json','cards-date.json'):
        c=next(c for c in load(root/filename)['cards'] if c['id']=='OG_034')
        assert c['cost']==0 and c['attack']==0 and c['text']=='' and 'TAUNT' in c['mechanics']
    timeline['2090-01-02']={'type':'SPELL','collectible':False,'spellSchool':None,'__remove':['attack','health','race','races']};put(p,timeline)
    subprocess.run([sys.executable,str(root/'tools/build-api.py')],check=True,capture_output=True)
    precise=next(c for c in load(root/'cards-date.json')['cards'] if c['id']=='OG_034')
    assert precise['type']=='SPELL' and precise['collectible'] is False and precise['spellSchool'] is None
    assert all(k not in precise for k in ('attack','health','race','races'))
    timeline['2090-01-03']={'cost':1,'__remove':['spellSchool']};put(p,timeline)
    subprocess.run([sys.executable,str(root/'tools/build-api.py')],check=True,capture_output=True)
    precise=next(c for c in load(root/'cards-date.json')['cards'] if c['id']=='OG_034');legacy=next(c for c in load(root/'cards.json')['cards'] if c['id']=='OG_034')
    assert 'spellSchool' not in precise and 'attack' not in precise and precise['cost']==1
    assert legacy['type']=='SPELL' and legacy['attack']==0 and legacy['health']==0 and legacy['race']=='' and legacy['races']==[] and legacy['spellSchool']==''
    for n in ('cards.json','render.json','history.json'):assert '__remove' not in (root/n).read_text()
    assert '__remove' in (root/'history-date.json').read_text()
    assert (r/'cards.json').read_bytes()==original and load(root/'metadata/OG_034.json')==load(r/'metadata/OG_034.json')
    print(json.dumps({'result':'pass','futureZeroEmptyTextAndKeywordPropagateToBothTransports':True,'futureTypeChangeFalseNullAndExplicitRemovalPreservedPrecisely':True,'legacySentinelsConfinedToOldOutputs':True,'immutableMetadataPreserved':True}))
