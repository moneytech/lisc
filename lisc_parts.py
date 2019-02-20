#!/bin/python3

## streams
def _read_char(stream):
    return [(stream.pop() and None) or stream.append(-1) or (None, stream) if pos >= len(stream[0]) else (None, stream) if pos == -1 else c.append(stream[0][pos]) or (stream.pop() and None) or stream.append(pos+1) or (c[0], stream) for c in [[]] for pos in [stream[1]]][0]

def _peek_char(stream):
    return [(None, stream) if pos >= len(stream[0]) else (None, stream) if pos == -1 else (stream[0][pos], stream) for pos in [stream[1]]][0]

def _make_stream(s):
    return [s, 0]

## readers
def _read_list(stream):
    return [[(_read_char(stream) and None) or loop[1:] if _peek_char(stream)[0] == ')' else loop[1:] if _peek_char(stream)[0] == None else loop.append(l_read(stream)) for l in loop] for loop in [[None]]][0][-1]

def _read_symbol(stream):
    return ''.join([[loop if _peek_char(stream)[0] == ')' else (_read_char(stream) and None) or loop if _peek_char(stream)[0] == ' ' else loop if _peek_char(stream)[0] == None else loop.append(_read_char(stream)[0]) for l in loop] for loop in [['']]][0][-1])

def _read_string(stream):
    return ('str', ''.join([[(_read_char(stream) and None) or chars if _peek_char(stream)[0] == '"' else loop.append(_read_char(stream)[0]) or chars for chars in loop] for loop in [['']]][0]))

def l_read(stream):
    return [[_read_char(stream) and loop.append(None) if  _peek_char(stream)[0] in [' ', '\n'] else None for l in loop] for loop in [[None]]] and (None if _peek_char(stream)[0] is None else (_read_char(stream) and None) or _read_list(stream) if _peek_char(stream)[0] == '(' else ((_read_char(stream) and None) or _read_string(stream)) if _peek_char(stream)[0] == '"' else _read_symbol(stream))

# constants and functions
_env = (None, {})
_env[1]['nil'] = []
_env[1]['t'] = 't'
_env[1]['atom'] = ('lambda', None, lambda o: 't' if type(o) is not list else [])
_env[1]['cons'] = ('lambda', None, lambda a, b: [a] if b in ['nil', []] else [a] + b if type(b) is list else '__{}_is_not_a_list__'.format(b))
_env[1]['car'] = ('lambda', None, lambda l: l[0])
_env[1]['cdr'] = ('lambda', None, lambda l: l[1:] if len(l) > 1 else [])
_env[1]['eq'] = ('lambda', None, lambda a, b: 't' if ('nil' in [a,b] and [] in [a,b]) or a == b else [])

_env[1]['load'] = ('lambda', None, lambda s: '__invalid_filename__' if type(s) is not tuple or s[0] != 'str' else [(lambda f: f if f is None else lis.append(l_eval(f)))(l_read(stream)) or lis for stream in [_make_stream(''.join([l.replace('\n', ' ') or l for l in open(s[1])]))] for lis in [[None]] for loop in lis][0][-1])

_env[1]['reads'] = ('lambda', None, lambda s: ('str', input(s[1])))

# evaluator
def l_eval(l, env=_env):
    return ('nil' if len(l) == 0 else (l_eval(l[2], env) if len(l) == 4 and l_eval(l[1], env) == 't' else l_eval(l[3], env)) if l[0] == 'if' else (l[1] if len(l) == 2 else '__quote_invalid_argument__') if l[0] == 'quote' else (('lambda', l[1], lambda new_env: l_eval(l[2], (env, new_env))) if len(l) == 3 else '__invalid_lambda_expression__') if l[0] == 'lambda' else (_env[1].update({l[1]: l_eval(l[2], env)}) or (_env[1][l[1]] if len(l) == 3 else '__define_invalid_argument__')) if l[0] == 'define' else [[fn[2](*eval_args) if fn[1] is None else fn[2](dict(zip(fn[1], eval_args))) if len(fn[1])+1 == len(l) else '__wrong_number_of_args__' for eval_args in [[l_eval(a, env) for a in l[1:]]]][0] if type(fn) is tuple and fn[0] == 'lambda' else '__undefined_operator__' for fn in [l_eval(l[0], env)]][0]) if type(l) is list else l if type(l) is tuple else [search_val(env, l) for _ in [None] for search_val in [lambda e, s: [v if v is not None else '__unbound_variable__' if e[0] is None else search_val(e[0], s) for v in [e[1].get(s, None)]][0]]][0] if type(l) is str else None if l is None else '__invalid_object__'

# printer
def l_print(l):
    return 'nil' if l == [] else '(' + ' '.join([l_print(e) for e in l]) + ')' if type(l) is list else repr(l[1]) if type(l) is tuple and l[0] == 'str' else '[{}]'.format(' '.join(['<fn {}>'.format(id(e)) if callable(e) else str(e) for e in l])) if type(l) is tuple else str(l)

if __name__ == '__main__':
    [b.append(l_read(_make_stream(input('> ')))) or (print(l_print(l_eval(b[-1]))) if b[-1] is not None else b.append('')) for b in [['']] for a in b]
