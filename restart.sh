kill -9 `lsof -t -i:25557`
python3 manage.py runserver 0.0.0.0:25557
