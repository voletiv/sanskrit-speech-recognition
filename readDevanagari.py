# READING DEVANAGARI DOCUMENTS
# Read devanagari text - https://www.quora.com/How-can-I-read-Hindi-data-in-Python
# Split into clusters - https://stackoverflow.com/questions/6805311/playing-around-with-devanagari-characters
# https://whatilearned2day.wordpress.com/2015/09/13/understanding-unicode-in-python-and-writing-text-in-devanagri-script/
# Unicode standard specification - http://www.unicode.org/versions/Unicode6.0.0/ch04.pdf
# Devanagari unicode data 0900 to 097F - http://unicode.org/charts/PDF/U0900.pdf
# Telugu unicode data 0C00 to 0C7F - http://unicode.org/charts/PDF/U0C00.pdf

# For compatibility between Python2 and Python3
from __future__ import print_function

import os
import unicodedata

rootDir = '/home/voletiv/GitHubRepos/sanskrit-speech-recognition'

# Devanagari digits
devanagariDigits = ['\u0966', '\u0967', '\u0968', '\u0969',
                    '\u096A', '\u096B', '\u096C', '\u096D', '\u096E', '\u096F']
devanagariDoubleDanda = '\u0965'
devanagariDanda = '\u0964'
hyphen = '\u002D'


###############################################################################
# CLEAN FILE
###############################################################################

# File without extras:
# only with the shlokas (including "__ uvaaca"), shloka numbers
fileName = os.path.join(rootDir, 'docs/BG-e.txt')

# Read all characters
with open(fileName, encoding='utf-8') as f:
    fileText = f.read()

# Split lines
fileLines = fileText.split('\n')

# Remove blank lines
fileLines = list(filter(('').__ne__, fileLines))

# Remove leading spaces, etc.
for i, line in enumerate(fileLines):
    # Remove leading spaces
    fileLines[i] = fileLines[i].lstrip()
    # Remove single dandas at the end of line
    fileLines[i] = fileLines[i].split(devanagariDanda)[0].rstrip()
    # Remove double dandas at the end of line, and the line numbers
    fileLines[i] = fileLines[i].split(devanagariDoubleDanda)[0].rstrip()

# Again remove blank lines
fileLines = list(filter(('').__ne__, fileLines))

y = fileLines

# Add stop character after every line
for i, line in enumerate(y):
    y[i] += devanagariDanda

# Write clean file
f = open(os.path.join(rootDir, 'docs/BG-clean.txt'), 'w')
for line in y:
    success = f.write(line + '\n')

# Find maxlen
maxlen = 0
for line in y:
    if len(line) > maxlen:
        maxlen = len(line)

print("maxlen =", maxlen)


###############################################################################
# READ DOCUMENTS
###############################################################################

# FULL

# File without extras; only with the shlokas, and "__ uvaaca"
fileName = os.path.join(rootDir, 'docs/BG-clean.txt')

# Read all characters
with open(fileName, encoding='utf-8') as f:
    BG = f.read()

# Split lines
BG = BG.split('\n')

# Replace with numbers
# 0 = OOV, 1 = space, 2 = \u0900, ... 101 = stopChar = '|', ... 130 = \u097F
yIdx = []
# Convert to numbers (starting at 1)
for line in BG:
    yLine = []
    for char in line:
        if char == ' ':
            yLine.append(1)
        else:
            yLine.append(ord(char) - ord('\u0900') + 1)
    yIdx.append(yLine)

yIdxPad = sequence.pad_sequences(yIdx, padding='post')


# CHAPTER 01

# File without extras; only with the shlokas, and "__ uvaaca"
fileName = os.path.join(rootDir, 'docs/BG-clean-C01.txt')

# Read all characters
with open(fileName, encoding='utf-8') as f:
    fileText01 = f.read()

# Split lines
fileLines01 = fileText01.split('\n')

