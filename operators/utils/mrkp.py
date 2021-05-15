import re
from enum import Enum

Prefix = Enum(
    'Prefix', 'TITLE REDDIT QUOTE COLOR STINGER IDLE ANGRY TWITTER PARAGRAPH AUDIO')

prefixes = {("title", "t"): Prefix.TITLE,
            ("reddit", "r"): Prefix.REDDIT,
            ("color", "c"): Prefix.COLOR,
            ("quote", "q"): Prefix.QUOTE,
            ("stinger", "s"): Prefix.STINGER,
            ("idle", "i"): Prefix.IDLE,
            ("angry", "ia"): Prefix.ANGRY,
            ("paragraph", "p"): Prefix.PARAGRAPH,
            ("audio", "a"): Prefix.AUDIO,
            ("twitter", "t"): Prefix.TWITTER}


class mrkpquery():
    def __init__(self, query):
        self.query = query

    def getoptions(self):
        if self.query[0] == ';':
            return False
        if ';' in self.query:
            optionstring = re.compile("^[^;]*;").findall(self.query)[0]
            if not optionstring:
                return False
            return list(optionstring)[:-1]

    def gettype(self):
        if ';' in self.query:
            typequery = re.sub('^[^;]*;', '', self.query)
        else:
            typequery = self.query
        typequery = re.sub('\..*$', '', typequery)
        for i in prefixes.keys():
            if typequery in i:
                return prefixes[i]
        return False

    def getparams(self):
        if not '.' in self.query:
            return [self.query]
        paramquery = re.sub('^[^.]*\.', '', self.query)
        returnlist = []
        returnlist.extend(paramquery.split("::"))
        return returnlist
