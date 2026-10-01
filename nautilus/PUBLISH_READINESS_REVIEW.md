# Проверка готовности к публикации

> **Исторический снимок первой проверки с повторной сверкой от 2026-09-23.** Исходные reviewer findings сохранены ниже. Полностью исправленные пункты зачёркнуты; у частично исправленных зачёркнута только доказанно закрытая часть. Публичный релиз всё ещё заблокирован до заполненного пилотного хронометража и фактической browser/keyboard/screen-reader проверки. Исходный `NO-GO` остаётся исторически верным.

**Повторная сверка:** 8 из 12 HIGH исправлены полностью, 3 исправлены частично, 1 остаётся открытым. Из 8 MEDIUM полностью исправлены 5, частично — 2, открыт — 1. Автоматические проверки `verify_courses.py` и `verify_source_snippets.py` прошли; пустые ручные протоколы не засчитывались как `PASS`.

**Дата:** 2026-09-22  
**Объект:** NautilusTrader Academy, 3 курса / 12 модулей / заявленные 1200 минут  
**Итоговый вердикт:** **NO-GO TO PUBLISH**

Проверку независимо и без редактирования учебных материалов провели три reviewer-а с разными линзами: педагогическая состоятельность, техническая/source-grounded корректность и release/accessibility readiness. Все три независимо вынесли `NO-GO TO PUBLISH`.

## Что подтверждено

- `verify_courses.py` проходит: 3 курса, 12 модулей, 1200 минут.
- Все три курса собираются воспроизводимо из `_base.html + modules/*.html + _footer.html`.
- Локальные `href`/`src`, quiz keys, chat sequences и flow JSON статически корректны.
- Обязательные интерактивы присутствуют: code-to-English, quizzes, glossary terms, group chat и data flow.
- Секретов, private keys, `.env`, cache/compiled junk и обещаний доходности не найдено.
- Rust-first направление, различение submit/fill и safety-гейты в целом выдержаны.

Эти результаты доказывают структурную целостность сборки, но не педагогическую, техническую и публикационную готовность.

## Критические блокеры

### ~~1. Неверно объяснены NautilusTrader Sandbox и Live~~ — ИСПРАВЛЕНО

- ~~**Evidence:** `courses/01-engine-foundations/modules/04-three-environments.html:6,19-25,51-64`.~~
- ~~**Проблема:** Sandbox представлен как testnet-площадка с reconnect/reconciliation, Live — как обязательно реальные деньги. Upstream `docs/concepts/architecture.md:150-154` задаёт `Sandbox = real-time data + simulated execution`, а `Live = real-time data + live venue connections`, включая paper и real accounts.~~
- ~~**До GO:** переписать экран, brief и quiz по канонической семантике; явно отделить Nautilus Sandbox от exchange testnet.~~
- **Повторная проверка:** module, brief, assembled index и quiz теперь определяют Sandbox как real-time data + simulated execution, Live — как live venue connections для paper или real account; exchange testnet явно отделён от Sandbox.

### ~~2. Provenance сниппетов заявлен неверно~~ — ИСПРАВЛЕНО

- ~~**Evidence:** `README.md:18-20` и 12 code sections в `courses/*/briefs/`.~~
- ~~**Проблема:** README заявляет дословный перенос и точные строки, но независимое сравнение с commit `84a98f7f3cc786085496976320c3cb320024217f` показало буквальное совпадение только для 3 из 12 диапазонов. Остальные дедентированы, сокращены или не соответствуют заявленному непрерывному диапазону.~~
- ~~**До GO:** либо восстановить точные непрерывные фрагменты и строки, либо честно маркировать адаптацию/сокращение; синхронизировать briefs, modules и собранные indexes.~~
- **Повторная проверка:** `python3 verify_source_snippets.py --source /tmp/nautilus_trader-course-source` подтвердил 12 точных непрерывных excerpts на pinned commit.

### 3. Заявленные 20 часов не подтверждены пилотным хронометражем — ЧАСТИЧНО

