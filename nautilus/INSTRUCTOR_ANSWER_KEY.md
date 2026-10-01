# Ответы преподавателя и правила оценивания

Этот файл предназначен для преподавателя. Он задаёт ожидаемые наблюдения, но не заменяет обсуждение причинной цепочки.

| Lab | Ключевые наблюдения | Минимальный PASS |
|---|---|---|
| 1.1 | Первая потеря между DataEngine input и Cache/store-publication path | Локализована граница, нет переписывания strategy |
| 1.2 | Data→DataEngine; validation→RiskEngine; venue command→ExecutionEngine; state→Cache/Portfolio | 10/12 primary owners верны, все спорные решения обоснованы |
| 1.3 | A subscription; B warm-up; C state/branch | Три причины не смешаны |
| 1.4 | Пройдены Backtest и Sandbox; Live execution не доказан | Sandbox не назван testnet, Live не равен real money |
| 2.1 | row 4 order, row 5 duplicate, row 6 range + crossed quote | Четыре проблемы с row IDs и audit disposition |
| 2.2 | fee, slippage и hash меняют evidence; B2 меняет ровно одно поле | Нет скрытого multi-variable comparison |
| 2.3 | Один квартал и пять вариантов создают selection risk | Есть falsifier и untouched-forward plan |
| 2.4 | Build/replay supported; profitability not evaluable; live/scale NO-GO | Следующий gate — forward |
| 3.1 | Core framework-owned; IDs/size/spread strategy-owned; quote event-local | Rust canonical; lifecycle у каждого поля |
| 3.2 | RiskEngine дал DENIED, execution/venue не вызывались | Нет retry submit; owner и evidence названы |
| 3.3 | Один changed parameter; все прочие inputs invariant | Locked build и machine-readable canonical report |
| 3.4 | NO-GO: forward missing, reconciliation unresolved, kill switch not drilled | Порядок remediation, abort, limits, rollback, owner |

## Правила подтверждения освоения

- Module quiz: минимум 80% правильных ответов с округлением требуемого количества вверх (`ceil(0,8 × N)`). Поэтому для 3 или 4 вопросов порог равен всем правильным ответам; интерфейс показывает счёт и итоговый verdict.
- Lab: все обязательные acceptance criteria выполнены.
- Повторная попытка разрешена после изучения объяснений. Преподаватель проверяет перенос понимания на лабораторном scenario, а не засчитывает один только запомненный quiz.
- До следующего курса допускается максимум один `REVISION_REQUIRED`, который закрывается до capstone.
- Capstone: минимум 75/100 и не менее 14/20 за Live safety.

## Пилотный хронометраж

До публичного релиза проведите минимум три наблюдаемых прогона на представителях целевой аудитории. Фиксируйте медиану и диапазон времени отдельно для объяснения, guided lab, самостоятельной работы и quiz. Значения в manifest считаются плановыми до появления этого evidence; после пилота обновите их без искусственного растягивания.
