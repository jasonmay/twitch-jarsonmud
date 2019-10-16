import ast

one_plus_one = ast.Expression(
    body=ast.BinOp(
        left=ast.Num(lineno=0, col_offset=0, n=1),
        op=ast.Add(lineno=0),
        right=ast.Num(lineno=0, col_offset=0, n=3),
        lineno=0,
        col_offset=0,
    ),
    lineno=0,
    col_offset=0,
)
a = compile(one_plus_one, "<string>", "eval")
print(eval(a))
print(dir(a))
