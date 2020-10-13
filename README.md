# KNUSD-20202-10

### 팀프로젝트를 위한 repository

- knu_reminder: project management
- main: webserver
- crawling: crawl API


### 파일 실행 방법:

**전제조건: 파이썬 장고 가상환경이 구축되어야함!!**

_처음 실행시_
1. `team10/knu_reminder/` 에 `secret.py` 파일 넣기. : 서버 실행을 위한 보안키, admin 아이디와 비밀번호 제공.
2. `cd team10` : manage.py가 있는 폴더로 이동
3. `python manage.py makemigrations main` : main 어플에 대한 db 변경사항 적용
4. `python manage.py migrate` : 모든 변경사항 db에 적용 후 db파일 생성
5. `python manage.py runserver` : 서버 실행, 자신의 로컬컴퓨터 ip주소로 할당됨.

_db 적용 후_
1. `python manage.py runserver` : 서버 실행

#### url 참고:

- `자신 ip주소/main/` 으로 접속하면 메인 화면으로 이동됨.
- `자신 ip주소/admin/` 으로 접속하면 관리자(데이터베이스) 사이트로 이동됨.

#### security 참고:

- `team10/knu_reminder/` 에 `secret.py` 파일 넣기.
- `서버 주소/admin/` 으로 접속한 후 admin id, password 를 입력하면 직접 데이터베이스를 관리할 수 있음.
