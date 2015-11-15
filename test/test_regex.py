import re

titles=["bio-dome", "biodome", "kick-ass", "don't go in the house", "ordinary_decent_criminal", "What the #$! Do We (K)now!"]
for title in titles:
	new_title = " ".join(map(str.title, re.findall(r"\w+'\w+|\w+-\w+|\w+", title)))
	if "_" in new_title:
		new_title = new_title.replace("_", " ")
	print new_title