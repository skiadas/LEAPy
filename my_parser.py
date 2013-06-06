import re
import operator as oper

def expression(rbp=0):
    global token, _context
    t = token
    token = next()
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.led(left)
    return left

def follow(context, key):
    "Word tokens will use this function to find how to interpret themselves. The context can be a class, function or dictionary, as long as it can be called with the token value, or has the value as a key, or as an attribute."
    val = context(key) if callable(context) else context[key] if key in context else getattr(context, key) if hasattr(context, key) else None
    if callable(val): val = val()
    return(val)

def parse(program, context = {}):
    global token, next, _context
    _context = context
    next = tokenize(program).next
    token = next()
    return expression()

class symbol_base(object):

    id = None # node/token type name
    value = None # used by literals
    first = second = third = None # used by tree nodes
    def nud(self):
        raise SyntaxError("Syntax error (%r)." % self.id)
    def led(self, left):
        raise SyntaxError("Unknown operator (%r)." % self.id)
    def __repr__(self):
        if self.id == "(name)" or self.id == "(literal)":
            return "(%s %s)" % (self.id[1:-1], self.value)
        out = [self.id, self.first, self.second, self.third]
        out = map(str, filter(None, out))
        return "(" + " ".join(out) + ")"

symbol_table = {}
def symbol(id, bp=0):
    try:
        s = symbol_table[id]
    except KeyError:
        class s(symbol_base):
            pass
        s.__name__ = "symbol-" + id # for debugging
        s.id = id
        s.value = None
        s.lbp = bp
        symbol_table[id] = s
    else:
        s.lbp = max(bp, s.lbp)
    return s

def infix(id, bp, op):
    def led(self, left):
        return op(left, expression(bp))
    symbol(id, bp).led = led

def prefix(id, bp, op):
    def nud(self):
        return op(expression(bp))
    symbol(id).nud = nud

def infix_r(id, bp, op):
    def led(self, left):
        return op(left, expression(bp-1))
    symbol(id, bp).led = led

def constant(val):
    @method(symbol("%s" % val))
    def nud(self):
        self.value = val
        return self.value

def advance(id=None):
    global token
    if id and token.id != id:
        raise SyntaxError("Expected %r" % id)
    token = next()

def method(s):
    # decorator
    assert issubclass(s, symbol_base)
    def bind(fn):
        setattr(s, fn.__name__, fn)
    return bind

symbol("(number)").nud = lambda self: float(self.value)
constant(True); constant(False); constant(None)
symbol("+", 100); symbol("-", 100)
symbol("*", 200); symbol("/", 200)
symbol("**", 300)
for x, op in [("and", oper.and_), ("or", oper.or_), ("is", oper.is_), ("is not", oper.is_not)]: infix(x, 30, op)
for x, op in [(">=", oper.ge),("<=", oper.le),("==", oper.eq), (">", oper.gt), ("<", oper.lt)]: infix(x, 50, op)
prefix("not", 40, oper.not_)
symbol("(end)")
infix("+", 100, oper.add); infix("-", 100, oper.sub)
infix("*", 200, oper.mul); infix("/", 200, oper.truediv)
prefix("+", 100, lambda x: x); prefix("-", 100, lambda x: -x)
infix_r("**", 300, oper.pow)
prefix("=>",10, lambda x, y: {y if x else False} )
@method(symbol("(word)"))
def nud(self):
    global _context
    return(follow(_context, self.value))

@method(symbol("("))
def nud(self):
    expr = expression()
    advance(")")
    return expr
symbol(")")


token_pat = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([+-/*]|[><=]=|[><]|=>|(?:is )not|is|and|or|not|[\(\)]|True|False|None)|([\w_.]+))")
def tokenize(program):
    for number, operator, word in token_pat.findall(program):
        if number:
            s = symbol("(number)")()
            s.value = number
            yield s
        elif operator:
            yield symbol(operator)()
        elif word:
            s = symbol("(word)")()
            s.value = word
            yield s
        else:
            raise SyntaxError("unknown expression.")
    yield symbol("(end)")
    yield StopIteration

if __name__ == "__main__":
    class TestContext(dict):
        def __init__(self):
            self.has_calc = False
            self['has_precalc'] = True
        def placement_score(self):
            return 42

    instr = r'''3+4.5 + 5
2+3*5
2+3*5.0 == 17
(2+3)*5
True and False
False or True
placement_score
has_calc
has_precalc
placement_score is None => none
not(has_precalc) and not(has_calc) => dept
has_calc and placement_score >= 32 => 121e
has_calc and placement_score >= 16 => 121
has_precalc and placement_score >= 6  => 111
placement_score >= 26              => 121
placement_score >= 6               => 111
True                               => dept'''.split("\n")


    test_c = TestContext()
    for x in instr:
        print x
        print "=>", parse(x, context = test_c)

