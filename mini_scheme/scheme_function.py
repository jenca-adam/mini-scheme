from .scheme_types import *
class SchemeTypeError(TypeError):pass
FUNCTIONS={}
def scheme_function(name,argtp=None):
    global FUNCTIONS
    def inner(fun):
        argtypes=argtp or [Any for _ in range(fun.__code__.co_argcount)]
        if fun.__code__.co_argcount!=len(argtypes):
            raise TypeError(
                    f"argtypes length does not match function argcount"
                    )
        def decorator(*args):
            if len(args)!=fun.__code__.co_argcount:
                raise SchemeTypeError(
                        f"invalid argcount for {name}, expected {fun.__code__.co_argcount}, got {len(args)}"
                        )
            for index,(argtype,arg) in enumerate(zip(argtypes,args)):
                if not argtype.check(arg):
                    raise SchemeTypeError(
                        f"argtype for argument#{index+1} of {name} not matched, expected {argtype()}"
                        )
            return fun(*(arg.value for arg in args))
        decorator.__name__=decorator.__qualname__=name    
        FUNCTIONS[name]=decorator
        return decorator
    return inner
def exists(function_name):
    return function_name in FUNCTIONS
def call_function(function_name,arguments):
    if not exists(function_name):
        raise SchemeTypeError(
            f"{function_name} is not a function"
            )
    return FUNCTIONS[function_name](*arguments.args)
@scheme_function("+",[NumericAtom,NumericAtom])
def __scheme_plus(n1,n2):
    return n1+n2
@scheme_function("-",[NumericAtom,NumericAtom])
def __scheme_minus(n1,n2):
    if n2>n1:
        return nil()
    return n1-n2
@scheme_function("*",[NumericAtom,NumericAtom])
def __scheme_mult(n1,n2):
    return n1*n2
@scheme_function(">",[NumericAtom,NumericAtom])
def __scheme_gt(n1,n2):
    return n1>n2
@scheme_function("<",[NumericAtom,NumericAtom])
def __scheme_lt(n1,n2):
    return n1<n2
@scheme_function("<=",[NumericAtom,NumericAtom])
def __scheme_leq(n1,n2):
    return n1<=n2
@scheme_function(">",[NumericAtom,NumericAtom])
def __scheme_geq(n1,n2):
    return n1>=n2
@scheme_function("and",[Boolean,Boolean])
def __scheme_and(b1,b2):
    return b1 and b2
@scheme_function("or",[Boolean,Boolean])
def __scheme_or(b1,b2):
    return b1 or b2
@scheme_function("not",[Boolean])
def __scheme_and(b):
    return not b
@scheme_function("/",[NumericAtom,NumericAtom])
def __scheme_div(n1,n2):
    return n1//n2
@scheme_function("add1",[NumericAtom])
def __scheme_add1(n):
    return n+1
@scheme_function("sub1",[NumericAtom])
def __scheme_sub1(n):
    return n-1
@scheme_function("cons",[Any,List])
def __scheme_cons(a,l):
    return [a]+l
@scheme_function("car",[List])
def __scheme_car(l):
    return l[0]
@scheme_function("cdr",[List])
def __scheme_cdr(l):
    return l[1:]

@scheme_function("equal?",[Any,Any])
def __scheme_equal(at1,at2):
    return at1==at2
@scheme_function("null?",[List])
def __scheme_null(l):
    return not l
