from board import board_from

def verify(level):
    if len(level) != 36:
        return 1
    for c in level:
        if not (c == 'o' or ('A' <= c <= 'Z')):
            return 2
    if 'A' not in level:
        return 3

    board = board_from(level)

    posA = []
    for r in range(6):
        row = board[r]
        for c in range(6):
            if row[c] == 'A':
                posA.append((r, c))
    posA.sort()

    rowsA = {r for r, _ in posA}
    colsA = sorted(c for _, c in posA)

    if 2 not in rowsA:
        return 4
    if len(rowsA) > 1:
        return 5
    if len(posA) != 2 or colsA[1] != colsA[0] + 1:
        return 6

    # Revisa cada coche distinto de 'o' y 'A'
    seen = set(level) - {'o', 'A'}
    for ch in seen:
        # Coordenadas del coche
        pos = []
        for r in range(6):
            row = board[r]
            for c in range(6):
                if row[c] == ch:
                    pos.append((r, c))
        pos.sort()

        rows = {r for r, _ in pos}
        cols = {c for _, c in pos}

        if len(rows) != 1 and len(cols) != 1:
            return 7

        ln = len(pos)
        if ln not in (2, 3):
            return 6

        if len(rows) == 1:
            xs = sorted(c for _, c in pos)
            if xs != list(range(xs[0], xs[0] + ln)):
                return 7
        else:
            ys = sorted(r for r, _ in pos)
            if ys != list(range(ys[0], ys[0] + ln)):
                return 7

    return 0