# Replace with numbers
# 0 = OOV, 1 = space, 2 = \u0900, ... 101 = stopChar = '|', ... 130 = \u097F
yIdx = []
# Convert to numbers (starting at 1)
for line in y:
    yLine = []
    for char in line:
        if char == ' ':
            yLine.append(1)
        else:
            yLine.append(ord(char) - ord('\u0900') + 1)
    yIdx.append(yLine)

yIdxPad = sequence.pad_sequences(yIdx, padding='post')


###############################################################################
# CHARACTERS ANALYSIS
###############################################################################

# # Find unicode name
# [unicodedata.name(c) for c in fileText[:10]]

# Find the categories spanned by all Devanagari characters
categories = []
chars = []
for c in range(0x7F):
    charNum = 0x0900 + c
    categories.append(unicodedata.category(chr(charNum)))
    if categories[-1] == 'Mc':
        chars.append(chr(charNum))

# Find the unique set of categories
categories = set(categories)

# Find all char names in one category
for c in chars:
    unicodedata.name(c)

# >>> categories
# {'Nd', 'Lo', 'Mn', 'Po', 'Lm', 'Mc'}
# Nd = Number, decimal digit : ०, १, २, ३, ४, ५, ६, ७, ८, ९
# Lo = Letter, other:
# ['ऄ', 'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ऌ', 'ऍ', 'ऎ', 'ए', 'ऐ', 'ऑ', 'ऒ', 'ओ', 'औ',
# 'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण',
# 'त', 'थ', 'द', 'ध', 'न', 'ऩ', 'प', 'फ', 'ब', 'भ', 'म',
# 'य', 'र', 'ऱ', 'ल', 'ळ', 'ऴ', 'व', 'श', 'ष', 'स', 'ह', 'ऽ', 'ॐ',
# 'क़', 'ख़', 'ग़', 'ज़', 'ड़', 'ढ़', 'फ़', 'य़',
# 'ॠ', 'ॡ', 'ॲ', 'ॳ', 'ॴ', 'ॵ', 'ॶ', 'ॷ', 'ॸ', 'ॹ', 'ॺ', 'ॻ', 'ॼ', 'ॽ', 'ॾ']
# Mn = Mark, non-spacing:
# ['ऀ', 'ँ', 'ं', 'ऺ', '़', 'ु', 'ू', 'ृ', 'ॄ', 'ॅ', 'ॆ', 'े', 'ै', '्',
# '॑', '॒', '॓', '॔', 'ॕ', 'ॖ', 'ॗ', 'ॢ', 'ॣ']
# 'DEVANAGARI SIGN INVERTED CANDRABINDU'
# 'DEVANAGARI SIGN CANDRABINDU'
# 'DEVANAGARI SIGN ANUSVARA'
# 'DEVANAGARI VOWEL SIGN OE'
# 'DEVANAGARI SIGN NUKTA'
# 'DEVANAGARI VOWEL SIGN U'
# 'DEVANAGARI VOWEL SIGN UU'
# 'DEVANAGARI VOWEL SIGN VOCALIC R'
# 'DEVANAGARI VOWEL SIGN VOCALIC RR'
# 'DEVANAGARI VOWEL SIGN CANDRA E'
# 'DEVANAGARI VOWEL SIGN SHORT E'
# 'DEVANAGARI VOWEL SIGN E'
# 'DEVANAGARI VOWEL SIGN AI'
# 'DEVANAGARI SIGN VIRAMA'
# 'DEVANAGARI STRESS SIGN UDATTA'
# 'DEVANAGARI STRESS SIGN ANUDATTA'
# 'DEVANAGARI GRAVE ACCENT'
# 'DEVANAGARI ACUTE ACCENT'
# 'DEVANAGARI VOWEL SIGN CANDRA LONG E'
# 'DEVANAGARI VOWEL SIGN UE'
# 'DEVANAGARI VOWEL SIGN UUE'
# 'DEVANAGARI VOWEL SIGN VOCALIC L'
# 'DEVANAGARI VOWEL SIGN VOCALIC LL'
# Po = punctuation, other:
# 'DEVANAGARI DANDA'
# 'DEVANAGARI DOUBLE DANDA'
# 'DEVANAGARI ABBREVIATION SIGN'
# Lm = Letter, modifier: 'DEVANAGARI SIGN HIGH SPACING DOT' = 'ॱ'
# Mc = Mark, space combining:
# 'DEVANAGARI SIGN VISARGA': 'ः'
# 'DEVANAGARI VOWEL SIGN OOE': 'ऻ'
# 'DEVANAGARI VOWEL SIGN AA': 'ा'
# 'DEVANAGARI VOWEL SIGN I': 'ि'
# 'DEVANAGARI VOWEL SIGN II': 'ी'
# 'DEVANAGARI VOWEL SIGN CANDRA O': 'ॉ'
# 'DEVANAGARI VOWEL SIGN SHORT O': ॊ'
# 'DEVANAGARI VOWEL SIGN O': 'ो'
# 'DEVANAGARI VOWEL SIGN AU': 'ौ'
# 'DEVANAGARI VOWEL SIGN PRISHTHAMATRA E': 'ॎ'
# 'DEVANAGARI VOWEL SIGN AW': 'ॏ'

