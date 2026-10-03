from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import httpx


# ---------------------------------------------------------
# FastAPI 앱 생성
# ---------------------------------------------------------

app = FastAPI(
    title="환율 계산기 API",
    description="FastAPI와 외부 환율 API를 이용한 환율 계산 서비스",
    version="1.0.0"
)


# 사용할 통화 목록
CURRENCIES = {
    "KRW",
    "USD",
    "EUR",
    "JPY",
    "GBP",
    "CNY",
    "AUD",
    "CAD"
}


# ---------------------------------------------------------
# 메인 홈페이지
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home():

    return """
<!DOCTYPE html>
<html lang="ko">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>환율 계산기</title>


    <style>

        * {
            box-sizing: border-box;
        }


        body {

            margin: 0;

            min-height: 100vh;

            display: flex;

            justify-content: center;

            align-items: center;

            font-family:
                Arial,
                "Noto Sans KR",
                sans-serif;

            background:
                linear-gradient(
                    135deg,
                    #dbeafe,
                    #f8fafc
                );

        }


        .container {

            width: 100%;

            max-width: 470px;

            padding: 20px;

        }


        .card {

            background: white;

            padding: 40px;

            border-radius: 24px;

            box-shadow:
                0 18px 50px
                rgba(0, 0, 0, 0.12);

        }


        .logo {

            text-align: center;

            font-size: 60px;

        }


        h1 {

            text-align: center;

            margin-top: 10px;

            margin-bottom: 8px;

            color: #0f172a;

        }


        .description {

            text-align: center;

            color: #64748b;

            margin-bottom: 30px;

        }


        label {

            display: block;

            margin-top: 18px;

            margin-bottom: 8px;

            font-weight: bold;

            color: #334155;

        }


        input,
        select {

            width: 100%;

            padding: 14px;

            font-size: 16px;

            border: 1px solid #cbd5e1;

            border-radius: 10px;

            background: white;

        }


        input:focus,
        select:focus {

            outline: none;

            border-color: #2563eb;

            box-shadow:
                0 0 0 3px
                rgba(37, 99, 235, 0.10);

        }


        .arrow {

            text-align: center;

            font-size: 28px;

            margin-top: 18px;

            color: #64748b;

        }


        button {

            width: 100%;

            padding: 15px;

            margin-top: 28px;

            border: none;

            border-radius: 10px;

            background: #2563eb;

            color: white;

            font-size: 17px;

            font-weight: bold;

            cursor: pointer;

        }


        button:hover {

            background: #1d4ed8;

        }


        button:disabled {

            background: #94a3b8;

            cursor: not-allowed;

        }


        .result {

            display: none;

            margin-top: 25px;

            padding: 22px;

            border-radius: 15px;

            background: #eff6ff;

            text-align: center;

        }


        .before {

            font-size: 18px;

            color: #475569;

        }


        .result-arrow {

            font-size: 22px;

            margin: 8px;

            color: #64748b;

        }


        .result-value {

            font-size: 30px;

            font-weight: bold;

            color: #2563eb;

        }


        .rate {

            margin-top: 16px;

            color: #475569;

        }


        .date {

            margin-top: 8px;

            font-size: 13px;

            color: #94a3b8;

        }


        .error {

            color: #dc2626;

        }


        .docs {

            margin-top: 25px;

            text-align: center;

        }


        .docs a {

            color: #2563eb;

            text-decoration: none;

            font-weight: bold;

        }


        .docs a:hover {

            text-decoration: underline;

        }


        .footer {

            margin-top: 25px;

            text-align: center;

            color: #94a3b8;

            font-size: 12px;

        }


        @media (max-width: 500px) {

            .card {

                padding: 28px;

            }

        }

    </style>

</head>


<body>


<div class="container">

    <div class="card">


        <div class="logo">
            💱
        </div>


        <h1>
            환율 계산기
        </h1>


        <div class="description">
            FastAPI를 이용한 환율 계산 서비스
        </div>


        <label for="amount">
            금액
        </label>


        <input
            id="amount"
            type="number"
            value="100"
            min="0.01"
            step="0.01"
        >


        <label for="fromCurrency">
            기준 통화
        </label>


        <select id="fromCurrency">

            <option value="USD">
                🇺🇸 USD - 미국 달러
            </option>

            <option value="KRW">
                🇰🇷 KRW - 대한민국 원
            </option>

            <option value="EUR">
                🇪🇺 EUR - 유로
            </option>

            <option value="JPY">
                🇯🇵 JPY - 일본 엔
            </option>

            <option value="GBP">
                🇬🇧 GBP - 영국 파운드
            </option>

            <option value="CNY">
                🇨🇳 CNY - 중국 위안
            </option>

            <option value="AUD">
                🇦🇺 AUD - 호주 달러
            </option>

            <option value="CAD">
                🇨🇦 CAD - 캐나다 달러
            </option>

        </select>


        <div class="arrow">
            ↓
        </div>


        <label for="toCurrency">
            변환 통화
        </label>


        <select id="toCurrency">

            <option value="KRW">
                🇰🇷 KRW - 대한민국 원
            </option>

            <option value="USD">
                🇺🇸 USD - 미국 달러
            </option>

            <option value="EUR">
                🇪🇺 EUR - 유로
            </option>

            <option value="JPY">
                🇯🇵 JPY - 일본 엔
            </option>

            <option value="GBP">
                🇬🇧 GBP - 영국 파운드
            </option>

            <option value="CNY">
                🇨🇳 CNY - 중국 위안
            </option>

            <option value="AUD">
                🇦🇺 AUD - 호주 달러
            </option>

            <option value="CAD">
                🇨🇦 CAD - 캐나다 달러
            </option>

        </select>


        <button
            id="convertButton"
            onclick="convertCurrency()"
        >
            환율 계산
        </button>


        <div
            id="result"
            class="result"
        >

            <div
                id="before"
                class="before"
            >
            </div>


            <div class="result-arrow">
                ↓
            </div>


            <div
                id="resultValue"
                class="result-value"
            >
            </div>


            <div
                id="rateText"
                class="rate"
            >
            </div>


            <div
                id="dateText"
                class="date"
            >
            </div>

        </div>


        <div class="docs">

            <a
                href="/docs"
                target="_blank"
            >
                FastAPI API 문서 보기
            </a>

        </div>


        <div class="footer">

            FastAPI Exchange Rate Calculator

        </div>


    </div>

</div>


<script>


function formatNumber(number) {

    return new Intl.NumberFormat(

        "ko-KR",

        {
            maximumFractionDigits: 2
        }

    ).format(number);

}


async function convertCurrency() {


    const amountInput =
        document.getElementById("amount");


    const amount =
        amountInput.value;


    const fromCurrency =
        document.getElementById(
            "fromCurrency"
        ).value;


    const toCurrency =
        document.getElementById(
            "toCurrency"
        ).value;


    const resultBox =
        document.getElementById(
            "result"
        );


    const resultValue =
        document.getElementById(
            "resultValue"
        );


    const button =
        document.getElementById(
            "convertButton"
        );


    if (
        amount === ""
        ||
        Number(amount) <= 0
    ) {

        alert(
            "0보다 큰 금액을 입력해주세요."
        );

        return;

    }


    resultBox.style.display =
        "block";


    resultValue.classList.remove(
        "error"
    );


    resultValue.innerText =
        "계산 중...";


    document.getElementById(
        "before"
    ).innerText = "";


    document.getElementById(
        "rateText"
    ).innerText = "";


    document.getElementById(
        "dateText"
    ).innerText = "";


    button.disabled =
        true;


    try {


        const url =

            "/api/convert"

            + "?amount="

            + encodeURIComponent(amount)

            + "&from_currency="

            + encodeURIComponent(
                fromCurrency
            )

            + "&to_currency="

            + encodeURIComponent(
                toCurrency
            );


        const response =
            await fetch(url);


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(

                data.detail

                ||

                "환율 계산 중 오류가 발생했습니다."

            );

        }


        document.getElementById(
            "before"
        ).innerText =

            formatNumber(
                data.amount
            )

            + " "

            + data.from_currency;


        resultValue.innerText =

            formatNumber(
                data.result
            )

            + " "

            + data.to_currency;


        document.getElementById(
            "rateText"
        ).innerText =

            "1 "

            + data.from_currency

            + " = "

            + formatNumber(
                data.rate
            )

            + " "

            + data.to_currency;


        document.getElementById(
            "dateText"
        ).innerText =

            "환율 기준일: "

            + data.date;


    }


    catch (error) {


        resultValue.classList.add(
            "error"
        );


        resultValue.innerText =
            error.message;


    }


    finally {


        button.disabled =
            false;


    }


}


document.getElementById(
    "amount"
).addEventListener(

    "keydown",

    function(event) {

        if (
            event.key === "Enter"
        ) {

            convertCurrency();

        }

    }

);


</script>


</body>

</html>
"""


