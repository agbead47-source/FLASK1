import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# 💡 세션(장바구니)을 사용하기 위한 필수 보안 키입니다! 
app.secret_key = "autumn_stationery_secret_key" 
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

products_data = [
    {
        "id": 1,
        "name": "TRAVELER'S NOTEBOOK / CAMEL",
        "desc": "시간이 지날수록 짙어지는 당신만의 에이징, 오리지널 카멜.",
        "price": "54,000 KRW",
        "image": "/static/images/item1.jpg"
    },
    {
        "id": 2,
        "name": "BRASS FOUNTAIN PEN",
        "desc": "황동이 뿜어내는 빈티지한 무게감, 닙을 타고 흐르는 기록.",
        "price": "82,000 KRW",
        "image": "/static/images/item2.jpg"
    },
    {
        "id": 3,
        "name": "AUTUMN RAIN INK",
        "desc": "도쿄의 젖은 아스팔트와 낙엽을 닮은 차분한 브라운 잉크.",
        "price": "24,000 KRW",
        "image": "/static/images/item3.jpg"
    },
    {
        "id": 4,
        "name": "BRASS CLIP / AIRPLANE",
        "desc": "바람에 날리는 페이지를 잡아주는 여행자의 시그니처 클립.",
        "price": "16,000 KRW",
        "image": "/static/images/item4.jpg"
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html', products=products_data)

@app.route('/shop/<int:product_id>')
def detail(product_id):
    selected_product = next((p for p in products_data if p['id'] == product_id), None)
    if selected_product:
        return render_template('detail.html', product=selected_product)
    return "NOT FOUND", 404

# 🛒 장바구니 담기
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    cart = session['cart']
    product = next((p for p in products_data if p['id'] == product_id), None)
    
    if product:
        cart.append(product)
        session['cart'] = cart
        session.modified = True
        
    return redirect(url_for('cart_page'))

# 🛒 장바구니 보기
@app.route('/cart')
def cart_page():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

# 🗑️ 장바구니 비우기
@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart_page'))

# 🤖 챗봇 API
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 힙하고 트렌디한 문구 편집숍의 시크한 큐레이터입니다. 트래블러스 팩토리 감성을 사랑하며, 답변은 짧고 감각적으로 해주세요."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": "SYSTEM ERROR: 직원이 커피를 내리고 있습니다. ☕"})

if __name__ == '__main__':
    app.run(debug=True)