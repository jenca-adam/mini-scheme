from .scheme_ast import ast
from .scheme_types import nil
from .scheme_function import GLOBAL_NAMESPACE
import readline
import traceback
import argparse
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
def run_str(code):
    result=[it.evaluate() for it in ast(code)]
    if len(result)==1:
        return result[0]
    elif len(result)==0:
        return nil()
    raise RunnerError("can eval only one expression")
def cmdline():
    readline.parse_and_bind('tab:complete')
    readline.set_completer_delims(' ()\t\n')
    while True:
        readline.set_completer(Completer(GLOBAL_NAMESPACE.keys()).complete)
        try:
            newcmd=input("?")
        except:
            break
        try:
            print(run_str(newcmd))
        except Exception as e:
            print("ERROR:")
            if not hasattr(e,"__name__"):
                traceback.print_exc()
                continue
            print(f"{e.__name__}: {str(e)}")
            
