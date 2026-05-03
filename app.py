import streamlit as st
import pandas as pd
import joblib
model = joblib.load('model.joblib')
st.title("Оценщик недвижимости в городе Астана")
st.write("Введите данные о своей квартиры🏠")
in_pledge = st.checkbox("Квартира в залоге?"
                       )
area = st.number_input(
    "Площадь (m²)", 
    min_value=10.0, 
    max_value=700.0, 
    value=50.0
)
room_count = st.number_input(
    "Количество комнат", 
    min_value=1, max_value=40, 
    value=2)
construction_year = st.number_input(
    "Год постройки",
    min_value=1950,
    max_value=2026,
    value=2015
)
ceiling_height = st.number_input(
    "Высота потолка",
    min_value=2.0,
    max_value=5.0,
    value=2.7
)
floor = st.number_input(
    "Этаж", 
    min_value=1,
    max_value=40,
    value=5
)
floor_count = st.number_input(
    "Количество этажей в доме", 
    min_value=1,
    max_value=40,
    value=9
)
elevator = st.selectbox("Лифт", ["Да", "Нет"])
elevator = "yes" if elevator == "Да" else "no"
if floor > floor_count:
    st.error("❌ Ошибка: Этаж не может быть больше количества этажей в доме!")
    st.stop()   # Останавливает выполнение программы (предсказание не будет показано)
if floor_count > 5 and elevator == "no":
    st.error("❌ В доме с более чем 5 этажами должен быть лифт! Пожалуйста, выберите 'Да'.")
    st.stop()
first_floor = (floor == 1)
last_floor = (floor == floor_count)
# Тип дома
house_type_options = {
    "Панельный": "panel",
    "Кирпичный": "brick",
    "Монолитный": "monolith"
}
house_type_label = st.selectbox("Тип дома", list(house_type_options.keys()))
house_type = house_type_options[house_type_label]
# Класс ЖК
complex_class_options = {
    "Эконом": "economy",
    "Комфорт": "comfort",
    "Бизнес": "business",
    "Премиум": "luxury"
}
complex_class_label = st.selectbox("Класс жилого комплекса", list(complex_class_options.keys()))
complex_class = complex_class_options[complex_class_label]
# Район
district_options = {"Алматы": "almaty", "Сарыарка": "saryarka", "Нура": "nura", "Есиль": "esil", "Байконыр": "baikonur"}
district_display = st.selectbox("Район", list(district_options.keys()))
district = district_options[district_display]
# Состояние 
condition_options = {
    "Хорошее": "good",
    "Среднее": "average", 
    "Требует ремонта": "needs repair",
    "Неизвестно": "unknown"
}
condition_label = st.selectbox("Состояние", list(condition_options.keys()))
condition = condition_options[condition_label]
# Ванная
bathroom_options = {
    "Совмещённый": "combined",
    "Раздельный": "separate",
    "2 и более": "2 or more",
    "Неизвестно": "unknown"
}
bathroom_label = st.selectbox("Ванная", list(bathroom_options.keys()))
bathroom_info = bathroom_options[bathroom_label]
# Паркинг
parking = st.selectbox("Парковка", ["Да", "Нет"])
parking = "yes" if parking == "Да" else "no"
input_data = pd.DataFrame({
    'owner': ['owner'],
    'house_type': [house_type],
    'in_pledge': [in_pledge],
    'construction_year': [construction_year],
    'ceiling_height': [ceiling_height],
    'bathroom_info': [bathroom_info],
    'condition': [condition],
    'area': [area],
    'room_count': [room_count],
    'floor': [floor],
    'floor_count': [floor_count],
    'district': [district],
    'complex_class': [complex_class],
    'parking': [parking],
    'elevator': [elevator],
    'last_floor': [last_floor],
    'first_floor': [first_floor]
})
input_data = pd.get_dummies(input_data)
columns = joblib.load('columns.joblib')
input_data = input_data.reindex(columns=columns, fill_value=0)
prediction = model.predict(input_data)[0]
st.success(f'Predicted price: {prediction:,.0f} KZT')

from openai import OpenAI

client = OpenAI(api_key="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")
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)
st.title("Помощник по недвижимости- ChatGPT")

user_input = st.text_input("Рекомендация")

if st.button("Send"):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    st.write(response.choices[0].message.content)