# ---------------------------------------------------------
# 환율 계산 API
# ---------------------------------------------------------

@app.get("/api/convert")
async def convert_currency(

    amount: float = Query(
        ...,
        gt=0,
        description="환전할 금액"
    ),

    from_currency: str = Query(
        "USD",
        description="기준 통화"
    ),

    to_currency: str = Query(
        "KRW",
        description="변환 통화"
    )

):


    # 대문자로 변환
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()


    # 지원 통화 검사
    if from_currency not in CURRENCIES:

        raise HTTPException(

            status_code=400,

            detail=
            f"지원하지 않는 통화입니다: {from_currency}"

        )


    if to_currency not in CURRENCIES:

        raise HTTPException(

            status_code=400,

            detail=
            f"지원하지 않는 통화입니다: {to_currency}"

        )


    # 같은 통화끼리 계산
    if from_currency == to_currency:

        return {

            "amount":
                amount,

            "from_currency":
                from_currency,

            "to_currency":
                to_currency,

            "rate":
                1.0,

            "result":
                amount,

            "date":
                "동일 통화"

        }


        # Frankfurter API
    url = (
        "https://api.frankfurter.dev/v2/rate/"
        + from_currency.lower()
        + "/"
        + to_currency.lower()
    )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)

        response.raise_for_status()
        data = response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="환율 서버 응답 시간이 초과되었습니다."
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="환율 정보를 가져오지 못했습니다."
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="외부 환율 서버 연결에 실패했습니다."
        )

    # 환율
    rate = float(data["rate"])

    # 실제 환전 계산
    result = amount * rate

    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "rate": rate,
        "result": round(result, 2),
        "date": data["date"]
    }
