## Module 3: Стратегия как проверяемая гипотеза

**Продолжительность:** 105 минут

### Prerequisites
- Ученик умеет читать run manifest из модуля 2.
- Понимает слова «позиция», long, short и flat на уровне состояния портфеля.
- Знает, что EMA — сглаженное среднее, а не предсказатель будущего.

### Learning Outcomes
К концу модуля ученик сможет:
1. Перевести ветвление `on_bar` в таблицу «условие → состояние → действие».
2. Объяснить, почему warm-up индикаторов и состояние позиции меняют допустимое действие.
3. Отделить сигнал стратегии от исполнения заявки и результата сделки.
4. Сформулировать фальсифицируемую гипотезу и план проверки без подбора параметров по будущему.

### Timebox (105 минут)
| Экран | Формат | Минуты | Результат |
|---|---|---:|---|
| 1. Термостат, а не оракул | теория + visual | 15 | видит стратегию как правило |
| 2. Дерево состояний | интерактивное демо | 20 | проходит ветви решений |
| 3. Код обработчика | code↔English | 25 | читает точную логику `on_bar` |
| 4. Лаборатория гипотезы | guided lab + практика | 30 | создаёт hypothesis card |
| 5. Сценарный квиз | квиз + разбор | 15 | распознаёт leakage и overfitting |
Итого: теория — 25, демо — 35, практика — 30, квиз и разбор — 15 минут.

### Teaching Arc
- **Metaphor:** термостат: наблюдает два порога и действует по заранее заданному правилу.
- **Opening hook:** EMA cross is useful here as a transparent experiment, not a promise of profit.
- **Key insight:** config separates parameters from event logic; position state changes the next action.
- **Why care:** helps steer AI toward explicit parameters and state-dependent behavior.

### Code Snippets (pre-extracted)
File: docs/getting_started/quickstart.py (lines 72-81, exact continuous excerpt from commit `84a98f7f3cc786085496976320c3cb320024217f`)
```python
    def on_bar(self, _bar: Bar) -> None:
        if not self.indicators_initialized():
            return

        if self.fast_ema.value >= self.slow_ema.value:
            if self.portfolio.is_net_flat(self.config.instrument_id):
                self.buy()
            elif self.portfolio.is_net_short(self.config.instrument_id):
                self.close_all_positions(self.config.instrument_id)
                self.buy()
```

### Interactive Elements
- Code↔English exact snippet.
- Quiz: 4 scenario questions about warm-up, flat/short state, parameter leakage, overfitting.
- Decision flow visualization with state branches.
- Aha callout: signal is not execution.

### Guided Lab (20 минут внутри экрана 4)
На четырёх последовательных барах ученику дают значения fast/slow EMA и состояние портфеля. Он вручную проходит guard `indicators_initialized()`, выбирает ветвь flat/short и записывает ожидаемое намерение стратегии. Затем отдельно отмечает неизвестные: fill, latency, fees и slippage.

### Самостоятельное задание (10 минут внутри экрана 4)
Сформулировать hypothesis card: правило, один изменяемый параметр, ожидаемое наблюдение, условие опровержения, out-of-sample период и запрещённые источники будущей информации.

### Артефакт ученика
Таблица переходов состояний и карточка проверяемой гипотезы с границами интерпретации.

### Критерии приёмки
- В таблице присутствует ветвь неинициализированных индикаторов с действием «ничего не делать».
- Flat и short разобраны отдельно; сигнал не назван исполненной сделкой.
- В гипотезе изменяется один фактор, есть условие опровержения и отдельный out-of-sample отрезок.
- Перечислены минимум три исполнения/рыночных допущения, которых нет в сигнале.
- Нет обещаний прибыли, обобщения на live или подгонки по тестовому периоду.

### Преподавательские заметки
- Не преподавать EMA как «хорошую стратегию»: это прозрачный учебный объект для трассировки.
- На вопрос «почему buy?» возвращать к состоянию портфеля и ветви, а не к интуиции о рынке.
- Развести три уровня: вычислен сигнал, создано намерение, произошло исполнение.
- Типичная ошибка: оптимизировать периоды на тех же данных и назвать результат проверкой; просить указать независимый период.

### Reference Files to Read
- interactive-elements.md → Code Translation, Scenario Quiz, Flow Diagrams, Glossary Tooltips, Callouts.
- content-philosophy.md and gotchas.md → fully.

### Connections
- Previous: reproducible run. Next: evidence limits. Russian; thermosat metaphor only here.
