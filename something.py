import z3


def solve(phi):
    s = z3.Solver()
    s.add(phi)
    s.check()
    return s.model()


# Simple solve
formula = z3.Int("x") / 7 == 6
print(solve(formula))

# Bit vectors
y = z3.BitVec("y", 8)
print(solve(y << 3 == 40))

# Quantifiers
z = z3.Int("z")
n = z3.Int("n")
print(solve(z3.ForAll([z], z * n == z)))

# Sketching
x = z3.BitVec("x", 8)
slow_expr = x * 2
h = z3.BitVec("h", 8)  # The hole, a.k.a. ??
fast_expr = x << h
goal = z3.ForAll([x], slow_expr == fast_expr)
print(solve(goal))
