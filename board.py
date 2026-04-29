def board_from(level):
    # Igual lógica, más rápido que list+slice repetidos
    return [list(level[i:i+6]) for i in range(0, 36, 6)]


def question(level, query, param=None):
    if query == "--howmany":
        # Evita crear la board si no hace falta
        return len(set(level) - {'o'})

    board = board_from(level)

    if query == "--size":
        ch = param
        return sum(1 for r in range(6) for c in range(6) if board[r][c] == ch)
    if query == "--whereis":
        ch = param
        result = [(r, c) for r in range(6) for c in range(6) if board[r][c] == ch]
        return "".join(f"({r},{c})" for r, c in result)
    if query == "--what":
        f, c = map(int, param.split(","))
        return board[f][c]
    return "Error"


def goal(level):
    # Evita construir toda la grid: basta la fila 2 y col 5
    return level[2*6 + 5] == 'A'


def move(level, moves):
    grid = board_from(level)

    for mov in moves.split(","):
        mov = mov.strip()
        if not mov:
            continue

        car = mov[0]
        sign = mov[1]
        amt = int(mov[2:])

        coords = []
        for r in range(6):
            row = grid[r]
            for c in range(6):
                if row[c] == car:
                    coords.append((r, c))
        coords.sort()

        rows = {r for r, _ in coords}
        horizontal = (len(rows) == 1)

        if horizontal:
            delta_r = 0
            delta_c = amt if sign == '+' else -amt
        else:
            delta_r = -amt if sign == '+' else amt
            delta_c = 0

        for r, c in coords:
            grid[r][c] = 'o'

        new_coords = [(r + delta_r, c + delta_c) for r, c in coords]

        for nr, nc in new_coords:
            if not (0 <= nr < 6 and 0 <= nc < 6):
                raise ValueError("Movimiento inválido")

        for nr, nc in new_coords:
            grid[nr][nc] = car

    return "".join("".join(fila) for fila in grid)
