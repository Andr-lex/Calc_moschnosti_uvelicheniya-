import streamlit as st
import math

st.set_page_config(page_title="Калькулятор производственных мощностей", layout="wide")

st.title("📊 Калькулятор потребности в площадях и рабочих местах")
st.subheader("Расчёт нормативной потребности в производственных, складских и бытовых площадях")

st.markdown("""
Инструмент рассчитывает нормативную потребность в рабочих местах и площадях исходя из
планового объёма выпуска и действующих норм выработки, и сравнивает её с предлагаемой
арендодателем площадью.

**Как пользоваться:** введите параметры в левой панели — расчёт и сравнение с предложением
арендодателя обновятся автоматически.
""")

st.sidebar.header("📝 Исходные данные")
val_plan = st.sidebar.number_input("Плановый годовой выпуск изделий (шт/год)", value=640000, step=10000)
val_fact = st.sidebar.number_input("Фактический выпуск за последние 12 месяцев (шт/год)", value=268000, step=10000)
val_shifts = st.sidebar.number_input("Число рабочих смен", value=2, min_value=1, max_value=3)
val_shift_hours = st.sidebar.number_input("Продолжительность смены (часов)", value=8, min_value=4, max_value=12)
val_fund = st.sidebar.number_input("Годовой фонд рабочего времени (часов/год)", value=1970, step=10)
val_norm_output = st.sidebar.number_input("Норма выработки на одно рабочее место (шт/год)", value=2800, step=100)
val_labor_intensity = st.sidebar.number_input("Трудоёмкость изготовления изделия (нормо-часов)", value=0.70, step=0.05, format="%.2f")
val_norm_fulfillment = st.sidebar.number_input("Коэффициент выполнения норм выработки", value=1.05, step=0.01, format="%.2f")

col1, col2 = st.columns(2)

with col1:
    st.header("⚙️ Рабочие места и производственная площадь")

    req_places = math.ceil(val_plan / val_norm_output)
    st.metric("Требуется рабочих мест всего", f"{req_places} мест")

    fact_places = st.number_input("Фактически развёрнуто мест сегодня", value=186)
    add_places = max(0, req_places - fact_places)
    st.metric("Требуется дополнительно развернуть", f"{add_places} мест")

    norm_sq = st.number_input("Норма площади на одно рабочее место (кв.м.)", value=4.5, step=0.1)
    add_prod_sq_pure = add_places * norm_sq
    k_passes = st.number_input("Коэффициент проходов и проездов", value=0.30, step=0.05)
    add_prod_sq_total = add_prod_sq_pure * (1.0 + k_passes)

    st.metric("Дополнительная производственная площадь", f"{add_prod_sq_total:.2f} кв.м.")

with col2:
    st.header("🏢 Складские, бытовые площади и итог")

    add_sklad_sq = st.number_input("Дополнительная складская площадь (кв.м.)", value=34.30, step=1.0)

    add_staff_shift = math.ceil(add_places / val_shifts)
    norm_byt = st.number_input("Санитарная норма бытовой площади на 1 чел. (кв.м.)", value=1.3, step=0.1)
    add_byt_sq = add_staff_shift * norm_byt
    st.metric("Дополнительная бытовая и административная площадь", f"{add_byt_sq:.2f} кв.м.")

    st.markdown("---")
    st.subheader("⚖️ Сравнение с предложением арендодателя")

    total_needed_add = add_prod_sq_total + add_sklad_sq + add_byt_sq
    st.write(f"**Итого требуется дополнительно по нормативам:** {total_needed_add:.2f} кв.м.")

    fact_sq = st.number_input("Фактическая площадь до расширения (кв.м.)", value=2400.00, step=10.0)
    total_limit = total_needed_add + fact_sq
    st.write(f"**Нормативно обоснованная площадь всего:** {total_limit:.2f} кв.м.")

    offer_sq = st.number_input("Предлагается арендодателем (кв.м.)", value=2778.70, step=10.0)
    diff = total_limit - offer_sq

    if diff < 0:
        st.error(f"🚨 Предложение превышает нормативный лимит на {abs(diff):.2f} кв.м.")
        st.markdown(f"""
        Заявленная арендодателем площадь превышает расчётный технологический лимит на
        `{abs(diff):.2f} кв.м.` Включение этой площади в договор приведёт к необоснованному
        росту затрат. Рекомендуется скорректировать условия договора.
        """)
    else:
        st.success(f"✅ Предложение в пределах норматива. Резерв: {diff:.2f} кв.м.")
