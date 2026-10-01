# Практикум: 12 лабораторных работ

Каждая лабораторная работа содержит входные данные, контрольные точки, ожидаемый результат и критерии приёмки. Не открывайте ответы преподавателя до завершения работы.

## 1.1 Потерянная котировка — 25 минут

### Вход

| Наблюдение | Значение |
|---|---|
| Adapter received | `QuoteTick EUR/USD ts_event=10:00:00.100` |
| DataEngine input | 1 event |
| Cache last quote | `None` |
| MessageBus publication | 0 events |
| Strategy callback | 0 calls |

### Работа

1. За 5 минут отметьте первую границу, на которой вход есть, а подтверждения выхода нет.
2. За 8 минут заполните event trace: компонент, вход, ожидаемый выход, наблюдение.
3. За 7 минут напишите три минимальные проверки без изменения strategy logic.
4. За 5 минут сформулируйте prompt AI, который запрещает широкую переработку до локализации.

**Checkpoint:** причина не называется до сравнения соседних границ.  
**Артефакт:** event trace + диагностический prompt.  
**Приёмка:** пять узлов, первая непроверенная граница, минимум две наблюдаемые проверки.

## 1.2 Кто владеет задачей — 25 минут

### Вход: 12 задач

Нормализовать QuoteTick; проверить max notional; сохранить last quote; пересчитать unrealized PnL; доставить event подписчикам; отправить команду venue; зарегистрировать Strategy; восстановить account report; выбрать data client; отклонить reduce-only violation; хранить position state; вызвать callback стратегии.

### Работа

Разложите карточки между `DataEngine`, `RiskEngine`, `ExecutionEngine`, `Cache`, `Portfolio`, `MessageBus`, `Trader`. Для каждой карточки укажите вход и выход. Три спорные карточки защитите письменно.

**Checkpoint:** «отправить команду venue» не принадлежит Strategy.  
**Артефакт:** responsibility matrix 12×4.  
**Приёмка:** один primary owner на задачу; соседний компонент указан только как collaborator.

## 1.3 Тишина в callback — 35 минут

### Вход: три случая

```text
A: on_start completed; subscribe_bars absent; on_bar calls=0
B: subscription active; bars received=8; indicator initialized=false
C: subscription active; indicator initialized=true; on_bar calls=8; orders=0
```

### Работа

Для каждого случая заполните callback passport: prerequisite, subscription, event, readiness gate, handler effect, diagnostic signal. Назначьте следующую минимальную проверку.

**Checkpoint:** B не исправляется `sleep`; C требует проверять branch/state, а не доставку.  
**Артефакт:** три callback passports.  
**Приёмка:** причины A/B/C различены, polling loop не предлагается.

## 1.4 Карта сред — 30 минут

### Вход

Сценарий: исторический replay прошёл; стратегия 40 минут обрабатывала real-time quotes с simulated execution; live execution client не подключался; exchange testnet не использовался.

### Работа

1. Классифицируйте пройденные этапы как Backtest/Sandbox/Live.
2. Отдельно укажите, что доказал и чего не доказал Nautilus Sandbox.
3. Постройте следующий gate без предположения, что Sandbox равен testnet.

**Артефакт:** environment evidence matrix.  
**Приёмка:** `Sandbox = real-time data + simulated execution`; `Live` допускает paper или real account.

## 2.1 Шесть тиков — 30 минут

### Входной набор

| row | ts_event UTC | ts_init UTC | bid | ask |
|---:|---|---|---:|---:|
| 1 | 10:00:00.100 | 10:00:00.110 | 1.1000 | 1.1002 |
| 2 | 10:00:01.100 | 10:00:01.115 | 1.1001 | 1.1003 |
| 3 | 10:00:03.100 | 10:00:03.120 | 1.1003 | 1.1005 |
| 4 | 10:00:02.100 | 10:00:02.118 | 1.1002 | 1.1004 |
| 5 | 10:00:03.100 | 10:00:03.120 | 1.1003 | 1.1005 |
| 6 | 10:05:30.000 | 10:05:30.010 | 1.1010 | 1.1009 |

Заявлено: EUR/USD, диапазон 10:00–10:05, UTC, без дублей, `bid <= ask`.

### Работа

Найдите нарушение порядка, дубликат, выход за диапазон и crossed quote. Отделите наблюдение от решения: ничего не удаляйте молча. Сформируйте data evidence sheet и quarantine list.

**Артефакт:** паспорт данных + четыре disposition решения.  
**Приёмка:** каждая проблема связана с row; исходная строка сохраняется; преобразование имеет причину и audit note.

## 2.2 Manifest A/B — 30 минут

### Вход

