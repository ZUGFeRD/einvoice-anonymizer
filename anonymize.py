#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'andreas starke'
# date: 09.06.2024

import logging
import sys
import codecs
from lxml import etree
import string
import random
import datetime
import time
# ===============================================================================
# logging
# ===============================================================================
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handlers and set level to INFO
ch_stdout = logging.StreamHandler(sys.stdout)
ch_stdout.setLevel(logging.DEBUG)
ch_stderr = logging.StreamHandler(sys.stderr)
ch_stderr.setLevel(logging.ERROR)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch_stdout.setFormatter(formatter)
ch_stderr.setFormatter(formatter)
# add chs to logger
logger.addHandler(ch_stdout)
logger.addHandler(ch_stderr)

DATE_FORMATS = [
    "%d.%m.%Y",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%d %m %Y",
    "%Y.%m.%d",
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y %m %d",
    "%d.%m",
    "%d/%m",
    "%d %m"
]

VOWELS_LOWERCASE = ["a", "e", "i", "o", "u", "ä", "ü", "ö"]
VOWELS_UPPERCASE = ["A", "E", "I", "O", "U", "Ä", "Ü", "Ö"]
CONSONANTS_LOWERCASE = list(set(string.ascii_lowercase).difference(VOWELS_LOWERCASE)) + ["ß"]
CONSONANTS_UPPERCASE = list(set(string.ascii_uppercase).difference(VOWELS_UPPERCASE))
LETTERS_LOWERCASE = string.ascii_lowercase + "äüöß"
LETTERS_UPPERCASE = string.ascii_uppercase + "ÄÜÖ"

    
def shuffle(original_value):
    """shuffles the characters in x to random characters
    
    @param original_value: string to be randomized
    """
    def randomize(x):
        """transforms a single chr or digit into a random one
        
        @param x: a single character
        @return: a single character
        """
        if x in LETTERS_LOWERCASE:
            if x in VOWELS_LOWERCASE:
                return random.choice(VOWELS_LOWERCASE)
            else:
                return random.choice(CONSONANTS_LOWERCASE)
        elif x in LETTERS_UPPERCASE:
            if x in VOWELS_UPPERCASE:
                return random.choice(VOWELS_UPPERCASE)
            else:
                return random.choice(CONSONANTS_UPPERCASE)
        elif x in string.digits:
            return random.choice(string.digits)
        else:
            return x
        
    def randomize_word(x):
        """shuffles a word into a random word
        
        @param x: a single word
        @return: a random word of the "same" type
        """
        for this_format in DATE_FORMATS:
            try:
                datetime.datetime.strptime(this_word, this_format)
                d = random.randint(1, int(time.time()))
                return datetime.datetime.fromtimestamp(d).strftime(this_format)
            except Exception:
                pass
        new_value = ""
        for this_character in x:
            new_value += randomize(this_character)
        return new_value
    
    if original_value is None:
        return None
    new_value = []
    for this_word in original_value.split(" "):
        new_value.append(randomize_word(this_word))
    return " ".join(new_value)


def main(xml_file, xpaths_file, mode="shuffle"):
    """transforms values behind the xpaths
    
    @param xpaths_file: filename containing newline separated xpaths
    @param mode: how to transform
    """
    all_paths = codecs.open(xpaths_file, "r", "utf-8").readlines()
    xml_struct = etree.parse(xml_file)
    nsmap = xml_struct.getroot().nsmap.copy()
    for this_path in all_paths:
        this_path = this_path.rstrip("\n")
        if this_path == "":
            continue
        try:
            to_anonymize = xml_struct.xpath(this_path, namespaces=nsmap)
        except Exception:
            pass
        for this_element in to_anonymize:
            original_value = this_element.text
            if mode == "shuffle":
                new_value = shuffle(original_value)
            this_element.text = new_value
            logger.info("{} - {}".format(original_value, new_value))
    
    outFile = open(xml_file, "wb")
    # outFile.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n')
    # Metadaten-XML-Datei schreiben
    xml_struct.write(outFile, pretty_print=True, xml_declaration=True, encoding="utf-8")
    outFile.close()

                
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
