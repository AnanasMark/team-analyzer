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

    score = 50 + synergy_score * 10 - disruption_score * 10

    if dev_count == 0:
        return "Провал", 0, ["Нет разработчиков — проект не может быть реализован."]
    if ba_count == 0 and expectation != "Концепт":
        return "Провал", 5, ["Нет аналитиков — постановка задач и требований будет проблемной."]
    if qa_count == 0 and expectation == "Готовый продукт":
        return "Сырой прототип", 25, ["Отсутствие тестировщиков критично для финального качества."]
    if qa_count > 0 and qa_count < dev_count / 4:
        disruption_score += 1
    if pm_count > 2 and dev_count == 0:
        disruption_score += 1
    if inadequate_count > len(team) * 0.3:
        return "Провал", 10, ["Слишком много участников с неподходящей квалификацией."]
    if flegma_count > len(team) / 2 and low_motivation_count > len(team) / 2:
        disruption_score += 1
    if deadline == "3 месяца" and expectation == "Готовый продукт":
        return "Провал", 15, ["Сроки слишком амбициозные для такого объема."]
    if deadline == "1 год" and expectation == "MVP":
        synergy_score = max(0, synergy_score - 1)

    comments = []
    if dev_count == 1:
        comments.append("Только один разработчик — высокая нагрузка и риск срыва сроков.")
    if qa_count == 0:
        comments.append("Нет QA — возможны ошибки и нестабильность в финальной версии.")
    if low_motivation_count >= 3:
        comments.append("Несколько участников с низкой мотивацией — это может тормозить процесс.")

    if dev_count >= 3 and qa_count > 0 and ba_count > 0 and synergy_score >= 2 and disruption_score == 0:
        return "Успешный MVP", min(score + 20, 95), comments
    elif dev_count >= 2 and qa_count > 0 and ba_count > 0 and synergy_score >= 1 and disruption_score <= 1:
        return "Частичный MVP", score, comments
    elif dev_count >= 2 and (qa_count > 0 or ba_count > 0) and disruption_score <= 2:
        return "Сырой прототип", max(score - 10, 30), comments
    else:
        return "Провал", max(score - 30, 10), comments

# Streamlit UI
st.title("Прогноз успеха команды")
st.subheader("Добавьте участников, ожидания и внешние события")

team = []
st.markdown("**Ожидания от команды:**")
deadline = st.selectbox("Срок реализации проекта/продукта", ["", "3 месяца", "6 месяцев", "1 год"], index=0)
expectation = st.selectbox("Тип результата", ["", "MVP", "Концепт", "Готовый продукт"], index=0)

st.markdown("**Выберите внешние события:**")
selected_events = st.multiselect("Факторы, влияющие на команду", external_events)

num_members = st.number_input("Сколько участников в команде?", min_value=1, max_value=20, value=5, step=1)

# Кнопка для случайного заполнения
if st.button("Заполнить всех участников случайно"):
    st.session_state.randomize = True
else:
    st.session_state.randomize = False

for i in range(int(num_members)):
    st.markdown(f"### Участник {i+1}")
    cols = st.columns(4)
    if st.session_state.get("randomize"):
        role = random.choice(roles)
        skill = random.choice(skill_levels)
        behavior = random.choice(behavior_types)
        motivation = random.choice(motivations)
    else:
        with cols[0]:
            role = st.selectbox(f"Роль", roles, key=f"role_{i}")
        with cols[1]:
            skill = st.selectbox(f"Навык", skill_levels, key=f"skill_{i}")
        with cols[2]:
            behavior = st.selectbox(f"Поведение", behavior_types, key=f"beh_{i}")
        with cols[3]:
            motivation = st.selectbox(f"Мотивация", motivations, key=f"mot_{i}")

    team.append({"role": role, "skill": skill, "behavior": behavior, "motivation": motivation})

if st.button("Анализировать"):
    result, probability, comments = success_level(team, selected_events, expectation, deadline)
    st.markdown(f"### 🧠 Прогноз: **{result}**")
    st.markdown(f"#### 🔢 Вероятность успеха: **{probability}%**")
    if comments:
        st.markdown("#### 📌 Комментарии:")
        for comment in comments:
            st.markdown(f"- {comment}")

    if result == "Провал":
        st.warning("Рекомендуется пересмотреть состав команды или устранить внешние препятствия")
    elif result == "Сырой прототип":
        st.info("Есть зацепка, но не хватает стабильности или компетенций")
    elif result == "Частичный MVP":
        st.success("Команда может показать результат, но не в полном объеме")
    else:
        st.balloons()
        st.success("Высокий шанс выпустить работающий MVP!")