| Поле | A | B |
|---|---|---|
| commit | `abc111` | `abc111` |
| instrument | `AUD/USD.SIM` | `AUD/USD.SIM` |
| start | `2026-01-01` | `2026-01-01` |
| end | `2026-03-31` | `2026-03-31` |
| fee model | `zero` | `0.2 bps` |
| slippage | `zero` | `1 tick` |
| fast/slow | `10/20` | `10/20` |
| catalog hash | `h1` | `h2` |

### Работа

Определите, какие различия делают результаты несопоставимыми, какие требуют нового run ID и какие артефакты надо запросить для `h1/h2`. Создайте B2, изменив только одну переменную.

**Артефакт:** manifest diff + B2.  
**Приёмка:** B2 имеет один controlled change; fee/slippage и catalog hash не скрыты.

## 2.3 Гипотеза, а не сигнал — 30 минут

### Вход

EMA cross дал положительный gross PnL на одном квартале. После fee/slippage PnL близок к нулю. На втором инструменте результат отрицателен. Период `10/20` выбран после просмотра пяти вариантов.

### Работа

Заполните hypothesis card: механизм, сигнал, действие, состояние, издержки, falsifier, альтернативное объяснение. Запишите один untouched-forward test.

**Артефакт:** hypothesis card + preregistered test.  
**Приёмка:** gross PnL не назван прибылью; multiple testing и selection bias отражены.

## 2.4 Границы утверждения — 30 минут

### Входной пакет доказательств

Есть build log, catalog manifest, deterministic replay и один positive result. Нет forward window, shadow report, reconciliation report, canary budget и kill-switch drill.

### Работа

Классифицируйте пять утверждений: «код собирается», «replay воспроизводим», «идея прибыльна», «система live-ready», «можно увеличить капитал». Для каждого дайте `SUPPORTED`, `NOT_EVALUABLE` или `NO-GO` и следующий необходимый evidence.

**Артефакт:** claim/evidence matrix.  
**Приёмка:** отсутствие артефакта не превращается в PASS; следующий gate — forward, а не live.

## 3.1 Карта владения Rust state — 28 минут

### Вход

Поля: `StrategyCore`, `instrument_a`, `instrument_b`, `trade_size`, `latest_spread`, `entry_threshold`, `logger`, `current_quote` внутри callback.

### Работа

Разделите framework plumbing, persistent strategy state, configuration и event-local values. Для каждого поля укажите owner и lifecycle. Затем составьте два AI-prompts, запрещающих дублировать `StrategyCore`.

**Артефакт:** Rust ownership map.  
**Приёмка:** Rust остаётся canonical runtime; event-local quote не хранится без причины.

## 3.2 Где исчезла заявка — 35 минут

### Входная трассировка

```text
quote_received=PASS
callback_entered=PASS
order_created=PASS client_order_id=O-17
risk_command=PASS
risk_event=DENIED reason=max_notional
execution_submit=ABSENT
venue_ack=ABSENT
```

### Работа

Постройте decision tree для четырёх симптомов: нет quote, нет callback, risk deny, unknown venue outcome. Для данного trace выберите owner и безопасную реакцию.

**Артефакт:** incident decision tree.  
**Приёмка:** deny не называется transport failure; повторный submit запрещён без idempotency/reconciliation.

## 3.3 Native backtest charter — 30 минут

### Вход

Два запуска Rust EmaCross: `10/20` и `20/50`; один и тот же catalog hash, fee model, slippage, time window и seed. Требуется canonical report без Python runtime dependency.

### Работа

Заполните charter: build command, locked dependencies, run configs, invariant inputs, single changed parameter, output hashes, report schema и failure policy.

**Артефакт:** native validation plan + A/B manifest.  
**Приёмка:** Python не требуется для build/replay/report; результаты имеют machine-readable provenance.

## 3.4 Live promotion dossier — 45 минут

### Вход

| Gate | Evidence |
|---|---|
| build | PASS |
| deterministic replay | PASS |
| untouched forward | missing |
| shadow | 24 h, 2 disconnects, recovered |
| reconciliation | one unresolved position mismatch |
| kill switch | not drilled |
| canary | budget proposed, not approved |

### Работа

1. Вынесите текущий вердикт.
2. Опишите порядок закрытия пробелов.
3. Заполните startup abort conditions, account-specific limits, kill-switch trigger, rollback и human owner.
4. Проведите tabletop incident: venue ack потерян после submit.

**Артефакт:** gate matrix + kill-switch runbook + incident log.  
**Приёмка:** verdict `NO-GO`; unresolved reconciliation и undrilled kill switch блокируют canary; повтор submit не выполняется вслепую.

## Как сдавать

Используйте соответствующие 12 разделов `LEARNER_WORKBOOK.md`. Каждый артефакт получает `PASS`, `REVISION_REQUIRED` или `NOT_EVALUABLE`. К итоговому проекту допускаются только 12 `PASS`; отсутствие входных данных не заменяется предположением.
