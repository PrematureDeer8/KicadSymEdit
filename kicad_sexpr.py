# NOTE: the .symbol_assets only works if you are not in the directory KicadSymEdit
try:
    from .symbol_assets import pin, rectangle, text_box
except ImportError:
    from symbol_assets import pin, rectangle, text_box
from s_expr import *

class KicadSexpr(SexpParser):
    def __init__(self, symbol_str : str, **kwargs) -> None:
        self._raw_sym_str = symbol_str;
        if(kwargs == dict()):
            print("Keyword arguments (kwargs) can not be none!");
            raise ValueError(f"Expected format:\n {self._raw_sym_str}");
        try:
            # formatted symbol string
            self._symbol_str = symbol_str.format(**kwargs);
        except TypeError as e:
            print(f"Type error: {e}");
            raise TypeError(f"Expected format:\n {self._raw_sym_str}");

        # convert the symbol string into sexpr object
        super().__init__(parseSexp(self._symbol_str));

    

class Pin(KicadSexpr):
    def __init__(self, **kwargs) -> None:
        self._str = pin;
        super().__init__(self._str, **kwargs);

class Rectangle(KicadSexpr):
    def __init__(self, **kwargs) -> None:
        # NOTE: grandparent class SexpParser intercepts this assignment 
        # because __setrattr__ operation was overloaded to treat this assignment
        # as an sexp object 
        # to bypass that overload use _varname infront of any attribute assignment
        self._str = rectangle;
        super().__init__(self._str, **kwargs);
