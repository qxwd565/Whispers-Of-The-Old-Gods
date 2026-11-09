"""Source-backed WoG observations and deliberately bounded gameplay projection."""
import copy,re,hashlib,json
from pathlib import Path
from date_schema import *
SOURCE='36969f9ade690085ac3d01f886dbd357644921e4'
ROOT=Path(__file__).resolve().parents[1]
RACES={'2':('DRAENEI','드레나이'),'11':('UNDEAD','언데드'),'14':('MURLOC','멀록'),'17':('MECHANICAL','기계'),'18':('ELEMENTAL','정령'),'20':('BEAST','야수'),'23':('PIRATE','해적'),'24':('DRAGON','용족')}
SCHOOLS={'1':'ARCANE','2':'FIRE','3':'FROST','4':'NATURE','5':'HOLY','6':'SHADOW','7':'FEL'}
TYPES={'4':'MINION','5':'SPELL','7':'WEAPON','10':'HERO_POWER'}
CLASSES={'0':'NEUTRAL','1':'DEATHKNIGHT','2':'DRUID','3':'HUNTER','4':'MAGE','5':'PALADIN','6':'PRIEST','7':'ROGUE','8':'SHAMAN','9':'WARLOCK','10':'WARRIOR','12':'NEUTRAL'}
KEYWORDS={'189':'WINDFURY','190':'TAUNT','191':'STEALTH','192':'SPELLPOWER','194':'DIVINE_SHIELD','197':'CHARGE','217':'DEATHRATTLE','218':'BATTLECRY','219':'SECRET','220':'COMBO','215':'OVERLOAD','311':'CANT_BE_TARGETED_BY_SPELLS','332':'CANT_BE_TARGETED_BY_HERO_POWERS','363':'POISONOUS','212':'ENRAGED','791':'RUSH','443':'CHOOSE_ONE','415':'DISCOVER','1211':'ELUSIVE'}

def observations(root=ROOT):
    manifest=load(root/'tools/wog-archive-evidence.json');pool={}
    for p in (root/'tools/archive-states').glob('*.json'):pool.update(load(p))
    def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    for key,value in pool.items():assert hashlib.sha256(canon(value)).hexdigest()[:20]==key
    refs={};result=[]
    for b in manifest['builds']:
        refs.update(b['changedStates'])
        for cid in b.get('removedIds',[]):refs.pop(cid)
        cards={cid:copy.deepcopy(pool[key]) for cid,key in refs.items()}
        assert len(cards)==b['cardCount'] and hashlib.sha256(canon(cards)).hexdigest()==b['extractedCardsSha256']
        result.append(dict(b,cards=cards))
    return result

def display(raw,cid):
    text=(raw or '').replace('[x]','')
    text=re.sub(r'[$#](?=\d)', '', text)
    # New native text builders use & after keyword punctuation; it is not a
    # literal visible ampersand. Original raw strings remain in the archive.
    if cid in ('OG_031','OG_330'):text=text.replace(':& ', ': ')
    # This dynamic token is the unchanged 1/1 Silver Hand Recruit, confirmed by
    # the preceding source and the pinned installed display; not a new effect.
    if cid=='OG_273':text=text.replace('{0}','1/1')
    if '{' in text or ':&' in text:raise ValueError('Unresolved native display template: '+cid)
    return BREAK.sub('<br></br>',text)

def baseline_abilities(card):
    owned=[name for tag,name in KEYWORDS.items() if int(card['Tag'].get(tag,0))>0]
    return sorted(owned)

def abilities(cid,text,initial):
    # Own release tags establish ownership, not referenced tags, bold spans,
    # AURA/TRIGGER implementation flags, or keywords granted to other cards.
    values=set(initial)
    if cid=='OG_311':values.add('DISCOVER')
    if cid in ('OG_150','OG_218') and '격노' not in text:values.discard('ENRAGED')
    if cid=='OG_044a':
        values.discard('CHARGE');values.discard('RUSH')
        values.add('RUSH' if '<b>속공' in text else 'CHARGE')
    if cid in ('OG_188','OG_334') and text.startswith('<b>도발'):values.add('TAUNT')
    if cid=='OG_209' and text.startswith('<b>주문 공격력'):values.add('SPELLPOWER')
    if cid=='OG_340' and '모면' in text:
        values-={'CANT_BE_TARGETED_BY_SPELLS','CANT_BE_TARGETED_BY_HERO_POWERS'};values.add('ELUSIVE')
    return sorted(values)

def observed_state(cid,card,current,initial):
    tags=card['Tag'];kind=TYPES[tags['202']]
    state={'id':cid,'dbfId':card['dbfId'],'name':card['name'],'type':kind,
           'cardClass':CLASSES[tags.get('199','0')],'classes':copy.deepcopy(current['classes']),
           # Noncollectible rarity tags changed independently of proven display.
           # Preserve the installed value as explicitly qualified, not invent a
           # dated rarity disappearance from a client implementation cleanup.
           'rarity':current['rarity'],'collectible':bool(int(tags.get('321','0'))),
           'cost':int(tags.get('48','0')),'text':display(card['rawText'],cid)}
    if kind in ('MINION','WEAPON'):state['attack']=int(tags.get('47','0'))
    if kind=='MINION':state['health']=int(tags.get('45','0'))
    if kind=='WEAPON':state['durability']=int(tags.get('187',tags.get('45','0')))
    race=tags.get('200','0')
    if race!='0':state['races']=[RACES[race][0]];state['race']=RACES[race][1]
    school=tags.get('1635','0')
    if school!='0':state['spellSchool']=SCHOOLS[school]
    state['mechanics']=abilities(cid,state['text'],initial)
    return state

def reconstruct(current,builds,dates):
    """Only changes with separately sourced effective Korean dates enter data."""
    timeline={};gaps=[];evidence=[];cid=current['id'];prior=None;canonical=None
    first=builds[0]['cards'][cid];initial=baseline_abilities(first)
    for b in builds:
        n=b['build'].split('.')[-1];card=b['cards'].get(cid)
        if card is None:continue
        state=observed_state(cid,card,current,initial)
        if prior is None:
            canonical=copy.deepcopy(state);timeline['2016-04-27']=copy.deepcopy(state)
            evidence.append({'date':'2016-04-27','build':b['build'],'source':b['source'],'fields':sorted(state)})
        else:
            changes=delta(prior,state)
            if changes:
                rule=dates.get(n)
                if rule:
                    when=rule['date']
                    # Apply only the proven fields changed in this exact build,
                    # never backfill a whole current snapshot into older dates.
                    canonical=apply(canonical,changes)
                    if when in timeline:
                        baseline=fold({d:v for d,v in timeline.items() if d<when}) or {}
                        timeline[when]=delta(baseline,canonical)
                    else:timeline[when]=changes
                    evidence.append({'date':when,'build':b['build'],'source':b['source'],'dateSource':rule['sources'],'fields':sorted(changes),'kind':rule.get('kind','archive-change')})
                else:
                    gaps.append({'beforeBuild':previous['build'],'firstObservedBuild':b['build'],'source':b['source'],'changes':changes,'status':'unresolved-effective-Korean-date; not emitted as dated history'})
        prior=state;previous=b
    timeline=dict(sorted(timeline.items()))
    # Different observations may share one patch day. Recalculate sparse deltas
    # after their effective-date grouping and reject redundant/invalid writes.
    validate_timeline(timeline)
    return timeline,gaps,evidence
