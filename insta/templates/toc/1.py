# Part (a) CFG simulation and parse tree

class Node:
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children or []

    def display(self, level=0):
        print("  " * level + self.symbol)
        for child in self.children:
            child.display(level + 1)

def leftmost_derivation():
    steps = []
    current = "S"
    steps.append(current)
    
    # S → A1B
    current = "A1B"
    steps.append(current)
    
    # A → 0A
    current = "0A1B"
    steps.append(current)

    # A → 0A
    current = "00A1B"
    steps.append(current)

    # A → ε
    current = "001B"
    steps.append(current)

    # B → 0B
    current = "0010B"
    steps.append(current)

    # B → 1B
    current = "00101B"
    steps.append(current)

    # B → ε
    current = "00101"
    steps.append(current)

    return steps

def rightmost_derivation():
    steps = []
    current = "S"
    steps.append(current)

    # S → A1B
    current = "A1B"
    steps.append(current)

    # B → 0B
    current = "A10B"
    steps.append(current)

    # B → 1B
    current = "A101B"
    steps.append(current)

    # B → ε
    current = "A101"
    steps.append(current)

    # A → 0A
    current = "0A101"
    steps.append(current)

    # A → 0A
    current = "00A101"
    steps.append(current)

    # A → ε
    current = "00101"
    steps.append(current)

    return steps

def build_parse_tree():
    return Node("S", [
        Node("A", [
            Node("0", []),
            Node("A", [
                Node("0", []),
                Node("A", [
                    Node("ε")
                ])
            ])
        ]),
        Node("1"),
        Node("B", [
            Node("0", []),
            Node("B", [
                Node("1", []),
                Node("B", [
                    Node("ε")
                ])
            ])
        ])
    ])

# Running
print("Leftmost Derivation:")
for step in leftmost_derivation():
    print(step)

print("\nRightmost Derivation:")
for step in rightmost_derivation():
    print(step)

print("\nParse Tree:")
tree = build_parse_tree()
tree.display()
