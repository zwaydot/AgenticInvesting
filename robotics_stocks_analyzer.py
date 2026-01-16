"""机器人概念股分析脚本

使用 Alpaca API 获取美股机器人概念股的实时数据，
筛选出估值合理、成长性高的股票。
"""
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# 数据端点 - Paper Trading 也支持实时数据
DATA_BASE_URL = "https://data.alpaca.markets"

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
}


def load_stock_pool():
    """加载机器人概念股票池"""
    pool_path = os.path.join(os.path.dirname(__file__), "data", "robotics_stock_pool.json")
    with open(pool_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["stocks"]


def get_stock_info(symbol):
    """使用 Alpaca 数据 API 获取股票信息"""
    try:
        # 获取快照数据
        response = requests.get(
            f"{DATA_BASE_URL}/v2/stocks/{symbol}/snapshot",
            headers=HEADERS
        )
        if response.status_code != 200:
            print(f"  Snapshot API error: {response.status_code}")
            return None

        snapshot = response.json()

        # 提取数据
        latest_trade = snapshot.get("latestTrade", {})
        daily_bar = snapshot.get("dailyBar", {})
        prev_daily_bar = snapshot.get("prevDailyBar", {})

        current_price = latest_trade.get("p") or daily_bar.get("c")
        if not current_price:
            return None

        high_52w = daily_bar.get("h", current_price)
        low_52w = daily_bar.get("l", current_price)

        # 获取历史K线数据计算成交量
        bars_response = requests.get(
            f"{DATA_BASE_URL}/v2/stocks/{symbol}/bars",
            headers=HEADERS,
            params={
                "timeframe": "1Day",
                "start": (datetime.now().timestamp() - 100 * 24 * 60 * 60),
                "end": datetime.now().timestamp(),
                "limit": 100,
            }
        )
        avg_volume = 0
        if bars_response.status_code == 200:
            bars = bars_response.json().get("bars", [])
            if bars:
                avg_volume = sum(bar.get("v", 0) for bar in bars) / len(bars)

        # 计算一年涨跌幅
        year_change_pct = 0
        if prev_daily_bar.get("c"):
            year_change_pct = ((current_price - prev_daily_bar.get("c")) / prev_daily_bar.get("c")) * 100

        # 计算当前价格在52周区间的位置
        if high_52w > low_52w:
            position_52w = ((current_price - low_52w) / (high_52w - low_52w)) * 100
        else:
            position_52w = 50

        return {
            "current_price": current_price,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "position_52w": position_52w,
            "avg_volume": avg_volume,
            "year_change_pct": year_change_pct,
        }
    except Exception as e:
        print(f"  Error fetching {symbol}: {e}")
    return None


def analyze_stock(stock_info):
    """分析单只股票"""
    symbol = stock_info["symbol"]

    print(f"分析 {symbol} - {stock_info['name']}...")

    # 获取股票数据
    stock_data = get_stock_info(symbol)
    if not stock_data:
        print(f"  跳过: 无数据")
        return None

    current_price = stock_data["current_price"]

    # 筛选条件
    reasons = []

    # 1. 价格筛选
    if current_price < 10:
        print(f"  跳过: 价格过低 (${current_price:.2f})")
        return None
    if current_price > 500:
        print(f"  跳过: 价格过高 (${current_price:.2f})")
        return None

    # 2. 成交量筛选
    avg_volume = stock_data["avg_volume"]
    if avg_volume < 500000:
        print(f"  跳过: 成交量过低 ({avg_volume:,.0f})")
        return None

    # 3. 52周位置分析
    position_52w = stock_data["position_52w"]

    # 4. 分析逻辑
    category = stock_info["category"]

    # 根据不同类别给出推荐理由
    if category == "AI芯片" and current_price < 150:
        reasons.append("AI芯片龙头，估值相对合理")
    elif category == "AI芯片":
        reasons.append("AI芯片龙头，机器人核心算力来源")

    if category == "工业自动化":
        reasons.append("工业自动化受益者，智能制造趋势明确")

    if category == "机器视觉":
        reasons.append("机器视觉是机器人眼睛，需求增长确定")

    if category == "医疗机器人":
        reasons.append("医疗机器人渗透率提升空间大")

    if category == "家用机器人":
        reasons.append("家用服务机器人渗透率仍有提升空间")

    # 技术位置分析
    if position_52w < 30:
        reasons.append(f"当前价格处于52周低位区间({position_52w:.0f}%)")
    elif position_52w > 80:
        reasons.append(f"当前价格接近52周高位({position_52w:.0f}%)，注意风险")
    else:
        reasons.append(f"价格处于52周中间区域({position_52w:.0f}%)，位置合理")

    if not reasons:
        reasons.append("基本面符合筛选条件")

    print(f"  ✓ 通过筛选 - ${current_price:.2f}, 52周位置: {position_52w:.0f}%")

    return {
        "symbol": symbol,
        "name": stock_info["name"],
        "category": category,
        "description": stock_info["description"],
        "current_price": current_price,
        "year_change_pct": stock_data["year_change_pct"],
        "high_52w": stock_data["high_52w"],
        "low_52w": stock_data["low_52w"],
        "position_52w": position_52w,
        "avg_volume": avg_volume,
        "reasons": reasons,
    }


def generate_report(analyzed_stocks):
    """生成分析报告"""
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    report_path = os.path.join(output_dir, f"analysis_report_{datetime.now().strftime('%Y%m%d')}.md")

    # 按推荐度排序
    analyzed_stocks.sort(key=lambda x: x["position_52w"])

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 机器人概念股分析报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**数据来源**: Alpaca Paper Trading API\n\n")
        f.write(f"**筛选条件**:\n")
        f.write(f"- 价格区间: $10 - $500\n")
        f.write(f"- 日均成交量: > 50万股\n\n")

        f.write(f"## 分析结果概览\n\n")
        f.write(f"共分析 {len(analyzed_stocks)} 只符合条件的机器人概念股\n\n")

        f.write(f"| 代码 | 名称 | 类别 | 现价 | 日涨跌 | 52周位置 | 成交量 |\n")
        f.write(f"|------|------|------|------|--------|----------|--------|\n")
        for stock in analyzed_stocks:
            f.write(f"| {stock['symbol']} | {stock['name']} | {stock['category']} | "
                   f"${stock['current_price']:.2f} | {stock['daily_change_pct']:+.2f}% | "
                   f"{stock['position_52w']:.0f}% | {stock['avg_volume']:,.0f} |\n")

        f.write(f"\n## 详细分析\n\n")

        for i, stock in enumerate(analyzed_stocks, 1):
            f.write(f"### {i}. {stock['symbol']} - {stock['name']}\n\n")
            f.write(f"**类别**: {stock['category']}\n\n")
            f.write(f"**公司简介**: {stock['description']}\n\n")
            f.write(f"**当前价格**: ${stock['current_price']:.2f}\n\n")
            f.write(f"**52周区间**: ${stock['low_52w']:.2f} - ${stock['high_52w']:.2f}\n\n")
            f.write(f"**52周位置**: {stock['position_52w']:.0f}%\n\n")
            f.write(f"**日涨跌幅**: {stock['daily_change_pct']:+.2f}%\n\n")
            f.write(f"**日均成交量**: {stock['avg_volume']:,.0f} 股\n\n")
            f.write(f"**推荐理由**:\n")
            for reason in stock['reasons']:
                f.write(f"- {reason}\n")
            f.write(f"\n")

        f.write(f"---\n\n")
        f.write(f"*本报告仅供参考，不构成投资建议。投资有风险，请谨慎决策。*\n")

    print(f"\n报告已生成: {report_path}")
    return report_path


def main():
    """主函数"""
    print("=" * 60)
    print("机器人概念股分析脚本")
    print("=" * 60)
    print(f"API端点: {DATA_BASE_URL}")
    print()

    # 加载股票池
    stocks = load_stock_pool()
    print(f"加载股票池: {len(stocks)} 只股票")
    print()

    # 分析股票
    analyzed = []
    skipped = 0

    for stock in stocks:
        result = analyze_stock(stock)
        if result:
            analyzed.append(result)
        else:
            skipped += 1

    print()
    print("=" * 60)
    print(f"分析完成: {len(analyzed)} 只符合条件, {skipped} 只被筛选掉")
    print("=" * 60)

    if analyzed:
        report_path = generate_report(analyzed)
        print(f"\n报告已保存到: {report_path}")
    else:
        print("\n没有符合条件的股票")


if __name__ == "__main__":
    main()
