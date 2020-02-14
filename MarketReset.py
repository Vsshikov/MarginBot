import json

rounds = [
          {'type': 'gamelpay',
           'name': 'GASPROM',
           'settable_const_num': 1,
           'nums': [
               dict(vname='N', value=6, type='const', comment=' - ёмкость рынка', is_settable=True, show=True),
               dict(vname='T', value=0, type='teams_in_market', comment=' - количество команд', is_settable=False, show=True)
           ],
           'coef_evaluation': 'N/T',
           'coef_tip': 'коэффициент = N/T'
           },
          {'type': 'gameplay',
           'name': 'STARTUP',
           'settable_const_num': 3,
           'nums': [
               dict(vname='C', value=6, type='const', comment=' - 1/(шанс успеха стартапа)', is_settable=True, show=True),
               dict(vname='W', value=6, type='const', comment=' - коффициент при успехе', is_settable=True, show=True),
               dict(vname = 'L', value=0.8, type='const', comment=' - коэффициент при провале', is_settable=True, show=True)
           ],
           'coef_evaluation': 'random_chance(C, W, L)',
           'coef_tip': 'Некоторый шанс, что коэффицент = W или L'
           },
          {'type': 'gameplay',
           'name': 'SBERBANK',
           'settable_const_num': 1,
           'nums': [
               dict(vname='N', value=1.1, type='const', comment=' - коэффициент для умножения актива', is_settable=True, show=True),
           ],
           'coef_evaluation': 'N',
           'coef_tip': '= N',
           },
    {'type': 'gameplay',
     'name': 'BOTH_EVEN',
     'settable_const_num': None,
     'nums': [
         dict(vname='A', value=1, type='const', comment=' - номер первой команды в списке секторов раунда', is_settable=True, show=True)
     ]
     'coef_evaluation': 'check_if_both_even('}
]

with open('Markets.json', 'w+') as event_file:
    json.dump(rounds, event_file, indent=4)