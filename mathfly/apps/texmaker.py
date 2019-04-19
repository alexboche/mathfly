

from dragonfly import (Grammar, Dictation, Function, Choice, Repeat,
                       IntegerRef)

from mathfly.lib.actions import Text, Key, Mouse, AppContext
from mathfly.lib import control
from mathfly.lib.merge.mergerule import MergeRule

# Texmaker keyboard shortcuts can be changed at 'Options - Configure TeXmaker - Shortcuts - Menus - Tools'self


class TexmakerRule(MergeRule):
    pronunciation = "texmaker"

    mapping = {
    # file
    "new [file]": Key("c-n"),
    "open": Key("c-o"),
    "open recent": Key("a-f, down:3, right"),
    "close": Key("c-w"),
    "exit": Key("c-q"),
    "restore previous session": Key("cs-f8"),
    
    # edit
    "[go to] line <m>": Key("c-g") + Text("%(m)s") + Key("enter"),
    "comment": Key("c-t"),
    "uncomment": Key("c-u"),
    "indent": Key("c-rangle"),
    "(outdent | unindent)": Key("c-langle"),
    "find [<text>]": Key("c-f/5") + Text("%(text)s"),
    "find next [<n>]": Key("c-m") * Repeat(extra="n"),
    "replace": Key("c-r"),
    "check spelling": Key("cs-f7"),
    "refresh structure": Key("cs-f1"),

    # tools
            # if you have f1 set to turn on/off microphone, you will need to reset the Texmaker shortcut 
    "quick build": Key("f1"), 
        # "LaTeX": Key("f2"), # not sure what this does so I'm going to comment it out
    "view DVI": Key("f3"),
    "DVI to postscript": Key("f4"),
    "view postscript": Key("f5"),
    "PDF latex": Key("f6"),
    "view PDF": Key("f7"),
    "postscript to PDF": Key("f8"),
    "DVI to PDF": Key("f9"),
    "view log": Key("f10"),
    "bibtech": Key("f11"),
    "make index": Key("f12"),


    # view
        # Texmaker doesn't seem to have tabs unless I'm missing something
    "next (document | dock) [<n>]": Key("a-pgdown") * Repeat(extra='n'),
    "(previous | prior)  (document | dock)": Key("a-pgup") * Repeat(extra='n'),
    "full-screen": Key("cs-f11"),
    "switch pane": Key("c-space"), # switch between editor and embedded viewer


    }


    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 10),
        IntegerRef("m", 1, 1000),
    ]

    defaults = {

    }


#---------------------------------------------------------------------------

context = AppContext(executable="texmaker")
grammar = Grammar("Texmaker", context=context)
rule = TexmakerRule(name="Texmaker")
grammar.add_rule(rule)
grammar.load()
