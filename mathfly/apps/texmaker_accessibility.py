"""
All credit to James Stout (aka WolfManStout)

These are text manipulation commands that emulate Dragon's "full text control" in a a very small number of applications
the applications I have seen it work in are Texmaker, Chrome, and Firefox.

In order for these commands to work you need to install some PREREQUISITES.
For instructions on installing the prerequisites for these commands,
please see https://github.com/wolfmanstout/pyia2

I will supplement the instructions given there, here.
1) you need to download or clone the repository there.
2) you need to Install python 2.7 and pip for Windows (but you probably have already done that)
3) Install comtypes library using pip 
    If you're using powershell, I believe the way to do that is to type in:
    py -2 -m pip install comtypes
4) "Register IAccessible2Proxy.dll with Windows (Note: this needs to be done with administration priveleges)"
    This is done by:
        a) going into the terminal in administrator mode
        b) navigating to the directory where you have the file IAccessible2Proxy.dll (this file is included in the pyia repository linked to above which you need to download)
        c) typing in: regsvr32 IAccessible2Proxy.dll
        d) pressing enter
    If I recall, if you do this correctly you should get a pop up box saying that it was successful.

For further information about these commands see:
http://handsfreecoding.org/2018/12/27/enhanced-text-manipulation-using-accessibility-apis/

In my experience, these commands don't always work. when they don't work,
you will probably get a message in the Natlink window saying something like
"nothing is focused" or "focused item is not text". When this happens, I recommend
switching to Google Chrome for a second (possibly the address bar if necessary since the commands are known to work there well)
and then switching back to the application you want, in this case Texmaker.
In my experience this will fix the problem temporarily.
"""

from dragonfly import (Grammar, Dictation, Function, Compound, Alternative,
                       Literal, CursorPosition, TextQuery, Choice, Repeat,
                       IntegerRef)

from dragonfly import get_accessibility_controller

from mathfly.lib.actions import Text, Key, Mouse, AppContext
from mathfly.lib import control
from mathfly.lib.merge.mergerule import MergeRule

accessibility = get_accessibility_controller()

class TexmakerAccessibilityRule(MergeRule):
    pronunciation = "texmaker accessibility"

    mapping = {
        

        # Accessibility API Mappings
        "go before <text_position_query>": Function(
            lambda text_position_query: accessibility.move_cursor(
                text_position_query, CursorPosition.BEFORE)),
        "go after <text_position_query>": Function(
            lambda text_position_query: accessibility.move_cursor(
                text_position_query, CursorPosition.AFTER)),
        "destruction <text_query>": Function(accessibility.select_text),
        "words <text_query> delete": Function(
            lambda text_query: accessibility.replace_text(text_query, "")),
        "replace <text_query> with <replacement>": Function(
            accessibility.replace_text),

    }


    extras = [
        Dictation("replacement"),
        Compound(
            name="text_query",
            spec=("[[([<start_phrase>] <start_relative_position> <start_relative_phrase>|<start_phrase>)] <through>] "
                  "([<end_phrase>] <end_relative_position> <end_relative_phrase>|<end_phrase>)"),
            extras=[Dictation("start_phrase", default=""),
                    Alternative([Literal("before"), Literal("after")],
                                name="start_relative_position"),
                    Dictation("start_relative_phrase", default=""),
                    Literal("through", "through", value=True, default=False),
                    Dictation("end_phrase", default=""),
                    Alternative([Literal("before"), Literal("after")],
                                name="end_relative_position"),
                    Dictation("end_relative_phrase", default="")],
            value_func=lambda node, extras: TextQuery(
                start_phrase=str(extras["start_phrase"]),
                start_relative_position=(CursorPosition[extras["start_relative_position"].upper()]
                                         if "start_relative_position" in extras else None),
                start_relative_phrase=str(extras["start_relative_phrase"]),
                through=extras["through"],
                end_phrase=str(extras["end_phrase"]),
                end_relative_position=(CursorPosition[extras["end_relative_position"].upper()]
                                       if "end_relative_position" in extras else None),
                end_relative_phrase=str(extras["end_relative_phrase"]))),
        Compound(
            name="text_position_query",
            spec="<phrase> [<relative_position> <relative_phrase>]",
            extras=[Dictation("phrase", default=""),
                    Alternative([Literal("before"), Literal("after")],
                                name="relative_position"),
                    Dictation("relative_phrase", default="")],
            value_func=lambda node, extras: TextQuery(
                end_phrase=str(extras["phrase"]),
                end_relative_position=(CursorPosition[extras["relative_position"].upper()]
                                       if "relative_position" in extras else None),
                end_relative_phrase=str(extras["relative_phrase"])))
    ]

    defaults = {

    }


#---------------------------------------------------------------------------

context = AppContext(executable="texmaker")
grammar = Grammar("TexmakerAccessibility", context=context)
rule = TexmakerAccessibilityRule(name="TexmakerAccessibility")
grammar.add_rule(rule)
grammar.load()
