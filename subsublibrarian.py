#! /usr/bin/python3

import os
#import json
# from google.cloud import translate
import nltk
import string
from nltk import word_tokenize, sent_tokenize, Text, FreqDist

# note to self: need to handle How It Is as a novel, which is technically all one sentence. Maybe use lines for sentences there? 
# right now, I'm using lines instead of sentences. Maybe the thing to do is to break up search results when result_line is longer than
# a certain length? I think that'd be smart.
# translate_client = translate.Client()

stopwords = nltk.corpus.stopwords.words('english')

play_list = [("Waiting for Godot", "En attendant Godot"), ("All That Fall", "Tous ceux qui tombent"), ("Act Without Words 1", "Acte sans paroles 1"), ("Act Without Words 2", "Acte sans paroles 2"), ("Endgame", "Fin de partie"),("Krapp's Last Tape", "La Dernière Bande"),("Embers", "Cendres"),("Happy Days", "Oh les beaux jours"),("Cascando", "Cascando"),("Play", "Comédie"),("Words and Music", "Paroles et musique"),("Eh Joe", "Dis Joe"),("Film", "Film"),("Breath", "Souffle"),("Come and Go", "Va et vient"),("Not I", "Pas moi"),("Footfalls", "Pas"),("Ghost Trio", "Trio du Fantôme"),("Rough for Radio 1", "Pochade radiophonique"),("Rough for Theatre 1", "Fragment de théâtre 1"),("Rough for Theatre 2", "Fragment de théâtre 2"),("That Time", "Cette fois"),("Rough for Radio 2", "Esquisse radiophonique"),("...but the clouds...",  "...que nuages..."),("A Piece of Monologue", "Solo"),("Ohio Impromptu", "Impromptu d'Ohio"),("Rockaby", "Berceuse"),("Nacht und Traume", "Nacht und Traume"),("What Where", "Quoi où"),("Catastrophe", "Catastrophe"),("Quad","Quad")]
novel_list = [("Molloy", "Molloy"), ("Malone Dies", "Malone meurt"), ("Murphy", "Murphy"), ("The Unnameable", "L'innommable"), ("Watt", "Watt"), ("How It Is", "Comment c'est"), ("Mercier and Camier", "Mercier et Camier"), ("Company", "Compagnie"), ("Ill Seen Ill Said", "Mal vu mal dit"), ("Worstword Ho", "Cap au pire")]
short_list = [("A Wet Night", "Rincée Nocturne"), ("Dante and the Lobster", "Dante et le homard"), ("Ding-Dong", "Ding-Dong"), ("Draff", "Résidu"), ("Fingal", "Fingal"), ("Love and Lethe", "Amour et léthé"), ("The Smeraldina's Billet Doux", "Le billet doux de la Smeraldina"), ("Walking Out", "Promenade"), ("What a Misfortune", "Quelle calamnité"), ("Yellow", "Bleme"), ("A Case in a Thousand",""), ("From an Abandoned Work", "D'un ouvrage abandonné"), ("Imagination Dead Imagine", "Imagination morte imaginez"), ("Enough", "Assez"), ("Ping", "Bing"), ("Texts for Nothing", "Textes pour rien"), ("Lessness", "Sans"), ("The Lost Ones", "Le Dépeupleur"), ("The Cliff", ""), ("",""), ("neither", "ni l’un ni l’autre"), ("All Strange Away", ""), ("Fizzles", "Foirades"), ("First Love", "Premier amour"), ("The Calmative", "Le calmant"), ("The End", "Le Fin"), ("The Expelled", "L’expulse"), ("Heard in the Dark 1", ""), ("Heard in the Dark 2", ""), ("One Evening", ""), ("Ceiling", "Plafond"), ("As the Story Was Told", ""), ("Stirrings Still", ""), ("Variations on a Still Point", "")]
directory = r"/Users/kenalba/Google Drive/beckett"

server = "www.especiallygreatliterature.com/"

defaultDirectory = "/srv/especiallygreatliterature.com/beckett"
path_list = []
plays = {}
novels = {}
shorts = {}
works = {}


def spinUp():
  filenames = getFileNames(defaultDirectory)
  initAll()

def getFileNames(directory):
  for root, dirs, files in os.walk(directory, topdown=False):
    for name in files:
      if name.find("txt") != -1:
        f = os.path.join(root, name)
        path_list.append(f)
  return path_list

