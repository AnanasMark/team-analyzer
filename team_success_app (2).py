import streamlit as st
import pandas as pd
from openai import OpenAI

st.title("🧠 Прогноз успеха команды")

api_key = st.text_input("🔑 Введите ProxyAPI ключ", type="password", key="api_key_input")
if api_key:
    st.session_state["api_key"] = api_key
api_key = st.session_state.get("api_key", "")

team = []

with st.expander("📦 Описание проекта"):
    description = st.text_area("Что вы реализуете?", help="Кратко опишите суть проекта — цель, аудиторию, основную задачу", max_chars=500)
    expectation = st.selectbox("Какой результат ожидается?", ["Фича", "MVP", "Концепт", "Готовый продукт"], help="Уровень полноты создаваемого результата: от простой функции до полноценного продукта")
    deadline = st.selectbox("Срок реализации", ["1 месяц", "3 месяца", "6 месяцев", "1 год"], help="Сколько времени планируется на реализацию проекта")

with st.expander("🏗️ Условия реализации проекта"):
    project_stage = st.selectbox("Текущий этап проекта", ["Инициация", "Планирование", "Реализация", "Проверка"], help="На каком этапе сейчас находится проект")
    methodology = st.selectbox("Какой подход используется?", ["Scrum", "Kanban", "Waterfall", "Нет явного подхода"], help="Какая методология используется для управления")
    has_pm = st.selectbox("Есть ли Project Manager или Scrum Master?", ["Да", "Нет"], help="Назначен ли кто-то ответственный за управление проектом")
    project_assets = st.multiselect("Что уже есть в проекте?", [
        "Фиксированный список фич (MVP backlog)",
        "План релиза / roadmap",
        "Определённые метрики успеха",
        "Регулярные стендапы / синки",
        "Чеклист готовности (DoD/DoR)"
    ], help="Какие документы и процессы уже определены в проекте")
    workload = st.selectbox("Занятость команды", ["Полная занятость", "Частичная занятость", "Неизвестно"], help="Насколько команда доступна для работы над проектом")
    team_experience = st.selectbox("Работали ли участники вместе ранее?", ["Да", "Нет", "Частично"], help="Был ли у команды предыдущий совместный опыт")
    technology_familiarity = st.selectbox("Опыт с технологиями", ["Хорошо знакома", "Частично", "Нет"], help="Насколько хорошо команда знакома с технологическим стеком проекта")
    has_external_dependencies = st.selectbox("Есть ли внешние зависимости?", ["Да", "Нет"], help="Потребуются ли внешние API, подрядчики или другие команды")
    mvp_clarity = st.selectbox("Фиксация MVP", ["Да", "Частично", "Нет"], help="Насколько чётко определено, что входит в минимально жизнеспособный продукт")

with st.expander("🌪️ Внешние события, влияющие на проект"):
    st.markdown("**🔻 Негативные события:**")
    negative_events = st.multiselect("Выберите негативные события:", [
        "Конфликты в команде",
        "Уходит ключевой сотрудник",
        "Непонятная цель проекта",
        "Конфликт лидерства",
        "Перегруз команды",
        "Потеря мотивации",
        "Низкая вовлечённость в коммуникации"
    ])

    st.markdown("**🔺 Положительные события:**")
    positive_events = st.multiselect("Выберите позитивные события:", [
        "Сильная мотивация",
        "Положительный фидбек от пользователей",
        "Поддержка проекта со стороны менеджмента",
        "Активная вовлечённость команды",
        "Инициатива от команды по улучшениям",
        "Повторное использование наработок / библиотек"
    ])

with st.expander("👥 Участники команды"):
    num_members = st.number_input("Сколько человек в команде?", min_value=1, max_value=20, value=5)

    roles = [
        "Product Owner", "Project Manager", "Tech Lead",
        "Business Analyst", "System Analyst", "Developer", 
        "QA", "UX/UI Designer", "DevOps / Infrastructure"
    ]
    skill_levels = ["junior", "middle", "senior", "неадекватен"]
    motivations = ["высокая", "средняя", "низкая"]

    for i in range(int(num_members)):
        st.markdown(f"**Участник {i+1}**")
        cols = st.columns(4)
        with cols[0]:
            role = st.selectbox("Роль", roles, key=f"role_{i}")
        with cols[1]:
            skill = st.selectbox("Навык", skill_levels, key=f"skill_{i}")
        with cols[2]:
            motivation = st.selectbox("Мотивация", motivations, key=f"motivation_{i}")
        team.append({"role": role, "skill": skill, "motivation": motivation})

if st.button("Проанализировать с помощью ИИ"):
    if not api_key:
        st.warning("Введите API ключ для запуска анализа.")
    else:
        prompt = f"""
Ты выступаешь как профессиональный аудитор проектов в IT, действующий по чеклисту зрелости и готовности проекта.

Проанализируй проект, используя приведённые данные как контекст. Не повторяй их дословно, а делай осмысленные выводы, как это сделал бы опытный консультант, руководитель проекта или продуктовый директор. Старайся выявлять неочевидные зависимости и проблемы, а не просто переформулировать то, что указал пользователь.

- Дай краткий прогноз успешности с указанием вероятности в формате **XX%**, выделенной жирным шрифтом, и поясни, что на неё влияет. Не дублируй полученные данные, сформируй поясление кратко.
- Построй таблицу рекомендаций, где в одном столбце указана ключевая проблема, а во втором — соответствующее решение. Проблемы ранжируй по степени важности: сначала самые критичные, потом менее значимые.
- Учитывай влияние внешних позитивных и негативных событий.
- Отдельно оцени сбалансированность состава команды: каких ролей не хватает для стабильной реализации проекта.
- Укажи, есть ли конфликты ролей или пробелы во взаимодействии.
- Отметь, какие аспекты проекта сейчас наиболее неопределённы (требования, сроки, технологии, коммуникации).
- Оцени уровень зрелости команды: низкий / средний / высокий — с кратким обоснованием.
- Добавь блок “Что хорошо”.
- Дай 3 персонализированных рекомендации: для Project Manager, команды и руководства.
- Укажи, можно ли запускать проект в текущем виде и при каких условиях.
- В финале — краткий итог в 1–2 предложениях, с readiness-грейдом (низкий / средний / высокий).

Описание проекта: {description}
Срок реализации: {deadline}
Ожидаемый результат: {expectation}
Внешние негативные события: {', '.join(negative_events)}
Внешние позитивные события: {', '.join(positive_events)}
Загрузка команды: {workload}
Опыт совместной работы: {team_experience}
Знакомство с технологиями: {technology_familiarity}
Внешние зависимости: {has_external_dependencies}
Фиксация скопа: {mvp_clarity}
Этап проекта: {project_stage}
Методология: {methodology}
Есть PM: {has_pm}
Проектные артефакты: {', '.join(project_assets)}

Состав команды:
        """
        for i, member in enumerate(team, 1):
            prompt += f"\n{i}. Роль: {member['role']}, Навык: {member['skill']}, Мотивация: {member['motivation']}"

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
