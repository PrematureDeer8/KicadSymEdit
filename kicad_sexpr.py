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
        # this if statement implies that their are some invalid keys
        if(set(kwargs.keys()) != self._str_attr):
            # XOR to get the missing keys
            invalid_keys = self._str_attr ^ set(kwargs.keys());
            missing_keys = self._str_attr & invalid_keys;
            wrong_keys = invalid_keys - missing_keys;
            if(missing_keys != set()):
                raise ValueError(f"Missing keys:\n {missing_keys}");
            else:
                raise ValueError(f"Invalid keys:\n {wrong_keys}");

        # formatted symbol string
        self._symbol_str = symbol_str.format(**kwargs);

        # convert the symbol string into sexpr object
        super().__init__(parseSexp(self._symbol_str));
        # set the action to overwrite for entire sexp hierarchy
        KicadSexpr.setaction(self, Sexp.OVERWRITE);

    
    # recursively set the action of every element below the sexp object
    @staticmethod
    def setaction(obj : object, action: int):
        if(isinstance(obj, SexpParser)):
            obj._action = action;
            for value in obj._value.values():
                KicadSexpr.setaction(value, action);
        
        return;
            


    # return all attributes of the format string
    @staticmethod
    def getattribute(fmt_string : str) -> set:
        return set(KicadSexpr.re_pat_attr.findall(fmt_string));
    

class Pin(KicadSexpr):
    _str = pin;
    def __init__(self, **kwargs) -> None:
        # default settings for Pin class 
        # NOTE: not all settings are listed
        self._default = {"graphic_style": "line", 
                   "orientation": 0, 
                   "length": 5.08, 
                   "name_size_x": 1.27, 
                   "name_size_y": 1.27,
                   "number_size_x": 1.27,
                   "number_size_y": 1.27};
        self._default = pd.Series(self._default);
        # get the mising the default keys
        missing_default_keys = ((set(kwargs.keys()) ^ set(self._default.keys())) & set(self._default.keys()));
        kwargs = dict(pd.concat([pd.Series(kwargs), self._default[list(missing_default_keys)]]));
        super().__init__(self._str, **kwargs);
    @staticmethod
    def getattribute() -> set:
        return KicadSexpr.getattribute(Pin._str);

class Rectangle(KicadSexpr):
    _str = rectangle;
    def __init__(self, **kwargs) -> None:
        # NOTE: grandparent class SexpParser intercepts this assignment 
        # because __setrattr__ operation was overloaded to treat this assignment
        # as an sexp object 
        # to bypass that overload use _varname infront of any attribute assignment
        self._default = {"stroke_width": 0, "stroke_type": "solid", "fill_type": "background"};
        self._default = pd.Series(self._default);
        # get the mising the default keys
        missing_default_keys = ((set(kwargs.keys()) ^ set(self._default.keys())) & set(self._default.keys()));
        kwargs = dict(pd.concat([pd.Series(kwargs), self._default[list(missing_default_keys)]]));
        super().__init__(self._str, **kwargs);
    @staticmethod
    def getattribute() -> set:
        return KicadSexpr.getattribute(Rectangle._str);

class Symbol(KicadSexpr):
    # In Kicad the sym_name ending with a _# is the unit number!
    _str = '(symbol "{sym_name}")';
    def __init__(self, **kwargs) -> None:
        # NOTE: action is set to Sexp.OVERWRITE by default
        super().__init__(self._str, **kwargs)