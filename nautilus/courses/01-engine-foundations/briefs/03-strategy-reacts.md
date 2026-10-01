## Модуль 3: Стратегия реагирует — 85 минут

### Prerequisites
- Пройдены модули 1–2; ученик различает доставку события и решение стратегии.
- Понимание, что бар — агрегированная порция рыночных данных.

### Learning outcomes
К концу модуля ученик сможет:
1. Объяснить контракт `on_start` и `on_bar` без чтения синтаксиса по символам.
2. Отличить событийный callback от polling loop.
3. Диагностировать отсутствие подписки, невызванный обработчик и незавершённый warm-up.
4. Спроектировать безопасный входной шлюз для новой стратегии.

### Teaching Arc
- **Metaphor:** датчик дыма: подписался, ждёт сигнал, действует только после события.
- **Opening hook:** стратегия не опрашивает рынок бесконечным циклом — движок вызывает её обработчики.
- **Key insight:** on_start настраивает подписки; on_bar принимает событие; warm-up prevents premature decisions.
- **Why care:** помогает распознавать неправильные polling loops и ошибки жизненного цикла.

### Хронометраж по экранам (ровно 85 минут)
| Экран | Теория | Демо | Практика | Квиз | Итого | Результат |
|---|---:|---:|---:|---:|---:|---|
| 1. Датчик, а не опросчик | 10 | 0 | 0 | 0 | 10 | отличает callback от polling |
| 2. Жизненный цикл | 5 | 15 | 0 | 0 | 20 | восстанавливает цепочку запуска |
| 3. Контракт в коде | 5 | 5 | 10 | 0 | 20 | читает подписку и warm-up gate |
| 4. Guided lab «Тишина в обработчике» | 0 | 0 | 25 | 0 | 25 | локализует три класса сбоев |
| 5. Инженерная проверка | 0 | 0 | 4 | 6 | 10 | переносит контракт на новый кейс |
| **Итого** | **20** | **20** | **39** | **6** | **85** | |

**Баланс форматов:** теория — 20 мин; демонстрация — 20 мин; практика — 39 мин; квиз — 6 мин. **Итого: 85 мин.**

### Code Snippets (pre-extracted)
File: docs/getting_started/quickstart.py (lines 67-74, exact continuous excerpt from commit `84a98f7f3cc786085496976320c3cb320024217f`)
```python
    def on_start(self) -> None:
        self.register_indicator_for_bars(self.config.bar_type, self.fast_ema)
        self.register_indicator_for_bars(self.config.bar_type, self.slow_ema)
        self.subscribe_bars(self.config.bar_type)

    def on_bar(self, _bar: Bar) -> None:
        if not self.indicators_initialized():
            return
```

### Interactive Elements
- Code↔English: exact snippet.
- Quiz: 3 debugging scenarios: no subscription, no warm-up, handler never called.
- Flow diagram: start → register indicators → subscribe → receive bar → warm-up gate.
- Aha callout: lifecycle callbacks are contracts.
- Pattern cards: symptom / evidence / next check.

### Guided lab — «Тишина в обработчике» (25 минут)
Три карточки инцидента: `on_bar` не вызывается; вызывается, но всегда возвращает; данные приходят другого `bar_type`. Ученик для каждой карточки отмечает ожидаемую точку жизненного цикла, минимальное доказательство и следующую проверку. Финал — AI-промпт, требующий сначала наблюдения, затем исправления.

### Самостоятельное задание (входит в экран 5)
Спроектировать контракт обработчика `on_quote_tick`: что регистрируется на старте, какое событие вызывает callback, какой readiness-gate нужен и что логировать при раннем выходе.

### Артефакт ученика
«Паспорт callback»: источник события, действие `on_start`, имя обработчика, условие готовности, ранний выход, диагностический сигнал.

### Критерии приёмки
- Нет бесконечного цикла опроса рынка.
- Подписка выполняется до ожидания события.
- Warm-up описан как проверка готовности, а не как задержка «на глаз».
- Для каждого симптома указано проверяемое доказательство.

### Преподавательские заметки
- Попросить учеников физически показать момент передачи управления движком стратегии.
- Не обещать фиксированное число баров для прогрева без данных о конкретном индикаторе.
- Если ученик сразу переписывает `on_bar`, вернуть к вопросу «вызывался ли он вообще?».
- Различать «callback вызван» и «торговое действие выполнено» — это разные границы.

### Reference Files to Read
- interactive-elements.md → Code Translation, Scenario Quiz, Flow Diagrams, Glossary Tooltips, Callouts.
- content-philosophy.md and gotchas.md → fully.

### Connections
- Previous: engine actors. Next: Backtest/Sandbox/Live. Russian; smoke-alarm metaphor only here.
