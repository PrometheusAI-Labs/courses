# Рабочая тетрадь ученика

Сохраняйте ответы после каждого модуля. Итоговый проект собирается из этих артефактов, поэтому не заменяйте их устными объяснениями.

## Шаблон трассировки события

| Шаг | Компонент-владелец | Вход | Выход | Где наблюдать | Что может сломаться |
|---:|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |

## Шаблон архитектурного решения

- Задача:
- Компонент-владелец:
- Почему не соседний компонент:
- Событие или команда на входе:
- Событие или состояние на выходе:
- Проверка успеха:
- Безопасное поведение при ошибке:

## Паспорт данных

- Поставщик и формат:
- Инструмент и venue:
- Тип данных:
- Диапазон времени и timezone:
- Значение `ts_event`:
- Значение `ts_init`:
- Проверка монотонности:
- Пропуски и дубликаты:
- Преобразования до каталога:
- Версия/хэш набора:

## Паспорт запуска

- Версия NautilusTrader:
- Версия стратегии:
- Параметры стратегии:
- Venue model:
- Data config:
- Execution/fee/slippage assumptions:
- Начальный баланс:
- Временной диапазон:
- Seed, если используется случайность:
- Команда запуска:
- Пути к отчётам:

## Карточка гипотезы

- Наблюдаемая неэффективность:
- Механизм, который может её создавать:
- Сигнал:
- Действие:
- Ограничения риска:
- Фальсифицирующий результат:
- Альтернативное объяснение:
- Метрика до издержек:
- Метрика после издержек:

## Лестница доказательств

| Gate | Что доказано | Что ещё не доказано | Артефакт | Решение |
|---|---|---|---|---|
| Build |  |  |  | GO / NO-GO |
| Deterministic replay |  |  |  | GO / NO-GO |
| Forward |  |  |  | GO / NO-GO |
| Shadow |  |  |  | GO / NO-GO |
| Canary |  |  |  | GO / NO-GO |
| Live expansion |  |  |  | GO / NO-GO |

## Карточка безопасности Live

- Account and venue:
- Allowed instruments:
- Max order quantity/notional:
- Max position:
- Rate limits:
- Reconciliation policy:
- Startup abort conditions:
- Kill switch trigger:
- Loss/time budget:
- Rollback procedure:
- Human owner:

---

## 12 обязательных результатов по модулям

Заполняйте раздел после соответствующей лаборатории из `LABS.md`. Каждый раздел сдаётся отдельно.

## Артефакт 1.1 — Event trace

- Симптом:
- Последняя подтверждённая граница:
- Первая неподтверждённая граница:
- Пять узлов `owner / input / expected output / observation / next check`:
- Prompt AI без широкого refactor:
- Checklist: [ ] 5 узлов [ ] 2 проверки [ ] нет догадки вместо evidence

## Артефакт 1.2 — Responsibility matrix

Для каждой из 12 карточек: `task / primary owner / input / output / collaborator / rationale`.

- Три спорных решения:
- Checklist: [ ] один primary owner [ ] Strategy не обходит Risk/Execution [ ] state ownership явно

## Артефакт 1.3 — Callback passports

Для A, B и C: `prerequisite / subscription / event / readiness gate / effect / diagnostic / next check`.

- Checklist: [ ] A/B/C различены [ ] нет sleep/polling как исправления [ ] проверка минимальна

## Артефакт 1.4 — Environment evidence matrix

| Environment | Data | Execution | Что доказано | Что не доказано | Следующий gate |
|---|---|---|---|---|---|
| Backtest | | | | | |
| Sandbox | | | | | |
| Live | | | | | |

- Checklist: [ ] Sandbox не равен testnet [ ] Live допускает paper/real [ ] real-money authority отдельно

## Артефакт 2.1 — Data evidence sheet

- Нарушения по row ID:
- Quarantine list:
- Разрешённые преобразования и причины:
- Hash/версия исходного набора:
- Checklist: [ ] порядок [ ] дубли [ ] диапазон [ ] bid/ask invariant [ ] audit note

## Артефакт 2.2 — Manifest diff и B2

- Поля A/B, которые различаются:
- Какие различия invalidating:
- Единственное изменение B2:
- Run ID и expected artifact paths:
- Checklist: [ ] one-variable test [ ] catalog hash [ ] fee/slippage [ ] code version

## Артефакт 2.3 — Hypothesis card

- Механизм:
- Signal / state / action:
- Издержки:
- Falsifier:
- Alternative explanation:
- Untouched-forward window и preregistered metric:
- Checklist: [ ] selection bias учтён [ ] gross != net [ ] есть falsifier

## Артефакт 2.4 — Claim/evidence matrix

| Claim | Evidence | SUPPORTED / NOT_EVALUABLE / NO-GO | Missing artifact | Next safe gate |
|---|---|---|---|---|
| Build | | | | |
| Replay | | | | |
| Profitability | | | | |
| Live readiness | | | | |
| Scale | | | | |

## Артефакт 3.1 — Rust ownership map

| Field | Framework / config / strategy / event-local | Owner | Lifecycle | Why |
|---|---|---|---|---|

- AI prompt 1:
- AI prompt 2:
- Checklist: [ ] Rust canonical [ ] StrategyCore не дублируется [ ] event-local state обоснован

## Артефакт 3.2 — Incident decision tree

- Branches: no quote / no callback / risk deny / unknown venue outcome.
- Для каждой: evidence, owner, safe action, forbidden action.
- Checklist: [ ] submit != fill [ ] deny != transport error [ ] blind retry запрещён

## Артефакт 3.3 — Native backtest charter

- Locked build command:
- Run A / Run B:
- Invariant inputs:
- Single changed parameter:
- Output hashes:
- Canonical report schema/path:
- Failure policy:
- Checklist: [ ] Python не runtime dependency [ ] machine-readable provenance [ ] one-variable comparison

## Артефакт 3.4 — Live promotion dossier

- Gate matrix: build / replay / forward / shadow / reconciliation / kill-switch drill / canary.
- Startup abort conditions:
- Account-specific limits:
- Kill-switch trigger and tested action:
- Unknown-outcome procedure:
- Rollback and human owner:
- Verdict and expiry time:
- Checklist: [ ] unresolved reconciliation blocks [ ] undrilled kill switch blocks [ ] canary bounded [ ] no blind resubmit

## Связь с итоговым проектом

| Capstone material | Supporting module artifacts |
|---|---|
| Architecture map | 1.1, 1.2, 1.3 |
| Environment and evidence boundaries | 1.4, 2.4 |
| Data and reproducible run | 2.1, 2.2 |
| Strategy hypothesis | 2.3 |
| Rust-native ownership and validation | 3.1, 3.3 |
| Order lifecycle | 3.2 |
| Live safety dossier | 3.4 |

Перед capstone все 12 артефактов должны иметь `PASS`. Статус `NOT_EVALUABLE` допустим как честная промежуточная фиксация недостающего входа, но блокирует допуск к capstone и никогда не считается разрешением live.
