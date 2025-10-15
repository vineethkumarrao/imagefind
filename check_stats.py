import requests

r = requests.get('http://localhost:8000/api/stats')
stats = r.json()['statistics']

print('\n' + '='*50)
print('DATABASE STATUS')
print('='*50)
print(f'Total images: {stats["total_images"]}')
print(f'Healthcare: {stats["categories"]["healthcare"]}')
print(f'Satellite: {stats["categories"]["satellite"]}')
print(f'Surveillance: {stats["categories"]["surveillance"]}')
print('='*50)
