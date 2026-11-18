with open(r'd:\ReactJs\aivolve-trading-ai\src\types\options.ts', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i in range(325, 345):
    print(f'{i+1}: {lines[i]}')
