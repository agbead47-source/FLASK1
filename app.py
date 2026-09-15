import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) # 깃허브 업로드용 안전한 키 세팅!

# 힙한 트래블러스 팩토리 감성의 상품 데이터
products_data = [
    {
        "id": 1,
        "name": "TRAVELER'S NOTEBOOK / CAMEL",
        "desc": "시간이 지날수록 짙어지는 당신만의 에이징, 오리지널 카멜.",
        "price": "54,000 KRW",
        "image": "https://images.unsplash.com/photo-1585675100414-22cb7f5e1844?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 2,
        "name": "BRASS FOUNTAIN PEN",
        "desc": "황동이 뿜어내는 빈티지한 무게감, 닙을 타고 흐르는 기록.",
        "price": "82,000 KRW",
        "image": "https://images.unsplash.com/photo-1580569214296-5cb2afe114bf?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 3,
        "name": "AUTUMN RAIN INK",
        "desc": "도쿄의 젖은 아스팔트와 낙엽을 닮은 차분한 브라운 잉크.",
        "price": "24,000 KRW",
        "image": "https://images.unsplash.com/photo-1524311583145-d5593bd24083?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 4,
        "name": "BRASS CLIP / AIRPLANE",
        "desc": "바람에 날리는 페이지를 잡아주는 여행자의 시그니처 클립.",
        "price": "16,000 KRW",
        "image": "https://images.unsplash.com/photo-1587847496664-585309320e6a?auto=format&fit=crop&w=800&q=80"
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