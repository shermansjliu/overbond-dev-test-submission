from app import *

def test_bm_yield_spread():
    g_bonds, c_bonds = load_csv("sample_input.csv")
    answers = dict()
    answers["C1"] = "G1"
    answers["C2"] = "G2"
    answers["C3"] = "G3"
    answers["C4"] = "G3"
    answers["C5"] = "G4"
    answers["C6"] = "G5"
    answers["C7"] = "G6"
    for cb_id, cb in c_bonds.items():
        gb_id, spread = calc_benchmark_yield_spread(cb_id, c_bonds, g_bonds)
        ans_spread = cb['yield'] - g_bonds[answers[cb_id]]['yield']
        assert gb_id == answers[cb_id]
        assert spread == ans_spread

