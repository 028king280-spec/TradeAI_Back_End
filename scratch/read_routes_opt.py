with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\api\routes\options.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i in range(110, 140):
    print(f'{i+1}: {lines[i]}')
