import streamlit as st
import pandas as pd
from openai import OpenAI

st.title("Прогноз успеха команды")
st.subheader("Добавьте участников, ожидания и внешние события")

api_key = st.text_input("🔑 Введите ProxyAPI ключ", type="password", key="api_key_input")
if api_key:
    st.session_state["api_key"] = api_key
api_key = st.session_state.get("api_key", "")

team = []
deadline = st.selectbox("Срок реализации проекта/продукта", ["", "1 месяц", "3 месяца", "6 месяцев", "1 год"], help="Сколько времени отводится команде на реализацию.")
expectation = st.selectbox("Тип результата", ["", "Фича", "MVP", "Концепт", "Готовый продукт"], help="Какой результат ожидается от команды.")
description = st.text_area("Краткое описание проекта", max_chars=500, help="Кратко опишите суть проекта.")
workload = st.selectbox("Уровень загрузки команды", ["Полная занятость", "Частичная занятость", "Неизвестно"], help="Насколько команда вовлечена в проект")
team_experience = st.selectbox("Работали ли участники вместе ранее?", ["Да", "Нет", "Частично"], help="Была ли у команды история совместной работы")
technology_familiarity = st.selectbox("Насколько команда знакома с нужными технологиями?", ["Хорошо знакома", "Частично", "Нет"], help="Есть ли опыт с Telegram API или другими ключевыми технологиями")
has_external_dependencies = st.selectbox("Есть ли внешние зависимости?", ["Да", "Нет"], help="Нужна ли интеграция с другими системами, API и т.п.")
mvp_clarity = st.selectbox("Сформулирован ли чётко список фич для MVP?", ["Да", "Частично", "Нет"], help="Насколько понятен объём MVP")

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

roles = [
    "Product Owner", "Project Manager", "Tech Lead",
    "Business Analyst", "System Analyst", "Developer", 
    "QA", "UX/UI Designer", "DevOps / Infrastructure"
]
skill_levels = ["junior", "middle", "senior", "неадекватен"]
behavior_types = ["инициативный", "флегматичный", "оппозиционный", "реактивный", "молчаливый"]
motivations = ["высокая", "средняя", "низкая"]

st.markdown("**Участники команды:**")

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
    st.divider()

if st.button("Проанализировать с помощью ИИ"):
    if not api_key:
        st.warning("Введите API ключ для запуска анализа.")
    else:
        prompt = f"""
Ты выступаешь как эксперт по командной динамике, управлению проектами и оценке проектных рисков в IT.

На основе приведённой информации про команду, цели проекта, сроков, внешней ситуации и организационного контекста:
- Сформулируй краткий прогноз успешности.
- Построй таблицу \"Проблема → Риск → Решение\".
- В конце добавь короткий блок \"Что хорошо\".
- Заверши вывод чётким итогом (1–2 предложения).

Описание проекта: {description}
Срок реализации: {deadline}
Ожидаемый результат: {expectation}
Внешние события: {', '.join(selected_events)}
Загрузка команды: {workload}
Опыт совместной работы: {team_experience}
Знакомство с технологиями: {technology_familiarity}
Внешние зависимости: {has_external_dependencies}
Фиксация скопа: {mvp_clarity}

Состав команды:
        """
        for i, member in enumerate(team, 1):
            prompt += f"\n{i}. Роль: {member['role']}, Навык: {member['skill']}, Поведение: {member['behavior']}, Мотивация: {member['motivation']}"

        with st.spinner("Обращение к ProxyAPI..."):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.proxyapi.ru/openai/v1"
        )

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Ты эксперт по оценке команд и проектного успеха."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content

        st.markdown("### 🧠 Ответ ИИ:")

        if "|" in result and result.count("|") > 5:
            lines = result.splitlines()
            table_lines = [line for line in lines if "|" in line and line.strip() and not line.strip().startswith("|")]
            if len(table_lines) > 1:
                headers = [h.strip() for h in table_lines[0].strip("|").split("|")]
                data_rows = [
                    [cell.strip() for cell in row.strip("|").split("|")]
                    for row in table_lines[1:]
                ]
                df = pd.DataFrame(data_rows, columns=headers)
                st.table(df)
                st.markdown("\n".join(lines))
            else:
                st.markdown(result)
        else:
            st.markdown(result)

    except Exception as e:
        st.error(f"Ошибка при обращении к ProxyAPI: {e}")