###############################################################################
# SPLIT SHLOKAS INTO SOUNDS
###############################################################################


def split_into_sounds(s, debug=False):
    """Generate the sound clusters for the string s."""
    # Initializations
    # Virama/halant: '्'
    devanagariVirama = u'\N{DEVANAGARI SIGN VIRAMA}'
    # Anusvara: 'ं'
    devanagariAnusvara = u'\N{DEVANAGARI SIGN ANUSVARA}'
    # Visarga: 'ः'
    devanagariVisarga = u'\N{DEVANAGARI SIGN VISARGA}'
    # Avagraha: 'ऽ'
    devanagariAvagraha = u'\N{DEVANAGARI SIGN AVAGRAHA}'
    sound = u''
    lastCharacter = ''
    lastCategory = ''
    character = ''
    category = ''
    endSound = False
    skipCategories = ['Z', 'P']
    skipCharacters = [devanagariAvagraha]
    stopCharacters = [devanagariVirama, devanagariAnusvara, devanagariVisarga]
    # For each character in string s
    for c, character in enumerate(s):
        if debug:
            print(c)
        # Find category of character
        category = unicodedata.category(character)[0]
        # If character is a space or a punctuation {'।', '॥', '॰'}
        if category in skipCategories:
            # Don't add it to sound
            continue
        # If character is avagraha {'ऽ'}
        if character in skipCharacters:
            # Don't add it to sound
            continue
        # If character is not space or punctuation, add it to sound
        sound += character
        # Find out the last-last-last-last, last-last, next
        # and next-next characters and category:
        # 1) Last-last-last-last character
        try:
            lastLastLastLastCharacter = s[c - 4]
            lastLastLastLastCategory = unicodedata.category(
                lastLastLastLastCharacter)[0]
        except IndexError:
            lastLastLastLastCharacter = ' '
            lastLastLastLastCategory = unicodedata.category(
                lastLastLastLastCharacter)[0]
        # 2) Last-last character
        try:
            lastLastCharacter = s[c - 2]
            lastLastCategory = unicodedata.category(lastLastCharacter)[0]
        except IndexError:
            lastLastCharacter = ' '
            lastLastCategory = unicodedata.category(lastLastCharacter)[0]
        # 3) Next character
        try:
            nextCharacter = s[c + 1]
            nextCategory = unicodedata.category(nextCharacter)[0]
            # If next character is space or punctuation, make it space so no
            # further decision is dependent on it
            if nextCategory in skipCategories:
                nextCharacter = ' '
                nextCategory = unicodedata.category(nextCharacter)[0]
                if debug:
                    print("nextCategory skip, new nextCharacter",
                          unicodedata.name(nextCharacter))
            # Else if next character is avagraha, ignore it and consider the
            # further next character
            elif nextCharacter in skipCharacters:
                nextCharacter = s[c + 2]
                nextCategory = unicodedata.category(nextCharacter)[0]
                if debug:
                    print("nextCharacter skip, new nextCharacter",
                          unicodedata.name(nextCharacter))
        except IndexError:
            nextCharacter = ' '
            nextCategory = unicodedata.category(nextCharacter)[0]
        # 4) Next-next character
        try:
            nextNextCharacter = s[c + 2]
            nextNextCategory = unicodedata.category(nextNextCharacter)[0]
            # If next or next-next character is space or punctuation, make it
            # space so no further decision is dependent on it
            if unicodedata.category(s[c + 1])[0] in skipCategories \
                    or nextNextCategory in skipCategories:
                nextNextCharacter = ' '
                nextNextCategory = unicodedata.category(nextNextCharacter)[0]
                if debug:
                    print("nextNextCategory skip, new nextNextCharacter",
                          unicodedata.name(nextNextCharacter))
            # Else if next or next-next character is avagraha, ignore it and
            # consider the further next character
            elif s[c + 1] in skipCharacters \
                    or nextNextCharacter in skipCharacters:
                nextNextCharacter = s[c + 3]
                nextNextCategory = unicodedata.category(nextNextCharacter)[0]
                if debug:
                    print("nextNextCharacter skip, new nextNextCharacter",
                          unicodedata.name(nextNextCharacter))
        except IndexError:
            nextNextCharacter = ' '
            nextNextCategory = unicodedata.category(nextNextCharacter)[0]
        # Debug print
        if debug:
            print(character, category, character == devanagariVirama,
                nextNextCharacter != devanagariVirama,
                lastLastCategory in skipCategories,
                (lastLastCharacter ==devanagariVirama and \
                    lastLastLastLastCategory in skipCategories),
                character != devanagariVirama, nextCategory != 'M',
                nextNextCharacter != devanagariVirama)
        # General: end at virama/halant
        # eg. धर्
        # and next-next character is not virama, end sound
        # eg. 'दृष्', 'ट्'
        if character == devanagariVirama \
                and nextNextCharacter != devanagariVirama:
            # But not if the last-last character was space or punctuation
            # eg. ' ', व्', 'यू'
            # or if last-last was virama and the last-last-last-last character
            # eg. ' ', स्त्', 'री', 'षु'
            # was of skipCategory
            if lastLastCategory in skipCategories \
                or (lastLastCharacter == devanagariVirama \
                    and lastLastLastLastCategory in skipCategories):
                # if lastLastCategory in skipCategories:
                endSound = False
            else:
                endSound = True
        # If current is not a virama,
        # 'रेकुरुक्'
        # and next character is not a Mark
        # 'म', 'म'
        # and next-next character is not virama
        # 'ध', 'र्'
        if character != devanagariVirama and nextCategory != 'M' \
                and nextNextCharacter != devanagariVirama:
            endSound = True
        # # Yield the sound
        if endSound:
            if sound:
                if debug:
                    print("...Yield")
                yield sound
                sound = u''
            endSound = False

