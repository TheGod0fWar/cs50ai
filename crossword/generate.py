import sys
from crossword import Crossword, Variable


class CrosswordCreator:
    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        self.enforce_node_consistency()
        if not self.ac3():
            return None
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for v in self.crossword.variables:
            for x in list(self.domains[v]):
                if v.length != len(x):
                    self.domains[v].remove(x)

    def revise(self, x, y):
        revised = False
        if self.crossword.overlaps[x, y]:
            i, j = self.crossword.overlaps[x, y]
            for v1 in list(self.domains[x]):
                letter_v1 = v1[i]
                letters = []
                for v2 in self.domains[y]:
                    letter_v2 = v2[j]
                    letters.append(letter_v2)
                if letter_v1 not in letters:
                    self.domains[x].remove(v1)
                    revised = True
        return revised

    def ac3(self, arcs=None):
        queue = []
        if arcs is None:
            for x in self.crossword.variables:
                neighbors = self.crossword.neighbors(x)
                for y in neighbors:
                    if (x, y) not in queue:
                        queue.append((x, y))
        else:
            queue = arcs

        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        words = list(assignment.values())
        if len(words) != len(set(words)):
            return False

        for v, word in assignment.items():
            if len(word) != v.length:
                return False

            neighbors = self.crossword.neighbors(v)
            for y in neighbors:
                if y in assignment:
                    overlap = self.crossword.overlaps[v, y]
                    if overlap:
                        i, j = overlap
                        if assignment[v][i] != assignment[y][j]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        variable = []
        for v in self.domains[var]:
            variable.append(v)
        return variable

    def select_unassigned_variable(self, assignment):
        for v in self.crossword.variables:
            if v not in assignment:
                return v
        return None

    def backtrack(self, assignment):
        unassigned = self.select_unassigned_variable(assignment=assignment)
        if not unassigned:
            return assignment

        for v in self.domains[unassigned]:
            assignment[unassigned] = v
            if self.consistent(assignment):
                res = self.backtrack(assignment=assignment)
                if res:
                    return res
            assignment.pop(unassigned)

        return None


def main():
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
