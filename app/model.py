import random

labels = ["Reddit_0", "Reddit_1"]

def classify(text):
	if (len(text) > 3):
		return labels[0]
	else:
		return labels[1]