echo 'db wating sleep' # DB 의 depends_on 을 걸었으나 느린관계로 sleep 추가
sleep 15s
python manage.py migrate
python manage.py runserver 0.0.0.0:8000