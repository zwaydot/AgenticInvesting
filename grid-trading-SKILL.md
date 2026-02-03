---
name: grid-trading
description: Design and execute grid trading strategies for stocks. Analyzes current price, position, valuation, and technical levels to create optimal buy/sell grid orders. Use when user wants to implement grid trading for profit-taking or dollar-cost averaging.
license: Complete terms in LICENSE.txt
---

This skill creates intelligent grid trading strategies tailored to the stock's current situation and the user's position.

## When to Use

Trigger this skill when the user:
- Says "网格交易" or "grid trading" for a specific stock
- Wants to set up systematic profit-taking on a winning position
- Wants to dollar-cost average into a position during a decline
- Asks to "分批止盈" (gradual profit-taking) or "分批建仓" (gradual position building)
- Requests automated buy/sell orders at specific price levels

## Core Logic

### Step 1: Identify Scenario Type

Determine whether this is:
- **Scenario A: Profit-Taking Grid** (止盈网格)
  - User has existing position with unrealized profit
  - Goal: Lock in profits gradually as price rises
  - Direction: Sell orders at ascending price levels

- **Scenario B: Accumulation Grid** (抄底网格)
  - User wants to build position or has no/small position
  - Goal: Lower average cost as price declines
  - Direction: Buy orders at descending price levels

### Step 2: Gather Market Intelligence

**MANDATORY data collection - execute in parallel:**

1. **Position Data** (if applicable):
   - Call `mcp__alpaca__get_open_position` with symbol
   - Get current holdings, average cost, unrealized P/L
   - Call `mcp__alpaca__get_account_info` for total equity

2. **Price Data**:
   - Call `mcp__alpaca__get_stock_latest_bar` for current price
   - Call `mcp__alpaca__get_stock_bars` with `days: 365` to get 52-week range
   - Identify: current price, 52-week high, 52-week low, key support/resistance levels

3. **Fundamental Data**:
   - Search web for: "{SYMBOL} forward PE ratio analyst estimates growth rate"
   - Extract: Forward PE, TTM PE, earnings growth rate, analyst price targets
   - Calculate PEG ratios (if applicable)

4. **Playbook Compliance Check**:
   - Read `/Users/zhangwei/Documents/ProductDev/Alpaca/Playbook.md`
   - Verify stock fits investment thesis (robotics industry chain)
   - Check valuation against Playbook thresholds
   - Review position sizing limits

### Step 3: Design Grid Strategy

#### For Profit-Taking Grid (Scenario A)

**Grid Architecture Selection:**

Choose based on user confidence and risk tolerance:

1. **Equal Proportion (Default)**
   - Each level sells same % of position (e.g., 25% each)
   - Best for: Uncertain about top, want steady profit locking
   - Example: 25%, 25%, 25%, 25%

2. **Pyramid (Aggressive)**
   - Sell less early, more later (e.g., 10%, 15%, 25%, 50%)
   - Best for: Confident in continued upside
   - Example: 10%, 15%, 25%, 50%

3. **Inverted Pyramid (Conservative)**
   - Sell more early, less later (e.g., 50%, 25%, 15%, 10%)
   - Best for: Fear of pullback, want to lock profits fast
   - Example: 50%, 25%, 15%, 10%

**Price Level Determination:**

Set grid levels using **multi-factor analysis**:

```
Level Selection Framework:
├─ Technical Levels
│  ├─ Round numbers ($300, $350, $400)
│  ├─ Prior resistance levels
│  ├─ Fibonacci extensions (1.272, 1.618)
│  └─ Bollinger Band upper limits
│
├─ Valuation Triggers (from Playbook)
│  ├─ Forward PE thresholds
│  ├─ PEG ratio warnings
│  └─ Industry-specific limits
│
└─ Percentage Gains
   ├─ +20%, +30%, +50% from current
   └─ Or from average cost if holding
```

**Recommended Grid Spacing**: 10-15% between levels (15-20% for volatile stocks)

