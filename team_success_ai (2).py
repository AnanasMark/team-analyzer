import streamlit as st
from openai import OpenAI

st.title("Прогноз успеха команды с помощью ИИ")
st.subheader("Добавьте участников, ожидания и внешние события")

api_key = st.text_input("🔑 Введите ProxyAPI ключ", type="password", key="api_key_input")
if api_key:
    st.session_state["api_key"] = api_key
api_key = st.session_state.get("api_key", "")

team = []
deadline = st.selectbox("Срок реализации проекта/продукта", ["", "1 месяц", "3 месяца", "6 месяцев", "1 год"], help="Сколько времени отводится команде на реализацию.")
expectation = st.selectbox("Тип результата", ["", "Фича", "MVP", "Концепт", "Готовый продукт"], help="Какой результат ожидается от команды.")
description = st.text_area("Краткое описание проекта", max_chars=500, help="Кратко опишите суть проекта.")

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

На основе приведённой информации про команду, цели проекта, сроков и внешней ситуации:
- Проанализируй вероятность успешной реализации проекта.
- Укажи сильные и слабые стороны команды.
- Выдели возможные риски и зоны внимания.
- Дай конкретные рекомендации для повышения шансов на успех.

Описание проекта: {description}
Срок реализации: {deadline}
Ожидаемый результат: {expectation}
Внешние события: {', '.join(selected_events)}

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
                st.markdown(result)
            except Exception as e:
                st.error(f"Ошибка при обращении к ProxyAPI: {e}")
