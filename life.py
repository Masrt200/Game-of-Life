from collections import defaultdict

class GAME:
    def __init__(self):
        self.liveCells = defaultdict(bool)
        self.cellCount = 0
        self.epochs = 0

    def next_epoch(self):
        liveCells = defaultdict(bool)
        visCells = defaultdict(bool)
        movs = [1, 0, 0, -1, 0, 1, 1, -1, -1, 1] # simple way to mov in a 3x3 grid

        for cell in self.liveCells.copy():
            for step in range(9):
                nCell = (cell[0] + movs[step], cell[1] + movs[step+1])
                if not visCells[nCell]:
                    visCells[nCell] = True

                    crowd = sum([self.liveCells[ (nCell[0] + movs[step], nCell[1] +  movs[step+1]) ] for step in range(9)])
                    crowd -= self.liveCells[nCell]

                    # conditions for living:
                    # ->  if alive, should have 2 or 3 neighbours
                    # ->  if dead, should have 3 neighbours 
                    if (crowd == 3) or (self.liveCells[nCell] and crowd == 2): 
                        liveCells[nCell] = True

        self.liveCells = liveCells
        self.cellCount = len(liveCells)
        self.epochs += 1

# '''benchmark
# ❯ python3 -m timeit -s "$code" "Conway.next_epoch()"
# 500 loops, best of 5: 444 usec per loop
# ❯ python3 -m timeit -s "$code" "Conway.next_epoch()"
# 1000 loops, best of 5: 237 usec per loop
# '''

# count alive cells
# and epochs passed