**Stop-Loss Protection:**
- MANDATORY: Set trailing stop or hard stop below current price
- Protects remaining position if price reverses
- Suggested: -8% to -12% from current price, or below key support

#### For Accumulation Grid (Scenario B)

**Grid Architecture Selection:**

1. **Equal Dollar (Beginner-Friendly)**
   - Invest same dollar amount at each level
   - Naturally buys more shares at lower prices
   - Example: $2,000 per level

2. **Pyramid (Recommended)**
   - Invest more at lower levels (e.g., 10%, 15%, 25%, 25%, 25%)
   - Concentrates firepower at better prices
   - Example: 10%, 15%, 25%, 25%, 25% of total capital

3. **Inverted Pyramid (Conservative)**
   - Invest more early, less later (e.g., 30%, 25%, 20%, 15%, 10%)
   - Participates in bounce quickly
   - Example: 30%, 25%, 20%, 15%, 10%

**Price Level Determination:**

```
Level Selection Framework:
├─ Technical Levels
│  ├─ Prior support levels
│  ├─ Moving averages (MA50, MA100, MA200)
│  ├─ Fibonacci retracements (0.382, 0.5, 0.618)
│  └─ Round numbers
│
├─ Valuation Targets (from Playbook)
│  ├─ Forward PE entering reasonable range
│  ├─ PEG < 1.5 for growth stocks
│  └─ Industry-specific buy zones
│
└─ Percentage Declines
   ├─ -5%, -10%, -15%, -20% from current
   └─ Based on volatility
```

**Total Stop-Loss (CRITICAL):**
- MANDATORY: Set absolute bottom where you exit completely
- Protects against failed thesis (e.g., "not really a bottom")
- Suggested: -25% to -35% from current price, or at major support break

### Step 4: Validate Against Playbook

**Pre-Execution Checklist:**

For Profit-Taking:
- [ ] Has position gained at least 15-20%? (worth setting grid)
- [ ] Are we near 52-week high? (trigger risk control rules)
- [ ] Does Forward PE exceed Playbook thresholds?
- [ ] Does PEG ratio trigger profit-taking warnings?
- [ ] Will remaining position after first grid still meet minimum size?

For Accumulation:
- [ ] Does stock fit Playbook investment scope? (robotics industry)
- [ ] Is current valuation within or below reasonable range?
- [ ] Have we identified clear support levels?
- [ ] Is total capital allocation within Playbook limits?
- [ ] Does this fit current cash management strategy?

**Red Flags to Warn User:**
- ⚠️ Chasing highs (buying near 52-week high)
- ⚠️ Catching falling knives (no clear support, downtrend intact)
- ⚠️ Position sizing violation (single stock >30% of portfolio)
- ⚠️ Valuation extreme (PEG >3.0 or Forward PE >>industry avg)

### Step 5: Present Strategy to User

**Output Format:**

