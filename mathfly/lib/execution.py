from mathfly.lib.actions import Text, Key, Mouse, AppContext
from mathfly.lib import utilities

# Alternate between executing as text and executing as keys
def alternating_command(command):
	if type(command) in [str, int, unicode]:
		Text(str(command)).execute()
	elif type(command) in [list, tuple]:
		for i in range(len(command)):
			if i%2==0:
				Text(command[i]).execute()
			else:
				Key(command[i]).execute()

def template(template):
	utilities.paste_string(template)

def paren_function(name, dl1="(", dl2=")"):
	e, text = utilities.read_selected(False)
	Text(name + dl1).execute()
	if text:
		utilities.paste_string(text)
		Text(dl2).execute()
	else:
		Text(dl2).execute()
		Key("left:" + str(len(dl2))).execute()