from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
P0A = And(AKnight,AKnave) # represents statement made by A

knowledge0 = And(
    Or(AKnight, AKnave), # A can be either Knight or Knave
    Implication(AKnight, P0A), #If A is Knight then What A said must be true which is "I am both knight and knaves"
    Implication(AKnave, Not(P0A)) #If A is Knave then What A said must be false which is Not of "I am both knight and knaves"
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
P1A = And(AKnave, BKnave) # Represent statement made by A

knowledge1 = And(
    Or(AKnight, AKnave), # A can be either Knight or Knave
    Or(BKnight, BKnave), # B can be either Knight or Knave
    Implication(AKnight, P1A), #If A is Knight then What A said must be true
    Implication(AKnave, Not(P1A)) #If A is Knave then What A said must be false which is Not of statement made
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
P2A = Or(And(AKnave,BKnave), And(AKnight, BKnight)) # Represents statement made by A
P2B = Not(P2A) # Represents statement made by B

knowledge2 = And(
    Or(AKnight, AKnave), # A can be either Knight or Knave
    Or(BKnight, BKnave), # B can be either Knight or Knave
    Implication(AKnight, P2A), #If A is Knight then What A said must be true
    Implication(AKnave, Not(P2A)), #If A is Knave then What A said must be false which is Not of statement made
    Implication(BKnight, P2B), #If B is Knight then What B said must be true
    Implication(BKnave, Not(P2B)), #If B is Knave then What B said must be false which is Not of statement made
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

P3A = Or(AKnight, AKnave) # Represents statement made by A
P3B = And(CKnave, Implication(Or(AKnight,AKnave), BKnave)) # Represents both statements made by B
P3C = AKnight # Represents statement made by C

knowledge3 = And(
    Or(AKnight, AKnave), # A can be either Knight or Knave
    Or(BKnight, BKnave), # B can be either Knight or Knave
    Or(CKnight, CKnave), # C can be either Knight or Knave
    Implication(AKnight, P3A), #If A is Knight then What A said must be true
    Implication(AKnave, Not(P3A)), #If A is Knave then What A said must be false which is Not of statement made
    Implication(BKnight, P3B), #If B is Knight then What B said must be true
    Implication(BKnave, Not(P3B)), #If B is Knave then What B said must be false which is Not of statement made 
    Implication(CKnight, P3C), #If C is Knight then What C said must be true
    Implication(CKnave, Not(P3C)), #If C is Knave then What C said must be false which is Not of statement made 
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
