# 비바이노베이션 과제

## 실행방법
```shell
docker-compose up -d
```

## DB Migration 방법
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