# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## ⛔ CRITICAL: 强制性投资策略规则

**在执行任何投资或交易相关操作前，必须先阅读并严格遵循 `Playbook.md` 中定义的策略。**

### 交易前强制检查清单

对于每个买入/卖出/分析请求，必须：

1. **读取 Playbook.md** - 理解当前策略框架
2. **验证策略符合性**：
   - 标的是否属于机器人产业链？
   - 是否满足选股标准（成长性、估值合理性）？
   - 是否违反风险控制规则（追高、仓位过重等）？
3. **拒绝不符合策略的请求** - 如果不符合，明确说明原因并拒绝执行

### 禁止行为

- ❌ 买入非机器人产业链标的（如消费股、金融股等）
- ❌ 在52周高位附近追涨
- ❌ 不做分析就执行交易
- ❌ 忽略仓位管理规则

**如果用户请求不符合 Playbook 策略，必须拒绝并解释原因。**

---

## 🤖 Memory Management System

### Auto-Save to Playbook.md

When user says "请记住..." or "记住...":
1. **Extract the core requirement** from the user's statement
2. **Add to Playbook.md** under `## 记忆库 (Memories)` section
3. **Format**: `- [YYYY-MM-DD] [记忆内容]`
4. **Subsequent sessions**: Automatically follow the memory rule

Example interaction:
- User: "请记住，计算个股仓位时，分母使用总资产（包含现金）"
- Action: Add to Playbook.md as `- [2026-01-17] 计算个股仓位时，分母使用总资产（包含现金），即：个股仓位占比 = 个股市值 / 总资产，现金仓位也需明确计算和展示`
- Result: All future portfolio calculations follow this rule

### Memory Retrieval

Before providing investment analysis or calculations:
1. **Read `Playbook.md`**, specifically the `## 记忆库 (Memories)` section
2. **Apply all memory rules** to current task
3. If memories conflict, ask user for clarification

---

## Project Overview

This is a **dual-account trading system** using AI agents:
- **Alpaca (Paper Trading)**: For strategy development and testing (US markets, no real money)
- **Longbridge (Live Trading)**: For real execution (SG/HK/US markets, real money)

## MCP Server Configuration

**IMPORTANT**: Both trading platforms are configured as MCP servers in `.claude/mcp.json`:

### Available MCP Tools

**Alpaca MCP** (`mcp__alpaca__*`):
- `get_account_info()` - Get Alpaca paper account status
- `get_all_positions()` - Get all positions
- `get_orders()` - Get order history
- `place_stock_order()` - Place stock orders
- And more... (see function list)

**Longbridge MCP** (`mcp__longbridge__*`):
- `account_balance()` - Get Longbridge account balance
- `stock_positions()` - Get stock positions
- `submit_order()` - Submit orders
- `quote()` - Get real-time quotes
- And more... (see function list)

### MCP Usage Rules for Claude

When user requests account information or trading operations:

1. **DO NOT explore project structure first** - MCP tools are already available
2. **DO NOT check if MCP is "working"** - both are configured and ready
3. **Directly call the appropriate MCP tool** based on the user's request
4. **Treat both MCPs equally** - don't prefer Alpaca just because it's mentioned more in docs

**Example - CORRECT behavior**:
```
User: "查看longbridge账户"
Claude: [Immediately calls mcp__longbridge__account_balance()]
```

**Example - WRONG behavior** (avoid this):
```
User: "查看longbridge账户"
Claude: [Reads mcp.json, calls ListMcpResourcesTool, explores files...]
        [Finally calls mcp__longbridge__account_balance()]
```

## Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys (copy from example and edit)
cp .env.example .env
# Edit .env with both Alpaca and Longbridge credentials
```

## Account Access via MCP

**Check Alpaca account:**
```python
mcp__alpaca__get_account_info()
mcp__alpaca__get_all_positions()
```

**Check Longbridge account:**
```python
mcp__longbridge__account_balance()
mcp__longbridge__stock_positions()
```
