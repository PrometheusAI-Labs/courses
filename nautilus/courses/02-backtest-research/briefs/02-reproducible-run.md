## Module 2: Воспроизводимый запуск

**Продолжительность:** 105 минут

### Prerequisites
- Завершён модуль 1 или есть эквивалентное понимание цепочки происхождения данных.
- Ученик различает инструмент, площадку и временной диапазон.
- Не требуется опыт настройки NautilusTrader: все используемые поля показаны в модуле.

### Learning Outcomes
К концу модуля ученик сможет:
1. Прочитать `BacktestDataConfig` как явный контракт входных данных.
2. Сравнить два запуска и выделить параметры, из-за которых результаты несопоставимы.
3. Собрать паспорт запуска с конфигурацией, идентификатором данных и ограничениями модели.
4. Дать AI-агенту инструкцию создать повторяемый эксперимент без скрытого состояния.

### Timebox (105 минут)
| Экран | Формат | Минуты | Результат |
|---|---|---:|---|
| 1. Паспорт эксперимента | теория + visual | 15 | понимает принцип явных входов |
| 2. Переговоры компонентов | group chat demo | 20 | различает роли участников запуска |
| 3. Точный рецепт | code↔English + демо | 25 | читает конфигурацию по полям |
| 4. Лаборатория сравнимости | guided lab + практика | 30 | оформляет run manifest |
| 5. Решение об аудите | квиз + разбор | 15 | диагностирует расхождения |
Итого: теория — 25, демо — 35, практика — 30, квиз и разбор — 15 минут.

### Teaching Arc
- **Metaphor:** паспорт эксперимента: что, где и за какой период измеряли.
- **Opening hook:** два запуска можно сравнивать только если их входы и среда заданы явно.
- **Key insight:** BacktestDataConfig and BacktestRunConfig make inputs visible and repeatable.
- **Why care:** helps AI generate experiments that can be audited instead of notebooks with hidden state.

### Code Snippets (pre-extracted)
File: docs/getting_started/backtest_high_level.py (lines 208-212, exact continuous excerpt from commit `84a98f7f3cc786085496976320c3cb320024217f`)
```python
config = BacktestRunConfig(
    venues=venue_configs,
    data=data_configs,
    engine=BacktestEngineConfig(),
)
```

### Interactive Elements
- Code↔English exact snippet.
- Quiz: 3 scenarios about differing time range, instrument, and venue model.
- Group chat: Researcher, Catalog, BacktestNode, SimulatedVenue negotiate a run.
- Numbered steps: immutable run recipe.

### Guided Lab (20 минут внутри экрана 4)
Даны два паспорта запуска: один отличается `start_time`, второй — `instrument_id` и моделью площадки. Ученик отмечает различия, решает, какие сравнения некорректны, и собирает минимальный повторяемый рецепт: версия данных, период, инструмент, площадка, engine config, параметры стратегии, версия кода.

### Самостоятельное задание (10 минут внутри экрана 4)
Написать проверяемый prompt для AI: создать второй запуск, изменив ровно один фактор, а остальные поля зафиксировать и вывести в итоговый manifest. Ученик выбирает фактор сам, но не трактует результат как доказательство прибыльности.

### Артефакт ученика
Run manifest и таблица сравнения двух запусков с колонками «поле», «запуск A», «запуск B», «влияние на сопоставимость».

### Критерии приёмки
- Зафиксированы данные, инструмент, временной диапазон, площадка, engine config и параметры стратегии.
- Между A и B изменён ровно один заявленный фактор либо расхождения явно помечены.
- Указана версия кода или commit/reference, позволяющий повторить эксперимент.
- Вывод ограничен воспроизводимостью результата под данной моделью; нет production-ready или profit claims.
- Prompt требует сохранить manifest вместе с результатами.

### Преподавательские заметки
- В чате дать компонентам «голос», но не приписывать им гарантий, которых нет в сниппете.
- Термин «immutable» объяснить как дисциплину фиксации рецепта, не как магическое свойство Python-объекта.
- При разборе отличий сначала спрашивать, можно ли сравнивать запуски, и только затем — почему.
- Типичная ошибка: сохранить итоговую метрику, но не входы; вернуть ученика к паспорту эксперимента.

### Reference Files to Read
- interactive-elements.md → Code Translation, Quizzes, Group Chat, Numbered Steps, Glossary Tooltips.
- content-philosophy.md and gotchas.md → fully.

### Connections
- Previous: data evidence. Next: strategy hypothesis. Russian; passport metaphor only here.
