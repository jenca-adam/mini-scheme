from .scheme_ast import ast
from .scheme_types import nil
from .scheme_repr import get_repr
from .scheme_function import GLOBAL_NAMESPACE
import readline
import traceback
from .__meta__ import __version__
class Completer(object):

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:
            if text:                
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:
                self.matches = self.options[:]

        try: 
            return self.matches[state]
        except IndexError:
            return None
class RunnerError(Exception):
    __name__='syntax-error'
def run_str(code,enable_more=False):
    result=[it.evaluate() for it in ast(code)]
    if enable_more:
        return result[-1]
    if len(result)==1:
        return result[0]
    elif len(result)==0:
        return nil()
    raise RunnerError("can eval only one expression")
def cmdline():
    readline.parse_and_bind('tab:complete')
    readline.set_completer_delims(' ()\t\n')
    print(f"""mini-scheme version {__version__}, Copyright (C) 2023 Adam Jenca
mini-scheme comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions, consult the license at https://github.com/jenca-adam/mini-scheme/blob/main/LICENSE for more information.""")    
    while True:
        readline.set_completer(Completer(GLOBAL_NAMESPACE.keys()).complete)
        try:
            newcmd=input("?")
        except:
            break
        try:
            print(get_repr(run_str(newcmd)))
        except Exception as e:
            print("ERROR:")
            if not hasattr(e,"__name__"):
                traceback.print_exc()
                continue
            print(f"{e.__name__}: {str(e)}")
            
