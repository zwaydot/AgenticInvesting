# Agentic Investing

AI-powered trading system with dual account support: **Alpaca (Paper Trading)** for strategy testing and **Longbridge (Live Trading)** for real execution.

## Account Setup

### Alpaca (Paper Trading - US Markets)
- For **strategy development and testing**
- No real money at risk
- Set up credentials in `.env`:

```bash
ALPACA_API_KEY=your_api_key
ALPACA_SECRET_KEY=your_secret_key
ALPACA_PAPER_TRADE=True
```

Get your keys from: https://alpaca.markets

### Longbridge (Live Trading - SG/HK/US Markets)
- For **real trading execution**
- Real money trading account
- Set up credentials in `.env`:

```bash
LONGPORT_APP_KEY=your_app_key
LONGPORT_APP_SECRET=your_app_secret
LONGPORT_ACCESS_TOKEN=your_access_token
LONGPORT_REGION=sg
```

Get your keys from: https://open.longbridge.com

## MCP Server Configuration

Both trading platforms are configured as MCP servers in `.claude/mcp.json`:
- `alpaca` - US paper trading via Alpaca API
- `longbridge` - Live trading via Longbridge API

## Project Structure

```
.
├── .claude/           # MCP server configurations
├── Playbook.md       # Investment strategy and rules
├── CLAUDE.md         # Instructions for Claude Code
└── .env              # API credentials (not in git)
```

## Investment Strategy

See `Playbook.md` for detailed strategy, risk management, and portfolio rules.
