#!/usr/bin/env python3
"""Independent literal balance/keyword/tribe fixtures, not generated expectations."""
from date_schema import *
from wog_history import ROOT

def state(cid,day):return fold(load(ROOT/'data'/f'{cid}.json'),day)
def check(cid,day,fields):
    actual=state(cid,day)
    for k,v in fields.items():assert json_equal(actual.get(k),v),(cid,day,k,actual.get(k),v)

assert state('OG_006','2016-04-26') is None
check('OG_211','2016-04-27',{'cost':8});check('OG_211','2016-10-03',{'cost':8});check('OG_211','2016-10-04',{'cost':9});check('OG_211','2020-03-18',{'cost':8})
for cid in ('OG_202c','OG_249a','OG_314b'):
    check(cid,'2016-08-09',{'cost':1});check(cid,'2016-08-10',{'cost':2})
assert 'race' not in state('OG_034','2016-07-12');check('OG_034','2016-07-13',{'races':['BEAST']})
assert 'race' not in state('OG_209','2017-07-10');check('OG_209','2017-07-11',{'races':['ELEMENTAL']})
check('OG_044a','2021-03-25',{'cost':5,'attack':4,'health':6,'mechanics':['CHARGE','TAUNT']})
check('OG_044a','2021-03-26',{'cost':5,'attack':5,'health':6,'mechanics':['RUSH','TAUNT']})
check('OG_044a','2023-04-05',{'cost':6,'attack':7,'health':9})
for cid,n in [('OG_047a',3),('OG_047b',3),('OG_195a',7),('OG_195b',7),('OG_202a',4),('OG_202b',4)]:
    check(cid,'2019-05-14',{'cost':0});check(cid,'2019-05-15',{'cost':n})
check('OG_273','2022-08-16',{'cost':5});check('OG_273','2022-08-17',{'cost':4})
check('OG_121','2023-08-22',{'cost':7,'attack':7,'health':7});check('OG_121','2023-08-23',{'cost':8,'attack':8,'health':8})
assert '버린 모든 카드' in state('OG_121','2023-08-23')['text']
check('OG_319','2023-08-23',{'attack':6,'health':7})
check('OG_282','2023-08-22',{'cost':9});check('OG_282','2023-08-23',{'cost':6});check('OG_282','2023-09-29',{'cost':7})
check('OG_044','2025-03-18',{'health':5});check('OG_044','2025-03-19',{'health':6})
for cid in ('OG_150','OG_218'):
    assert 'ENRAGED' in state(cid,'2018-04-10')['mechanics'];assert 'ENRAGED' not in state(cid,'2018-04-11')['mechanics']
for cid in ('OG_045','OG_080e','OG_081','OG_044'):
    assert state(cid,'2016-04-27')['mechanics']==[],cid
check('OG_311','2016-04-27',{'mechanics':['DISCOVER']});check('OG_209','2023-08-23',{'mechanics':['SPELLPOWER']})
check('OG_340','2024-03-12',{'mechanics':['ELUSIVE','TAUNT']})
assert state('OG_340','2024-03-11')['mechanics']==['CANT_BE_TARGETED_BY_HERO_POWERS','CANT_BE_TARGETED_BY_SPELLS','TAUNT']
check('OG_033','2016-04-27',{'attack':2,'durability':2});assert 'health' not in state('OG_033','2016-04-27')
check('OG_086','2016-04-27',{'cost':0});assert 'attack' not in state('OG_086','2016-04-27')
assert 'spellSchool' not in state('OG_023','2021-03-25');check('OG_023','2021-03-26',{'spellSchool':'NATURE'})
print('Independent WoG balance, ownership, keyword, typed-zero and replay fixtures passed')