def searchSents(string, lang, genre):
    # to do: support regexes
    # This only searches for strings on a sentence level.
    string = string.lower()
    result_dict = {}
    sents = []
    if genre == "drama":
        dict_to_search = plays
    elif genre == "novel":
        dict_to_search = novels
    elif genre == "short":
        dict_to_search = shorts
    for work in dict_to_search.keys():
        if lang == "en":
            sents = dict_to_search[work]["sents_en"]
        else:
            sents = dict_to_search[work]["sents_fr"]
        result_index = 0
        for x in range(0, len(sents)):
            if string in sents[x].lower():
                if work not in result_dict.keys():
                    result_dict[work] = {}
                result_dict[work][result_index] = []
                if len(sents[x]) > 200:
                    location = sents[x].find(string)
                    result_dict[work][result_index].append(sents[x][(location-75):(location+75)])
                else:    
                    try:
                        previous_line = sents[x-1]
                    except IndexError:
                        previous_line = ""
                    try:
                        next_line = sents[x+1]
                    except IndexError:
                        next_line = ""
                    result_dict[work][result_index].append(previous_line)
                    result_dict[work][result_index].append(sents[x])
                    result_dict[work][result_index].append(next_line)
                result_index = result_index + 1
        if result_index != 0:
            print("Found " + str(result_index) + " results in " + work + ".")
    return result_dict

def searchRaws(string, lang, genre):
  string = string.lower()
  textsToSearch = []
  result_dict = {}
  if genre == "drama":
      dict_to_search = plays
  elif genre == "novel":
      dict_to_search = novels
  elif genre == "short":
      dict_to_search = shorts
  for work in dict_to_search.keys():
    if lang == "en":
      raw = dict_to_search[work]["raw_en"]
    else:
      raw = dict_to_search[work]["raw_fr"]
    if string in raw:
      textsToSearch.append(work)
      print("Found string in" + work)
  for work in textsToSearch:
    getSents(work, genre)
    if lang == "en":
      sents = dict_to_search[work]["sents_en"]
    else:
      sents = dict_to_search[work]["sents_fr"]
    result_index = 0
    for x in range(0, len(sents)):
      if string in sents[x].lower():
          if work not in result_dict.keys():
              result_dict[work] = {}
          result_dict[work][result_index] = []
          if len(sents[x]) > 200:
              location = sents[x].find(string)
              result_dict[work][result_index].append(sents[x][(location-75):(location+75)])
          else:    
              try:
                previous_line = sents[x-1]
              except IndexError:
                  previous_line = ""
              try:
                  next_line = sents[x+1]
              except IndexError:
                  next_line = ""
              result_dict[work][result_index].append(previous_line)
              result_dict[work][result_index].append(sents[x])
              result_dict[work][result_index].append(next_line)
          result_index = result_index + 1
    if result_index != 0:
        print("Found " + str(result_index) + " results in " + work + ".")
  return result_dict

def printResults(result_dict):
    for key in result_dict.keys():
        print("* * * Found " + str(len(result_dict[key].keys())) + " results in " + key)
        for x in range(0, len(result_dict[key].keys())):
            print("\n")
            print("#" + str(x+1))
            for line in result_dict[key][x]:
                print(line)
        print("\n##########\n")
        
def getFrenchTitle(title_en, genre):
  if genre == "drama":
      title_fr = [title[1] for title in play_list if title[0] == title_en]
  elif genre == "novel":
      title_fr = [title[1] for title in novel_list if title[0] == title_en]
  elif genre == "short":
      title_fr = [title[1] for title in short_list if title[0] == title_en]
  return title_fr[0]
  
def getURL(path):
  split_path = path.split("/")
  file_info = [entry for entry in split_path if split_path.index(entry) >= split_path.index("beckett")]
  url = server + "/".join(file_info )
  url = url.replace(".txt", ".html")
  return url

