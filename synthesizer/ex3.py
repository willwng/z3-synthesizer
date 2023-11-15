import ex2
import sys
import lark
import re

holes = 0

def desugar_hole_var(source):
    global holes
    # such a hacky way
    buffer = ""
    var_buffer = ""
    reading_vars = False
    for i in range(len(source)):
        curr = source[i]
        if curr == "{":
            reading_vars = True
        elif curr == "}":
            # Flush the var_buffer into buffer
            stuff = var_buffer.split(",")
            var_buffer = ""
            var1 = stuff[0]
            var2 = stuff[1]
            buffer += f"(h{holes} ? {var1} : {var2})"
            holes += 1
            reading_vars = False
        elif reading_vars: 
            var_buffer += curr
        else:
            buffer += curr

    return buffer

def desugar_hole(source):
    parts = source.split('??')
    out = []
    for (i, part) in enumerate(parts[:-1]):
        out.append(part)
        out.append('(hb{0} ? x : hn{0})'.format(i))
    out.append(parts[-1])
    return ''.join(out)


def simplify(tree, subst={}):
    op = tree.data

    if op in ('add', 'sub', 'mul', 'div', 'shl', 'shr', 'neg', 'if'):
        for i in range(len(tree.children)):
            tree.children[i] = simplify(tree.children[i], subst)

    if op == 'if':
        cond = tree.children[0]
        if cond.data == 'var':
            name = cond.children[0]
            if name in subst:
                val = subst[name]
                if val.as_signed_long():
                    return tree.children[1]
                else:
                    return tree.children[2]

    return tree


def ex3(source):
    src1, src2 = source.strip().split('\n')
    # src2 = desugar_hole(src2)  # Allow ?? in the sketch part.
    src2 = desugar_hole_var(src2)  # Allow ?? in the sketch part.

    parser = lark.Lark(ex2.GRAMMAR)
    tree1 = parser.parse(src1)
    tree2 = parser.parse(src2)

    model = ex2.synthesize(tree1, tree2)
    print(ex2.pretty(tree1))

    values = ex2.model_values(model)
    simplify(tree2, values)  # Remove foregone conclusions.
    print(ex2.pretty(tree2, values))


if __name__ == '__main__':
    ex3(sys.stdin.read())
