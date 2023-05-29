from .scheme_types import *
from .scheme_pair import Pair,EmptyList
from .scheme_repr import get_repr
import typing
import sys
import inspect
sys.setrecursionlimit(10000000)

class SchemeTypeError(TypeError):
    __name__="type-error"
class SchemeBuiltinError(Exception):
    __name__="builtin-error"
GLOBAL_NAMESPACE={}
BUILTINS={}
class Namespace:
    def __init__(self,initial={}):
        self.contents={}
        self.contents.update(GLOBAL_NAMESPACE)
        self.contents.update(initial)
    def __getitem__(self,item):
        return self.contents.get(item,nil())
    def __contains__(self,item):
        return item in self.contents
    def __setitem__(self,item,value):
        self.contents[item]=value
    def updated(self,d):
        return Namespace({**self.contents,**d})
    @property
    def extra(self):
        return {k:v for (k,v) in self.contents.items() if k not in GLOBAL_NAMESPACE}
    def __repr__(self):
        return f"<Namespace with extra vars {self.extra}>"
def is_special_form(signature):
    return 2 in [i.kind.value for i in signature.parameters.values()]
def _check_argtype(t,arg):
    if isinstance(arg,tuple):
        return all(t.check(i) for i in arg)
    return t.check(arg)
def check_argtypes(function,args,name):
    argtypes=typing.get_type_hints(function)
    signature=inspect.signature(function)
    if is_special_form(signature):
        return True
    try:
        bound=signature.bind(*args)
    except:
        argcount=function.__code__.co_argcount
        raise SchemeTypeError(
                        f"invalid argcount for {name}, expected {argcount}, got {len(args)}"
                        )
    for argn in bound.arguments:
        if argn not in argtypes:
            argtypes[argn]=Any
    for index,argname in enumerate(bound.arguments):
        arg=bound.arguments[argname]
        check=argtypes[argname]
        if not _check_argtype(check,arg):
                    raise SchemeTypeError(
                        f"argtype for argument#{index+1}({argname}) of {name} not matched, expected {check()}, got {getattr(arg,'type',find_type_by_value(arg))}"
                        )

        

def scheme_def(name):
    global GLOBAL_NAMESPACE
    def inner(fun):
        def decorator(*oargs,namespace=None):
            args=[arg.evaluate(namespace) for arg in oargs]
            check_argtypes(fun,args,name)
            return fun(*args)
        decorator.__name__=decorator.__qualname__=name    
        GLOBAL_NAMESPACE[name]=decorator
        BUILTINS[name]=decorator
        return fun
    return inner
def scheme_spdef(name):
    global GLOBAL_NAMESPACE
    def inner(fun):
        def decorator(*args,**kwargs):
            return fun(*args,**kwargs)
        decorator.__name__=decorator.__qualname__=name    
        GLOBAL_NAMESPACE[name]=decorator
        BUILTINS[name]=decorator
        return fun
    return inner

def exists(function_name,namespace=None):
    namespace=namespace or Namespace()
    return callable(namespace[function_name])
def call_function(function,arguments,namespace=None):
    if isinstance(function,str): # by name

        namespace=namespace or Namespace()
        if not exists(function,namespace):
            raise SchemeTypeError(
                f"{function_name} is not a function"
                )
        return namespace[function](*arguments.args,namespace=namespace)
    return function(*arguments.args,namespace=namespace)


@scheme_def("+")
def _scheme_plus(n1:NumericAtom,n2:NumericAtom):
    return n1+n2

@scheme_def("-")
def _scheme_minus(n1:NumericAtom,n2:NumericAtom):
    return n1-n2

@scheme_def("*")
def _scheme_mult(n1:NumericAtom,n2:NumericAtom):
    return n1*n2

@scheme_def(">")
def _scheme_gt(n1:NumericAtom,n2:NumericAtom):
    return n1>n2

@scheme_def("<")
def _scheme_lt(n1:NumericAtom,n2:NumericAtom):
    return n1<n2

@scheme_def("<=")
def _scheme_leq(n1:NumericAtom,n2:NumericAtom):
    return n1<=n2

@scheme_def(">=")
def _scheme_geq(n1:NumericAtom,n2:NumericAtom):
    return n1>=n2

@scheme_def("and")
def _scheme_and(b1:Boolean,b2:Boolean):
    return b1 and b2

@scheme_def("or")
def _scheme_or(b1:Boolean,b2:Boolean):
    return b1 or b2

@scheme_def("not")
def _scheme_not(b:Boolean):
    return not b
@scheme_def("display")
def _scheme_display(t:Any):
    print(get_repr(t),end="")
    return nil()

@scheme_def("newline")
def _scheme_newline():
    print()
    return nil()

@scheme_def("/")
def _scheme_div(n1:NumericAtom,n2:NumericAtom):
    return n1//n2
@scheme_def("zero?")
def _scheme_zero(n:NumericAtom):
    return n==0
@scheme_def("add1",)
def _scheme_add1(n:NumericAtom):
    return n+1

@scheme_def("sub1",)
def _scheme_sub1(n:NumericAtom):
    return n-1

@scheme_def("cons")
def _scheme_cons(a,l):
    return Pair(a,l)

@scheme_def("car")
def _scheme_car(l:List):
    return l.car

@scheme_def("cdr")
def _scheme_cdr(l):
    return l.cdr

@scheme_def("equal?")
def _scheme_equal(at1,at2):
    return at1==at2

@scheme_def("null?")
def _scheme_null(l:List):
    return isinstance(l,EmptyList) or not l


@scheme_spdef("read")
def _scheme_read(namespace=None):
    from .scheme_ast import ast
    inp=input()
    return ast(inp)[0].evaluate(namespace)

@scheme_spdef("cond")
def _scheme_cond(*qs:List,namespace=None):
    for q in qs:
        if q.args[0].evaluate(namespace):
            return q.args[1].evaluate(namespace)
    return nil()
@scheme_spdef("define")
def _scheme_define(*args,namespace=None):
    # THIS IS ATROCIOUS!!!!!!
    # Fix. somehow ?!
    name,val=args
    if name.content in BUILTINS:
        raise SchemeBuiltinError(
            f"refusing to rename built-in function {name.content}"
            )
    global GLOBAL_NAMESPACE
    GLOBAL_NAMESPACE[name.content]=val.evaluate()
    return nil()
@scheme_spdef("lambda")
def _scheme_lambda(*defn,namespace=None):
    ns=namespace or Namespace()
    args=[i.content for i in defn[0].args]
    def decorated(*a,namespace=None):
        got=(arg.evaluate(namespace) for arg in a)
        namespace=(namespace or Namespace()).updated(ns.extra)
        if len(a)!=len(args):
            raise SchemeTypeError(
                    "invalid argcount for lambda")
        newns=namespace.updated({k:v for k,v in zip(args,got)})
        for arg in defn[1:-1]:
            arg.evaluate(newns)
        return defn[-1].evaluate(newns)
        
    return decorated

@scheme_spdef("begin")
def _scheme_begin(*lst,namespace=None):
    for i in lst:
        i.evaluate(namespace)
    return i.evaluate(namespace)
@scheme_spdef("let")
def _scheme_let(bindings,expr,namespace=None):
     namespace=namespace or Namespace()
     new_namespace=namespace.updated({binding.args[0].content:binding.args[1].evaluate(namespace) for binding in bindings.args})
     return expr.evaluate(new_namespace)
