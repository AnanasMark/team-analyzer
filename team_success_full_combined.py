
def success_level(team, events, expectation, deadline):
    probability = 50
    comments = []
    roles = [member['role'] for member in team]
    skills = [member['skill'] for member in team]
    behaviors = [member['behavior'] for member in team]
    motivations = [member['motivation'] for member in team]

    if roles.count('Developer') == 0:
        probability -= 40
        comments.append("Нет разработчиков — нечем реализовывать продукт.")
    elif roles.count('Developer') == 1:
        probability -= 20
        comments.append("Только один разработчик — низкая скорость реализации.")

    if roles.count('QA') == 0:
        probability -= 10
        comments.append("Нет QA — продукт может быть нестабильным.")

    if roles.count('Project Manager') > 1 or roles.count('Product Owner') > 1:
        comments.append("Слишком много менеджмента — вы уверены, что все окей?")

    if all(skill == 'junior' or skill == 'неадекватен' for skill in skills):
        probability -= 30
        comments.append("Слишком низкий уровень компетенций у всей команды.")

    if all(mot == 'низкая' for mot in motivations):
        probability -= 30
        comments.append("У всех участников низкая мотивация.")

    if any(event in events for event in ["конфликты между участниками", "уходит ключевой сотрудник", "игнор в чате"]):
        probability -= 15
        comments.append("Есть риски из-за конфликтов или потери связи в команде.")

    if "непонятная цель" in events:
        probability -= 20
        comments.append("Непонятная цель — команда может двигаться в разные стороны.")

    if all(skill in ["middle", "senior"] for skill in skills) and "сильная мотивация" in events and expectation == "MVP":
        probability += 30
        comments.append("Команда замотивирована и опытна для реализации MVP.")

    if all(p['behavior'] == 'инициативный' for p in team):
        probability += 10
        comments.append("Команда инициативна — высокая вовлеченность в результат.")

    if deadline == "1 месяц" and len(team) < 4:
        probability -= 15
        comments.append("Недостаточно участников для быстрой реализации в срок 1 месяц.")

    if "положительный фидбек от пользователей" in events:
        probability += 10
        comments.append("Позитивный отклик пользователей может усилить мотивацию команды.")

    if not events and len(team) >= 6 and all(skill != "неадекватен" for skill in skills):
        probability += 20
        comments.append("Полная команда, без внешних угроз, с адекватными навыками — высокая устойчивость.")

    probability = max(0, min(probability, 100))

    if probability < 30:
        return "Провал", probability, comments
    elif probability < 50:
        return "Сырой прототип", probability, comments
    elif probability < 70:
        return "Частичный MVP", probability, comments
    elif probability >= 70:
        return "Успешный MVP", probability, comments
    return "Неопределено", probability, comments