def getPath(title, path_list, language="en"):
  filename = title.lower()
  accents = [("é", "e"), ("ô", "o"), ("ù", "u"), ("è", "e"), ("â", "a"), (" ", "_"), ("'", ""), (".", "")]
  for x in range(0, len(accents)):
    hit = filename.find(accents[x][0])
    if hit != -1:
      filename = filename.replace(accents[x][0], accents[x][1])
  filename = filename + ".txt"
  if language == "en":
    file_path = [path for path in path_list if filename in path and "english" in path]
  elif language == "fr":
    file_path = [path for path in path_list if filename in path and "french" in path]
  if len(file_path) == 0:
    print(" XXX Could not find " + title)
    return None
  else:
    print(" !!! Found " + title)
    return file_path[0]

# def machineTranslateText(playDict, sourceLanguage):
#   if sourceLanguage == "french":
#     translation = translate_client.translate(playDict["raw_fr"], target_language = "en")
#   elif sourceLanguage == "english":
#     translation = translate_client.translate(playDict["raw_en"], target_language = "fr")
#   return translation


## def translateSentences(sents, language):

def txtToDict(title_en, genre, getSents=True):
  work = {}
  path_en  = getPath(title_en, path_list)
  file_en = open(path_en, "r", encoding="utf-8")
  work["title_en"] = title_en
  work["path_en"] = path_en
  work["raw_en"] = file_en.read()
#  play["words_en"] = word_tokenize(play["raw_en"])
#  play["text_en"] = Text(play["words_en"])
  work["url_en"] = getURL(path_en)
  if getSents:
    work["sents_en"] = sent_tokenize(work["raw_en"])

  title_fr = getFrenchTitle(title_en, genre)
  path_fr = getPath(title_fr, path_list, language="fr")
  if path_fr != None:
    file_fr = open(path_fr, "r", encoding="utf-8")
    work["title_fr"] = title_fr
    work["path_fr"] = path_fr
    work["raw_fr"] = file_fr.read()
#    play["words_fr"] = word_tokenize(play["raw_fr"])
#    play["text_fr"] = Text(play["words_fr"])
    work["url_fr"] = getURL(path_fr)
    if getSents:
      work["sents_fr"] = sent_tokenize(work["raw_fr"])
  print("Successfully gobbled up " + title_en + ", AKA " + title_fr)
  file_en.close()
  return work

def initPlays(getSents=True):
    for x in range(0, len(play_list)):
        plays[play_list[x][0]] = txtToDict(play_list[x][0], "drama", getSents)

def initNovels(getSents=True):
    for x in range(0, len(novel_list)):
        novels[novel_list[x][0]] = txtToDict(novel_list[x][0], "novel", getSents)

def initShorts(getSents=True):
    for x in range(0, len(short_list)):
        shorts[short_list[x][0]] = txtToDict(short_list[x][0], "short", getSents)

def getSents(title_en, genre):
  if genre == "drama":
    plays[title_en] = txtToDict(title_en, "drama")
  elif genre == "novel":
    novels[title_en] = txtToDict(title_en, "novel")
  elif genre == "short":
    shorts[title_en] = txtToDict(title_en, "short")

def initAll():
    initPlays()
    initNovels()
    initShorts()
    works["plays"] = plays
    works["novels"] = novels
    works["shorts"] = shorts

def initAllRaw():
    initPlays(getSents=False)
    initNovels(getSents=False)
    initShorts(getSents=False)
    works["plays"] = plays
    works["novels"] = novels
    works["shorts"] = shorts

def getTopTwentyfive(words_txt, stopwords):
  words_clean = [word.lower() for word in words_txt]
  words_clean = [word for word in words_clean if word not in string.punctuation]
#gets with stop words:
#  fd_words_sw = nltk.FreqDist(words_clean)  
  words_clean = [word for word in words_clean if word not in stopwords]
  words_clean = [word for word in words_clean if "'" not in word]
  words_clean = [word for word in words_clean if "." not in word]
  fd_words_clean = nltk.FreqDist(words_clean)
  return fd_words_clean.most_common(25)

def makeAllHTML(plays, novels, shorts):
  for play in plays:
    makeHTML(plays[play], "en")
    makeHTML(plays[play], "fr")
  for novel in novels:
    makeHTML(novels[novel], "en")
    makeHTML(novels[novel], "fr")
  for short in shorts:
    makeHTML(shorts[short], "en")
    makeHTML(shorts[short], "fr")

