from board import board_from

def _get_vehicle_positions(level_str):
    # Evita board_from en bucle: recorre la cadena una vez
    pos = {}
    for idx, ch in enumerate(level_str):
        if ch == 'o':
            continue
        r, c = divmod(idx, 6)
        lst = pos.get(ch)
        if lst is None:
            pos[ch] = [(r, c)]
        else:
            lst.append((r, c))
    # Orden igual que antes
    for k in pos:
        pos[k].sort()
    return pos


def heuristic_value(level_str, which):
    vehicles = _get_vehicle_positions(level_str)

    A_cells = vehicles.get("A", [])
    if not A_cells:
        return 0

    rA = A_cells[0][0]
    max_cA = max(c for _, c in A_cells)

    # h0: casillas hasta la salida
    h0 = 5 - max_cA
    if h0 < 0:
        h0 = 0

    # h1: bloqueadores delante (mismo criterio exacto que el original)
    blockers = set()
    for v, cells in vehicles.items():
        if v == "A":
            continue

        rows = [r for r, _ in cells]
        cols = [c for _, c in cells]

        if len(set(rows)) == 1:
            if rows[0] == rA and min(cols) > max_cA:
                blockers.add(v)
        else:
            col = cols[0]
            if col > max_cA and col <= 5 and (min(rows) <= rA <= max(rows)):
                blockers.add(v)

    h1 = len(blockers)

    if which == 0:
        return h0
    elif which == 1:
        return h1
    elif which == 2:
        return h0 + h1
    else:
        return 0
