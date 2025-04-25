# Part (b) Grammar reduction and CNF conversion

def print_simplified_grammar():
    print("Simplified Grammar (No Left Recursion):")
    print("E  → T E'")
    print("E' → + T E' | ε")
    print("T  → F T'")
    print("T' → * F T' | ε")
    print("F  → (E) | a")

def print_cnf_grammar():
    print("\nGrammar in CNF:")
    print("E  → T E1")
    print("E1 → P X1 | ε")
    print("X1 → T E1")
    print("T  → F T1")
    print("T1 → M X2 | ε")
    print("X2 → F T1")
    print("F  → L X3 | A")
    print("X3 → E R")
    print("P  → '+'")
    print("M  → '*'")
    print("L  → '('")
    print("R  → ')'")
    print("A  → 'a'")

# Running
print_simplified_grammar()
print_cnf_grammar()
