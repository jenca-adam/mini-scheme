from .lexer import Token
class nil:
    @classmethod
    def check(cls,a):
        return a==cls
    def __repr__(self):
        return 'nil'
class SchemeType:
    _tokens=NotImplemented
    @classmethod
    def check(cls,block):

        return (type(block)==type(cls) and issubclass(cls,block)) or block.token in cls._tokens
    @classmethod
    def __repr__(cls):
        return f"Type {cls.__name__}" 
class LambdaFunction(SchemeType):
    @classmethod
    def evaluate(cls,content):
        raise NotImplementedError(":(")
    @classmethod
    def check(cls,block):
        return block.token==Token.LIST and block.args and block.args[0].content=="lambda"

class Any:
    @classmethod
    def check(cls,*_):
        return True
class List(SchemeType):
    @classmethod
    def evaluate(cls,content,block):
        from . import call_function,exists,Block
        if content[0].token==Token.ARGUMENT_OR_FUNCTION and exists(content[0].content):
            return call_function(content[0].content,Block(content[1:],Token.LIST))
        return [i.value for i in content]
    _tokens=[Token.LIST]
class Atom(SchemeType):
    _tokens=[Token.ATOM,Token.NUMERICAL_ATOM]
class Boolean(SchemeType):
    _tokens=[Token.TRUE,Token.FALSE]
    @classmethod
    def evaluate(cls,content,_):
        return content=="#t"
class NonNumericAtom(Atom):
    @classmethod
    def evaluate(cls,content,_):
        return content
    _tokens=[Token.ATOM]
class NumericAtom(Atom):
    @classmethod
    def evaluate(cls,content,_):
        return int(content)
    _tokens=[Token.NUMERICAL_ATOM]
class ArgumentOrFunction(SchemeType):
    @classmethod
    def evaluate(cls,content,block):
        return content
    _tokens=[Token.ARGUMENT_OR_FUNCTION]



SCHEME_CHECKABLE_TYPES=[LambdaFunction,List,Boolean,NumericAtom,NonNumericAtom,ArgumentOrFunction]
def find_type(block):
    for s in SCHEME_CHECKABLE_TYPES:
        if s.check(block):
            return s()
    return Any