```markdown
## 📊 {SYMBOL} 网格交易策略

### 当前市场状态
| 指标 | 数值 | 评估 |
|------|------|------|
| 当前价格 | ${PRICE} | - |
| 52周区间 | ${LOW} - ${HIGH} | 当前位于 {XX}% |
| Forward PE | {PE} | {合理/偏高/偏低} |
| 预期 PEG | {PEG} | {优秀/合理/警戒} |

### 持仓状况（如适用）
- 持仓数量: {QTY} 股
- 平均成本: ${AVG_COST}
- 未实现盈利: ${UNREALIZED_PL} ({PERCENT}%)
- 仓位占比: {POSITION_PCT}%

### 网格策略设计

**策略类型**: {止盈网格 / 抄底网格}
**网格架构**: {等比例 / 金字塔 / 倒金字塔}
**总档位数**: {N} 档

| 档位 | 价格 | 操作 | 数量/金额 | 触发条件 | 理由 |
|------|------|------|-----------|----------|------|
| 1 | ${PRICE_1} | {买入/卖出} | {AMOUNT_1} | 价格达到 ${PRICE_1} | {技术位/估值/涨跌幅} |
| 2 | ${PRICE_2} | {买入/卖出} | {AMOUNT_2} | 价格达到 ${PRICE_2} | ... |
| ... | ... | ... | ... | ... | ... |
| N | ${PRICE_N} | {买入/卖出} | {AMOUNT_N} | 价格达到 ${PRICE_N} | ... |

### 风险控制
- **止损/止盈位**: ${STOP_PRICE}
- **保护对象**: {剩余底仓 / 已投入资金}
- **触发条件**: 价格{跌破/涨至} ${STOP_PRICE}

### Playbook 合规性检查
✅ / ⚠️ / ❌ {检查项1}
✅ / ⚠️ / ❌ {检查项2}
...

### 预期收益（如适用）
- 第1档成交: 锁定利润 ${PROFIT_1} 或 降低成本至 ${NEW_AVG_1}
- 第2档成交: 锁定利润 ${PROFIT_2} 或 降低成本至 ${NEW_AVG_2}
- 全部成交: 总计锁定 ${TOTAL_PROFIT} 或 最终成本 ${FINAL_AVG}

### 执行建议
{是否建议立即执行，或等待更好时机}
```

### Step 6: Execute Orders (If User Approves)

**Order Execution Protocol:**

1. **Confirm with User:**
   - Ask: "是否立即执行以上网格订单？"
   - Wait for explicit approval

2. **Place Orders in Sequence:**
   - Use `mcp__alpaca__place_stock_order` for each grid level
   - For profit-taking: `type: "limit"`, `side: "sell"`
   - For accumulation: `type: "limit"`, `side: "buy"`
   - Set `time_in_force: "gtc"` (Good Till Cancelled)
   - Use descriptive `client_order_id`: e.g., `"{SYMBOL}_GRID_{PRICE}"`

3. **Place Stop Order:**
   - Use `type: "stop"` for stop-loss
   - Set `stop_price` at calculated level
   - Quantity = remaining shares/position after grid

4. **Verify and Report:**
   - Check all order statuses (should be "ACCEPTED")
   - Report order IDs to user for tracking
   - Provide summary table of active orders

**Error Handling:**
- If any order fails, report immediately and stop execution
- Check: Insufficient shares/cash, price validation, market hours
- Offer to retry or adjust parameters

## Execution Steps Summary

```
1. Identify Scenario (Profit-Taking vs Accumulation)
   ↓
2. Gather Data (Position, Price, Fundamentals, Playbook)
   ↓
3. Design Grid (Architecture, Levels, Stop-Loss)
   ↓
4. Validate Against Playbook (Compliance Check)
   ↓
5. Present Strategy to User (Markdown Report)
   ↓
6. Execute Orders (If Approved)
   ↓
7. Monitor & Report (Order Status Confirmation)
```

## Advanced Features

### Dynamic Grid Adjustment

**Trailing Grid (Profit-Taking):**
- After each level executes, consider raising stop-loss
- New stop = previous grid level (lock in gains)
- Prevents giving back realized profits

**Adaptive Grid (Accumulation):**
- If price breaks below lowest grid, reassess thesis
- Option 1: Add deeper levels (if thesis intact)
- Option 2: Trigger total stop-loss (if thesis broken)

### Multi-Stock Grid Portfolio

When managing grids for multiple stocks:
- Track total capital allocated to all grids
- Ensure aggregate position sizing within Playbook limits
- Coordinate grid executions to maintain diversification
- Report consolidated grid status on request

### Grid Performance Tracking

After execution, offer to:
- Calculate actual vs. expected returns as grids execute
- Track which levels have filled
- Suggest adjustments based on market changes
- Generate performance report on request

## Important Notes

### For Profit-Taking Grids:
- **DON'T** set grids so tight that every small bounce triggers (min 10% spacing)
- **DO** check if after-hours/pre-market prices already exceeded grid levels
- **DO** consider current volatility (widen grids for volatile stocks)
- **DON'T** feel obligated to hold a "core position" if valuation is extreme

