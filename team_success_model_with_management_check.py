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
    if role_counter['Product Owner'] == 0 and role_counter['Project Manager'] == 0:
        comments.append("Нет Project или Product Manager — высокая вероятность распада команды без контроля.")

    if dev_count >= 3 and qa_count > 0 and ba_count > 0 and synergy_score >= 2 and disruption_score == 0:
        return "Успешный MVP", min(score + 20, 95), comments
    elif dev_count >= 2 and qa_count > 0 and ba_count > 0 and synergy_score >= 1 and disruption_score <= 1:
        return "Частичный MVP", score, comments
    elif dev_count >= 2 and (qa_count > 0 or ba_count > 0) and disruption_score <= 2:
        return "Сырой прототип", max(score - 10, 30), comments
    else:
        return "Провал", max(score - 30, 10), comments
