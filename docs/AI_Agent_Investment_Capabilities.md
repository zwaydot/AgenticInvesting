# AI 投资分析与交易能力总结

## 更新时间
2025-01-13

---

## 一、投资分析能力

### 1.1 数据获取与分析
- **实时市场数据**: 通过 Alpaca Data API 获取股票快照、历史K线、52周高低点
- **基本面分析**: PE、PB、PS、ROE、收入增长率、利润率等估值指标
- **技术分析**: 52周位置分析、波动率计算

### 1.2 行业与公司分析
- **机器人产业链梳理**: 按类别分类（工业机器人、AI芯片、机器视觉、医疗机器人等）
- **公司竞争力分析**: 如 TER 收购 Universal Robots 的战略意义
- **同业对比**: 与 TSLA、NVDA、ABB、IRBT 等的对比分析

### 1.3 估值与策略建议
- **估值判断**: TTM PE vs Forward PE 分析，判断估值合理性
- **买入价位规划**: 保守/稳健/当前价三种策略
- **仓位管理**: 建议分批建仓、止损位设置

---

## 二、交易执行能力

### 2.1 账户管理
- 查询账户余额、购买力
- 查看持仓和订单状态

### 2.2 订单下单
- **限价单**: 设置目标价位等待成交
- **仓位控制**: 根据账户资金计算合理买入数量
- **风险管理**: GTC 订单、止损建议

### 2.3 实际执行案例
| 股票 | 类型 | 数量 | 价格 | 状态 |
|------|------|------|------|------|
| CGNX | 限价买入 | 1524股 | $38.20 | accepted |
| NVDA | 限价买入 | 300股 | $186.00 | accepted |
| TER | 限价买入 | 26股 | $190.00 | accepted |

---

## 三、用到的工具

### 3.1 Alpaca Trading API
```python
# Paper Trading 端点
BASE_URL = "https://paper-api.alpaca.markets/v2"

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
}

# 账户信息
GET /v2/account

# 下单
POST /v2/orders
{
    "symbol": "TER",
    "qty": 26,
    "side": "buy",
    "type": "limit",
    "limit_price": 190.00,
    "time_in_force": "gtc"
}

# 查询订单
GET /v2/orders

# 查询持仓
GET /v2/positions

# 查询资产
GET /v2/assets/{symbol}
```

### 3.2 Alpaca Data API
```python
# 数据端点
DATA_URL = "https://data.alpaca.markets/v2"

# 股票快照
GET /v2/stocks/{symbol}/snapshot

# 历史K线
GET /v2/stocks/{symbol}/bars
params = {
    "timeframe": "1Day",
    "start": timestamp,
    "limit": 100
}
```

### 3.3 yfinance (Python 库)
```python
import yfinance as yf

ticker = yf.Ticker("TER")
info = ticker.info              # 基本面数据
financials = ticker.financials  # 财务报表
hist = ticker.history(period="1y")  # 历史价格
```

### 3.4 MCP 工具 (Claude Code)
```bash
# 注册 MCP 服务器
claude mcp add alpaca --scope user --transport stdio uvx alpaca-mcp-server serve \
  --env ALPACA_API_KEY=xxx \
  --env ALPACA_SECRET_KEY=xxx

# 查看状态
claude mcp list
```

---

## 四、投资分析框架

```
1. 行业选择 → 机器人产业链（AI芯片、工业自动化、机器视觉）
2. 个股筛选 → 价格区间 $10-$500、成交量筛选、52周位置分析
3. 基本面分析 → PE、PEG、ROE、收入增长率、现金流
4. 估值判断 → TTM vs Forward PE、同业对比
5. 买入策略 → 理想价位、分批建仓、止损位
6. 交易执行 → 限价单、仓位控制
```

---

## 五、机器人概念股分析案例

### 5.1 TER (Teradyne) 深度分析

**估值数据**
| 指标 | 数值 | 评价 |
|------|------|------|
| 市值 | $356.9亿 | - |
| 市盈率(TTM) | 81.29倍 | ⚠️ 偏高 |
| 市盈率(预期) | 43.32倍 | ✓ 相对合理 |
| ROE | 15.77% | ✓ 优秀 |

**投资亮点**
- 收购 Universal Robots (协作机器人全球龙头，市占率50-60%)
- 半导体测试设备传统业务稳健
- 直接受益于 AI 芯片测试需求

**买入建议**
- 保守价位: $140-$160
- 稳健价位: $170-$190
- 当前价位 $224 偏高，建议等待回调

### 5.2 其他机器人概念股
| 代码 | 名称 | 类别 | 现价 | 特点 |
|------|------|------|------|------|
| NVDA | NVIDIA | AI芯片 | $184.82 | 机器人核心算力 |
| CGNX | Cognex | 机器视觉 | $39.42 | 机器人的眼睛 |
| ISRG | Intuitive Surgical | 医疗机器人 | $572.85 | 手术机器人龙头 |

---

## 六、可改进方向

1. **技术分析增强**: 加入移动平均线、RSI、MACD 等指标
2. **量化筛选**: 构建多因子筛选模型
3. **回测系统**: 验证策略历史表现
4. **风险模型**: VaR 计算、相关性分析
5. **实时监控**: 订单成交提醒、止盈止损自动执行

---

## 七、会话记录存档

### [2025-01-13] 机器人概念股分析与交易

#### 核心任务
- 分析美股机器人概念股，筛选估值合理、成长性高的标的
- 深度分析 TER (Teradyne) 的投资价值
- 使用 Alpaca Paper Trading API 执行限价买入订单

#### 展示能力
- **行业分析**: 梳理机器人产业链（工业机器人、AI芯片、机器视觉、医疗机器人、家用机器人）
- **个股筛选**: 按价格区间、成交量、52周位置筛选
- **估值分析**: PE、PB、PS、ROE、收入增长率等多维度分析
- **技术分析**: 52周位置判断买入时机
- **仓位管理**: 根据5%仓位原则计算买入数量
- **交易执行**: 限价单 (GTC) 下单

#### 使用工具
**Alpaca Trading API**
```python
# 账户查询
GET https://paper-api.alpaca.markets/v2/account

# 下单 (限价单)
POST https://paper-api.alpaca.markets/v2/orders
{
    "symbol": "TER",
    "qty": 26,
    "side": "buy",
    "type": "limit",
    "limit_price": 190.00,
    "time_in_force": "gtc"
}
```

**Alpaca Data API**
```python
# 股票快照
GET https://data.alpaca.markets/v2/stocks/{symbol}/snapshot

# 历史K线
GET https://data.alpaca.markets/v2/stocks/{symbol}/bars
```

**yfinance**
```python
import yfinance as yf
ticker = yf.Ticker("TER")
info = ticker.info  # PE、PB、ROE、收入增长率等
```

#### 关键输出
**TER 分析结论**
- Forward PE 43倍相对合理（TTM PE 81倍受周期底部影响）
- 当前价格 $224 处于 52周高位 (96.8%)，不建议追高
- 理想买入价位 $140-$190
- 核心竞争力：Universal Robots (协作机器人龙头，50-60%市占率)

**交易执行**
| 股票 | 数量 | 限价 | 仓位 | 状态 |
|------|------|------|------|------|
| CGNX | 1524股 | $38.20 | - | accepted |
| NVDA | 300股 | $186.00 | - | accepted |
| TER | 26股 | $190.00 | 5% | accepted |

#### 风险提示
- Paper Trading 环境部分股票不可交易（如 ABB）
- 限价单可能长期未成交，需定期检查
- 投资有风险，本分析仅供参考
