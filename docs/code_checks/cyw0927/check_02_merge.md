# 코드 단위 검증 기록

## 1. 작성자
- GitHub ID: cyw0927
- 담당 기능: 주문, 주문 상세, 상품 데이터 병합

## 2. 검증 단위
- 기능명: `orders`, `order_items`, `products` 데이터 병합
- 관련 파일: `notebooks/02_analysis.ipynb`
- 관련 Issue: 담당자 B 분석 작업

## 3. 코드 목적
서로 분리되어 있는 주문 상세, 주문, 상품 데이터를 하나의 DataFrame으로 연결한다.

이를 통해 주문 상세 데이터에 주문 날짜, 결제 방법, 주문 상태, 상품명, 상품 카테고리 정보를 추가하여 이후 분석에 사용할 수 있도록 한다.

## 4. 입력
- DataFrame: `order_items`
  - `order_id`
  - `product_id`
  - `quantity`
  - `unit_price`
  - `item_amount`

- DataFrame: `orders`
  - `order_id`
  - `customer_id`
  - `order_date`
  - `payment_method`
  - `order_status`

- DataFrame: `products`
  - `product_id`
  - `product_name`
  - `category`
  - `price`

## 5. AI 활용
- 사용 도구: ChatGPT
- 질문 내용: 주문 상세 데이터에 주문 정보와 상품 정보를 병합하는 방법과 병합 결과를 검증하는 방법
- AI가 제안한 핵심 내용:
  - `merge()`를 사용하여 DataFrame 병합
  - `order_id`를 기준으로 `order_items`와 `orders` 병합
  - `product_id`를 기준으로 `products` 추가 병합
  - `how="left"`를 사용하여 주문 상세 데이터의 행을 유지
  - 병합 전후 행 수와 주요 컬럼의 결측치 여부 확인

## 6. 실행 전 예상
`order_items`의 행 수는 14,603행이다.

정상적으로 병합된다면 병합 후에도 14,603행이 유지되고, 각 주문 상세 행에 주문 날짜, 주문 상태, 상품명, 카테고리 정보가 추가될 것으로 예상했다.

## 7. 실행 코드

```python
before_rows = len(order_items)

merged = order_items.merge(
    orders,
    on="order_id",
    how="left"
)
```

상품 데이터 추가 병합:

```python
merged = merged.merge(
    products,
    on="product_id",
    how="left"
)
```

검증 코드:

```python
assert len(merged) == before_rows
assert merged["order_date"].notna().all()
assert merged["order_status"].notna().all()
assert merged["product_name"].notna().all()
assert merged["category"].notna().all()

print("데이터 병합 검증 완료")
```

## 8. 실제 결과
병합 전 `order_items`의 행 수는 14,603행이었고, 병합 후에도 14,603행으로 유지되었다.

`orders`에 있던 주문 날짜, 결제 방법, 주문 상태 정보가 정상적으로 추가되었고, `products`에 있던 상품명과 카테고리 정보도 정상적으로 추가되었다.

주요 컬럼에 결측치가 발생하지 않았으며 `assert` 실행 시 오류가 발생하지 않았다.

## 9. 검증 방법
- 정상 조건:
  - `order_id`를 기준으로 주문 정보가 정상적으로 연결되는지 확인
  - `product_id`를 기준으로 상품 정보가 정상적으로 연결되는지 확인

- 예외 조건:
  - 병합 후 행 수가 증가하거나 감소하지 않는지 확인
  - 병합 실패로 주요 컬럼에 결측치가 발생하지 않는지 확인

- 직접 비교한 값:
  - 병합 전 행 수: 14,603
  - 병합 후 행 수: 14,603

- assert 또는 수동 확인 방법:
  - `assert len(merged) == before_rows`
  - 주요 컬럼의 `notna().all()` 확인
  - `display(merged.head())`를 사용하여 병합 결과를 직접 확인

## 10. AI 코드에서 수정한 부분
실제 데이터의 컬럼 구조를 확인한 뒤 `order_id`와 `product_id`를 병합 기준으로 사용했다.

또한 단순히 병합하는 것에서 끝내지 않고, 병합 전후 행 수를 비교하고 주요 컬럼의 결측치 여부를 확인하는 검증 코드를 추가했다.

## 11. 결과 해석
주문 상세 데이터에 주문 정보와 상품 정보가 정상적으로 연결되었다.

이 병합된 데이터를 이용하면 주문 상태별 주문 건수, 카테고리별 매출, 월별 주문 금액 등의 분석을 수행할 수 있다.

## 12. 아직 이해되지 않는 부분
`left`, `right`, `inner` 병합 방식의 기본 차이는 확인했지만, 복잡한 다대다 관계의 병합은 추가 학습이 필요하다.