import re
from enum import Enum

from operators.utils.strips import gettemplate

# various markp utilities

# provide api to parse markup string
class mrkpquery():
    def __init__(self, query):
        if not query[0] == ';':
            self.valid = False
        else:
            self.valid = True
            self.query = query

        self.name = query.split(';')[1]
        if gettemplate(self.name) is None:
            self.valid = False
            return
        self.arguments = query.split(';')[2:]

