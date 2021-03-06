# Copyright (C) 2012  Lukas Rist
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import re
import math
import sys
from brushes import php_brush, perl_brush


class LangClassifier():
    """
    Inspired by http://stackoverflow.com/questions/475033/detecting-programming-language-from-a-snippet
    """
    def __init__(self):
        self.data = {}
        self.totals = {}
        self.train(open("lang/code.pl").read(), "perl")
        self.train(open("lang/code.php").read(), "php")

    def words(self, code):
        # Split on everything else than a-z and discard empty parts
        #word_list = re.split("[^a-z]", code)
        word_list = code.split()
        return filter(bool, word_list)

    def train(self, code, lang):
        # Trains the classifier
        self.data[lang] = {}
        for word in self.words(code):
            if word in self.data[lang]:
                self.data[lang][word] += 1
            else:
                self.data[lang][word] = 1
            if word in self.totals:
                self.totals[word] += 1
            else:
                self.totals[word] = 1

    def prob(self, words, lang):
        # Calculates the probability
        res = 0.0
        for word in words:
            try:
                res = res + math.log(self.totals[word] / self.data[lang][word])
            except(KeyError):
                continue
        return res

    def classify(self, code):
        # Classifies the input code
        lang_prob = {}
        words = self.words(code)
        for lang in self.data.iterkeys():
            prob = self.prob(words, lang)
            lang_prob[prob] = lang
        #print "Calculated probabilities (smaller == more likely):", lang_prob
        return "Input file is most likely: " + lang_prob[min(lang_prob.keys())]

# Test the shit
#lang_classifier = LangClassifier()
# Minimal train
#lang_classifier.train(open("code.pl").read(), "perl")
#lang_classifier.train(open("code.php").read(), "php")
#lang_classifier.classify(open(sys.argv[1]).read())
