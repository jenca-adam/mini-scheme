import enum
import regex as re

class Token(enum.Enum):
    NUMERICAL_ATOM = re.compile(r"([\s(']|^)(?P<content>-?\d+)([\s)]|$)")
    ATOM = re.compile(r"(?P<content>[^'()\s]+)")
    LIST = re.compile(r"(?P<content>\()")
    LITERAL = re.compile(r"(?P<content>')")
    END=re.compile(r"(?P<content>\))")
    
    TRUE="TRUE"
    FALSE="FALSE"
class TokenMatch:
    def __init__(self,token,match,literal):
        self.token=token
        self.match=match
        self.literal=literal
    def __repr__(self):
        return f'<TokenMatch { "literal" if self.literal else "" } {self.token} @ {self.match},matching {self.match.group("content")!r}>'

def reverse_search(matches,index):
    if matches[index].token==Token.LITERAL:
        return True
    if matches[index-1].token==Token.LITERAL:
        return True
    return False
def fix_literal(fat,matches,index):
    return TokenMatch(fat.token,fat.match,reverse_search(matches,index))
def get_match_start(match):
    return match.match.start()+match.match.group().index(match.match.group('content')[0])
def tokenize(t):
    matches=[]
    for token in Token:
        if isinstance(token.value,re.Pattern):
            finditer = token.value.finditer(t,overlapped=True ) if token==Token.NUMERICAL_ATOM else token.value.finditer(t)
            for match in finditer:
                matches.append(TokenMatch(token,match,False))
    matches.sort(key = lambda q: get_match_start(q))
    return [fix_literal(x,matches,i) for i,x in enumerate(matches) if x.token!=Token.LITERAL and not (x.token!=Token.NUMERICAL_ATOM and x.match.group("content").replace("-",'').isnumeric())]
