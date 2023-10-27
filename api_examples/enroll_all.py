import requests

base_url = 'http://127.0.0.1:8000/api/'

# recuperar todos los cursos
r = requests.get(f'{base_url}courses/')

print(r)

courses = r.json()

# available_courses = ', '.join([course['title'] for course in courses])
# print(f'Availble courses: {available_courses}')