# 핵심 지표 표시 검증

## 검증 대상
Streamlit 핵심 지표 표시 기능

## AI 제안 코드
총 주문 수, 총 매출, 총 고객 수를 계산하여 st.metric()으로 표시하도록 작성하였다.

## 검증 방법
1. Streamlit 앱을 실행하였다.
2. 총 주문 수, 총 매출, 총 고객 수가 화면에 표시되는지 확인하였다.
3. CSV 데이터에서 계산한 값과 화면의 값을 비교하였다.

## 검증 결과
총 주문 수, 총 매출, 총 고객 수가 정상적으로 표시되었다.

총 매출은 order_items의 quantity와 unit_price를 곱한 후 합산하여 계산하였다.

## 수정 사항
초기에는 orders["total_amount"]를 사용했으나 실제 orders.csv에 total_amount 컬럼이 없었다.
따라서 quantity * unit_price 방식으로 수정하였다.