def makeHTML(txtDict, lang):
  if ("path_" + lang) in txtDict.keys():
    path = txtDict["path_"+lang]
    other_lang = ""
    if lang == "en":
      other_lang = "fr"
    else:
      other_lang = "en"
    other_url = "url_" + other_lang
    other_title = "title_" + other_lang
    play = open(path, "r", encoding="utf-8")
    inputList = [line for line in play]
    outputFileName = path.replace("txt", "html")
    if os.path.isfile(outputFileName):
      os.remove(outputFileName)
    outputFile = open(outputFileName, "w", encoding="utf-8")
    outputFile.write("<html><head><style>div.right {text-align: right}div.center {align-items: center}body {  padding-left: 100px;  padding-right: 100px;  width: 600px;    text-indent: 1.5em;  background-color: #F3F3F3;}</style><body>")
    outputFile.write("<title>"+inputList[0]+"</title>")
    outputFile.write("<h2>"+inputList[0]+"</h2>")
    if other_url in txtDict.keys():
      outputFile.write("AKA <a href='http://" + txtDict[other_url] + "'>" + txtDict[other_title] + "</a><br>")
    for x in range(1, len(inputList)):
      outputFile.write(inputList[x]+"<br>")
    outputFile.write("<HR></body>")
    print("Wrote " + inputList[0] + " to " + outputFileName)
  else:
    print(txtDict["title_en"] + " not found")

def writeResults(result_dict):
    output_directory = directory + "/code/results.html"
    output = open(output_directory, "w", encoding = "utf-8")
    output.write("<html><head><style>div.right {text-align: right}div.center {align-items: center}body {  padding-left: 100px;  padding-right: 100px;  width: 600px;    text-indent: 1.5em;  background-color: #F3F3F3;}</style><body>")
    output.write("<title>Search results</title>")
    output.write("<h2>Search results</h2>")
    for key in result_dict.keys():
        output.write("<h3>* * * Found " + str(len(result_dict[key].keys())) + " results in " + key + "</h3>")
        for x in range(0, len(result_dict[key].keys())):
            output.write("<br>")
            output.write("<h4>#" + str(x+1) + "</h4>")
            for line in result_dict[key][x]:
                output.write(line + "<br>")
        output.write("<hr>")
    output.write("</body></html>")
    output.close()
    print("Output written to " + directory)
    
def searchInterface():
    print("Welcome to the subsublibrarian. Set 'genre', 'language', and 'string' and then type 'search' to execute your search.\n")
    command = ""
    genre = "drama"
    language = "en"
    string = ""
    print("Alternatively, type 'set' to set a search from scratch.\n")
    while command != "exit":
        command = input("Input command.\n")
        if command == "genre":
            command = input("Set genre. Options are 'drama', 'novel', 'short', or 'all'. (All not supported yet).\n")
        elif command == "language":
            language = input("Set language. Options are 'en' or 'fr'.\n")
        elif command == "string":
            string = input("Set search string. Not case sensitive. Regular expressions are not supported yet.\n")
        elif command == "set":
            genre = input("Set genre. Options are 'drama', 'novel', 'short', or 'all'.\n")
            language = input("Set language. Options are 'en' or 'fr'.\n")
            string = input("Set search string. Not case sensitive. Regular expressions are not supported yet.\n")
        elif command == "search":
            print("Searching for " + string + " in genre: " + genre + " and language: " + language)
            results = searchSents(string, language, genre)
            ## writeResults(results)
            return results

def getSpeakers(raw_script):
  play_lines = raw_script.split("\n\n")
  play_lines = [line.strip() for line in play_lines]
  play_dialogue = [line for line in play_lines if ":" in line]
  play_speakers = [line.split(":")[0].strip() for line in play_dialogue]
  play_speakers = [line for line in play_speakers if len(line)<25]
  speaker_dist = FreqDist(play_speakers)
  return speaker_dist         
        
        
## I need to correlate French text with English text. Step one is bringing in the brute-force equivalences, copypasted (probs) from the Google Drive.

## I'll make a dictionary, is what I'll do, for ease of use.

## The dictionary should have one entry for each play.

# e.g. plays["A Piece of Monologue"] = {
#   title_en: "A Piece of Monologue"
#   title_fr: "Solo"
#   file_location_en : "/english/drama/a_piece_of_monologue.txt"
#   file_location_fr : "/french/drama/solo.txt"
#   raw_en : //txt_en.read()
#   raw_fr : //txt_fr.read()
#   }

path_list = getFileNames(directory)
