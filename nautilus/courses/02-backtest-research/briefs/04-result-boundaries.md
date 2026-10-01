## Module 4: Что результат доказывает — и чего не доказывает

**Продолжительность:** 110 минут

### Prerequisites
- Завершены модули 1–3: данные, run manifest и проверяемая гипотеза.
- Ученик различает сигнал, смоделированное исполнение и реальное исполнение.
- Готовность применять NO-GO, если доказательств недостаточно.

### Learning Outcomes
К концу модуля ученик сможет:
1. Проследить цепочку `build → strategy config → run → results` и назвать границы каждого шага.
2. Классифицировать доказательство по лестнице backtest → forward → shadow → canary → live.
3. Принять evidence-bounded GO/NO-GO решение с явными условиями следующего этапа.
4. Собрать итоговый evidence pack, не превращая синтетический результат в production authority.

### Timebox (110 минут)
| Экран | Формат | Минуты | Результат |
|---|---|---:|---|
| 1. Краш-тест модели | теория + visual | 15 | видит ценность и границы теста |
| 2. Трасса запуска | code↔English + демо | 25 | связывает config, build и results |
| 3. Лестница доказательств | интерактивные badges | 25 | различает уровни уверенности |
| 4. Лаборатория evidence pack | guided lab + практика | 30 | оформляет решение и следующий gate |
| 5. GO/NO-GO квиз | квиз + итог | 15 | применяет границы к новым кейсам |
Итого: теория — 25, демо — 40, практика — 30, квиз и разбор — 15 минут.

### Teaching Arc
- **Metaphor:** краш-тест автомобиля: ценный контролируемый тест, но не все дороги и водители мира.
- **Opening hook:** deterministic run tells you what happened under the model, not what live venue must do.
- **Key insight:** build/run/results form a trace; promotion still needs forward, shadow, reconciliation and bounded live gates.
- **Why care:** prevents synthetic evidence from being labeled production-ready.

### Code Snippets (pre-extracted)
File: docs/getting_started/backtest_high_level.py (lines 224-236, exact continuous excerpt from commit `84a98f7f3cc786085496976320c3cb320024217f`)
```python
node = BacktestNode(configs=[config])
node.build()

node.add_builtin_strategy(
    config.id,
    "EmaCross",
    EmaCrossConfig(
        instrument_id=instrument.id,
        trade_size=Quantity.from_int(1_000_000),
        fast_period=10,
        slow_period=20,
    ),
)
```

### Interactive Elements
- Code↔English exact snippet.
- Quiz: 4 GO/NO-GO evidence scenarios.
- Evidence ladder: backtest → forward → shadow → canary → live, with badges.
- Final checklist and next-course CTA.

### Guided Lab (20 минут внутри экрана 4)
Ученику даны артефакты: catalog manifest, run config, код стратегии, один backtest result и отсутствующий reconciliation report. Он сортирует их по уровням доказательств, формулирует допустимый вывод и выбирает следующий безопасный gate. Правильный итог не обязательно GO; NO-GO с точным пробелом считается сильным результатом.

### Самостоятельное задание (10 минут внутри экрана 4)
Собрать evidence pack для условного исследования: claim, supporting evidence, missing evidence, risks, decision, next gate, rollback/stop conditions. Любое сильное утверждение должно ссылаться на конкретный артефакт.

### Артефакт ученика
Evidence matrix и одностраничное решение GO/NO-GO для перехода только на следующий ограниченный этап.

### Критерии приёмки
- Каждое утверждение связано с артефактом или помечено как неподтверждённое.
- Backtest не используется как доказательство live profitability или production readiness.
- Отсутствие reconciliation/forward/shadow evidence приводит к явному ограничению или NO-GO.
- Следующий gate ограничен по времени, капиталу/риску и содержит stop condition.
- Решение воспроизводимо: сохранены config, данные/их идентификатор, код и результаты.

### Преподавательские заметки
- Хвалить точный NO-GO: цель — качество решения, а не продвижение любой ценой.
- «Детерминированный» не значит «реалистичный»: он означает повторяемость в заданной модели.
- Не превращать лестницу в автоматический конвейер; каждый уровень требует своих артефактов и проверки.
- Финальный CTA вести к Rust/live path только как к следующему курсу и набору gates, не как к готовому запуску.

### Reference Files to Read
- interactive-elements.md → Code Translation, Quizzes, Permission Badges, Numbered Steps, Glossary Tooltips.
- content-philosophy.md and gotchas.md → fully.

### Connections
- Previous: strategy hypothesis. Next: course 03 Rust live path. Russian; no profitability claims.
