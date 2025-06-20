
def success_level(team, events, expectation, deadline):
    score = 0
    comments = []
    roles = [p['role'] for p in team]
    skills = [p['skill'] for p in team]
    behaviors = [p['behavior'] for p in team]
    motivations = [p['motivation'] for p in team]

    # Базовые условия
    if 'Developer' not in roles:
        comments.append("Нет разработчиков — нечем реализовывать продукт.")
        return "Провал", 5, comments
    if roles.count('Product Owner') > 1 or roles.count('Project Manager') > 1:
        comments.append("Слишком много менеджмента, возможен конфликт интересов.")
        score -= 5

    if roles.count('QA') == 0:
        comments.append("Нет тестировщиков — риски по качеству высоки.")
        score -= 5

    # Оценка навыков
    score += skills.count('senior') * 4
    score += skills.count('middle') * 2
    score -= skills.count('неадекватен') * 5

    # Поведение
    score += behaviors.count('инициативный') * 2
    score -= behaviors.count('оппозиционный') * 3
    score -= behaviors.count('флегматичный') * 1

    # Мотивация
    score += motivations.count('высокая') * 2
    score -= motivations.count('низкая') * 3

    if motivations.count('низкая') >= 3:
        comments.append("Много участников с низкой мотивацией — это тревожный сигнал.")

    # Внешние события
    for e in events:
        if e in ["конфликты между участниками", "уходит ключевой сотрудник", "борьба двух лидеров", "непонятная цель", "перегруз команды разработки", "игнор в чате"]:
            score -= 5
        elif e in ["сильная мотивация", "инициатива от QA", "положительный фидбек от пользователей"]:
            score += 3

    # Ожидания и сроки
    if deadline == "1 месяц":
        score -= 5
    if deadline == "1 год":
        score += 2
    if expectation == "Готовый продукт":
        score += 2
    elif expectation == "Фича":
        score -= 1

    # Финальная оценка
    if score < 10:
        return "Провал", max(score * 2, 5), comments
    elif score < 20:
        return "Сырой прототип", min(score * 2, 40), comments
    elif score < 30:
        return "Частичный MVP", min(score * 2, 70), comments
    else:
        return "Успешный MVP", min(score * 2, 95), comments
