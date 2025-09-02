from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector

app = Flask(__name__)

# 🔐 Replace with your Hugging Face token
HF_API_KEY = "hf_your_token_here"  # Get at: https://huggingface.co/settings/tokens

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='MyPass123!',  # ← Your MySQL root password
        database='mealmatch'
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    ingredients = request.form['ingredients']
    prompt = f"Suggest 3 simple recipes using: {ingredients}. Include name, ingredients, and instructions."

    try:
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers=headers,
            json={"inputs": prompt}
        )

        if response.status_code != 200:
            return jsonify({"error": f"AI error: {response.status_code}"}), 500

        result = response.json()
        recipe_text = result[0]['generated_text'] if isinstance(result, list) and len(result) > 0 else str(result)

        # Save to DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_inputs (user_ingredients, generated_recipe) VALUES (%s, %s)", 
                      (ingredients, recipe_text))
        conn.commit()
        conn.close()

        return jsonify({"recipes": recipe_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)