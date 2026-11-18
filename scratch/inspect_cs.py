import inspect
import sys
sys.path.append(r'd:\ReactJs\aivolve-trading-ai\backend')
import app.options.contract_selector as cs
print('Doc:', inspect.getdoc(cs)[:500])
classes = [c for c in dir(cs) if inspect.isclass(getattr(cs, c)) and getattr(cs, c).__module__ == 'app.options.contract_selector']
print('Classes:', classes)
funcs = [f for f in dir(cs) if inspect.isfunction(getattr(cs, f)) and getattr(cs, f).__module__ == 'app.options.contract_selector']
print('Functions:', funcs[:15])
