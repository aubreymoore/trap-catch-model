# Import the required module for text 
# to speech conversion
from gtts import gTTS

# This module is imported so that we can 
# play the converted audio
import os

# The text that you want to convert to audio
mytext = 'This presentation is about the coconut rhinoceros beetle, Oryctes rhinoceros. I hope you enjoy it.'

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
myobj = gTTS(text=mytext, lang='en', tld='ca')

# Saving the converted audio in a mp3 file named
# welcome 
myobj.save("welcome.mp3")

# Playing the converted file
os.system("ffplay welcome.mp3")