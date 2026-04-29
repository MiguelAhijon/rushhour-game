from verify import verify

def successors(level):
    if verify(level) != 0:
        return []

    # Construye la grid de forma eficiente
    grid = [list(level[i:i+6]) for i in range(0, 36, 6)]
    sucesores = []

    def mover(coche, dx, dy, pasos):
        # Calcula coords una sola vez por coche (en llamada)
        coords = []
        for r in range(6):
            row = grid[r]
            for c in range(6):
                if row[c] == coche:
                    coords.append((r, c))
        coords.sort()

        # Copia superficial de filas (más rápido que list comp profunda completa)
        new = [row[:] for row in grid]

        for r, c in coords:
            new[r][c] = 'o'

        # Escribimos en posiciones desplazadas
        for r, c in coords:
            nr = r + dy * pasos
            nc = c + dx * pasos
            new[nr][nc] = coche

        # Ensambla estado
        new_state = "".join("".join(fila) for fila in new)

        # Coste compatible con el original
        cost = 6 - pasos

        if dx != 0:
            signo = '+' if dx == 1 else '-'
        else:
            signo = '+' if dy == -1 else '-'

        accion = f"{coche}{signo}{pasos}"
        return [accion, new_state, cost]

    # Orden determinista por carácter como antes
    for ch in sorted(set(level)):
        if ch == 'o':
            continue

        # Recolecta coordenadas del coche en la grid base
        coords = []
        for r in range(6):
            row = grid[r]
            for c in range(6):
                if row[c] == ch:
                    coords.append((r, c))
        coords.sort()

        filas = {r for r, _ in coords}
        cols = {c for _, c in coords}

        if len(filas) == 1:
            row = next(iter(filas))
            c1 = min(cols)
            c2 = max(cols)

            # Mover derecha
            max_right = 5 - c2
            k = 1
            while k <= max_right and grid[row][c2 + k] == 'o':
                sucesores.append(mover(ch, 1, 0, k))
                k += 1

            # Mover izquierda
            max_left = c1
            k = 1
            while k <= max_left and grid[row][c1 - k] == 'o':
                sucesores.append(mover(ch, -1, 0, k))
                k += 1

        else:
            col = next(iter(cols))
            r1 = min(filas)
            r2 = max(filas)

            # Mover arriba
            max_up = r1
            k = 1
            while k <= max_up and grid[r1 - k][col] == 'o':
                sucesores.append(mover(ch, 0, -1, k))
                k += 1

            # Mover abajo
            max_down = 5 - r2
            k = 1
            while k <= max_down and grid[r2 + k][col] == 'o':
                sucesores.append(mover(ch, 0, 1, k))
                k += 1

    return sucesores
