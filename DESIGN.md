# Overview

There is a MUD genre that I hold close to my heart called AberMUD. Believe it or not, I was really into Perl for a while. I even tried [reviving AberMUD](https://github.com/jasonmay/abermud) with the hope that I could make a very flexible and extensible world. Even after putting so much work into making it easy to add new things to the world, I noticed that I still had to modify the codebase for every new quest. The quests are the fun part! They are unpredictable and challenging. Any special case logic keeps a game interesting. Turns out special cases are hard to configure.

I am a few decades late to this already long-dead fad that is known as MUDs, but I plan to use this project to introduce interesting systems design concepts, code layout decisions, and see how they play out. If all goes well, I will have build **the most flexible world building tool for MUDs on the planet**. Yes, even more flexible than [LPMud](https://en.wikipedia.org/wiki/LPMud).

AberMUD instances are derived from "dirt" codebases, iDirt, CDirt, etc. LPMud accomplishes this, to an extent, by offering its own programming language, but still restricts the developer to its limited hooks.

With the advent of reactive web apps, native mobile apps, and quick prototyping tools, I feel that I can modernize the MUD platform and reintroduce the veterans as well as possibly introduce the textually creative souls into the world of interactive prose. And what if I made custom hooks available almost every possible change in MUD state without compromising performance?

Allow me to indulge you a little in my evil plans.

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

Accessing arbitrary variables and functions via user input? Terrible idea. I am proposing a few abstractions that might involve some minor overhead on the designer's point of view to make it efficient, but allowing making new node types and functions should simplify that.

Here is a (very rough) proposed example:

```json
[
  {
    "node": "Assign",
    "variable": "loc_id",
    "expression": {
      "node": "PlayerProperty",
      "key": "location"
    }
  },
  {
    "node": "Assign",
    "variable": "loc",
    "expression": {
      "node": "Entity",
      "key": {
        "node": "Variable",
        "var_name": "loc_id"
      }
    }
  },
  {
    "node": "Assign",
    "variable": "directions",
    "expression": {
      "node": "List",
      "elements": [
        {
          "node": "StringLiteral",
          "literal_value": "north"
        },
        {
          "node": "StringLiteral",
          "literal_value": "south"
        },
        {
          "node": "StringLiteral",
          "literal_value": "east"
        },
        {
          "node": "StringLiteral",
          "literal_value": "west"
        },
        {
          "node": "StringLiteral",
          "literal_value": "up"
        },
        {
          "node": "StringLiteral",
          "literal_value": "down"
        }
      ]
    }
  },
  {
    "node": "SendToPlayer",
    "expression": {
      "node": "EntityProperty",
      "entity": {
        "node": "Variable",
        "var_name": "loc"
      },
      "property": {
        "node": "StringLiteral",
        "literal_value": "title"
      }
    }
  },
  {
    "node": "SendToPlayer",
    "expression": {
      "node": "EntityProperty",
      "entity": {
        "node": "Variable",
        "var_name": "loc"
      },
      "property": {
        "node": "StringLiteral",
        "literal_value": "title"
      }
    }
  },
  {
    "node": "SendToPlayer",
    "expression": {
      "node": "EntityProperty",
      "entity": {
        "node": "Variable",
        "var_name": "loc"
      },
      "property": {
        "node": "StringLiteral",
        "literal_value": "description"
      }
    }
  },
  {
    "node": "SendToPlayer",
    "expression": {
      "node": "EntityProperty",
      "entity": {
        "node": "Variable",
        "var_name": "loc"
      },
      "property": {
        "node": "StringLiteral",
        "literal_value": "description"
      }
    }
  },
  {
    "node": "Loop",
    "iter_var_name": "mob",
    "list_expression": {
      "node": "Entities",
      "filter": {
        "node": "Compare",
        "operator": "EntityType",
        "left": {
          "node": "Variable",
          "var_name": "mob"
        },
        "right": {
          "node": "StringLiteral",
          "literal_value": "Mobile"
        }
      }
    },
    "body": [
      {
        "node": "SendToPlayer",
        "expression": {
          "node": "EntityProperty",
          "entity": {
            "node": "Variable",
            "var_name": "mob"
          },
          "key": {
            "node": "Variable",
            "var_name": "standing_description"
          }
        }
      }
    ]
  },
  {
    "node": "Loop",
    "iter_var_name": "obj",
    "list_expression": {
      "node": "Entities",
      "filter": {
        "node": "Compare",
        "operator": "EntityType",
        "left": {
          "node": "Variable",
          "var_name": "obj"
        },
        "right": {
          "node": "StringLiteral",
          "literal_value": "Object"
        }
      }
    },
    "body": [
      {
        "node": "SendToPlayer",
        "expression": {
          "node": "EntityProperty",
          "entity": {
            "node": "Variable",
            "var_name": "obj"
          },
          "key": {
            "node": "Variable",
            "var_name": "description"
          }
        }
      }
    ]
  },
  {
    "node": "Loop",
    "iter_var_name": "direction",
    "list_expression": {
      "node": "Variable",
      "var_name": "directions"
    },
    "body": [
      {
        "node": "If",
        "condition": {
          "node": "Compare",
          "operator": "In",
          "iter_expression": {
            "node": "Variable",
            "var_name": "direction"
          },
          "collection_expression": {
            "node": "EntityProperty",
            "entity": {
              "node": "Variable",
              "var_name": "loc"
            },
            "property": {
              "node": "Variable",
              "var_name": "exits"
            }
          }
        },
        "if_body": {
          "node": "SendToPlayer",
          "expression": {
            "node": "StringConcat",
            "strings": [
              {
                "node": "Variable",
                "var_name": "direction"
              },
              {
                "node": "StringLiteral",
                "literal_value": ": "
              },
              {
                "node": "EntityProperty",
                "entity": {
                  "node": "Entity",
                  "key": {
                    "node": "Subscript",
                    "base": {
                      "node": "EntityProperty",
                      "entity": {
                        "node": "Variable",
                        "var_name": "loc"
                      },
                      "property": {
                        "node": "StringLiteral",
                        "literal_value": "exits"
                      }
                    },
                    "index": {
                      "node": "StringLiteral",
                      "literal_value": "direction"
                    }
                  }
                },
                "property": {
                  "node": "StringLiteral",
                  "literal_value": "title"
                }
              }
            ]
          }
        },
        "else_body": {}
      }
    ]
  }
]
```

Notice that there is no concept of using existing variable names. Any new variables are ones I create within the scope of the AST. This prevents remote execution. Entities are called using abstract nodes, like "Entity" and "EntityProperty" instead of actual variable names and having the ability to call dangerous functions on them.

#### Why not just make a language? Wouldn't that be much less effort to write?

You know what, you're right. That would be less effort to write than a gigantic JSON structure every time we want to write custom logic. If we don't decouple it with an abstracted AST, the language could also be a security nightmare. Anybody can write their own grammar that builds an AST. The extra benefit of having an AST to work with directly is building the AST with concepts other than languages or grammars. Perhaps logic you can change with a website and validate. Or a fluid tree building flow from a native mobile app.

### Prevalence of Code Objects

Custom code objects will be called in every possible event I can think of that involves a mutation. Generalizing the data into entities makes this much easier. Every entity change can be gated through functions, and hooks can be provided that loop through custom code. For instance: before every entity property change, after every entity property change, maybe a hook wrapper around the entity property change itself so we can modify what the change result will be, etc. Maybe you want to incorporate weather in your MUD. Maybe the weather will change over time and want to address things like burn damage or frostbite. Weather is an entity, have an entity instance, and have hooks on the property changes. Players will have their own ephemeral entity instances (attached by a connector_id), and if they, for example, enter a room that's too hot because of the weather entity, a change of the entity ("player") property ("location") can trigger that effect.

Of course, players will each have their own timer settings to call arbitrary things, such as slow damage over time based on conditions, etc.
