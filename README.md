# FastAPI 환율 계산기

FastAPI와 외부 환율 API를 이용하여 만든 환율 계산 웹 서비스입니다.

## 주요 기능

- 이름 입력 인사 API
- 두 숫자 곱셈 API
- 실제 환율 정보를 이용한 환율 계산
- 웹 기반 환율 계산기
- FastAPI Swagger API 문서 제공

## 사용 기술

- Python
- FastAPI
- Uvicorn
- HTTPX
- HTML
- CSS
- JavaScript
- Frankfurter Exchange Rate API

## API

### 환율 계산

GET /api/convert

예시:

/api/convert?amount=100&from_currency=USD&to_currency=KRW


### 이름 인사

GET /hello

예시:

/hello?name=홍길동


### 곱셈

GET /multiply

예시:

/multiply?a=10&b=20


### API 문서

/docs
