import streamlit as st
import math

st.set_page_config(page_title="Калькулятор Формы 15", layout="wide")

st.title("📊 Интерактивный калькулятор потребности в мощностях (ФОРМА № 15)")
st.subheader

st.markdown("""
Этот калькулятор предназначен для верификации заявок на расширение площадей 
**Инструкция:** Введите параметры в левой панели. Расчёт потребности и анализ излишков произойдут автоматически.
""")

# Левая колонка - Ввод данных
st.sidebar.header("📝 1. Исходные данные")
val_1 = st.sidebar.number_input("Плановый годовой выпуск изделий после расширения (шт/год)", value=640000, step=10000)
val_2 = st.sidebar.number_input("Фактический выпуск за последние 12 месяцев (шт/год)", value=268000, step=10000)
val_3 = st.sidebar.number_input("Режим работы (число рабочих смен)", value=2, min_value=1, max_value=3)
val_4 = st.sidebar.number_input("Продолжительность рабочей смены (часов)", value=8, min_value=4, max_value=12)
val_5 = st.sidebar.number_input("Годовой фонд рабочего времени (часов/год)", value=1970, step=10)
val_6 = st.sidebar.number_input("Норма выработки на одно рабочее место швеи (шт/год)", value=2800, step=100)
val_7 = st.sidebar.number_input("Трудоемкость пошива одного изделия (нормо-часов)", value=0.70, step=0.05, format="%.2f")
val_8 = st.sidebar.number_input("Коэффициент выполнения норм выработки", value=1.05, step=0.01, format="%.2f")

# Правая колонка - Расчеты
col1, col2 = st.columns(2)

with col1:
    st.header("⚙️ 2. Технологический расчет")
    
    # Расчет рабочих мест
    req_places = math.ceil(val_1 / val_6)
    st.metric("Необходимо рабочих мест швей всего", f"{req_places} мест")
    
    fact_places = st.number_input("Фактически развернуто мест на сегодня (ввод факта)", value=186)
    add_places = max(0, req_places - fact_places)
    st.metric("Требуется дополнительно развернуть", f"{add_places} мест")
    
    # Производственная площадь
    norm_sq = st.number_input("Норма площади на одно рабочее место швеи (кв.м.)", value=4.5, step=0.1)
    add_prod_sq_pure = add_places * norm_sq
    k_passes = st.number_input("Коэффициент проходов и проездов (30% = 0.30)", value=0.30, step=0.05)
    add_prod_sq_total = add_prod_sq_pure * (1.0 + k_passes)
    
    st.metric("Обоснованный прирост производственной площади", f"{add_prod_sq_total:.2f} кв.м.")

with col2:
    st.header("🏢 3. Складские, бытовые площади и итоги")
    
    add_sklad_sq = st.number_input("Обоснованный прирост складской площади (кв.м.)", value=34.30, step=1.0)
    
    # Бытовая площадь
    add_staff_shift = math.ceil(add_places / val_3)
    norm_byt = st.number_input("Санитарная норма бытовой площади на 1 человека (кв.м.)", value=1.3, step=0.1)
    add_byt_sq = add_staff_shift * norm_byt
    st.metric("Обоснованный прирост бытовой площади", f"{add_byt_sq:.2f} кв.м.")
    
    st.markdown("---")
    st.subheader("⚖️ Баланс и верификация предложения")
    
    total_needed_add = add_prod_sq_total + add_sklad_sq + add_byt_sq
    st.write(f"**Итого требуется дополнительно по нормативам:** {total_needed_add:.2f} кв.м.")
    
    fact_sq = st.number_input("Фактическая площадь ОП до расширения (кв.м.)", value=2400.00, step=10.0)
    total_limit = total_needed_add + fact_sq
    st.write(f"**Предельно допустимая общая площадь всего:** {total_limit:.2f} кв.м.")
    
    offer_sq = st.number_input("Предлагается собственником к подписанию по договору (кв.м.)", value=2778.70, step=10.0)
    diff = total_limit - offer_sq
    
    if diff < 0:
        st.error(f"🚨 ВНИМАНИЕ! Выявлены излишки площадей: {abs(diff):.2f} кв.м.")
        st.markdown(f"""
        **Рекомендация:** Собственник навязывает вам лишние `{abs(diff):.2f} кв.м.`, которые не подтверждены технологическим расчетом. 
        Принятие этих затрат приведет к завышению себестоимости!
        **Данную разницу необходимо исключить из договора аренды.**
        """)
    else:
        st.success(f"✅ Расчет чистый. Навязанных излишков не обнаружено. Свободный резерв: {diff:.2f} кв.м.")
