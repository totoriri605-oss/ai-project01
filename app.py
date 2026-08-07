# 2.프로젝트 제목과 설명을 표시합니다.
# app.py에 쓰는 이유는 app.py -> streamlit이 코드를 읽음 -> 웹 화면을 만들어주는 구조이기 때문
import streamlit as st
import pandas as pd

from src.charts import create_category_sales_chart, create_order_status_chart

st.set_page_config(layout="wide") #금액이 커지는 경우 대비하여 화면을 넓게 쓰기

st.title("온라인 쇼핑몰 데이터 분석 대시보드")
st.write("온라인 쇼핑몰의 주문 및 상품 데이터를 확인하는 대시보드입니다.")

# 데이터 불러오기
orders = pd.read_csv("data/raw/orders.csv")
customers = pd.read_csv("data/raw/customers.csv")
order_items = pd.read_csv("data/raw/order_items.csv")
products = pd.read_csv("data/raw/products.csv")

# 4. 사이드바에 필터를 구현합니다.
st.sidebar.header("필터")

# 카테고리 필터 (카테고리 컬럼에서 중복을 빼고 종류만 가져오기)
category_options = ["전체"] + sorted(products["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox(
    "카테고리",
    category_options
)

# 주문 상태 필터
status_options = ["전체"] + sorted(orders["order_status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox(
    "주문 상태",
    status_options
)

# 5. 필터 적용 결과를 계산합니다.

# 상품 주문 데이터와 상품 데이터 연결
filtered_items = order_items.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
)

# 주문 데이터 복사
filtered_orders = orders.copy()

# 카테고리 필터 적용
if selected_category != "전체":
    filtered_items = filtered_items[
        filtered_items["category"] == selected_category
    ]

    filtered_orders = filtered_orders[
        filtered_orders["order_id"].isin(filtered_items["order_id"])
    ]

# 주문 상태 필터 적용
if selected_status != "전체":
    filtered_orders = filtered_orders[
        filtered_orders["order_status"] == selected_status
    ]

# 최종 선택된 주문에 해당하는 상품만 남기기
filtered_items = filtered_items[
    filtered_items["order_id"].isin(filtered_orders["order_id"])
]

# 8.데이터가 없을 때 안내 메시지를 표시합니다.
if filtered_orders.empty or filtered_items.empty:
    st.warning("선택한 필터 조건에 해당하는 데이터가 없습니다.")
    st.stop()

# 3.핵심 지표를 표시합니다.
# 핵심 지표 계산
# total_orders = len(orders)
# total_sales = (order_items["quantity"] * order_items["unit_price"]).sum()
# total_customers = len(customers)
#->해당 코드는 필터를 적용하기 전 전체 데이터를 계산하는 것이기 때문에 다음과 같이 바꾸주어야 한다.

# 핵심 지표 계산
total_orders = filtered_orders["order_id"].nunique()

total_sales = (
    filtered_items["quantity"] * filtered_items["unit_price"]
).sum()

total_customers = filtered_orders["customer_id"].nunique()

# 핵심 지표 표시
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("총 주문 수", f"{total_orders:,}건")

with col2:
    st.metric("총 매출", f"{total_sales:,.0f}원")

with col3:
    st.metric("총 고객 수", f"{total_customers:,}명")

# 6. 차트 2개 이상을 구현합니다.
st.subheader("카테고리별 매출")
fig1 = create_category_sales_chart(filtered_items)
st.pyplot(fig1, use_container_width=False)

st.subheader("주문 상태별 주문 수")
fig2 = create_order_status_chart(filtered_orders)
st.pyplot(fig2, use_container_width=False)

# 7. 필터 결과를 표로 표시합니다.

st.subheader("필터 적용 결과")

result_table = filtered_orders.merge(
    filtered_items[
        ["order_id", "product_id", "category", "quantity", "unit_price"]
    ],
    on="order_id",
    how="left"
)

# 각 상품의 매출 계산
result_table["sales"] = (
    result_table["quantity"] * result_table["unit_price"]
)

# 표 표시
st.dataframe(result_table, use_container_width=True)

#9.필터별 결과를 직접확인합니다. (없는 조합 찾기)
# 카테고리 + 주문 상태별 주문 건수 확인
check_data = order_items.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
)

check_data = check_data.merge(
    orders[["order_id", "order_status"]],
    on="order_id",
    how="left"
)

st.write(
    check_data.groupby(["category", "order_status"])
    .size()
    .unstack(fill_value=0)
)