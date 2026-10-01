## Module 4: Live без самообмана

### Teaching Arc
- **Metaphor:** шлюз перед выходом в открытое море: проверяет системы и синхронизирует состояние до старта.
- **Opening hook:** a node can connect successfully and still be unsafe if local and venue state disagree.
- **Key insight:** adapters, credentials, reconciliation, risk limits, lifecycle and shutdown are independent gates.
- **Why care:** prevents a connectivity probe from being mislabeled as live readiness.

### Code Snippets (pre-extracted)
File: docs/how_to/run_rust_live_trading.md (lines 63-78, exact continuous excerpt from commit `84a98f7f3cc786085496976320c3cb320024217f`)
```rust
let mut node = LiveNode::builder(trader_id, Environment::Live)?
    .with_name("MY-NODE-001".to_string())
    .with_logging(log_config)
    .add_data_client(
        None,
        Box::new(OKXDataClientFactory::new()),
        Box::new(data_config),
    )?
    .add_exec_client(
        None,
        Box::new(OKXExecutionClientFactory::new()),
        Box::new(exec_config),
    )?
    .with_reconciliation(false) // Simplified; enable in production
    .with_delay_post_stop_secs(5)
    .build()?;
```

### Interactive Elements
- Code↔English exact snippet, explicitly flag the reconciliation warning.
- Quiz: 4 safety/promotion scenarios.
- Layer toggle: connectivity / auth / reconciliation / shadow / canary.
- Gate ladder with NO-GO states and kill switch.

### Reference Files to Read
- interactive-elements.md → Code Translation, Quizzes, Layer Toggle, Permission Badges, Numbered Steps, Glossary Tooltips, Callouts.
- content-philosophy.md and gotchas.md → fully.

### Connections
- Previous: native backtest. Next: learner chooses adapter/strategy specialization. Russian; safety-first, no live authorization.

### Duration
- **Total: 125 minutes.** Screen 1 — 14 min theory + 10 min gate overview; screen 2 — 14 min theory + 16 min code demo; screen 3 — 14 min layer-toggle demo; screen 4 — 10 min promotion-ladder workshop; screen 5 — 20 min guided lab; screen 6 — 15 min independent assignment + 12 min quiz.
- Format totals: theory 28 min, demo 40 min, practice 45 min, quiz 12 min.

### Learning Outcomes
By the end, the learner can:
1. Distinguish connectivity, authentication, reconciliation, risk controls, lifecycle, and shutdown as independent live gates.
2. Preserve the promotion ladder build → deterministic replay/backtest → untouched forward → shadow → bounded canary → live expansion with explicit NO-GO criteria.
3. Explain why reconciliation must compare local and venue truth before trading is enabled.
4. Specify a kill switch with triggers, actions, acknowledgement, recovery, and audit evidence.
5. Refuse to label a successful connection probe as live readiness.

### Prerequisites
- Modules 1–3 and the native Rust backtest charter completed.
- Basic concepts of credentials, position, open order, and production incident.
- A safe sandbox or paper environment; this module grants no authorization to place real orders.

### Guided Lab — «Предпусковой шлюз» (20 min)
1. Review the builder snippet and flag the production-dangerous `with_reconciliation(false)` setting.
2. Build a gate matrix for connectivity, auth, instrument metadata, reconciliation, risk limits, observability, graceful stop, and kill switch.
3. Define evidence for each promotion step: build, replay/backtest, forward, shadow, bounded canary, live expansion.
4. Run a tabletop incident: venue has an open order missing locally. Decide the fail-closed action, owner, and recovery evidence.

### Independent Assignment (15 min)
Create a go/no-go dossier for a hypothetical one-instrument canary. Include maximum exposure, order-rate limit, stale-data trigger, reconciliation mismatch trigger, manual and automatic kill switches, rollback path, and sign-off roles.

### Learner Artifact
- A production-readiness gate matrix, promotion dossier, and kill-switch runbook suitable for review before any live authorization.

### Acceptance Criteria
- The exact ladder build → replay/backtest → forward → shadow → bounded canary → live expansion is present and cannot be skipped.
- Each rung has entry evidence, bounded scope, exit criteria, and NO-GO conditions.
- Reconciliation compares orders, fills, positions and execution identifiers and defaults to fail-closed on mismatch. Balance and margin validation are a separate account-state/risk gate.
- Kill switch stops new risk, defines open-order handling, records the trigger, and requires controlled recovery.
- Connectivity and authentication alone never produce a GO verdict.
- Rust remains the authoritative runtime and report source; Python is not a canonical dependency.

### Instructor Notes
- Say explicitly: the code sample is simplified and the false reconciliation flag is a warning, not a recommendation.
- Keep safety language evidence-based: the course does not approve live deployment.
- During the tabletop, do not let learners «fix forward» before preserving state and stopping new risk.
- Require a named human owner for canary promotion and kill-switch recovery.
- End with a verbal audit: «что доказывает готовность, кто разрешает следующий шаг, как остановить систему?»
