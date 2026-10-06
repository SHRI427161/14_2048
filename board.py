import random
from unittest import result

SIZE = 4


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def slide_line(line):
        values = [x for x in line if x]
        result = []
        merged = False

        for value in values:
            if result and result[-1] == value and not merged:
                result[-1] *= 2
                merged = True
            else:
                result.append(value)
                merged = False

        return result + [0] * (SIZE - len(result))

    @staticmethod
    def merge_score(line):
        values = [x for x in line if x]
        result = []
        score = 0
        merged = False

        for value in values:
            if result and result[-1] == value and not merged:
                result[-1] *= 2
                score += result[-1]
                merged = True
            else:
                result.append(value)
                merged = False

        return score

    def move_left(self):
        changed = False

        for r in range(SIZE):
            old = self.grid[r][:]
            new = self.slide_line(old)

            if old != new:
                self.score += self.merge_score(old)
                changed = True

            self.grid[r] = new

        return changed

    def move_right(self):
        changed = False

        for r in range(SIZE):
            old = self.grid[r][:]
            reversed_old = list(reversed(old))
            new = list(reversed(self.slide_line(reversed_old)))

            if old != new:
                self.score += self.merge_score(reversed_old)
                changed = True

            self.grid[r] = new

        return changed

    def move_up(self):
        changed = False

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new = self.slide_line(old)

            if old != new:
                self.score += self.merge_score(old)
                changed = True

            for r in range(SIZE):
                self.grid[r][c] = new[r]

        return changed

    def move_down(self):
        changed = False

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            reversed_old = list(reversed(old))
            new = list(reversed(self.slide_line(reversed_old)))

            if old != new:
                self.score += self.merge_score(reversed_old)
                changed = True

            for r in range(SIZE):
                self.grid[r][c] = new[r]

        return changed

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True

        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True

                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True

        return False