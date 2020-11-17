# KNUSD-20202-10

### 팀프로젝트를 위한 repository

- knu_reminder: project management
- main: webserver
- crawling: crawl API


### 파일 실행 방법:

_장고 가상환경 설정_

// version은 security tab에서 확인
1. `파이썬3 설치하기` _// py -3 -V 으로 버전 확인._
2. `pip install virtualenvwrapper-win` : 파이썬 가상 환경 정보 자동 저장 툴
3. `mkvirtual 가상환경이름` : 새 파이썬 가상환경 생성
4. `workon 가상환경이름` : 파이썬 가상 환경 실행 _// workon 으로 파이썬 가상환경 리스트 확인 가능_
5. `pip install django` : 파이썬 가상 환경에 장고 설치 
6. `pip install 패키지이름` : 그 외 패키지 설치 _// pip list 로 패키지 리스트 확인_

    - 패키지: requests, bs4, django-social-share, PyJWT

_번외: 버전 관리_
1. `pip install -U pip setuptools wheel` : 패키지 툴 업그레이드
2. `pip install pyopenssl ndg-httpsclientpyasnl` : InsecurePlatformWarning 대처

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
