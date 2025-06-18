
import streamlit as st
import random
from collections import Counter

# Опции выбора
roles = ["рандомно", "Product Owner", "Project Manager", "Tech Lead", "Business Analyst", "System Analyst", "Developer", "QA"]
skill_levels = ["рандомно", "junior", "middle", "senior", "неадекватен"]
behavior_types = ["рандомно", "инициативный", "флегматичный", "оппозиционный", "реактивный", "молчаливый"]
motivations = ["рандомно", "высокая", "средняя", "низкая"]
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

# Модель оценки
def success_level(team, events, expectation, deadline):
    role_counter = Counter([p['role'] for p in team])
    dev_count = role_counter['Developer']
    qa_count = role_counter['QA']
    ba_count = role_counter['Business Analyst'] + role_counter['System Analyst']
    pm_count = role_counter['Project Manager'] + role_counter['Product Owner']
    inadequate_count = sum(1 for p in team if p['skill'] == "неадекватен")

    flegma_count = sum(1 for p in team if p['behavior'] in ["флегматичный", "молчаливый"])
    low_motivation_count = sum(1 for p in team if p['motivation'] == "низкая")

    synergy_signals = ["инициатива", "положительный фидбек", "сильная мотивация"]
    disruption_signals = ["конфликт", "уходит", "игнор", "перегруз", "нет мотивации", "борьба"]
    synergy_score = sum(any(s in e for s in synergy_signals) for e in events)
    disruption_score = sum(any(s in e for s in disruption_signals) for e in events)

    if dev_count == 0:
        return "Провал"
    if ba_count == 0 and expectation != "Концепт":
        return "Провал"
    if qa_count == 0 and expectation == "Готовый продукт":
        return "Сырой прототип"
    if qa_count > 0 and qa_count < dev_count / 4:
        disruption_score += 1
    if pm_count > 2 and dev_count == 0:
        disruption_score += 1
    if inadequate_count > len(team) * 0.3:
        return "Провал"
    if flegma_count > len(team) / 2 and low_motivation_count > len(team) / 2:
        disruption_score += 1
    if deadline == "3 месяца" and expectation == "Готовый продукт":
        return "Провал"
    if deadline == "1 год" and expectation == "MVP":
        synergy_score = max(0, synergy_score - 1)

    if dev_count >= 3 and qa_count > 0 and ba_count > 0 and synergy_score >= 2 and disruption_score == 0:
        return "Успешный MVP"
    elif dev_count >= 2 and qa_count > 0 and ba_count > 0 and synergy_score >= 1 and disruption_score <= 1:
        return "Частичный MVP"
    elif dev_count >= 2 and (qa_count > 0 or ba_count > 0) and disruption_score <= 2:
        return "Сырой прототип"
    else:
        return "Провал"

# Streamlit UI
st.title("Прогноз успеха команды")
st.subheader("Добавьте участников, ожидания и внешние события")

team = []
with st.form("team_form"):
    st.markdown("**Ожидания от команды:**")
    deadline = st.selectbox("Срок реализации проекта/продукта", ["", "3 месяца", "6 месяцев", "1 год"], index=0)
    expectation = st.selectbox("Тип результата", ["", "MVP", "Концепт", "Готовый продукт"], index=0)

    st.markdown("**Выберите внешние события:**")
    selected_events = st.multiselect("Факторы, влияющие на команду", external_events)

    num_members = st.number_input("Сколько участников в команде?", min_value=1, max_value=20, value=5)

    for i in range(num_members):
        st.markdown(f"### Участник {i+1}")
        cols = st.columns(4)
        with cols[0]:
            role = st.selectbox(f"Роль", roles, key=f"role_{i}")
        with cols[1]:
            skill = st.selectbox(f"Навык", skill_levels, key=f"skill_{i}")
        with cols[2]:
            behavior = st.selectbox(f"Поведение", behavior_types, key=f"beh_{i}")
        with cols[3]:
            motivation = st.selectbox(f"Мотивация", motivations, key=f"mot_{i}")

        if role == "рандомно":
            role = random.choice(roles[1:])
        if skill == "рандомно":
            skill = random.choice(skill_levels[1:])
        if behavior == "рандомно":
            behavior = random.choice(behavior_types[1:])
        if motivation == "рандомно":
            motivation = random.choice(motivations[1:])

        team.append({"role": role, "skill": skill, "behavior": behavior, "motivation": motivation})

    submitted = st.form_submit_button("Анализировать")

if submitted:
    result = success_level(team, selected_events, expectation, deadline)
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
