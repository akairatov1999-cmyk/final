import streamlit as st
import pandas as pd
import joblib
model = joblib.load('model.joblib')
st.title("Оценщик недвижимости в городе Астана")
st.write("Введите данные о своей квартиры")
area = st.number_input("Площадь (m²)", min_value=10.0, max_value=700.0, value=50.0)
room_count = st.number_input("Количество комнат", min_value=1, max_value=43, value=2)
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
floor = st.number_input("Этаж", min_value=1, value=5)
floor_count = st.number_input("Количество этажей в доме", min_value=1, value=9)
if floor > floor_count:
    st.error("❌ Ошибка: Этаж не может быть больше количества этажей в доме!")
    st.stop()   # Останавливает выполнение программы (предсказание не будет показано)
first_floor = (floor == 1)
last_floor = (floor == floor_count)
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
elevator = st.selectbox(
    "Лифт",
    ["yes", "no"]
)
input_data = pd.DataFrame({
    'owner': ['owner'],
    'complex_name': ['unknown'],
    'house_type': ['monolith'],
    'in_pledge': [False],
    'construction_year': [construction_year],
    'ceiling_height': [ceiling_height],
    'bathroom_info': [bathroom_info],
    'condition': [condition],
    'area': [area],
    'room_count': [room_count],
    'floor': [floor],
    'floor_count': [floor_count],
    'district': [district],
    'complex_class': ['comfort'],
    'parking': [parking],
    'elevator': [elevator],
    'schools_within_500m': [2],
    'kindergartens_within_500m': [2],
    'park_within_1km': [True],
    'distance_to_center': [5],
    'distance_to_botanical_garden': [3],
    'distance_to_triathlon_park': [4],
    'distance_to_astana_park': [4],
    'distance_to_treatment_facility': [6],
    'distance_to_railway_station_1': [8],
    'distance_to_railway_station_2': [9],
    'distance_to_industrial_zone': [10],
    'last_floor': [last_floor],
    'first_floor': [first_floor]
})
input_data = pd.get_dummies(input_data)
columns = joblib.load('columns.joblib')
input_data = input_data.reindex(columns=columns, fill_value=0)
prediction = model.predict(input_data)[0]
st.success(f'Predicted price: {prediction:,.0f} KZT')