- **Evidence:** `INSTRUCTOR_GUIDE.md:5,35`, `courses/03-rust-live/briefs/01-rust-anatomy.md:40-42`, `courses/03-rust-live/modules/01-rust-anatomy.html:101-114`, `verify_courses.py:108-109`.
- **Проблема:** validator суммирует заявленные числа, но не доказывает реальный seat time. ~~Часть HTML-практик значительно короче таймбоксов и не содержит обещанных разборов, материалов и checkpoint-ов.~~
- **До GO:** ~~дать 12 исполнимых сценариев с входами, промежуточными проверками, ожидаемыми артефактами и answer keys;~~ провести пилотный хронометраж минимум на трёх представителях аудитории.
- **Повторная проверка:** `LABS.md`, `LEARNER_WORKBOOK.md` и `INSTRUCTOR_ANSWER_KEY.md` закрывают контентную часть. `PILOT_TIMING_RECORD.md` остаётся пустым, поэтому фактические 20 часов не доказаны.

### ~~4. Для ключевых labs отсутствуют исходные кейсы~~ — ИСПРАВЛЕНО

- ~~**Evidence:** `courses/02-backtest-research/modules/01-data-evidence.html:104-117`, `modules/02-reproducible-run.html:73-85` и соответствующие briefs.~~
- ~~**Проблема:** заявлены набор из шести тиков и паспорта A/B, но сами значения и дефекты не предоставлены.~~
- ~~**До GO:** добавить копируемые/downloadable datasets, manifests/passports, карточки инцидентов, ожидаемые наблюдения и instructor answer key.~~
- **Повторная проверка:** `LABS.md` содержит все 12 входных кейсов, включая шесть тиков, manifest A/B, checkpoints, ожидаемые результаты и связь с answer key.

### ~~5. Workbook не покрывает 12 обязательных артефактов~~ — ИСПРАВЛЕНО

- ~~**Evidence:** `CURRICULUM.md:42-47`, `LEARNER_WORKBOOK.md:5-85`, module briefs.~~
- ~~**Проблема:** curriculum обещает один проверяемый артефакт на модуль, но workbook содержит 7 общих шаблонов и не даёт формы для ряда обязательных результатов.~~
- ~~**До GO:** создать 12 пронумерованных workbook-секций с input case, полями, acceptance checklist и связью с capstone.~~
- **Повторная проверка:** `LEARNER_WORKBOOK.md` содержит 12 секций `Артефакт 1.1`–`3.4`, checklist для каждой и отдельную mapping-таблицу к capstone.

### ~~6. Learner UI не полностью локализован~~ — ИСПРАВЛЕНО

- ~~**Evidence:** `courses/01-engine-foundations/main.js:184-200,335-336,397-399`; тот же JS используется во всех курсах.~~
- ~~**Проблема:** quiz/chat/flow показывают английские `Pick an answer first!`, `Exactly!`, `Not quite.`, `messages`, `Step` в заявленном русскоязычном курсе.~~
- ~~**До GO:** добавить поддерживаемый слой русской локализации и проверить все UI-состояния.~~
- **Повторная проверка:** learner-facing runtime русифицирован; verifier запрещает прежние английские фразы, а shared `main.js` идентичен во всех трёх курсах.

### ~~7. Workbook и capstone отсутствуют в публикуемом HTML-маршруте~~ — ИСПРАВЛЕНО

- ~~**Evidence:** `courses/index.html:38-65`, `CAPSTONE.md:7-30`.~~
- ~~**Проблема:** каталог обещает workbook/capstone, но ссылается только на три курса; внутри курсов нет переходов к материалам и назад к каталогу.~~
- ~~**До GO:** опубликовать материалы в доступном формате и связать catalog → courses → workbook/capstone → back/next navigation.~~
- **Повторная проверка:** `courses/resources.html`, `courses/docs/index.html` и footer каждого курса связывают каталог, labs, workbook, capstone, документы и межкурсовую навигацию; document integration QA имеет `PASS`.

