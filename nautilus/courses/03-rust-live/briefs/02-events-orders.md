## Module 2: От события к заявке

### Teaching Arc
- **Metaphor:** аварийная служба: зарегистрировала канал, получает вызов, формирует заявку, передаёт по цепочке.
- **Opening hook:** on_quote is not the exchange; it creates a command that still passes risk and execution.
- **Key insight:** subscription, callback, order factory, and submit are separate boundaries.
- **Why care:** lets AI debugging distinguish no data, no callback, rejected risk, and failed venue transport.

### Code Snippets (pre-extracted)
File: docs/how_to/write_rust_strategy.md (lines 90-106, exact continuous excerpt from commit `84a98f7f3cc786085496976320c3cb320024217f`)
```rust
impl DataActor for MyStrategy {
    fn on_start(&mut self) -> anyhow::Result<()> {
        self.subscribe_quotes(self.instrument_id, None, None);
        Ok(())
    }

    fn on_quote(&mut self, quote: &QuoteTick) -> anyhow::Result<()> {
        let order = self.order().market(
            self.instrument_id,
            OrderSide::Buy,
            self.trade_size,
            None, None, None, None, None, None, None,
        );
        self.submit_order(order, None, None, None)?;
        Ok(())
    }
}
```

### Interactive Elements
- Code↔English exact snippet.
- Quiz: 4 debugging scenarios across the four boundaries.
- Group chat: Adapter, Strategy, RiskEngine, ExecutionEngine, Venue.
- Message flow: quote → handler → order → risk → execution.

### Reference Files to Read
- interactive-elements.md → Code Translation, Quizzes, Group Chat, Message Flow, Glossary Tooltips.
- content-philosophy.md and gotchas.md → fully.

### Connections
- Previous: Rust anatomy. Next: native backtest. Russian; avoid implying sample buys are safe strategy logic.

### Duration
- **Total: 110 minutes.** Screen 1 — 12 min theory + 8 min boundary map; screen 2 — 14 min theory + 14 min code demo; screen 3 — 12 min animated chat + 12 min data-flow trace; screen 4 — 15 min guided lab; screen 5 — 10 min independent assignment + 3 min review; screen 6 — 10 min quiz.
- Format totals: theory 26 min, demo 46 min, practice 28 min, quiz 10 min.

### Learning Outcomes
By the end, the learner can:
1. Trace quote → callback → order command → risk decision → execution transport without collapsing the boundaries.
2. Diagnose four distinct symptoms: no subscription, no callback, risk rejection, and venue transport failure.
3. Explain that `submit_order` requests an action; it does not prove an exchange fill.
4. Formulate an observability request for an AI agent with one checkpoint per boundary.

### Prerequisites
- Module 1 ownership map completed.
- Basic trading vocabulary: quote, buy order, venue.
- No knowledge of networking or asynchronous programming is assumed.

### Guided Lab — «Найдите пропавший вызов» (15 min)
1. Run the message-flow animation one step at a time and record the evidence expected at each hop.
2. Work through four incident cards: silent adapter, callback counter at zero, risk rejection, timeout after execution dispatch.
3. For each incident, name the last proven boundary and the next component to inspect.
4. Draft a structured log checklist with correlation ID, instrument, event time, order ID, risk verdict, and venue acknowledgement.

### Independent Assignment (13 min including review)
Create a troubleshooting decision tree for «котировка пришла, но сделки нет». It must branch before proposing a fix and must never interpret order creation as a fill. Peer-review it against the five-actor chat.

### Learner Artifact
- A one-page event-to-order trace with five checkpoints, expected evidence, owner component, and a compact incident decision tree.

### Acceptance Criteria
- Subscription and callback are separate checkpoints.
- Order creation, risk approval, dispatch, acknowledgement, and fill are not conflated.
- Every branch starts from observable evidence, not guesses.
- The sample market buy is labeled educational, not safe production logic.
- The AI prompt requests logs/metrics at each boundary without changing the strategy behavior.

### Instructor Notes
- Play the group chat slowly first; replay all messages only after learners predict the next speaker.
- Keep asking «что уже доказано, а что только предполагается?».
- Do not describe `on_quote` as an exchange callback; it is a strategy handler invoked by the runtime.
- Reinforce that a successful function return is not proof of venue acceptance or fill.
- Use wrong quiz answers to show which boundary the learner skipped.
