# 코드 단위 검증 기록

## 1. 작성자
- GitHub ID: cyw0927
- 담당 기능: 주문 상세 금액 계산 및 핵심 지표 분석

## 2. 검증 단위
- 기능명: 주문 상세 금액(item_amount) 계산
- 관련 파일: `notebooks/02_analysis.ipynb`
- 관련 Issue: 담당자 B 분석 작업

## 3. 코드 목적
주문 상세 데이터에서 주문 수량(`quantity`)과 주문 당시 단가(`unit_price`)를 곱하여 각 주문 상세의 금액인 `item_amount`를 계산한다.

이 값을 이후 총 주문 금액, 평균 주문 금액, 카테고리별 매출, 월별 매출 계산에 사용한다.

## 4. 입력
- DataFrame: `order_items`
- 사용 컬럼:
  - `quantity`
  - `unit_price`

## 5. AI 활용
- 사용 도구: ChatGPT
- 질문 내용: 주문 상세 금액을 계산하는 방법과 계산 결과를 직접 검증하는 방법
- AI가 제안한 핵심 내용:
  - `quantity * unit_price`로 `item_amount` 컬럼 생성
  - 첫 번째 행의 값을 직접 계산하여 실제 생성된 값과 비교
  - `assert`를 사용해 예상값과 실제값이 같은지 확인

## 6. 실행 전 예상
각 행의 `item_amount` 값은 해당 행의 `quantity × unit_price`와 같을 것으로 예상했다.

## 7. 실행 코드

```python
order_items["item_amount"] = (
    order_items["quantity"] * order_items["unit_price"]
)
```

검증 코드:

```python
sample = order_items.iloc[0]

expected = sample["quantity"] * sample["unit_price"]
actual = sample["item_amount"]

print("예상값:", expected)
print("실제값:", actual)

assert expected == actual
```

## 8. 실제 결과
`item_amount` 컬럼이 정상적으로 생성되었다.

첫 번째 행의 `quantity × unit_price`로 직접 계산한 예상값과 실제 `item_amount` 값이 동일했으며, `assert` 실행 시 오류가 발생하지 않았다.

## 9. 검증 방법
- 정상 조건: 정상 행에서 `quantity × unit_price`와 `item_amount` 비교
- 예외 조건: 실제 컬럼명이 코드와 일치하는지 확인
- 직접 비교한 값: `expected`와 `actual`
- assert 또는 수동 확인 방법:
  - `assert expected == actual`
  - `display()`로 앞부분 데이터를 출력하여 수동 확인

## 10. AI 코드에서 수정한 부분
실제 데이터의 컬럼명인 `quantity`, `unit_price`, `item_amount`에 맞추어 코드를 사용했다.

검증 과정에서는 단순히 계산 결과를 출력하는 것에서 끝내지 않고, 직접 계산한 예상값과 실제값을 `assert`로 비교하도록 구성했다.

## 11. 결과 해석
주문 상세별 금액이 정상적으로 계산되었다.

`item_amount`는 이후 총 주문 금액, 평균 주문 금액, 카테고리별 매출, 월별 매출 계산에 사용할 수 있다.

## 12. 아직 이해되지 않는 부분
현재 검증한 범위에서는 없음.