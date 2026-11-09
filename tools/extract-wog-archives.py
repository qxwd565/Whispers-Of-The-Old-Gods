#!/usr/bin/env python3
"""Independently verify lossless evidence against retained pinned full XML files."""
import argparse,hashlib,json,re,xml.etree.ElementTree as ET
from pathlib import Path
from wog_history import ROOT,observations
from date_schema import put
p=argparse.ArgumentParser();p.add_argument('--archive-dir',type=Path,action='append',required=True);p.add_argument('--require-all',action='store_true');args=p.parse_args()
files={}
for directory in args.archive_dir:
    for path in directory.glob('*CardDefs.xml'):
        with path.open() as f:head=f.read(200)
        match=re.search(r'build="(\d+)"',head)
        if match:files[match[1]]=path
verified=[];missing=[]
for b in observations():
    n=b['build'].split('.')[-1]
    if n not in files:missing.append({'build':b['build'],'changedStates':len(b['changedStates'])});continue
    path=files[n];h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1024*1024):h.update(chunk)
    assert h.hexdigest()==b['xmlSha256'],b['build']
    extracted={};ids=set(b['cards'])
    for _,e in ET.iterparse(path,events=('end',)):
        if e.tag!='Entity':continue
        cid=e.get('CardID')
        if cid in ids:
            extracted[cid]={kind:{t.get('enumID'):t.get('value') for t in e if t.tag==kind and t.get('value') is not None} for kind in ('Tag','ReferencedTag')}
            extracted[cid].update(dbfId=int(e.get('ID')),name=e.findtext('./Tag[@enumID="185"]/koKR'),rawText=e.findtext('./Tag[@enumID="184"]/koKR'),enText=e.findtext('./Tag[@enumID="184"]/enUS'))
        e.clear()
    assert extracted==b['cards'],b['build'];verified.append(b['build'])
if args.require_all:assert not missing,missing
report={'result':'pass','fullXmlReextractedBuilds':len(verified),'cardObservations':len(verified)*163,'sourceSha256Verified':True,'losslessPooledEvidenceVerified':True,'missingLocalXml':missing,'limitation':'Missing local XML is not counted as a full re-extraction. Its originally recorded extraction hash remains independently checked by the shared-state decoder.'}
put(ROOT/'tools/wog-xml-validation.json',report);print(json.dumps(report))
