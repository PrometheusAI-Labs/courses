## Модуль 4: Три среды — один каркас, разные доказательства — 90 минут

### Prerequisites
- Пройдены модули 1–3; ученик умеет трассировать событие, роли компонентов и lifecycle стратегии.
- Базовое различение исторических данных, тестовой площадки и реального капитала.

### Learning outcomes
К концу модуля ученик сможет:
1. Сравнить Backtest, Sandbox и Live по часам, данным, исполнению, риску и сверке состояния.
2. Объяснить, почему общий каркас уменьшает drift кода, но не уравнивает доказательства.
3. Построить promotion-gate между средами с измеримыми критериями.
4. Отклонить опасный вывод «зелёный бэктест = готово к продакшену».

### Teaching Arc
- **Metaphor:** авиасимулятор, учебный полёт и реальный рейс: похожие органы управления, разные последствия.
- **Opening hook:** одинаковая стратегия может работать в Backtest, Sandbox и Live, но это не делает результаты равноценными.
- **Key insight:** Backtest uses historical data and simulated execution; Sandbox uses real-time data with simulated execution; Live uses live venue connections and may target paper or real accounts. Shared architecture reduces code drift but does not erase venue, network, timing and reconciliation risk.
- **Why care:** prevents the claim that a green backtest proves production readiness.

### Хронометраж по экранам (ровно 90 минут)
| Экран | Теория | Демо | Практика | Квиз | Итого | Результат |
|---|---:|---:|---:|---:|---:|---|
| 1. Три режима полёта | 15 | 0 | 0 | 0 | 15 | различает назначение сред |
| 2. Что реально меняется | 5 | 15 | 0 | 0 | 20 | сравнивает пять измерений |
| 3. Каркас BacktestEngine | 0 | 10 | 5 | 0 | 15 | читает минимальную конфигурацию |
| 4. Guided lab «Допуск к рейсу» | 0 | 0 | 25 | 0 | 25 | строит promotion-gates |
| 5. Решение о запуске | 0 | 0 | 5 | 10 | 15 | принимает evidence-based решение |
| **Итого** | **20** | **25** | **35** | **10** | **90** | |

**Баланс форматов:** теория — 20 мин; демонстрация — 25 мин; практика — 35 мин; квиз — 10 мин. **Итого: 90 мин.**

### Code Snippets (pre-extracted)
File: docs/getting_started/quickstart.py (lines 205-209, exact continuous excerpt from commit `84a98f7f3cc786085496976320c3cb320024217f`)
```python
engine = BacktestEngine(
    config=BacktestEngineConfig(
        logging=LoggerConfig(stdout_level=LogLevel.ERROR),
    ),
)
```

### Interactive Elements
- Code↔English: exact snippet.
- Quiz: 4 promotion decisions from backtest to sandbox/live.
- Layer toggle: Backtest / Sandbox / Live, showing clock, data, execution, risk. Explicitly state that Nautilus Sandbox is not an exchange testnet and Live does not necessarily mean real money.
- Permission/config badges: доказательства, необходимые для перехода.
- Final map and next-course CTA: course 02.

### Guided lab — «Допуск к рейсу» (25 минут)
Для стратегии с хорошим историческим результатом ученик строит две двери: Backtest→Sandbox и Sandbox→Live. У каждой двери минимум четыре измеримых доказательства: качество/целостность данных, поведение исполнения, риск-лимиты, сверка позиций и аварийная остановка. Затем отмечает, какие доказательства невозможно получить в предыдущей среде.

### Самостоятельное задание (входит в экран 5)
Получен отчёт: «бэктест зелёный, 50 sandbox-ордеров без ошибок». Принять решение GO / NO-GO для live с минимальным капиталом, перечислить недостающие доказательства и сформулировать запрос AI на их сбор без автоматического запуска торговли.

### Артефакт ученика
Promotion checklist на одну страницу: среда, доступные доказательства, критерий выхода, стоп-условие, владелец проверки, ссылка на наблюдаемый отчёт.

### Критерии приёмки
- Backtest, Sandbox и Live не названы взаимозаменяемыми.
- Для каждого перехода есть измеримые критерии и стоп-условия.
- Реальный запуск не разрешён только на основании доходности или отсутствия ошибок.
- В checklist присутствуют исполнение, риск, reconciliation и kill switch.

### Преподавательские заметки
- В начале спросить: «Что авиасимулятор принципиально не может доказать?» — перенести ответы на trading.
- Не обсуждать прибыльность как гарантию; цель — качество доказательств и эксплуатационная готовность.
- Подчеркнуть, что Sandbox тоже может отличаться от реальной площадки по ликвидности и задержкам.
- В финале связать четыре модуля одной картой: событие → актёры → callback → среда доказательств.

### Reference Files to Read
- interactive-elements.md → Code Translation, Quizzes, Layer Toggle, Glossary Tooltips, Permission Badges.
- content-philosophy.md and gotchas.md → fully.

### Connections
- Previous: strategy callbacks. Next: course 02 data/research. Russian; safety-first, never imply profitability.
