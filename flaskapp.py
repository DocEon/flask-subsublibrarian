#! /usr/bin/python3

from flask import Flask, request, render_template
from subsublibrarian import *

app = Flask(__name__)

spinUp()

@app.route("/", methods=["GET", "POST"])
def subsublibrarian():
	error = None
	if request.method == "GET":
		return render_template("subsublibrarian_form.html")
	elif request.method == "POST":
		genre = request.form["genre"]
		language = request.form["language"]
		searchString = request.form["searchString"]
		resultDict = searchSents(searchString, language, genre)
		numberOfTexts = len(resultDict.keys())
		numberOfHits = 0
		for text in resultDict.keys():
			for hit in resultDict[text]:
				numberOfHits = numberOfHits + 1
		if numberOfHits == 0:
			return "No results found!"
		else:
			return render_template("searchresult.html", resultDict = resultDict, urllist = [getURL(getPath(key, path_list)) for key in resultDict.keys()], numberOfHits = numberOfHits, searchString = searchString)
	else:
		return "Test test test test test"

if __name__ == "__main__":
	app.run()
