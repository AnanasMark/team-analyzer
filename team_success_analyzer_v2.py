
import streamlit as st
import random
from collections import Counter

# Опции выбора
roles = ["Product Owner", "Project Manager", "Tech Lead", "Business Analyst", "System Analyst", "Developer", "QA"]
skill_levels = ["", "junior", "middle", "senior", "неадекватен"]
behavior_types = ["", "инициативный", "флегматичный", "оппозиционный", "реактивный", "молчаливый"]
motivations = ["", "высокая", "средняя", "низкая"]
external_events = [
    "конфликт между участниками",
    "уходит разработчик",
    "непонятная цель",
    "спонтанный лидер",
    "инициатива от QA",
    "фидбек от пользователей",
    "перегруз аналитиков",
    "потеря мотивации",
    "регулярные стендапы",
    "игнор в чате"
]

# Модель оценки

def success_level(team, events):
    dev_strength = sum(1 for p in team if p['role'] == "Developer" and p['skill'] in ["middle", "senior"])
    qa_ok = any(p['role'] == "QA" and p['skill'] != "неадекватен" for p in team)
    ba_ok = any(p['role'] in ["Business Analyst", "System Analyst"] and p['skill'] != "неадекватен" for p in team)

    synergy_signals = ["инициатива", "фидбек", "стендапы"]
    disruption_signals = ["конфликт", "уходит", "игнор", "перегруз", "потеря"]

    synergy_score = sum(any(s in e for s in synergy_signals) for e in events)
    disruption_score = sum(any(s in e for s in disruption_signals) for e in events)

    if dev_strength >= 3 and qa_ok and ba_ok and synergy_score >= 2 and disruption_score == 0:
        return "Успешный MVP"
    elif dev_strength >= 2 and qa_ok and ba_ok and synergy_score >= 1 and disruption_score <= 1:
        return "Частичный MVP"
    elif dev_strength >= 2 and (qa_ok or ba_ok) and disruption_score <= 2:
        return "Сырой прототип"
    else:
        return "Провал"

# Streamlit UI
st.title("Прогноз успеха команды")
st.subheader("Добавьте участников, ожидания и внешние события")

team = []
with st.form("team_form"):
    num_members = st.number_input("Сколько участников в команде?", min_value=1, max_value=20, value=5)

    for i in range(num_members):
        with st.expander(f"Участник {i+1}", expanded=True):
            role = st.selectbox(f"Роль участника {i+1}", roles, key=f"role_{i}")
            skill = st.selectbox(f"Навык участника {i+1}", skill_levels, key=f"skill_{i}")
            behavior = st.selectbox(f"Поведение участника {i+1}", behavior_types, key=f"beh_{i}")
            motivation = st.selectbox(f"Мотивация участника {i+1}", motivations, key=f"mot_{i}")
            team.append({"role": role, "skill": skill, "behavior": behavior, "motivation": motivation})

    st.markdown("**Выберите внешние события:**")
    selected_events = st.multiselect("Факторы, влияющие на команду", external_events)

    st.markdown("**Ожидания от команды:**")
    deadline = st.selectbox("Срок реализации", ["", "3 месяца", "6 месяцев", "1 год"], index=0)
    expectation = st.selectbox("Тип результата", ["", "MVP", "Концепт", "Готовый продукт"], index=0)

    submitted = st.form_submit_button("Анализировать")

if submitted:
    result = success_level(team, selected_events)
    st.markdown(f"### 🧠 Прогноз: **{result}**")
    if result == "Провал":
        st.warning("Рекомендуется пересмотреть состав команды или устранить внешние препятствия")
    elif result == "Сырой прототип":
        st.info("Есть зацепка, но не хватает стабильности или компетенций")
    elif result == "Частичный MVP":
        st.success("Команда может показать результат, но не в полном объеме")
    else:
        st.balloons()
        st.success("Высокий шанс выпустить работающий MVP!")
