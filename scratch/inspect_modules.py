import inspect
import sys

sys.path.append(r'd:\ReactJs\aivolve-trading-ai\backend')

modules_to_inspect = [
    'app.options.option_risk_engine',
    'app.options.paper_trading.cost_calculator',
    'app.options.paper_trading.paper_engine',
    'app.options.paper_trading.feature_pipeline',
    'app.options.market_state_engine',
    'app.backtesting.risk_analytics',
    'app.backtesting.portfolio_ledger',
]

for mod_name in modules_to_inspect:
    try:
        mod = __import__(mod_name, fromlist=[''])
        print(f'=== MODULE: {mod_name} ===')
        print(f'Doc: {inspect.getdoc(mod)}')
        classes = [c for c in dir(mod) if inspect.isclass(getattr(mod, c)) and getattr(mod, c).__module__ == mod_name]
        funcs = [f for f in dir(mod) if inspect.isfunction(getattr(mod, f)) and getattr(mod, f).__module__ == mod_name]
        print(f'Classes: {classes}')
        for c in classes:
            cls_obj = getattr(mod, c)
            methods = [m for m in dir(cls_obj) if not m.startswith('__') and callable(getattr(cls_obj, m))]
            print(f'  Class {c}: methods={methods}')
        print(f'Functions: {funcs}')
        print('='*50)
    except Exception as e:
        print(f'Error importing {mod_name}: {e}')
