def test_greeks_formatting(greeks, delta=0.5, theta_day=-10.0):
    gamma_val = round(greeks['gamma'], 5) if (greeks and greeks.get('gamma') is not None) else None
    vega_val = round(greeks['vega'], 2) if (greeks and greeks.get('vega') is not None) else None
    return {
        'delta': round(delta, 3) if delta is not None else None,
        'gamma': gamma_val,
        'thetaPerDay': round(theta_day, 2) if theta_day is not None else None,
        'vega': vega_val,
    }

print('Valid Greeks:', test_greeks_formatting({'delta': 0.5123, 'gamma': 0.001234, 'theta': -12.345, 'vega': 8.123}, 0.5123, -12.345))
print('None Greeks:', test_greeks_formatting(None))
print('Empty Greeks:', test_greeks_formatting({}))
print('None values in Greeks:', test_greeks_formatting({'gamma': None, 'vega': None}))
