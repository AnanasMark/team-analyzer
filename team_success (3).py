import streamlit as st
import random
from collections import Counter

# --- Аналитическая логика ---
def success_level(team, selected_events, expectation, deadline):
    score = 0
    comments = []

    # Проверка ролей и состава
    role_counts = Counter([p['role'] for p in team])
    if role_counts['Developer'] == 0:
        comments.append("Нет разработчиков — нечем реализовывать продукт.")
        score -= 30
    elif role_counts['Developer'] == 1:
        comments.append("Один разработчик — слишком медленная разработка.")
        score -= 10
    elif role_counts['Developer'] >= 4 and role_counts['QA'] <= 1:
        comments.append("Много разработчиков и мало тестировщиков — возможны проблемы с качеством.")
        score -= 5

    if role_counts['Project Manager'] > 1 or role_counts['Product Owner'] > 1:
        comments.append("Слишком много менеджмента, вы уверены что всё окей?)")

    if role_counts['Project Manager'] == 0 and role_counts['Product Owner'] == 0:
        comments.append("Отсутствие управления — высока вероятность распада команды.")
        score -= 15

    # Навыки
    low_skills = [p for p in team if p['skill'] in ['junior', 'неадекватен']]
    if len(low_skills) > len(team) // 2:
        comments.append("Слишком много участников с низким уровнем навыков.")
        score -= 15

    # Поведение
    oppo = [p for p in team if p['behavior'] == 'оппозиционный']
    if len(oppo) >= 2:
        comments.append("Много оппозиционных участников может привести к конфликтам и замедлению.")
        score -= 10
    elif any(p['behavior'] == 'оппозиционный' for p in team):
        score -= 5

    # Мотивация
    if all(p['motivation'] == 'низкая' for p in team):
        comments.append("Вся команда с низкой мотивацией — крайне высокий риск провала.")
        score -= 25
    elif sum(1 for p in team if p['motivation'] == 'низкая') >= len(team) // 2:
        comments.append("Многие участники с низкой мотивацией.")
        score -= 10

    # Сроки
    if deadline == "1 месяц":
        score -= 15
    elif deadline == "3 месяца":
        score += 5
    elif deadline == "6 месяцев":
        score += 10
    elif deadline == "1 год":
        score += 0

    # Ожидания
    if expectation == "Фича":
        score += 10
    elif expectation == "MVP":
        score += 5
    elif expectation == "Готовый продукт":
        score -= 10

    # Внешние события
    for e in selected_events:
        if e in ["конфликты между участниками", "борьба двух лидеров", "уходит ключевой сотрудник", "перегруз команды разработки", "нет мотивации", "игнор в чате"]:
            comments.append(f"Негативное влияние: {e}")
            score -= 10
        elif e == "непонятная цель":
            comments.append("Неясная цель может дезориентировать команду.")
            score -= 10
        elif e == "сильная мотивация":
            comments.append("Позитивный эффект: сильная мотивация.")
            score += 10
        elif e == "положительный фидбек от пользователей":
            comments.append("Позитивный эффект: пользователи довольны!")
            score += 10
        elif e == "инициатива от QA":
            score += 5

    # Штраф если нет положительных и негативных событий, но команда адекватная
    if len(selected_events) == 0 and len(comments) == 0 and len(team) >= 5 and all(p['skill'] != 'неадекватен' for p in team):
        score += 15

    # Вычисление финального результата
    score = max(0, min(100, 50 + score))
    probability = score

    if score >= 85:
        result = "Успешный MVP"
    elif score >= 70:
        result = "Частичный MVP"
    elif score >= 55:
        result = "Сырой прототип"
    elif score >= 40:
        result = "Маленький результат"
    elif score >= 20:
        result = "Фича или техническое демо"
    else:
        result = "Провал"

    return result, probability, comments


# --- Интерфейс Streamlit ---

if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

if st.session_state.analyzed:
    if st.button("🔄 Изменить команду"):
        st.session_state.analyzed = False
        st.rerun()

if not st.session_state.analyzed:
    st.title("Прогноз успеха команды")
    st.subheader("Добавьте участников, ожидания и внешние события")

    team = []
    deadline = st.selectbox("Срок реализации проекта/продукта", ["", "1 месяц", "3 месяца", "6 месяцев", "1 год"])
    expectation = st.selectbox("Тип результата", ["", "Фича", "MVP", "Концепт", "Готовый продукт"])
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
    selected_events = st.multiselect("Внешние события", external_events)
    num_members = st.number_input("Сколько участников в команде?", min_value=1, max_value=20, value=5)

    roles = ["Product Owner", "Project Manager", "Tech Lead", "Business Analyst", "System Analyst", "Developer", "QA"]
    skill_levels = ["junior", "middle", "senior", "неадекватен"]
    behavior_types = ["инициативный", "флегматичный", "оппозиционный", "реактивный", "молчаливый"]
    motivations = ["высокая", "средняя", "низкая"]

    st.markdown("**Участники команды:**")
    for i in range(int(num_members)):
        st.markdown(f"**Участник {i+1}**")
        cols = st.columns(4)
        with cols[0]:
            role = st.selectbox("Роль", roles, key=f"role_{i}")
        with cols[1]:
            skill = st.selectbox("Навык", skill_levels, key=f"skill_{i}")
        with cols[2]:
            behavior = st.selectbox("Поведение", behavior_types, key=f"beh_{i}")
        with cols[3]:
            motivation = st.selectbox("Мотивация", motivations, key=f"mot_{i}")
        team.append({"role": role, "skill": skill, "behavior": behavior, "motivation": motivation})

    if st.button("Анализировать"):
        st.session_state.analyzed = True
        st.session_state.team = team
        st.session_state.deadline = deadline
        st.session_state.expectation = expectation
        st.session_state.selected_events = selected_events
        st.rerun()

else:
    result, probability, comments = success_level(
        st.session_state.team,
        st.session_state.selected_events,
        st.session_state.expectation,
        st.session_state.deadline
    )
    st.markdown(f"### 🧠 Прогноз: **{result}**")
    st.markdown(f"#### 🔢 Вероятность успеха: **{probability}%**")
    if comments:
        st.markdown("#### 📌 Комментарии:")
        for comment in comments:
            st.markdown(f"- {comment}")
