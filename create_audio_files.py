from icecream import ic
import re
from gtts import gTTS
import os

PRESENTATION_PATH = "/home/aubrey/Desktop/trap-catch-model/reveal.js/plumes_audio.html"
AUDIO_DIR = "/home/aubrey/Desktop/trap-catch-model/audio"

os.makedirs(AUDIO_DIR, exist_ok=True)

with open(PRESENTATION_PATH) as f:
    html = f.read()

regex = r"<section data-audio-src=\"(.*)\">"
matches = re.finditer(regex, html, re.MULTILINE)
ic(matches)
audiolist = []
for match in matches:
    audiolist.append(match.group(1))
ic(audiolist)

regex = r"<aside class=\"notes\">"
matches = re.finditer(regex, html, re.MULTILINE)
startlist = []
for match in matches:
    startlist.append(match.end(0))
ic(startlist)
assert len(audiolist)==len(startlist)

regex = r"</aside>"
matches = re.finditer(regex, html, re.MULTILINE)
endlist = []
for match in matches:
    endlist.append(match.start(0))
ic(endlist)

assert len(startlist)==len(endlist)

stringlist = []
for i in range(len(startlist)):
    s = html[startlist[i] : endlist[i]].strip()
    s =' '.join(s.split())
    s = s.replace("'", "", -1)
    ic(i, s)
    stringlist.append(s)

for i, audio in enumerate(audiolist):
    s = stringlist[i]
    myobj = gTTS(text=s, lang='en', tld='ca')
    filepath = f'{AUDIO_DIR}/{audiolist[i]}'
    myobj.save(filepath)

print('FINISHED')




# # The text that you want to convert to audio
# mytext = 'This presentation is about the coconut rhinoceros beetle, Oryctes rhinoceros. I hope you enjoy it.'

# # Language in which you want to convert
# language = 'en'

# # Passing the text and language to the engine, 
# # here we have marked slow=False. Which tells 
# # the module that the converted audio should 
# # have a high speed
# myobj = gTTS(text=mytext, lang='en', tld='ca')

# # Saving the converted audio in a mp3 file named
# # welcome 
# myobj.save("welcome.mp3")

# # Playing the converted file
# os.system("ffplay -autoexit welcome.mp3")







