import enum
import re

class Token(enum.Enum):
    NUMERICAL_ATOM = re.compile(r"[\s(]?(\d+)[\s)]?")
    ARGUMENT_OR_FUNCTION_OR_ATOM = re.compile(r"([^'()\s\d]+)")
    LIST = re.compile(r"(\()")
    LITERAL = re.compile(r"(')")
    END=re.compile(r"(\))")
    
    TRUE="TRUE"
    FALSE="FALSE"
    ATOM="ATOM"
    ARGUMENT_OR_FUNCTION="ARGUMENT_OR_FUNCTION"
class TokenMatch:
    def __init__(self,token,match):
        self.token=token
        self.match=match
    def __repr__(self):
        return f'<TokenMatch {self.token} @ {self.match},matching {self.match.groups()[0]!r}>'

def reverse_search(matches,index):
    if matches[index-1].token==Token.LITERAL:
        return Token.ATOM
    level=1
    while index>0:
        index-=1
        if matches[index].token==Token.LIST:
            level-=1
        elif matches[index].token==Token.END:
            level+=1
        if level==0 and matches[index].token==Token.LITERAL:
            return Token.ATOM
    return Token.ARGUMENT_OR_FUNCTION
def variable_or_atom(fat,matches,index):
    if fat.token==Token.ARGUMENT_OR_FUNCTION_OR_ATOM:
        return TokenMatch(reverse_search(matches,index),fat.match)
    return fat
def get_match_start(match):
    return match.match.start()+match.match.group().index(match.match.groups()[0])
def tokenize(t):
    matches=[]
    for token in Token:
        if isinstance(token.value,re.Pattern):
            for match in token.value.finditer(t):
                matches.append(TokenMatch(token,match))
    matches.sort(key = lambda q: get_match_start(q))
    return [variable_or_atom(x,matches,i) for i,x in enumerate(matches) if x.token!=Token.LITERAL]
