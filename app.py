import streamlit as st
import pandas as pd
import joblib
model = joblib.load('model.joblib')
st.title("Оценщик недвижимости в городе Астана")
st.write("Введите данные о своей квартиры")
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
    value=5
)
floor_count = st.number_input(
    "Количество этажей в доме", 
    min_value=1, 
    value=9
)
elevator = st.selectbox(
    "Лифт",
    ["yes", "no"]
)
if floor > floor_count:
    st.error("❌ Ошибка: Этаж не может быть больше количества этажей в доме!")
    st.stop()   # Останавливает выполнение программы (предсказание не будет показано)
if floor_count > 5 and elevator == "no":
    st.error("❌ В доме с более чем 5 этажами должен быть лифт! Пожалуйста, выберите 'yes'.")
    st.stop()
first_floor = (floor == 1)
last_floor = (floor == floor_count)
house_type = st.selectbox(
    "Тип дома", 
    ["panel", "brick", "monolith", "block"]
)
complex_class = st.selectbox(
    "Класс жилого комплекса", 
                             ["economy", "comfort", "business", "luxury"]
)
district = st.selectbox(
    "Район",
    ["Алматы", "Есиль", "Сарыарка", "Байконур"]
)
condition = st.selectbox(
    "Состояние",
    ["good", "average", "needs repair", "unknown"]
)
bathroom_info = st.selectbox(
    "Ванная",
    ["combined", "separate", "2 or more", "unknown"]
)
parking = st.selectbox(
    "Паркинг",
    ["yes", "no"]
)
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
