import yfinance as yf
from yahooquery import search
from langchain.agents import Tool
import json
import matplotlib.pyplot as plt
import io
import base64

class RevenueTool:
    def __init__(self):
        self.name = "revenue_tool"
        self.description = "Get quarterly revenue for any company (e.g., 'apple', 'infosys', 'tcs')."

    # Helper: Map company name to ticker
    def get_ticker_from_name(self, company_name: str) -> str:
        result = search(company_name)
        if result and "quotes" in result:
            for item in result["quotes"]:
                if "symbol" in item:
                    return item["symbol"]
        return None

    # Tool 1: Get quarterly revenues of any company
    def get_company_revenue(self, company_name: str) -> str:
        try:
            ticker_symbol = self.get_ticker_from_name(company_name)
            if not ticker_symbol:
                return f"Ticker not found for company: {company_name}"

            ticker = yf.Ticker(ticker_symbol)
            df = ticker.quarterly_income_stmt

            if "Total Revenue" not in df.index:
                return f"Total Revenue not found in income statement for {company_name}"

            revenue = df.loc["Total Revenue"].dropna().sort_index(ascending=False).head(3)

            result = {str(date.date()): float(value) for date, value in revenue.items()}
            return json.dumps(result)  # instead of return result

        except Exception as e:
            return f"Error fetching revenue for {ticker_symbol}: {e}"

    # Tool definition for LangChain
    def get_tool(self) -> Tool:
        return Tool(
            name=self.name,
            func=self.get_company_revenue,
            description=self.description
        )

    # New method: Plot revenue from provided JSON and company name
    def plot_revenue_from_data(self, company_name: str, revenue_json: str) -> str:
        try:
            data = json.loads(revenue_json.replace("'", '"'))  # Ensure proper JSON
            dates = list(data.keys())[::-1]
            values = list(data.values())[::-1]

            if not dates or not values:
                return None

            plt.figure(figsize=(8, 5))
            bars = plt.bar(dates, values, color="skyblue", edgecolor="black")
            plt.xlabel("Quarter")
            plt.ylabel("Revenue")
            plt.title(f"Last 3 Quarterly Revenues of {company_name.title()}")
            plt.xticks(rotation=30)
            plt.tight_layout()

            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval/1e9:.2f}B', ha='center', va='bottom', fontsize=8)

            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            encoded = base64.b64encode(buf.read()).decode("utf-8")
            buf.close()
            plt.close()

            return encoded

        except Exception as e:
            return None