# sc-servers

에어텍 Raspberry pi3 축사 서버  
코드에 대한 자세한 설명은 아래 코드의 주석을 참고해주시길 바랍니다.  
현재 Frontend 대시보드 작업 완료


```
BLE 자동 연결 코드 참고: /opt/sc-servers/sc_project/farm_0001/__init__.py   
                         /opt/sc-servers/sc_project/farm_0001/bg_scheduler.py
                         /opt/sc-servers/sc_project/farm_0001/bt_auto_connect.py
```

### 1. 기본 세팅 (필수)

```
cd /opt/
git clone http://210.115.226.45/lab1336/sc-servers.git
cd sc-servers
pip3 install -r requirements.txt
./gen_env.sh # .env 파일 생성 (postgreSQL id, password)
```

### 2. postgreSQL DB 실행
```
cd postgresql
./run # postgresql DB 백그라운드 실행
docker ps # 실행확인

```

### 3. Django 서버 실행
```
cd sc_project
# super-user 수정 (Django admin id)
sudo nano init_user.py (ID 만 수정하고 PW 는 admin 페이지에서 변경 할것)
./run # 기본 실행시 (터미널이 꺼지면 동작 X)
# 이후 init_user.py 의 ID 와 PW 로 admin 페이지 접속 가능 (주소는 설정한 고정아이피 또는 ifconfig 참고)
# Django에서 postgreSQL DB 설정은 /opt/sc-servers/sc_project/sc_project/setting.py 참고
```


### 4. 자동실행

```
# /etc/rc.local 수정
# exit 0 위에 아래코드 추가

/opt/sc-servers/sc_project/run.sh &

```

### 5. 데이터 추출

```
cd /opt/sc-servers/sc_project
# 장치 정보 추출
python3 manage.py dumpdata --indent 2 farm_0001.Bt_dev > sc_dev.json
# 블투투스 데이터 추출
python3 manage.py dumpdata --indent 2 farm_0001.Bt_data > sc_data.json
```

### 6. 서버 종료 방법 (수동)

```
# 프로세스 확인
root@farm_0001:/opt/sc-servers# ps -ef | grep python3
root      1838   402  0 20:26 pts/0    00:00:00 grep --color=auto python3
root      1946   933  0 18:38 ?        00:00:15 python3 /opt/sc-servers/sc_project/manage.py runserver 0:80 --noreload

# 해당 프로세스 강제 종료
kill -9 1946
```

### 7. 서버 종료 방법 (자동)

```
./server_exit.sh
```


### 8. farm 이름 변경

```
./farm_change.sh <현재 farm 이름> <변경할 farm 이름>
```

### 9. admin 페이지, django rest api 페이지, frontend(대시보드) 접속 방법

```
admin 페이지 : <라즈베리파이 IP>/admin
django-rest-api 페이지 : <라즈베리파이 IP>/api
frontend(대시보드) : <라즈베리파이 IP>
```