### 8. License/third-party notice добавлены, ответственная проверка не зафиксирована — ЧАСТИЧНО

- **Evidence:** `README.md:18-20`; в дереве отсутствуют `LICENSE` и `THIRD_PARTY_NOTICES`.
- **Проблема:** пакет повторно распространяет точные/адаптированные фрагменты проекта LGPL-3.0-only ~~без лицензионного текста, copyright notice и маркировки адаптаций~~.
- **До GO:** ~~добавить полный LGPL-3.0 text, third-party notice с точным commit и copyright, обозначить адаптации;~~ получить и зафиксировать ответственную лицензионную проверку формата распространения.
- **Повторная проверка:** `LICENSES/nautilus-trader-LGPL-3.0.txt`, `THIRD_PARTY_NOTICES.md` и `LICENSE.md` существуют и опубликованы в HTML. Отдельный подписанный/названный legal review в evidence не найден.

### ~~9. Интерактивы недоступны с клавиатуры и screen reader~~ — ИСПРАВЛЕНО В КОДЕ

- ~~**Evidence:** `courses/01-engine-foundations/modules/02-engine-team.html:42`, `courses/03-rust-live/modules/01-rust-anatomy.html:74`, `courses/01-engine-foundations/main.js:150,457`.~~
- ~~**Проблема:** кликабельные `div` и `span` не имеют keyboard semantics, focus, roles и связей с обновляемым описанием.~~
- ~~**До GO:** заменить управления на buttons либо добавить Enter/Space, focus, `aria-expanded`/`aria-selected`, `aria-controls` и live announcement.~~
- **Повторная проверка:** runtime добавляет keyboard handlers, focus semantics, `aria-pressed`/`aria-selected`/`aria-controls` и live announcements; verifier проверяет обязательные markers. Полный ручной keyboard/screen-reader протокол всё ещё является отдельным release gate.

### 10. Mobile reflow исправлен в CSS, полный 200% прогон не выполнен — ЧАСТИЧНО

- **Evidence:** `courses/01-engine-foundations/styles.css:798,1166-1172`, `courses/03-rust-live/modules/04-live-safety.html:57`.
- **Проблема:** ~~mobile override стирает верхний отступ под fixed nav; четыре `.layer-tabs` не переносятся на узком viewport.~~
- **До GO:** ~~сохранить mobile nav offset, сделать tabs wrap/scroll-safe~~ и пройти Chrome desktop/mobile/200% без overlap и двумерного скролла.
- **Повторная проверка:** mobile `.module` сохраняет nav offset, `.layer-tabs` использует `flex-wrap`. `BROWSER_ACCESSIBILITY_QA.md` не заполнен; document-only smoke test не заменяет полный 200% прогон курсов.

### 11. Контраст основных controls ниже WCAG AA — ОТКРЫТ

- **Evidence:** `courses/02-backtest-research/_base.html:26`, `courses/03-rust-live/_base.html:26`, `styles.css:456,803`.
- **Проблема:** белый 14 px текст на vermillion и forest accents имеет около 4.11:1 и 4.25:1 при требовании 4.5:1.
- **До GO:** скорректировать colors/text и повторить contrast audit для всех control states.
- **Повторная проверка:** пункт не закрыт. Текущий `--color-accent: #D94F30`; контраст белого текста составляет примерно `4.11:1`. Этот цвет по-прежнему используется для 14 px quiz buttons и активных layer tabs, поэтому требование `4.5:1` не выполнено. Полный contrast/forced-colors протокол также пуст.

### ~~12. Не определён publish root~~ — ИСПРАВЛЕНО

- ~~**Evidence:** `README.md:14`, `courses/index.html:44`; корневой `index.html` и hosting config отсутствуют.~~
- ~~**Проблема:** публикация корня стандартным static host не открывает каталог.~~
- ~~**До GO:** добавить root entrypoint либо зафиксировать `courses/` как publish directory и проверить конечные URLs.~~
- **Повторная проверка:** корневой `index.html` существует, ведёт к трём курсам и ресурсам; локальные маршруты и конечные HTML-документы проверяются verifier-ом.

