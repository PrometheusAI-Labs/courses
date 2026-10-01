# Статус версии-кандидата

**Дата:** 2026-09-22  
**Источник:** NautilusTrader `develop` @ `84a98f7f3cc786085496976320c3cb320024217f`  
**Объект:** 3 курса, 12 модулей, 1200 плановых минут

## Текущий вердикт

| Область | Статус | Evidence |
|---|---|---|
| Техническая корректность | **GO** | Независимый read-only review; точные snippets; согласованные Backtest/Sandbox/Live, Rust-first и safety semantics |
| Внутренние учебные материалы | **GO** | Независимый read-only review; 12 labs, 12 workbook artifacts, executable mastery и capstone rubric |
| Release artifact | **REVISION REQUIRED** | Publish root, локальные assets/links, localization и статические keyboard controls готовы; contrast defect и формальная license review остаются открыты |
| Публичный релиз | **NO-GO** | Не исправлен подтверждённый contrast defect; не заполнены pilot timing и ручной browser/accessibility QA |

`GO` в первых двух строках означает готовность учебного содержания к внешним проверкам. Release artifact и публичный допуск остаются заблокированы перечисленными ниже условиями.

## Автоматически подтверждено

- `python3 verify_courses.py` — PASS: 3 курса, 12 модулей, 1200 плановых минут.
- `python3 verify_source_snippets.py --source /tmp/nautilus_trader-course-source` — PASS: 12 точных непрерывных excerpts на pinned commit.
- `node --check courses/01-engine-foundations/main.js` — PASS; shared runtime идентичен во всех трёх курсах.
- Собранные `index.html` идентичны `_base.html + modules/*.html + _footer.html`.
- Локальные ссылки существуют, duplicate IDs не найдены, обязательных внешних runtime/font requests нет.
- Release junk (`.DS_Store`, `*.pyc`, caches) отсутствует и проверяется verifier-ом.

## Закрытые замечания независимой проверки

- Исправлена семантика Sandbox и Live; Sandbox отделён от exchange testnet.
- Все 12 source snippets восстановлены как точные непрерывные excerpts.
- Добавлены 12 исполнимых labs, 12 workbook artifacts, answer key, mastery verdict и многоуровневая capstone rubric.
- Синхронизирована лестница `build → replay/backtest → untouched forward → shadow → bounded canary → live expansion`.
- Исправлены границы Adapter/DataEngine и scope reconciliation; balance/margin вынесены в отдельный account-state/risk gate.
- Добавлены LGPL text, third-party notice, pinned source и non-affiliation notice.
- Русифицирован runtime; добавлены keyboard semantics, focus styles, reduced motion и mobile reflow. Contrast finding не закрыт: белый текст на `#D94F30` даёт около `4.11:1` вместо требуемых `4.5:1`.
- Добавлены publish root, каталог, resources route и межкурсовая навигация.

## Оставшиеся внешние условия публикации

### 0. Контраст и license review

- заменить либо скорректировать `--color-accent: #D94F30` для controls с белым текстом и повторить проверку всех состояний;
- зафиксировать ответственную проверку формата распространения LGPL snippets и подготовленных notices.

### 1. Пилотный хронометраж

Заполнить `PILOT_TIMING_RECORD.md` минимум по трём представителям аудитории, рассчитать медиану и диапазон, затем:

- подтвердить диапазон 1080–1320 минут; либо
- скорректировать `course-manifest.json`, curriculum и learner-facing duration claims по фактическому evidence.

### 2. Проверка в браузерах и доступность

Заполнить `BROWSER_ACCESSIBILITY_QA.md` на том же release archive:

- desktop 1440×900;
- mobile 390×844;
- 200% zoom;
- keyboard-only;
- screen reader;
- reduced motion и forced colors;
- console/runtime regression.

## Условие разрешения на публичную публикацию

Публичный релиз получает `GO` только если оба протокола имеют итоговый `PASS`, найденные дефекты исправлены, автоматические проверки повторно зелёные и финальный чистый архив проверен по checksum. Реальная публикация требует отдельной явной авторизации.
