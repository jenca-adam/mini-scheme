from .lexer import Token
from .scheme_pair import Pair,EmptyList
class SchemeNameError(Exception):
    __name__="name-error"
class nil:
    @classmethod
    def check(cls,a):
        return a==cls or a.__class__==cls
    def __repr__(self):
        return 'nil'
class SchemeType:
    _tokens=NotImplemented
    _pythontypes=NotImplemented
    @classmethod
    def check(cls,block,force_token=False):
        if getattr(block,'token',None)==Token.ARGUMENT_OR_FUNCTION:
            return block.token in cls._tokens
        if (type(block)==type(cls)):
            return True
        return (block.token in cls._tokens) if force_token else (type(getattr(block,'value',block)) in cls._pythontypes)
    @classmethod
    def __repr__(cls):
        return f"Type {cls.__name__}" 
class Unknown(SchemeType):
    _tokens=[]
    _pythontypes=[]

class Any:
    @classmethod
    def check(cls,*_):
        return True
class List(SchemeType):
    @classmethod
    def evaluate(cls,content,block,namespace=None):
        from . import call_function,exists,Block
        if content and callable(content[0].evaluate(namespace)): 
            return call_function(content[0].evaluate(namespace),Block(content[1:],Token.LIST),namespace)
        return Pair.from_list([i.evaluate(namespace) for i in content])
    _tokens=[Token.LIST]
    _pythontypes=[Pair,EmptyList,list]
class Atom(SchemeType):
    _tokens=[Token.ATOM,Token.NUMERICAL_ATOM]
    _pythontypes=[str,int]
class Boolean(SchemeType):
    _tokens=[Token.TRUE,Token.FALSE]
    _pythontypes=[bool]
    @classmethod
    def evaluate(cls,content,*_):
        return content=="#t"
class NonNumericAtom(Atom):
    @classmethod
    def evaluate(cls,content,*_):
        return content
    _tokens=[Token.ATOM]
    _pythontypes=[str]
class NumericAtom(Atom):
    @classmethod
    def evaluate(cls,content,*_):
        return int(content)
    _tokens=[Token.NUMERICAL_ATOM]
    _pythontypes=[int]
class ArgumentOrFunction(SchemeType):
    @classmethod
    def evaluate(cls,content,block,namespace=None):
        from . import Namespace
        namespace=namespace or Namespace()
        if content in namespace:
            return namespace[content]
        raise SchemeNameError(
                            f"name {content!r} is not defined in the current namespace"
                            )
    _tokens=[Token.ARGUMENT_OR_FUNCTION]
    _pythontypes=[]

SCHEME_CHECKABLE_TYPES=[List,Boolean,NumericAtom,NonNumericAtom,ArgumentOrFunction]
def find_type_by_value(val):
    for s in SCHEME_CHECKABLE_TYPES:
        if type(val) in s._pythontypes:
            return s()
    return Unknown()
def find_type(block,force_token=False):
    for s in SCHEME_CHECKABLE_TYPES:
        if s.check(block,force_token):
            return s()
    return Unknown()
