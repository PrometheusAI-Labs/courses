## Module 1: Анатомия Rust-стратегии

### Teaching Arc
- **Metaphor:** кабина пилота: core is the certified controls, fields are mission-specific settings.
- **Opening hook:** Rust strategy can run natively without Python being the runtime authority.
- **Key insight:** StrategyCore provides runtime plumbing; the struct owns instrument and size.
- **Why care:** helps tell AI which state belongs in the strategy and which belongs in framework core.

### Code Snippets (pre-extracted)
File: docs/how_to/write_rust_strategy.md (lines 18-30, exact continuous excerpt from commit `84a98f7f3cc786085496976320c3cb320024217f`)
```rust
use nautilus_model::{
    data::QuoteTick,
    enums::OrderSide,
    identifiers::{InstrumentId, StrategyId},
    types::Quantity,
};
use nautilus_trading::{nautilus_strategy, strategy::{Strategy, StrategyConfig, StrategyCore}};

pub struct MyStrategy {
    core: StrategyCore,
    instrument_id: InstrumentId,
    trade_size: Quantity,
}
```

### Interactive Elements
- Code↔English exact snippet.
- Quiz: 3 ownership/design scenarios.
- Architecture diagram: StrategyCore vs domain fields vs event handlers.
- Hero: cockpit labeled parts.

### Reference Files to Read
- interactive-elements.md → Code Translation, Quizzes, Architecture Diagram, Glossary Tooltips, Pattern Cards.
- content-philosophy.md and gotchas.md → fully.

### Connections
- Previous: course 02. Next: events/orders. Russian; forest accent.

### Duration
- **Total: 105 minutes.** Screen 1 — 12 min theory + 8 min visual walkthrough; screen 2 — 15 min theory + 12 min code demo; screen 3 — 10 min architecture demo + 18 min guided lab; screen 4 — 20 min independent assignment; screen 5 — 10 min quiz.
- Format totals: theory 37 min, demo 30 min, practice 28 min, quiz 10 min.

### Learning Outcomes
By the end, the learner can:
1. Explain why `StrategyCore` is framework plumbing while `instrument_id` and `trade_size` are strategy-owned domain state.
2. Point to the struct boundary when asking an AI assistant to add state without duplicating runtime responsibilities.
3. Classify a proposed field as core-owned, strategy-owned, or event-local and justify the choice.
4. Describe Rust as the authoritative runtime for the strategy, not a helper behind a canonical Python process.

### Prerequisites
- Understand that a trading strategy reacts to market data and may produce orders.
- Be able to read short code fragments with guidance; no prior Rust syntax is required.
- Know the difference between an instrument (what is traded) and a quantity (how much).

### Guided Lab — «Разложите кабину по отсекам» (18 min)
1. Mark `core`, `instrument_id`, and `trade_size` on the architecture diagram.
2. For each field, write who owns its lifecycle and what would break if it were duplicated.
3. Add three hypothetical needs—last quote, risk limit, logger—and place each in core, strategy state, or event-local context.
4. Write one precise AI instruction: «Добавь … в структуру стратегии; не дублируй обязанности `StrategyCore`».

### Independent Assignment (20 min)
Design the state map for a Rust-first two-instrument spread strategy. Include framework plumbing, two instrument identifiers, order size, latest spread value, and a configurable threshold. Do not write executable code; produce an ownership map and two AI prompts.

### Learner Artifact
- One-page «паспорт состояния Rust-стратегии»: three ownership zones, at least five fields, lifecycle notes, and two implementation prompts for an AI coding agent.

### Acceptance Criteria
- `StrategyCore` is not treated as a place for domain parameters.
- Every proposed field has exactly one owner and a stated lifecycle.
- The artifact explicitly says Rust is the canonical runtime.
- Both AI prompts name the target boundary and forbid duplicating framework plumbing.
- The quiz reasoning distinguishes ownership from syntax memorization.

### Instructor Notes
- Open with the cockpit metaphor, then drop it once the real struct is visible.
- Ask «кто обязан помнить это значение между событиями?» whenever learners hesitate.
- Do not teach Rust syntax exhaustively; focus on responsibility and ownership vocabulary.
- Common misconception: `core` means «business core». Correct it: here it is framework-provided runtime machinery.
- Before moving on, ask one learner to explain why `trade_size` belongs beside `instrument_id`.
