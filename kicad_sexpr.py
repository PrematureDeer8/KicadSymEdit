# NOTE: the .symbol_assets only works if you are not in the directory KicadSymEdit
try:
    from .symbol_assets import pin, rectangle, text_box
except ImportError:
    from symbol_assets import pin, rectangle, text_box
from s_expr import *
import re
import pandas as pd


class KicadSexpr(SexpParser):
    re_pat_attr = re.compile(r'\{(\w+)\}');
    def __init__(self, symbol_str : str, **kwargs) -> None:
        # string attributes
        self._str_attr = KicadSexpr.getattribute(symbol_str);
        self._raw_sym_str = symbol_str;
        if(set(kwargs.keys()) != self._str_attr):
            # XOR to get the missing keys
            missing_keys = self._str_attr ^ set(kwargs.keys());
            raise ValueError(f"Missing keys:\n {missing_keys}");

        # formatted symbol string
        self._symbol_str = symbol_str.format(**kwargs);

        # convert the symbol string into sexpr object
        super().__init__(parseSexp(self._symbol_str));

    # return all attributes of the format string
    @staticmethod
    def getattribute(fmt_string : str) -> set:
        return set(KicadSexpr.re_pat_attr.findall(fmt_string));
    

class Pin(KicadSexpr):
    def __init__(self, **kwargs) -> None:
        self._str = pin;
        # default settings for Pin class 
        # NOTE: not all settings are listed
        default = {"graphic_style": "line", 
                   "orientation": 0, 
                   "length": 5.08, 
                   "name_size_x": 1.27, 
                   "name_size_y": 1.27,
                   "number_size_x": 1.27,
                   "number_size_y": 1.27};
        default = pd.Series(default);
        # get the mising the default keys
        missing_default_keys = ((set(kwargs.keys()) ^ set(default.keys())) & set(default.keys()));
        kwargs = dict(pd.concat([pd.Series(kwargs), default[list(missing_default_keys)]]));
        super().__init__(self._str, **kwargs);

class Rectangle(KicadSexpr):
    def __init__(self, **kwargs) -> None:
        # NOTE: grandparent class SexpParser intercepts this assignment 
        # because __setrattr__ operation was overloaded to treat this assignment
        # as an sexp object 
        # to bypass that overload use _varname infront of any attribute assignment
        self._str = rectangle;
        default = {"stroke_width": 0, "stroke_type": "solid", "fill_type": "background"};
        default = pd.Series(default);
        # get the mising the default keys
        missing_default_keys = ((set(kwargs.keys()) ^ set(default.keys())) & set(default.keys()));
        kwargs = dict(pd.concat([pd.Series(kwargs), default[list(missing_default_keys)]]));
        super().__init__(self._str, **kwargs);
