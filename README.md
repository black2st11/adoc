# 비바이노베이션 과제

## django 를 선택하게 된 이유
개인적인 사유로 인하여 시간의 촉박함과 가장 자주 사용했던 부분이기에 사용했습니다. \
그렇다고 django 에 모든 부분을 사용하는 것이 아닌 django 에서는 잘 다루지 않는 service layer 형태로 분리해서 진행하였습니다.

## 코드 스타일
최소 아래의 코드 규칙을 적용했습니다.
- black
- isort

## 실행방법
```shell
docker-compose up -d
```

## DB Migration 방법
django 의 기본 migration 을 적용합니다.
mongodb 의 경우 따로 migration 없이 schema validation 을 적용했습니다.
```
python manage.py migrate
```

## API 명세
### 유저관련
#### 회원가입 (POST /users/signup)

request(body)
```json
{
    "email": "str",
    "password": "str",
    "re_password": "str"
}
```

response
```json
{
  "message": "str"
}
```

#### 로그인 (POST /users/login)

request(body)
```json
{
  "email": "str",
  "password": "str"
}
```

response
```json
{
  "access_token": "str",
  "refresh_token": "str"
}
```

#### 토큰 재발급 (POST /users/refresh)

request(header)
```json
{
  "Authorization": "str"
}
```

request(body)
```json
{
  "refresh_token": "str"
}
```

response
```json
{
  "access_token": "str",
  "refresh_token": "str"
}
```

#### 로그아웃 (POST /users/logout)

request(header)
```json
{
  "Authorization": "str"
}
```

response
```json
{
  "message": "str"
}
```


### 게시글 관리
#### 게시글 생성 (POST /posts)
request(header)
```json
{
  "Authorization": "str"
}
```

request(body)
```json
{
  "title": "str",
  "content": "str"
}
```

response
```json
{
  "_id": "str"
}
```

#### 게시글 조회 (GET /posts)
request(query)
```json
{
  "page": "int|None",
  "size": "int|None",
  "author_id": "int|None",
  "order_by": "str|None",
  "order": "int|None"
}
```

response
```json
{
  "page": "int",
  "size": "int",
  "total_page": "int",
  "total": "int",
  "items": [{
    "_id": "str",
    "title": "str",
    "content": "str",
    "created_at": "str",
    "author_id": "int"
  }]
}
```

#### 게시글 수정 (PUT /posts/{post_id})
request(header)
```json
{
  "Authorization": "str"
}
```

request(path)
```json
{
  "post_id": "str"
}
```

request(body)
```json
{
  "title": "str",
  "content": "str"
}
```

response
```json
{
  "message": "str"
}
```

#### 게시글 조회 (GET /posts/{post_id})
request(path)
```json
{
  "post_id": "str"
}
```

response
```json
{
  "_id": "str",
  "title": "str",
  "content": "str",
  "created_at": "str",
  "author_id": "int"
}
```

#### 게시글 삭제 (DELETE /posts/{post_id})
request(header)
```json
{
  "Authorization": "str"
}
```

request(path)
```json
{
  "post_id": "str"
}
```

response
```json
{
  "message": "str"
}
```