# Overview

There is a MUD genre that I hold close to my heart called AberMUD. Believe it or not, I was really into Perl for a while. I even tried [reviving AberMUD](https://github.com/jasonmay/abermud) with the hope that I could make a very flexible and extensible world. Even after putting so much work into making it easy to add new things to the world, I noticed that I still had to modify the codebase for every new quest. The quests are the fun part! They are unpredictable and challenging. Any special case logic keeps a game interesting. Turns out special cases are hard to configure.

I am a few decades late to this already long-dead fad that is known as MUDs, but I plan to use this project to introduce interesting systems design concepts, code layout decisions, and see how they play out. If all goes well, I will have build **the most flexible world building tool for MUDs on the planet**. Yes, even more flexible than [LPMud](https://en.wikipedia.org/wiki/LPMud).

AberMUD instances are derived from "dirt" codebases, iDirt, CDirt, etc. LPMud accomplishes this, to an extent, by offering its own programming language, but still restricts the developer to its limited hooks.

With the advent of reactive web apps, native mobile apps, and quick prototyping tools, I feel that I can modernize the MUD platform and reintroduce the veterans as well as possibly introduce the textually creative souls into the world of interactive prose. And what if I made custom hooks available almost every possible change in MUD state without compromising performance?

Allow me to indulge a little in my evil plans.

# Architecture

## World Storage

AberMUDs have a very rigid grammar for building worlds. I have never played LPMud, but I believe it's code stored in a database, managed in a way that one can edit code straight from the MUD itself.

My idea is to take the concept of things like "locations", "objects", "mobiles", "quests", "inventory", "currency", and generalize them to an extreme, as in, store as much of the logic in a database and as little in a static codebase as possible.

### Model Representation

Here's the very naive first pass at how this would look like as a schema:

| **[Entities](#entities)** |
| ------------ |
| id           |
| label        |

| **[Properties](#properties)** |
| -------------- |
| id             |
| property\_name |
| property\_type |

| **[FlagChoices](#flagchoices)** |
| -------------- |
| id             |
| property\_id |
| flag\_name |

| **[EntityInstances](#entityinstances)** |
| ------------------- |
| id                  |
| entity\_id          |
| moniker             |
| zone                |

| **[PropertyInstances](#propertyinnstances)** |
| -------------------   |
| id                    |
| property\_id          |
| entity\_instance\_id  |
| value\_str            |
| value\_int            |
| value\_bool           |
| value\_struct         |
| value\_binary         |

### Entities

An entity is basically the root of any concept in a MUD. It will have very few records. Some examples this would be for are:

* Locations
* Objects
* Mobiles
* Quests
* Currency

### Properties

One entity will have zero or more properties. A property can be something like the name, location ID, player ID, etc.

### FlagChoices

Flag choices are a list of flags. Let's say an entity has a property "spell", and the possible spells are: "Heal", "Missile", and "Silence". Spells would have a list of flags, and these would be the choices as constraints. Or maybe the spell assignments would point to the flag IDs. I'll leave that as an implementation detail, or maybe I'll leave it up to the designer!

### EntityInstances

Let's assume that locations are considered an entity. If there is an entry of "Location" in [Entities](#entities), then all locations (location "instances") will be saved here in EntityInstances.

### PropertyInstances

Property instances are occurrences of a specific property. For instance, "Name" would be a property, "Shopkeeper", "Bear", "Jerry Seinfeld" would be the property instances.


## Model interaction

If things like locations and currency are completely dynamic, how do we even handle that in code? This is where the magic comes in. I don't think I can even effectively convey this without jumping straight into an example. This involves building my own turing complete AST that uses Python's AST components and compiles it down to python code objects.

### Example: Locations

Let's write it as if we were being old-school and not trying anything fancy, in typical AberMUD fashion:

```python
loc_id = players[plr_id].location
loc = locations[loc_id]
directions = ["north", "south", "east", "west", "up", "down"]
loc_mobiles = [m for m in mobiles if m.location == loc_id]
loc_objects = [o for o in objects if o.location == loc_id]

print(loc.title)  # "Hallway" etc
print(loc.description)  # "You see blah. There is light shining in from blah."
for m in loc_mobiles:
    print(m.standing_description)  # "Jerry Seinfeld is standing here." etc
for o in loc_objects:
    print(o.description)  # "Jerry Seinfeld is standing here." etc
for direction in directions:
    if direction in loc.exits:  # "North: Room of Treasures" etc
        print(direction + ": " + locations[loc.exits[direction]].title)
```

I'll explain in a second, but for your information, this is what the AST of this python code looks like:

```python
Module(
    body=[
        Assign(
            targets=[Name(id="loc_id", ctx=Store())],
            value=Attribute(
                value=Subscript(
                    value=Name(id="players", ctx=Load()),
                    slice=Index(value=Name(id="plr_id", ctx=Load())),
                    ctx=Load(),
                ),
                attr="location",
                ctx=Load(),
            ),
        ),
        Assign(
            targets=[Name(id="loc", ctx=Store())],
            value=Subscript(
                value=Name(id="locations", ctx=Load()),
                slice=Index(value=Name(id="loc_id", ctx=Load())),
                ctx=Load(),
            ),
        ),
        Assign(
            targets=[Name(id="directions", ctx=Store())],
            value=List(
                elts=[
                    Str(s="north"),
                    Str(s="south"),
                    Str(s="east"),
                    Str(s="west"),
                    Str(s="up"),
                    Str(s="down"),
                ],
                ctx=Load(),
            ),
        ),
        Assign(
            targets=[Name(id="loc_mobiles", ctx=Store())],
            value=ListComp(
                elt=Name(id="m", ctx=Load()),
                generators=[
                    comprehension(
                        target=Name(id="m", ctx=Store()),
                        iter=Name(id="mobiles", ctx=Load()),
                        ifs=[
                            Compare(
                                left=Attribute(
                                    value=Name(id="m", ctx=Load()),
                                    attr="location",
                                    ctx=Load(),
                                ),
                                ops=[Eq()],
                                comparators=[Name(id="loc_id", ctx=Load())],
                            )
                        ],
                    )
                ],
            ),
        ),
        Assign(
            targets=[Name(id="loc_objects", ctx=Store())],
            value=ListComp(
                elt=Name(id="o", ctx=Load()),
                generators=[
                    comprehension(
                        target=Name(id="o", ctx=Store()),
                        iter=Name(id="objects", ctx=Load()),
                        ifs=[
                            Compare(
                                left=Attribute(
                                    value=Name(id="o", ctx=Load()),
                                    attr="location",
                                    ctx=Load(),
                                ),
                                ops=[Eq()],
                                comparators=[Name(id="loc_id", ctx=Load())],
                            )
                        ],
                    )
                ],
            ),
        ),
        Print(
            dest=None,
            values=[
                Attribute(value=Name(id="loc", ctx=Load()), attr="title", ctx=Load())
            ],
            nl=True,
        ),
        Print(
            dest=None,
            values=[
                Attribute(
                    value=Name(id="loc", ctx=Load()), attr="description", ctx=Load()
                )
            ],
            nl=True,
        ),
        For(
            target=Name(id="m", ctx=Store()),
            iter=Name(id="loc_mobiles", ctx=Load()),
            body=[
                Print(
                    dest=None,
                    values=[
                        Attribute(
                            value=Name(id="m", ctx=Load()),
                            attr="standing_description",
                            ctx=Load(),
                        )
                    ],
                    nl=True,
                )
            ],
            orelse=[],
        ),
        For(
            target=Name(id="o", ctx=Store()),
            iter=Name(id="loc_objects", ctx=Load()),
            body=[
                Print(
                    dest=None,
                    values=[
                        Attribute(
                            value=Name(id="o", ctx=Load()),
                            attr="description",
                            ctx=Load(),
                        )
                    ],
                    nl=True,
                )
            ],
            orelse=[],
        ),
        For(
            target=Name(id="direction", ctx=Store()),
            iter=Name(id="directions", ctx=Load()),
            body=[
                If(
                    test=Compare(
                        left=Name(id="direction", ctx=Load()),
                        ops=[In()],
                        comparators=[
                            Attribute(
                                value=Name(id="loc", ctx=Load()),
                                attr="exits",
                                ctx=Load(),
                            )
                        ],
                    ),
                    body=[
                        Print(
                            dest=None,
                            values=[
                                BinOp(
                                    left=BinOp(
                                        left=Name(id="direction", ctx=Load()),
                                        op=Add(),
                                        right=Str(s=": "),
                                    ),
                                    op=Add(),
                                    right=Attribute(
                                        value=Subscript(
                                            value=Name(id="locations", ctx=Load()),
                                            slice=Index(
                                                value=Subscript(
                                                    value=Attribute(
                                                        value=Name(
                                                            id="loc", ctx=Load()
                                                        ),
                                                        attr="exits",
                                                        ctx=Load(),
                                                    ),
                                                    slice=Index(
                                                        value=Name(
                                                            id="direction", ctx=Load()
                                                        )
                                                    ),
                                                    ctx=Load(),
                                                )
                                            ),
                                            ctx=Load(),
                                        ),
                                        attr="title",
                                        ctx=Load(),
                                    ),
                                )
                            ],
                            nl=True,
                        )
                    ],
                    orelse=[],
                )
            ],
            orelse=[],
        ),
    ]
)
```

Now let's imagine if we allowed any quest writer to just write python and inject it straight into the server. That is a security nightmare! Just one forkbomb away from total destruction.

How do we solve that? By **abstracting all dangerous operations with our own AST**. The reason this is even a potential solution is that Python can compile a Python AST down into a [code object](https://docs.python.org/3/c-api/code.html), which (I think) has just as much performance overhead as a .pyc file, which is what any .py script compiles down to when run from the shell.

Accessing arbitrary variables and functions? Terrible idea. 

Here is a proposed example (obviously likely to change).

```
[
    "TODO"
]
```
