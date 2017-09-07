import unicodedata

# For compatibility between Python2 and Python3
from __future__ import print_function


###############################################################################
# FIND ROOT DIRECTORY
###############################################################################

rootDir = os.path.dirname(os.path.realpath(__file__))


###############################################################################
# READ AND WRITE FILE
###############################################################################

def read_unicode_file(fileName):
    '''Read a unicode file.'''
    # Read all characters
    with open(fileName, encoding='utf-8') as f:
        fileText = f.read()
    # Split lines
    fileLines = fileText.split('\n')
    return fileLines

def write_unicode_file(fileName, fileText):
    '''Write a unicode file.'''
    f = open(fileName, 'w')
    for line in fileText:
        success = f.write(line + '\n')


###############################################################################
# CONVERT LIST OF UNICODE CHARACTER SEQUENCES TO PADDED LIST OF INDICES 
###############################################################################


def unicode_file_to_idx_sequences(fileLines,
                                    pad=True,
                                    padding='post',
                                    maxlen=None):
    '''Convert list of unicode character sequences to padded list of indices.'''
    # Replace with numbers
    # 0 = OOV, 1 = space, 2 = \u0900, ... 101 = stopChar = '|', ... 130 = \u097F
    yIdx = []
    # Convert to numbers (starting at 2, 1 being space)
    for line in fileLines:
        yLine = []
        for char in line:
            if char == ' ':
                yLine.append(1)
            else:
                yLine.append(ord(char) - ord('\u0900') + 2)
        yIdx.append(yLine)
    # Pad sequences
    if pad:
        yIdx = sequence.pad_sequences(yIdx, padding=padding, maxlen=maxlen)
    # Return
    return yIdx


###############################################################################
# SPLIT SHLOKAS INTO SYLLABLE (guru and laghu)
###############################################################################


def shlokas_to_syllables(shlokasLines, ignoreUvacha=False, ignoreExtras=False):
    """Return a list of constituent syllables of shlokas in shlokasLines.
    Input
    shlokasLines : list of strings of shlok lines
    Ouptuts
    shlokasSyllables : list of lists of constituent syllables of all shlokas in input
    allSyllables : list of all syllables ordered as per shlokasLines
    """
    allSyllables = []
    shlokasSyllables = []
    # For each shlok
    for s, shlok in enumerate(shlokasLines):
        # Ignore uvacha lines
        if ignoreUvacha:
            if 'धृतराष्ट्र उवाच' in shlok or 'सञ्जय उवाच' in shlok \
                    or 'अर्जुन उवाच' in shlok or 'श्रीभगवानुवाच' in shlok:
                continue
        # Ignore other lines
        if ignoreExtras:
            if 'ॐ तत्सदिति' in shlok or 'ब्रह्मविद्यायां' in shlok \
                    or 'ऽध्यायः' in shlok:
                continue
        # Find the list of syllables in the shlok
        shlokSyllables = list(split_shlok_into_syllables(shlok))
        # Append list of lists of syllables
        shlokasSyllables.append(shlokSyllables)
        # Append list of all syllables
        for syllable in shlokSyllables:
            allSyllables.append(syllable)
    return shlokasSyllables, allSyllables


def split_shlok_into_syllables(shlok, debug=False):
    """Split the shlok into its constituent syllables.
    Input
    shlok : one shlok line string
    Ouptut
    (yield, not return)
    syllables : a generator of each constituent syllables of shlok
    """
    # Initializations
    # Virama/halant: '्'
    devanagariVirama = u'\N{DEVANAGARI SIGN VIRAMA}'
    # Anusvara: 'ं'
    devanagariAnusvara = u'\N{DEVANAGARI SIGN ANUSVARA}'
    # Visarga: 'ः'
    devanagariVisarga = u'\N{DEVANAGARI SIGN VISARGA}'
    # Avagraha: 'ऽ'
    devanagariAvagraha = u'\N{DEVANAGARI SIGN AVAGRAHA}'
    syllable = u''
    lastCharacter = ''
    lastCategory = ''
    character = ''
    category = ''
    endSyllable = False
    skipCategories = ['Z', 'P']
    skipCharacters = [devanagariAvagraha]
    stopCharacters = [devanagariVirama, devanagariAnusvara, devanagariVisarga]
    # Remove all spaces in shlok
    s = "".join(shlok.split(' '))
    # For each character in string s
    for c, character in enumerate(s):
        if debug:
            print(c)
        # Find category of character
        category = unicodedata.category(character)[0]
        # If character is a space or a punctuation {'।', '॥', '॰'}
        if category in skipCategories:
            # Don't add it to syllable
            continue
        # If character is avagraha {'ऽ'}
        if character in skipCharacters:
            # Don't add it to syllable
            continue
        # If character is not space or punctuation, add it to syllable
        syllable += character
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
        # and next-next character is not virama, end syllable
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
                endSyllable = False
            else:
                endSyllable = True
        # If current is not a virama,
        # 'रेकुरुक्'
        # and next character is not a Mark
        # 'म', 'म'
        # and next-next character is not virama
        # 'ध', 'र्'
        if character != devanagariVirama and nextCategory != 'M' \
                and nextNextCharacter != devanagariVirama:
            endSyllable = True
        # # Yield the syllable
        if endSyllable:
            if syllable:
                if debug:
                    print("...Yield")
                yield syllable
                syllable = u''
            endSyllable = False