### For Accumulation Grids:
- **DON'T** assume "it can't go lower" - always set total stop-loss
- **DO** verify fundamentals haven't deteriorated (earnings, guidance, news)
- **DO** check overall market conditions (avoid catching knives in crashes)
- **DON'T** allocate all cash to one stock's grid (diversification)

### Playbook Integration:
- Grid trading is a **tool**, not a substitute for strategy
- If fundamentals change (e.g., company no longer fits robotics theme), cancel grids
- Valuation thresholds in Playbook override grid logic
- Cash management rules still apply (don't over-allocate)

## Example Scenarios

### Example 1: Profit-Taking for TER

```
Situation:
- Position: 44 shares @ $228 avg cost
- Current Price: $298
- Unrealized Gain: +30.7%
- Forward PE: 47.8, PEG: 0.96

Strategy: Equal Proportion Grid (4 levels)
- $300: Sell 11 shares (25%)
- $320: Sell 11 shares (25%)
- $340: Sell 11 shares (25%)
- $360: Sell 11 shares (25%)
- Stop: $280 (protects if reversal)

Rationale:
✅ Strong gain justifies profit-taking
✅ Near 52-week high (risk management)
✅ Equal proportions (uncertain about top)
```

### Example 2: Accumulation for NVDA

```
Situation:
- No Position
- Current Price: $800
- 52-Week Range: $600 - $950
- Forward PE: 40, down from recent highs
- User has $20,000 to allocate

Strategy: Pyramid Grid (5 levels)
- $780 (-2.5%): Buy $2,000 (10%)
- $760 (-5%):   Buy $3,000 (15%)
- $740 (-7.5%): Buy $5,000 (25%)
- $720 (-10%):  Buy $5,000 (25%)
- $700 (-12.5%): Buy $5,000 (25%)
- Stop: $650 (total stop-loss if thesis breaks)

Rationale:
✅ Valuation improving from highs
✅ Pyramid concentrates buying at better prices
✅ Stop at major support level (~$650)
```

## Configuration

**Required Tools:**
- `mcp__alpaca__get_open_position` - Check current holdings
- `mcp__alpaca__get_account_info` - Get portfolio size
- `mcp__alpaca__get_stock_latest_bar` - Current price
- `mcp__alpaca__get_stock_bars` - Historical price data
- `mcp__alpaca__place_stock_order` - Execute grid orders
- `WebSearch` - Get fundamental data
- `Read` - Access Playbook.md

**Playbook Path:**
- `/Users/zhangwei/Documents/ProductDev/Alpaca/Playbook.md`

**Key Playbook Sections to Reference:**
- 核心策略框架 → 估值标准
- 止损止盈策略 → 触发条件
- 仓位管理 → 单只上限
- 风险控制 → 不追高原则

## Error Handling

**Common Issues:**

1. **Insufficient Shares/Cash:**
   - Reduce grid quantity or levels
   - Suggest partial grid execution

2. **Price Already Exceeded Grid Level:**
   - Warn user and suggest adjusting upward
   - Or execute as market order if user confirms

3. **After-Hours / Market Closed:**
   - Orders will queue for next session
   - Explain GTC behavior to user

4. **Playbook Violations:**
   - Clearly state the violation
   - Ask user if they want to override (document decision)

5. **API Errors:**
   - Report exact error message
   - Suggest troubleshooting steps
   - Offer to retry or adjust parameters

## Best Practices

1. **Always explain the "why"** behind each grid level
2. **Show the math** - calculate profit/loss scenarios
3. **Respect Playbook rules** - warn when strategy conflicts with investment thesis
4. **Use parallel tool calls** - gather data efficiently
5. **Confirm before executing** - never place orders without explicit approval
6. **Track order IDs** - help user monitor execution
7. **Offer follow-ups** - suggest checking status later or adjusting strategy

---

**Skill Version:** 1.0.0
**Last Updated:** 2026-02-03
**Maintained by:** Investment Strategy Team
