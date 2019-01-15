'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef
from dragonfly import AppContext, Grammar, Repeat

from mathfly.lib import control, utilities
from mathfly.lib.dfplus.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/scientific_notebook.toml")
CORE = utilities.load_toml_relative("config/core.toml")

def texchar(symbol):
    keychain = "ctrl:down, "
    for character in symbol:
        keychain = keychain + character + ", "
    keychain=keychain + "ctrl:up"
    Key(keychain).execute()

def greek(big, greek_letter):
    if big:
        greek_letter = greek_letter.upper()
    Key("c-g, " + greek_letter).execute()

def matrix(rows, cols):
    Key("f10/5, i/5, down:8, enter/50").execute()
    Key(str(rows) + "/50, tab, " + str(cols) + "/50, enter").execute()

class sn_mathematics(MergeRule):
    pronunciation = "Scientific notebook maths"

    mapping = {
        BINDINGS["symbol_prefix"] + " <symbol>":
            Function(texchar),
        #
        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":
            Function(greek),
        BINDINGS["accent_prefix"] + " <accent>":
            Key("%(accent)s"),

        "<misc_sn_keys>":
            Key("%(misc_sn_keys)s"),
        "<misc_sn_text>":
            Text("%(misc_sn_text)s"),
            
        #
        "matrix <rows> by <cols>":
            Function(matrix),

        "<numbers> <denominator>":
            Key("c-f, %(numbers)s, down, %(denominator)s, right"),

        "mathematics test": Text("test successful"),

    }

    extras = [
        IntegerRef("rows", 1, 6),
        IntegerRef("cols", 1, 6),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("big", {CORE["capitals_prefix"]: True}),
        Choice("greek_letter", BINDINGS["greek_letters"]),
        Choice("symbol", BINDINGS["tex_symbols"]),
        Choice("accent", BINDINGS["accents"]),
        Choice("misc_sn_keys", BINDINGS["misc_sn_keys"]),
        Choice("misc_sn_text", BINDINGS["misc_sn_text"]),
        Choice("denominator", BINDINGS["denominators"]),
    ]

    defaults = {
        CORE["capitals_prefix"]: False,
    }

control.nexus().merger.add_global_rule(sn_mathematics())


class SNRule(MergeRule):
    pronunciation = "scientific notebook"

    mapping = {
        "new file": Key("c-n"),
        "open file": Key("c-o"),
        "save as": Key("cs-s"),

        "toggle math": Key("c-m"),
        "toggle text": Key("c-t"),

        "undo [<n>]": Key("c-z")*Repeat(extra="n"),
        "redo [<n>]": Key("c-y")*Repeat(extra="n"),
        # "next tab [<n>]": Key("c-pgdown")*Repeat(extra="n"),
        # "prior tab [<n>]": Key("c-pgup")*Repeat(extra="n"),
        # "close tab [<n>]": Key("c-w/20")*Repeat(extra="n"),

        # "view PDF": Key("c-r"),
        # "update PDF": Key("cs-r"),

        # "move line up [<n>]": Key("a-up")*Repeat(extra="n"),
        # "move line down [<n>]": Key("a-down")*Repeat(extra="n"),

        # "insert <environment>": Key("a-i, h, %(environment)s"),
        # "insert <mode>": Key("a-p, %(mode)s"),

        }
    extras = [
        IntegerRef("n", 1, 10),
        
    ]
    defaults = {
        "n": 1,
    }

context = AppContext(executable="scientific notebook")
grammar = Grammar("scientific notebook", context=context)
rule = SNRule(name="scientific notebook")
grammar.add_rule(rule)
grammar.load()