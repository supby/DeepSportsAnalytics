import urllib

f = urllib.urlopen("https://nhlpredictor.herokuapp.com/api/v1.0/updatemodel")
print f.read()