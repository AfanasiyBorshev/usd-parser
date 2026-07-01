import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# Настройка страницы
st.set_page_config(page_title="Курс Доллара ПСБ", page_icon="💵", layout="wide")

st.title("💵 Курс доллара (ПС Банк)")
st.write("Данные автоматически собираются каждый час с сайта ПС Банка.")

try:
    # Читаем CSV файл
    df = pd.read_csv('rates.csv', sep=';', encoding='utf-8-sig')
    
    # Создаем удобную колонку для графика
    df['Дата и время'] = pd.to_datetime(df['Дата'] + ' ' + df['Время'])
    
    # Показываем таблицу
    st.subheader("📊 Таблица курсов")
    st.dataframe(df)
    
    # Рисуем график
    st.subheader(" График изменения курса")
    fig = px.line(df, x='Дата и время', y=['Покупка', 'Продажа'], 
                  title='Динамика курса USD (Наличные)',
                  labels={'value': 'Курс (₽)', 'variable': 'Тип курса'},
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Кнопка скачивания в Excel
    st.subheader("⬇️ Скачать данные")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Скачать в Excel (.xlsx)",
        data=excel_data,
        file_name=f'usd_rates_{datetime.now().strftime("%Y%m%d")}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

except FileNotFoundError:
    st.error("❌ Файл rates.csv не найден! Сначала нужно запустить парсер.")
except Exception as e:
    st.error(f"Произошла ошибка при чтении файла: {e}")
