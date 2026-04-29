import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="eme Perfume Store", page_icon="🌸", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

.stApp {
    background: linear-gradient(135deg, #fff1f5 0%, #ffffff 55%, #fff7f9 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff0f5, #ffffff);
    border-right: 1px solid #ffd6e3;
}

.main-title {
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    color: #262633;
    margin-top: 20px;
}

.eme {
    color: #ff5fa2;
    font-style: italic;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 17px;
    margin-bottom: 25px;
}

.logo-box {
    text-align: center;
    padding: 10px 0 25px 0;
}

.logo-bottle {
    font-size: 58px;
}

.logo-eme {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 46px;
    color: #8b5d5d;
    margin-top: -10px;
}

.logo-small {
    letter-spacing: 7px;
    font-size: 13px;
    color: #9b6c6c;
}

.card {
    background: white;
    border: 1px solid #ffd6e3;
    border-radius: 15px;
    box-shadow: 0 6px 18px rgba(255, 105, 150, 0.12);
    padding: 12px;
    margin-bottom: 18px;
}

.product-title {
    font-size: 18px;
    font-weight: 700;
    color: #292938;
}

.product-desc {
    color: #666;
    font-size: 14px;
    min-height: 42px;
}

.price {
    font-weight: 800;
    color: #111;
    font-size: 16px;
}

.badge {
    background: #ffe6f0;
    color: #ff4f93;
    padding: 5px 12px;
    border-radius: 12px;
    font-size: 13px;
    display: inline-block;
}

.cart-box {
    background: white;
    border: 1px solid #ffd6e3;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 8px 22px rgba(255, 105, 150, 0.12);
}

.cart-item {
    border-bottom: 1px solid #ffe2ea;
    padding: 10px 0;
}

.checkout-box {
    background: white;
    border: 1px solid #ffd6e3;
    border-radius: 18px;
    padding: 22px;
    margin-top: 25px;
    box-shadow: 0 8px 22px rgba(255, 105, 150, 0.12);
}

.footer {
    text-align: center;
    color: #777;
    padding: 20px;
    border-top: 1px solid #ffd6e3;
}
</style>
""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "show_checkout" not in st.session_state:
    st.session_state.show_checkout = False

products = pd.read_csv("products.csv")

with st.sidebar:
    st.markdown("""
    <div class="logo-box">
        <div class="logo-bottle">🌷</div>
        <div class="logo-eme">eme</div>
        <div class="logo-small">PERFUME</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🌸 Categories")

    categories = ["All", "Women", "Men", "Unisex", "Luxury", "Floral", "Woody"]
    selected_category = st.radio("Choose category", categories)

    st.markdown("### 💎 Price Range")
    max_price = st.slider(
        "Maximum price",
        int(products["price"].min()),
        int(products["price"].max()),
        int(products["price"].max())
    )

    st.markdown("""
    <br>
    <div style="background:#ffeaf2;padding:20px;border-radius:15px;text-align:center;">
        <b>🌸 About <span style="color:#ff5fa2;">eme</span></b>
        <p style="font-size:14px;color:#666;">At eme, we believe every scent tells a story. Find yours.</p>
        <span style="color:#ff5fa2;">♥</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">Welcome to <span class="eme">eme</span> Perfume Store</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover your signature scent 💗</div>', unsafe_allow_html=True)

top1, top2, top3 = st.columns([3, 1, 1])

with top1:
    search = st.text_input("", placeholder="Search for perfumes...")

with top2:
    sort_option = st.selectbox("Sort by", ["Newest", "Price: Low to High", "Price: High to Low"])

with top3:
    cart_count = sum(st.session_state.cart.values())
    st.markdown(f"""
    <div style="background:#ff6f9f;color:white;padding:13px;border-radius:10px;text-align:center;margin-top:28px;">
        🛍️ Cart ({cart_count})
    </div>
    """, unsafe_allow_html=True)

filtered = products[products["price"] <= max_price]

if selected_category != "All":
    filtered = filtered[filtered["category"] == selected_category]

if search:
    filtered = filtered[filtered["name"].str.contains(search, case=False, na=False)]

if sort_option == "Price: Low to High":
    filtered = filtered.sort_values("price", ascending=True)
elif sort_option == "Price: High to Low":
    filtered = filtered.sort_values("price", ascending=False)

main_col, cart_col = st.columns([4, 1.4])

with main_col:
    st.markdown("## Available Perfumes")

    cols = st.columns(4)

    for index, row in filtered.reset_index(drop=True).iterrows():
        with cols[index % 4]:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.image(row["image"], use_container_width=True)

            st.markdown(f'<div class="product-title">{row["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="product-desc">{row["description"]}</div>', unsafe_allow_html=True)

            left, right = st.columns([1, 1])
            with left:
                st.markdown(f'<div class="price">{row["price"]} SAR</div>', unsafe_allow_html=True)
            with right:
                st.markdown(f'<div class="badge">{row["category"]}</div>', unsafe_allow_html=True)

            if st.button("🛍️ Add to cart", key=f"add_{index}_{row['name']}"):
                product_name = row["name"]
                if product_name in st.session_state.cart:
                    st.session_state.cart[product_name] += 1
                else:
                    st.session_state.cart[product_name] = 1
                st.session_state.show_checkout = False
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

with cart_col:
    st.markdown('<div class="cart-box">', unsafe_allow_html=True)
    st.markdown("## 🛍️ Your Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty")
    else:
        total = 0

        for name, qty in list(st.session_state.cart.items()):
            product = products[products["name"] == name].iloc[0]
            item_total = product["price"] * qty
            total += item_total

            st.markdown('<div class="cart-item">', unsafe_allow_html=True)
            st.image(product["image"], width=70)
            st.write(f"**{name}**")
            st.write(f"{product['price']} SAR × {qty}")

            minus, plus, remove = st.columns(3)

            with minus:
                if st.button("−", key=f"minus_{name}"):
                    st.session_state.cart[name] -= 1
                    if st.session_state.cart[name] <= 0:
                        del st.session_state.cart[name]
                    st.rerun()

            with plus:
                if st.button("+", key=f"plus_{name}"):
                    st.session_state.cart[name] += 1
                    st.rerun()

            with remove:
                if st.button("🗑️", key=f"remove_{name}"):
                    del st.session_state.cart[name]
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"### Total: {total} SAR")

        if st.button("Checkout", type="primary"):
            st.session_state.show_checkout = True
            st.rerun()

        if st.button("Clear Cart"):
            st.session_state.cart = {}
            st.session_state.show_checkout = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_checkout and st.session_state.cart:
    st.markdown('<div class="checkout-box">', unsafe_allow_html=True)
    st.markdown("## 💳 Complete Your Order")

    order_total = 0
    order_items = []

    for name, qty in st.session_state.cart.items():
        product = products[products["name"] == name].iloc[0]
        item_total = product["price"] * qty
        order_total += item_total
        order_items.append(f"{name} x{qty}")

    st.write("### Order Summary")
    for item in order_items:
        st.write(f"- {item}")

    st.markdown(f"### Total: {order_total} SAR")

    with st.form("checkout_form"):
        customer_name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        address = st.text_area("Delivery Address")

        payment_method = st.selectbox(
            "Payment Method",
            ["Cash on Delivery", "Mada", "Apple Pay", "Visa / Mastercard"]
        )

        notes = st.text_area("Notes Optional")

        submit_order = st.form_submit_button("Place Order")

        if submit_order:
            if customer_name.strip() == "" or phone.strip() == "" or address.strip() == "":
                st.error("Please fill Full Name, Phone Number, and Delivery Address.")
            else:
                new_order = pd.DataFrame([{
                    "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "customer_name": customer_name,
                    "phone": phone,
                    "email": email,
                    "address": address,
                    "payment_method": payment_method,
                    "items": ", ".join(order_items),
                    "total": order_total,
                    "notes": notes
                }])

                try:
                    old_orders = pd.read_csv("orders.csv")
                    all_orders = pd.concat([old_orders, new_order], ignore_index=True)
                except FileNotFoundError:
                    all_orders = new_order

                all_orders.to_csv("orders.csv", index=False)

                st.success(f"Order placed successfully! Total: {order_total} SAR 💗")
                st.balloons()

                st.session_state.cart = {}
                st.session_state.show_checkout = False

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    © 2024 eme Perfume Store &nbsp; | &nbsp; Made with 💗 by <i>eme</i>
</div>
""", unsafe_allow_html=True)