# This little script compares Thunderlord's Decree to Deathfire Torch


def deathfire(ap, bonus_ad, target_mr, apen=0, apen_pc=0, piercing=True):
    if piercing:
        apen_pc = 0.07
    effective_mr = target_mr * (1-apen_pc) - apen # assumed > 0
    dmg = 6 + 0.5 * bonus_ad + 0.2 * ap
    return (100/(100+effective_mr)) * dmg


def thunderlord(ap, bonus_ad, target_mr, lvl, apen=0, apen_pc=0, precision=True):
    if precision:
        apen += 0.6 + 0.06*(lvl-1)
    effective_mr = target_mr * (1-apen_pc) - apen # assumed > 0
    dmg = 10 * lvl + 0.2 * bonus_ad + 0.1 * ap
    return (100/(100+effective_mr)) * dmg


def analyze(indata):
    target_mr = 30
    print('Printing stats as Thunderlord, Deathfire vs target magic resist % i' % target_mr)
    for lvl in range(1, 19):
        td = thunderlord(   indata.get('ap', 0) + indata.get('ap18',0)*lvl,
                            indata.get('bonus_ad', 0),
                            target_mr,
                            lvl,
                            indata.get('apen', 0))
        df = deathfire(     indata.get('ap', 0) + indata.get('ap18',0)*lvl,
                            indata.get('bonus_ad', 0),
                            target_mr,
                            indata.get('apen', 0))
        print('Lvl 1: %5.5f, %5.5f' % (td, df))


apen_ap_ap18 = {'apen': 7.8, 'ap': 15, 'ap18': 28}
apen_ap_ap= {'apen': 7.8, 'ap': 15+1.19*9}
apen_apen_apen = {'apen': 2.01*6+7.8}
test_brand = {'apen': 7.8, 'ap': 11, 'bonus_ad':6.8}

analyze(apen_ap_ap)