###############################################################################
# FIND SHLOAS LENGTHS
###############################################################################


def shlok_lengths(shlokasSyllables):
    """Return a dictionary of lengths of syllables of shlokas in shlokasSyllables.
    Input
    shlokasSyllables : list of lists of syllables in every shloka
    Ouptuts
    shlokLengths : dictionary of shlok_lengths:shlok_numbers
    """
    shlokLengths = {}
    for i, shlokSyllables in enumerate(shlokasSyllables):
            lenSyllables = len(shlokSyllables)
            if lenSyllables not in shlokLengths.keys():
                shlokLengths[lenSyllables] = [i]
            else:
                shlokLengths[lenSyllables].append(i)
    return shlokLengths


###############################################################################
# BINARIZE SHLOKA SYLLABLES (guru=1 and laghu=0)
###############################################################################


def binarize_shlokas_syllables(shlokasSyllables):
    """Change shlok syllables to 0 or 1 for laghu or guru syllables
    Input
    shloksyllables : list of lists of syllables in every shloka
    Ouptut
    shlokSyllables : list of lists of 0 & 1, 0 for Laghu, 1 for Guru
    """
    shlokasBinarySyllables = []
    # For the list of syllables of each shlok
    for s, shlok in enumerate(shlokasSyllables):
        # Make a new array
        shlokasBinarySyllables.append([])
        # For each syllable, find its binary syllable
        for syllable in shlok:
            shlokasBinarySyllables[s].append(binarize_syllable(syllable))
    return shlokasBinarySyllables


def binarize_syllable(syllable):
    """Return 1 or 0 depending on Guru or Laghu syllable.
    Input
    syllable : string of characters denoting a syllable
    Ouptut
    0 for Laghu, 1 for Guru
    """
    guruMarkers = [u'\N{DEVANAGARI LETTER AA}', u'\N{DEVANAGARI LETTER II}',
        u'\N{DEVANAGARI LETTER UU}', u'\N{DEVANAGARI LETTER E}',
        u'\N{DEVANAGARI LETTER AI}', u'\N{DEVANAGARI LETTER O}',
        u'\N{DEVANAGARI LETTER AU}', u'\N{DEVANAGARI VOWEL SIGN AA}',
        u'\N{DEVANAGARI VOWEL SIGN II}', u'\N{DEVANAGARI VOWEL SIGN UU}',
        u'\N{DEVANAGARI VOWEL SIGN E}', u'\N{DEVANAGARI VOWEL SIGN AI}',
        u'\N{DEVANAGARI VOWEL SIGN O}', u'\N{DEVANAGARI VOWEL SIGN AU}',
        u'\N{DEVANAGARI SIGN ANUSVARA}', u'\N{DEVANAGARI SIGN VISARGA}',
        u'\N{DEVANAGARI SIGN VIRAMA}']
    # For each character in the syllable
    for c, character in enumerate(syllable):
        # If character is one of the guru markers
        if character in guruMarkers:
            # If it's not virama, definitely the syllable is Guru
            if character != u'\N{DEVANAGARI SIGN VIRAMA}':
                return 1
            # If it is a virama, the syllable is Guru if
            # the virama is not in the second position
            elif character == u'\N{DEVANAGARI SIGN VIRAMA}' and c != 1:
                return 1
    # Else the syllable is Laghu
    return 0
