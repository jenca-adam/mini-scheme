# mini-scheme

`mini-scheme` is a lightweight command-line scheme interpreter written in Python.
It's still not yet finished and tested properly, and some features aren't yet added(for example `let*` and `letrec`).

## Installation

Since `mini-scheme` is still in its alpha/prototype stage, it's not yet uploaded anywhere besides GitHub. That doesn't mean you can't install it, though.
You can install it by simply cloning the repository ,cd-ing into it and running
```
python -m pip install .
```

## Running mini-scheme

To run interactive prompt, similar to that of Python, use 
```
python -m mini_scheme
```
If you want to run a Scheme program in mini-scheme, use the `-f` or `--file` flag.
```
python -m mini_scheme -f my_program.scm
```
## mini-scheme as a Python library
The key function is `mini_scheme.run_str()`, which takes a piece of Scheme code, and evaluates it.
Its result is a list of Python objects corresponding to the results of expressions given in the Scheme code.
## Contribute to mini-scheme

If you'd like to add/fix something in mini-scheme, fork the repository and make a pull-request.
The code is kind of spaghetti, so be warned before you try fixing something.

