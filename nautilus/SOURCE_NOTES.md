# Источники и решения по версии

## Зафиксированная линия

Материалы подготовлены по ветке `develop` на commit `84a98f7f3cc786085496976320c3cb320024217f`. На этой линии README описывает Rust-native v2 runtime, Python как control plane и возможность писать mission-critical trading systems полностью на Rust.

Для production-практики нельзя автоматически переносить примеры с `develop`: upstream рекомендует `master` как последнюю выпущенную версию, а `develop` — как активную ветку разработки. Перед новым потоком курса преподаватель должен перепроверить migration guide, API и строки сниппетов.

## Главные первичные файлы

| Тема | Файл в NautilusTrader |
|---|---|
| Общая архитектура и поток событий | `docs/concepts/architecture.md` |
| MessageBus и модели сообщений | `docs/concepts/message_bus.md` |
| Стратегия и быстрый бэктест | `docs/getting_started/quickstart.py` |
| Catalog + config-driven backtest | `docs/getting_started/backtest_high_level.py` |
| Rust-стратегия | `docs/how_to/write_rust_strategy.md` |
| Rust-бэктест | `docs/how_to/run_rust_backtest.md` |
| Rust LiveNode | `docs/how_to/run_rust_live_trading.md` |
| Различия backtest/live | `docs/concepts/live.md` |
| Адаптеры | `docs/developer_guide/adapters.md` |

## Канонические границы

- Venue-specific Adapter разбирает внешний payload и создаёт доменное рыночное событие; DataEngine затем обрабатывает, кэширует, публикует и маршрутизирует его к подписчикам.
- Команда стратегии проходит RiskEngine до ExecutionEngine и venue client.
- В документации ветки `develop` контексты определены так: Backtest — исторические данные и симулированное исполнение; Sandbox — данные реального времени и симулированное исполнение; Live — данные реального времени и реальные подключения к площадкам. Live может работать с paper или real account в зависимости от адаптера и аккаунта.
- Backtest и Live разделяют каркас, но не одинаковые транспорт, тайминг, внешнюю активность и reconciliation.
- `with_reconciliation(false)` в live guide помечено как упрощение; production-пример должен включать reconciliation.
- Публичное подключение к данным не доказывает authenticated submit/cancel, reconciliation, shadow или canary.
- В Rust-first треке Python допустим только как необязательный инструмент ручного просмотра; он не является обязательной runtime- или canonical-report зависимостью.

Эти формулировки повторно сверены 22 сентября 2026 года с текущей документацией NautilusTrader `develop`: `docs/concepts/overview.md`, `docs/concepts/architecture.md`, `docs/how_to/run_rust_backtest.md` и Rust `LiveNode` examples. Зафиксированные кодовые выдержки по-прежнему проверяются локально относительно точного commit, указанного выше.

## План обновления курса

1. Обновить локальный снимок репозитория.
2. Сравнить `README.md`, migration guide и версии toolchain.
3. Перепроверить все пути и номера строк из `briefs/`.
4. Запустить сборку трёх курсов и визуальную проверку desktop/mobile/zoom 200%.
5. Зафиксировать новый commit в `course-manifest.json`, `README.md` и этой заметке.
