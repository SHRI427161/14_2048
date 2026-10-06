from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.history = []

    def display(self):
        print("\n" + "+------+------+------+------+")

        for row in self.board.grid:
            print("|" + "|".join(
                f"{x:^6}" if x else f"{' ':^6}"
                for x in row
            ) + "|")
            print("+------+------+------+------+")

        print("Score:", self.board.score, " Best:", self.best_score)

    def move(self, key):
        moves = {
            "a": self.board.move_left,
            "d": self.board.move_right,
            "w": self.board.move_up,
            "s": self.board.move_down
        }

        if key not in moves:
            return False

        # Save the state before the move for one-level undo.
        previous_grid = [row[:] for row in self.board.grid]
        previous_score = self.board.score

        changed = moves[key]()

        if changed:
            # Keep only one undo state.
            self.history = [(previous_grid, previous_score)]

            # Add a random tile only after a successful move.
            self.board.add_random_tile()

            # Track the best score for this game run.
            self.best_score = max(
                self.best_score,
                self.board.score
            )

            directions = {
                "a": "left",
                "d": "right",
                "w": "up",
                "s": "down"
            }

            # One action-level feedback message.
            if self.board.score > previous_score:
                print(f"Moved {directions[key]} — merge!")
            else:
                print(f"Moved {directions[key]}.")

        return changed

    def undo(self):
        if not self.history:
            return False

        previous_grid, previous_score = self.history.pop()

        # Restore the previous board.
        self.board.grid = [row[:] for row in previous_grid]

        # Restore the previous score.
        self.board.score = previous_score

        return True

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")

        while True:
            self.display()

            # Task 2: win detection.
            if any(2048 in row for row in self.board.grid):
                print("You reached 2048!")
                return

            # Task 2: no legal moves.
            if not self.board.can_move():
                print("No legal moves remain.")
                return

            key = input("> ").strip().lower()

            if key == "q":
                return

            if key == "u":
                if self.undo():
                    print("Move undone.")
                else:
                    print("Nothing to undo.")
                continue

            if key not in "wasd":
                print("Use W/A/S/D.")
                continue

            self.move(key)