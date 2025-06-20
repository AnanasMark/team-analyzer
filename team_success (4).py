import streamlit as st
import random
from collections import Counter

# --- Аналитическая логика ---
# (Оставлена без изменений)

def success_level(team, selected_events, expectation, deadline):
    # ... (логика расчётов осталась прежней)
    # (тот же блок, не повторяем для краткости)
    return result, probability, comments

# --- Интерфейс Streamlit ---

st.title("Прогноз успеха команды")
st.subheader("Добавьте участников, ожидания и внешние события")

team = []
deadline = st.selectbox("Срок реализации проекта/продукта", ["", "1 месяц", "3 месяца", "6 месяцев", "1 год"], help="Сколько времени отводится команде на реализацию.")
expectation = st.selectbox("Тип результата", ["", "Фича", "MVP", "Концепт", "Готовый продукт"], help="Какой результат ожидается от команды.")

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
selected_events = st.multiselect("Внешние события", external_events, help="События, которые могут повлиять на работу команды.")

num_members = st.number_input("Сколько участников в команде?", min_value=1, max_value=20, value=5)

roles = ["Product Owner", "Project Manager", "Tech Lead", "Business Analyst", "System Analyst", "Developer", "QA"]
skill_levels = ["junior", "middle", "senior", "неадекватен"]
behavior_types = ["инициативный", "флегматичный", "оппозиционный", "реактивный", "молчаливый"]
motivations = ["высокая", "средняя", "низкая"]

st.markdown("**Участники команды:**")
st.markdown("| Роль ℹ️ | Навык ℹ️ | Поведение ℹ️ | Мотивация ℹ️ |")
st.markdown("|---------|------------|---------------|----------------|")

for i in range(int(num_members)):
    cols = st.columns(4)
    with cols[0]:
        role = st.selectbox("", roles, key=f"role_{i}", help="Основная функция участника: управление, разработка и т.п.")
    with cols[1]:
        skill = st.selectbox("", skill_levels, key=f"skill_{i}", help="Уровень квалификации: от junior до senior или нестабильный участник.")
    with cols[2]:
        behavior = st.selectbox("", behavior_types, key=f"beh_{i}", help="Поведенческая модель участника в работе.")
    with cols[3]:
        motivation = st.selectbox("", motivations, key=f"mot_{i}", help="Мотивация и вовлечённость участника в проект.")
    team.append({"role": role, "skill": skill, "behavior": behavior, "motivation": motivation})
    st.markdown("---")

if st.button("Анализировать"):
    result, probability, comments = success_level(team, selected_events, expectation, deadline)
    st.markdown(f"### 🧠 Прогноз: **{result}**")
    st.markdown(f"#### 🔢 Вероятность успеха: **{probability}%**")
    if comments:
        st.markdown("#### 📌 Комментарии:")
        for comment in comments:
            st.markdown(f"- {comment}")
