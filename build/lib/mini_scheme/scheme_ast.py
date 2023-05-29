from .lexer import tokenize,TokenMatch,Token
from .scheme_types import find_type
from .scheme_function import Namespace
class ASTError(Exception):
    __name__="parse-error"
class Block:
    def __init__(self,args,token,content=None):
        self.args=args
        self.content=content or args
        self.token=token
        self.type=find_type(self,True)
        self.value=None
    def evaluate(self,namespace=None):
        self.value=self.value or self.type.evaluate(self.content,self,namespace)
        return self.value
    def __repr__(self):
        return f'{self.content}'
def _astize(t):
    if isinstance(t,TokenMatch):
        if t.match.group()=="#t":
            t.token=Token.TRUE
        elif t.match.group()=="#f":
            t.token=Token.FALSE
        return Block([],t.token,t.match.group('content'))
    return Block(_ast(t[1:-1]),t[0].token)
def _ast(tokens):
    l=[]
    nl=[]
    p=[]
    level=0
    index=0
    for token in tokens:
        if token.token == Token.LIST:
            level+=1
            p.append(token)
        if level==0:
            l.append(token)
        if level>0:
            nl.append(token)
        if token.token == Token.END:
            if level==0:
                raise ASTError(f"Extra closing parenthese at pos {token.match.start()}")
            level-=1
            if level==0:
                l.append(nl)
                nl=[]
    if level>0:
        raise ASTError(f"Unenclosed parenthese at pos {p[level-1].match.start()}")
    return [_astize(tok) for tok in l]
def ast(raw):
    return _ast(tokenize(raw))
        