## MEDIUM, обязательные до release candidate

- ~~`lang="en"` в трёх русскоязычных `_base.html` и собранных indexes.~~ **ИСПРАВЛЕНО:** все learner pages используют `lang="ru"`, это проверяет verifier.
- Glossary tooltips не покрывают каждый технический термин при первом употреблении. **ОТКРЫТ:** наличие glossary terms в каждом модуле проверяется, но полнота покрытия всех терминов и именно первого употребления — нет.
- ~~Evidence ladder противоречива: часть файлов включает `forward`, часть объявляет полную лестницу без него.~~ **ИСПРАВЛЕНО:** зафиксирована лестница `build → replay/backtest → untouched forward → shadow → bounded canary → live expansion`.
- Distractors в quiz часто карикатурны; ~~нет mastery threshold~~ и повторного эквивалентного сценария. **ЧАСТИЧНО:** порог 80% и retry реализованы; эквивалентный, но новый повторный сценарий отсутствует, часть distractors остаётся заведомо неправдоподобной.
- ~~Capstone rubric не описывает уровни частичного выполнения.~~ **ИСПРАВЛЕНО:** `CAPSTONE.md` задаёт четыре уровня по каждому критерию и правила промежуточного балла.
- ~~Google Fonts создаёт внешний privacy/network dependency;~~ CSP/referrer policy отсутствуют. **ЧАСТИЧНО:** внешние font/runtime requests удалены и запрещены verifier-ом; CSP/referrer policy не добавлены.
- ~~Verifier жёстко зависит от абсолютного `~/.codex/skills/...` и не покрывает release gates.~~ **ИСПРАВЛЕНО:** verifier использует только пути относительно `__file__` и проверяет release files, links, docs hashes, localization, accessibility markers и release junk.
- ~~Нет `prefers-reduced-motion`; глобальные arrow-key handlers могут конфликтовать с controls.~~ **ИСПРАВЛЕНО:** reduced-motion CSS добавлен; глобальная навигация игнорирует form controls, links, buttons и ARIA controls.

## Согласие и расхождения reviewer-ов

- **Согласие:** зелёный structural validator недостаточен для GO; итог — NO-GO.
- **Согласие:** ~~provenance wording и `lang` требуют исправления.~~ Оба пункта исправлены и проверяются автоматически.
- **Согласие:** нужен реальный desktop/mobile/200% и accessibility прогон.
- **Уточнение:** release-review счёл общие financial/live boundaries ответственными; technical-review обнаружил локальную, но существенную ошибку именно в определениях Sandbox/Live. ~~Это не противоречие: safety-tone в целом хороший, конкретная модель среды — неверна.~~ Каноническая модель среды восстановлена.
- **Уникальная педагогическая находка:** ~~самостоятельная исполнимость не доказана;~~ реальные 20 часов всё ещё не доказаны пилотом.
- **Уникальная release-находка:** ~~license files, статическая keyboard accessibility и publish-root исправлены;~~ контраст остаётся дефектом, а ответственная license review и полный ручной accessibility/reflow QA не зафиксированы.

## Условия повторного GO-review

1. Закрыты все 12 HIGH с привязкой к commit/diff.
2. Все 12 labs имеют входы, checkpoints, expected outputs и answer keys.
3. Workbook содержит 12 модульных артефактов и capstone mapping.
4. Source snippets/provenance проверены автоматически относительно pinned commit.
5. Добавлены license и third-party notice.
6. Пройдены keyboard-only, screen-reader, WCAG contrast, desktop, mobile и 200% zoom проверки.
7. Проверен release artifact из чистой распакованной копии и конечный publish URL.
8. Два новых независимых reviewer-а не находят blocker/HIGH.

До выполнения этих условий публикация курса не рекомендуется.
