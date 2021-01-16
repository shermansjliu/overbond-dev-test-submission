import csv
from scipy.interpolate import interp1d
from typing import Dict


def app() -> None:
    # Separated govt bonds and c bonds because calculating benchmark yield spread
    # checks 1 corporate bond against all govt bonds
    f_name = input("csv name (with.csv): ")
    g_bonds, c_bonds = load_csv(f_name)

    print_benchmark_yield_spread(c_bonds, g_bonds)
    print("\n")
    print_interpolated_yield_spread(c_bonds, g_bonds)
    assert len(c_bonds) > 0 and len(g_bonds) > 0


def load_csv(file_name: str) -> (Dict, Dict):
    g_bonds = {}
    c_bonds = {}

    with open(file_name, mode='r') as bond_file:
        csv_reader = csv.DictReader(bond_file)

        for row in csv_reader:
            bond_id, term, _yield, bond_type = row['bond'], row['term'], row['yield'], row['type']
            term = float(term.split(' ')[0])
            _yield = float(_yield[:-2])

            bond_info = {'term': term, 'yield': _yield}

            if bond_type == "government":
                g_bonds[bond_id] = bond_info
            else:
                c_bonds[bond_id] = bond_info
    return g_bonds, c_bonds


def print_benchmark_yield_spread(c_bonds, g_bonds) -> None:
    """
       @c_bonds: Dict[str,[Dict[str, float]]
       @g_bonds: Dict[str,[Dict[str, float]]

       Prints the benchmark yield spread of all corporate bonds
       """
    for cb_id, info in c_bonds.items():
        bm_bond_id, yield_spread = calc_benchmark_yield_spread(cb_id, c_bonds, g_bonds)
        print("bond,benchmark,spread_to_benchmark")
        print(f"{cb_id},{bm_bond_id}, {yield_spread:.2f}%")


def print_interpolated_yield_spread(c_bonds, g_bonds) -> None:
    """
    @c_bonds: Dict[str, Dict[str, float]]
    @g_bonds: Dict[str, Dict[str, float]]

    Prints the interpolated yield spread of all corporate bonds
    """
    for cb_id, cb in c_bonds.items():
        yield_spread_to_curve = calc_spread_to_curve(cb_id, c_bonds, g_bonds)
        print("bond,spread_to_curve")
        print(f"{cb_id}, {yield_spread_to_curve:.2f}%")


def calc_benchmark_yield_spread(cb_id, c_bonds, g_bonds) -> (str, float):
    """
    @cb_id: str
    @c_bonds:  Dict[str, Dict[str, float]]
    @g_bonds: Dict[str, Dict[str, float]]
    Returns the yield spread and the corresponding govt benchmark bond for <c_bond>

    """
    min_term_diff = float('inf')
    bm_bond = ""

    for gb in g_bonds:
        term_diff = abs(c_bonds[cb_id]['term'] - g_bonds[gb]['term'])
        if term_diff < min_term_diff:
            min_term_diff = term_diff
            bm_bond = gb

    yield_spread = c_bonds[cb_id]['yield'] - g_bonds[bm_bond]['yield']  # Govt bm yield < corporate bond yield
    return f"{bm_bond}", yield_spread


def calc_spread_to_curve(cb_id, c_bonds, g_bonds) -> float:
    """
    @cb_id: str
    @c_bonds:  Dict[str, Dict[str, float]]
    @g_bonds: Dict[str, Dict[str, float]]
    Returns interpolated spread
    prerequisite:
        interpolation is always possible
    Returns interpolated yield spread
    """

    inter_func = interp1d([b_info['term'] for b_info in g_bonds.values()], [b_info['yield'] for b_info in g_bonds.values()])

    interpolated_yield = inter_func(c_bonds[cb_id]['term'])
    spread_to_curve = c_bonds[cb_id]['yield'] - interpolated_yield
    return spread_to_curve


if __name__ == "__main__":
    app()
