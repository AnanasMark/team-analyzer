import streamlit as st
import random
from collections import Counter

# Опции выбора
roles = ["Product Owner", "Project Manager", "Tech Lead", "Business Analyst", "System Analyst", "Developer", "QA"]
skill_levels = ["junior", "middle", "senior", "неадекватен"]
behavior_types = ["инициативный", "флегматичный", "оппозиционный", "реактивный", "молчаливый"]
motivations = ["высокая", "средняя", "низкая"]
external_events = [
    "конфликты между участниками",
    "уходит ключевой сотрудник",
    "непонятная цель",
    "борьба двух лидеров",
    "инициатива от QA",
    "положительный фидбек от пользователей",
    "перегруз команды разработки",
    "нет мотивации",
    "сильная мотивация",
    "игнор в чате"
]

# Интерфейс Streamlit
st.title("Прогноз успеха команды")
st.subheader("Добавьте участников, ожидания и внешние события")

team = []
st.markdown("**Ожидания от команды:**")
deadline = st.selectbox("Срок реализации проекта/продукта 🕒", ["", "1 месяц", "3 месяца", "6 месяцев", "1 год"], index=0, help="Чем короче срок, тем выше нагрузка и риски. Оптимальные сроки — 3-6 месяцев.")
expectation = st.selectbox("Тип результата 🎯", ["", "Фича", "MVP", "Концепт", "Готовый продукт"], index=0, help="Фича — простая функция. MVP — минимально жизнеспособный продукт. Концепт — идея в виде прототипа. Готовый продукт — полноценное решение.")

st.markdown("**Выберите внешние события:**")
selected_events = st.multiselect("Факторы, влияющие на команду 🌐", external_events, help="Внешние обстоятельства, способные повлиять на результат. Учитываются как позитивные, так и дестабилизирующие.")

num_members = st.number_input("Сколько участников в команде? 👥", min_value=1, max_value=20, value=5, step=1, help="Количество членов команды. Оптимально 5-10 человек.")

for i in range(int(num_members)):
    st.markdown(f"### Участник {i+1}")
    cols = st.columns(4)
    with cols[0]:
        role = st.selectbox(f"Роль ❓", roles, key=f"role_{i}", help="Должность или функция участника в команде")
    with cols[1]:
        skill = st.selectbox(f"Навык 📚", skill_levels, key=f"skill_{i}", help="Оценка уровня компетенций участника")
    with cols[2]:
        behavior = st.selectbox(f"Поведение 🧠", behavior_types, key=f"beh_{i}", help="Тип поведения влияет на взаимодействие в команде")
    with cols[3]:
        motivation = st.selectbox(f"Мотивация 🔥", motivations, key=f"mot_{i}", help="Настрой и вовлеченность участника")
    team.append({"role": role, "skill": skill, "behavior": behavior, "motivation": motivation})

if st.button("Анализировать"):
    from analyzer import success_level  # Предположим, что логика оценки вынесена в analyzer.py
    result, probability, comments = success_level(team, selected_events, expectation, deadline)
    st.markdown(f"### 🧠 Прогноз: **{result}**")
    st.markdown(f"#### 🔢 Вероятность успеха: **{probability}%**")
    if comments:
        st.markdown("#### 📌 Комментарии:")
        for comment in comments:
            st.markdown(f"- {comment}")

    # Уточнение условий высокого шанса успеха
    high_chance_notes = []
    if probability >= 70:
        high_chance_notes.append("Сбалансированная команда с необходимыми ролями")
        if any(p['behavior'] == "инициативный" for p in team):
            high_chance_notes.append("Присутствуют инициативные участники")
        if all(p['motivation'] != "низкая" for p in team):
            high_chance_notes.append("Отсутствует низкая мотивация")
        if any("положительный фидбек" in e for e in selected_events):
            high_chance_notes.append("Получен положительный фидбек от пользователей")

    # Дополнительное условие: полная команда, адекватные сроки и отсутствие отрицательных и положительных событий
    required_roles = {"Developer", "QA", "Business Analyst", "Project Manager", "Product Owner"}
    team_roles = set(p['role'] for p in team)
    negative_events = [
        "конфликты между участниками", "уходит ключевой сотрудник", "непонятная цель",
        "борьба двух лидеров", "перегруз команды разработки", "нет мотивации", "игнор в чате"]
    positive_events = ["положительный фидбек от пользователей", "сильная мотивация", "инициатива от QA"]

    if required_roles.intersection(team_roles) and not any(e in selected_events for e in negative_events + positive_events):
        if deadline in ["3 месяца", "6 месяцев"]:
            probability = max(probability, 95)
            high_chance_notes.append("Полная команда, без внешних угроз и стимулов, с адекватными сроками — высокая структурная устойчивость")

    if high_chance_notes:
        st.markdown("#### ⭐ Почему шансы высоки:")
        for note in high_chance_notes:
            st.markdown(f"- {note}")

    # Финальный вывод
    if result == "Провал":
        st.warning("Рекомендуется пересмотреть состав команды или устранить внешние препятствия")
    elif result == "Сырой прототип":
        st.info("Есть зацепка, но не хватает стабильности или компетенций")
    elif result == "Частичный MVP":
        st.success("Команда может показать результат, но не в полном объеме")
    elif result == "Успешный MVP":
        st.balloons()
        st.success("Высокий шанс выпустить работающий MVP!")
    elif result.startswith("Фича") or result.startswith("Маленький результат"):
        st.info("Частичный, но полезный результат возможен при фокусе на простых задачах")