# Make sounds length list
shlokLengths = {}
for i in range(len(y)):
    if 'धृतराष्ट्र उवाच' not in y[i] \
            and 'सञ्जय उवाच' not in y[i] and 'अर्जुन उवाच' not in y[i] \
            and 'श्रीभगवानुवाच' not in y[i] and 'ॐ तत्सदिति' not in y[i] \
            and 'ब्रह्मविद्यायां' not in y[i] and 'ऽध्यायः।' not in y[i]:
        lenSounds = len(list(split_into_sounds(y[i])))
        if lenSounds not in shlokLengths.keys():
            shlokLengths[lenSounds] = [i]
        else:
            shlokLengths[lenSounds].append(i)

# Save shlokLengths and indices
np.save(os.path.join(rootDir, "docs/shlokLengths.npy"), shlokLengths)

# Read shlokLengths
shlokLengths = np.load(os.path.join(rootDir, "docs/shlokLengths.npy")).item()

# Find number of shlokas of each length
for key in sorted(shlokLengths.keys()):
    print(key, len(shlokLengths[key]))

# 11 215
# 12 5 : [118, 119, 177, 710, 1303]
# 16 1291
# 17 1 : मदनुग्रहाय परमं गुह्यमध्यात्मसंज्ञितम् ॥ ११-१॥(1)


