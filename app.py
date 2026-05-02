from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

# Загружаем обученный пайплайн
model = joblib.load('bmw_global_model.joblib')

# Инициализируем приложение
app = Flask(__name__)

# Список признаков в том же порядке, что и при обучении
FEATURES = ['Units_Sold', 'Avg_Price_EUR', 'BEV_Share', 'Premium_Share', 'GDP_Growth', 'Fuel_Price_Index']

@app.route('/', methods=['GET'])
def home():
    return "BMW Prediction API is running"

@app.route('/predict', methods=['POST'])
def predict():
    """
    Эндпоинт для получения предсказаний.
    Ожидает JSON с ключом 'data' — список объектов, каждый из которых содержит значения всех признаков.
    Пример:
    {
        "data": [
            {"Units_Sold": 100, "Avg_Price_EUR": 25000, "BEV_Share": 0.1, "Premium_Share": 0.2, "GDP_Growth": 2.5, "Fuel_Price_Index": 1.2},
            ...
        ]
    }
    """
    try:
        input_data = request.get_json()
        if not input_data or 'data' not in input_data:
            return jsonify({'error': 'Missing "data" field in JSON'}), 400

        records = input_data['data']
        # Преобразуем список записей в DataFrame
        df_input = pd.DataFrame(records)
        # Проверяем, что все необходимые признаки присутствуют
        missing = set(FEATURES) - set(df_input.columns)
        if missing:
            return jsonify({'error': f'Missing features: {missing}'}), 400

        # Извлекаем признаки в правильном порядке
        X = df_input[FEATURES].values

        # Предсказание
        predictions = model.predict(X)
        # Если нужны вероятности, раскомментируйте следующую строку
        # probabilities = model.predict_proba(X)[:, 1]

        # Формируем ответ
        result = []
        for i, pred in enumerate(predictions):
            item = {
                'prediction': int(pred),
                # 'probability': float(probabilities[i])
            }
            result.append(item)

        return jsonify({'predictions': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# === 6. Запуск ===
if __name__ == '__main__':
    print()
    print("=" * 50)
    print("  Сервер запущен!")
    print("  http://localhost:5000")
    print("=" * 50)
    print()
    # debug=False — для стабильной работы
    # host='0.0.0.0' — слушаем со всех адресов (нужно для ngrok)
    app.run(debug=False, host='0.0.0.0', use_reloader=False, port=5000)
