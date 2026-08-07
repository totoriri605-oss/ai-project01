# 6. 차트 2개 이상을 구현합니다.

import matplotlib.pyplot as plt
from matplotlib import font_manager

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()

plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False


# 카테고리별 매출 차트
def create_category_sales_chart(filtered_items):
    data = filtered_items.copy()

    # 각 상품 주문의 매출 계산
    data["sales"] = data["quantity"] * data["unit_price"]

    # 카테고리별 매출 합계
    category_sales = data.groupby("category")["sales"].sum()

    # 차트 만들기
    fig, ax = plt.subplots(figsize=(7, 4))
    category_sales.plot(kind="bar", ax=ax)

    ax.set_xlabel("카테고리")
    ax.set_ylabel("매출")

    plt.tight_layout()

    return fig


# 주문 상태별 주문 수 차트
def create_order_status_chart(filtered_orders):

    # 주문 상태별 주문 수 계산
    status_counts = filtered_orders["order_status"].value_counts()

    # 차트 만들기
    fig, ax = plt.subplots(figsize=(7, 4))
    status_counts.plot(kind="bar", ax=ax)

    ax.set_xlabel("주문 상태")
    ax.set_ylabel("주문 수")

    plt.tight_layout()

    return fig