# TEST SPLIT_INTO_SOUNDS

# mySounds = list(split_into_sounds(y[6], debug=True))
# print(len(mySounds), mySounds)

# Incomplete!!!
specialShlokas11 = [114, 115, 116, 117, #॥ २-५॥
                    120, 121,           #॥ २-६॥
                    122, 123, 124, 125, #॥ २-७॥
                    126, 127, 128, 129, #॥ २-८॥
                    154, 155, 156, 157, #॥ २-२०॥
                    160, 161, 162, 163, #॥ २-२२॥
                    176, 178, 179,      #॥ २-२९॥
                    262, 263, 264, 265, #॥ २-७०॥
                    703, 704, 705, 706, #॥ ८-९॥
                    707, 708, 709,      #॥ ८-१०॥
                    711, 712, 713, 714, #॥ ८-११॥
                    747, 748, 749, 750, #॥ ८-२८॥
                    793, 794, 795, 796, #॥ ९-२०॥
                    797, 798, 799, 800, #॥ ९-२१॥
                    952, 953, 954, 955, #॥ ११-१५॥
                    956, 957, 958, 959 #॥ ११-१६॥
                    #॥ ११-१८॥
                    ]
specialShlokas12 = [118, 119, 177, 710]
specialShlokas17 = [
                    921                 #॥ ११-१॥(1)
                    ]
# Test split_sound
for i in range(len(y)):
    mySounds = list(split_into_sounds(y[i]))
    if len(mySounds) != 16 and 'धृतराष्ट्र उवाच' not in y[i] \
            and 'सञ्जय उवाच' not in y[i] and 'अर्जुन उवाच' not in y[i] \
            and 'श्रीभगवानुवाच' not in y[i] and 'ॐ तत्सदिति' not in y[i] \
            and 'ब्रह्मविद्यायां' not in y[i] and 'ऽध्यायः।' not in y[i] \
            and i not in specialShlokas11 and i not in specialShlokas12 \
            and i not in specialShlokas17:
        print(i)
        print(y[i])
        print(len(mySounds), mySounds)
        break


###############################################################################
# SPLIT SHLOKAS INTO SOUNDS
###############################################################################

# # Combine two padas of a shlok into one line in the file
# # TODO: not perfect
# y = []
# first = True
# for line in fileLines01:
#     if 'धृतराष्ट्र उवाच' in line or 'सञ्जय उवाच' in line \
#             or 'अर्जुन उवाच' in line or 'श्रीभगवानुवाच' in line:
#         if first is False:
#             # Remove space at the end
#             y[-1] = y[-1][:-1]
#         y.append(line)
#         uvaaca = True
#     else:
#         if first:
#             # If line has a hyphen at the end, don't add space
#             if line[-1] == hyphen:
#                 y.append(line.split(hyphen)[0])
#             else:
#                 y.append(line + ' ')
#             first = False
#         else:
#             # If previous line was "_ uvaacha"
#             if uvaaca is True:
#                 # Even if this is the second paada, add it to the next line
#                 y.append(line)
#             else:
#                 y[-1] += line
#             first = True
#             uvaaca = False

# # Write clean file
# f = open('BG_clean_C01_32.txt', 'w')
# for line in y:
#     success = f.write(line+'\n')
