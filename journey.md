# October 15, 2019

## Yaegi vs Compiled Python

As referenced in my Twitch channel page, I chose to use compiled Python in my [design document](https://github.com/jasonmay/twitch-jarsonmud/blob/master/DESIGN.md).

[Yaegi](https://github.com/containous/yaegi) is something I recently learned about, that might be worth exploring. I am going in blind, but we will be evaluating and debating on whether this has the flexibility we want, and if not, we will disregard this as a contender and stay the course with compiled Python!

Hopefully we get to some actual AST building and benchmarking!

### Show notes:

The reason I chose Python over Go for Jarsonmud is that I wanted to be able to break syntax down to an abstract syntax tree (AST) and convert the AST into fast running bytecode. I looked into Go for this, and it has support to build ASTs and convert Go to a tree, but (at this time) the tree can't be compiled into bytecode. Python can do this! (Refer to the ast package, and .pyc files).

[Python black](https://pypi.org/project/black/) is nice!

**References**:

[Yaegi](https://godoc.org/github.com/containous/yaegi)

[Getting to/from AST with Python](https://greentreesnakes.readthedocs.io/en/latest/tofrom.html)

[Python built-in AST package](https://docs.python.org/3/library/ast.html)
