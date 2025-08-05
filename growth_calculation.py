from langchain.agents import Tool
import json
from revenue import RevenueTool  # local import to avoid circular dependency

class CalculationTool:
    def __init__(self):
        self.name = "calculation_tool"
        self.description = "Calculates QoQ growth rates and average growth from a dict of revenues by date."

    # Tool 2: Calculator – compute QoQ growth and average
    def custom_growth(self, data: str) -> str:
        try:
            if isinstance(data, str):
                data = json.loads(data.replace("'", '"'))

            if not isinstance(data, dict):
                return "Invalid input format. Expected a dict of revenues by date."

            # Sort by date descending
            sorted_data = sorted(data.items(), reverse=True)
            dates = [k for k, _ in sorted_data[:3]]
            values = [v for _, v in sorted_data[:3]]

            if len(values) < 2:
                return "Not enough data to calculate growth."

            growth = {}
            for i in range(1, len(values)):
                rate = ((values[i-1] - values[i]) / values[i]) * 100
                growth[f"{dates[i]} → {dates[i-1]}"] = round(rate, 2)

            avg_growth = round(sum(growth.values()) / len(growth), 2)

            result = "\n".join([f"{period}: {rate}%" for period, rate in growth.items()])
            result += f"\n\nAverage Growth Rate: {avg_growth}%"
            return result

        except Exception as e:
            return f"Error in growth calculation: {e}"
    
    # New method for app use (returns both structured values and growth string)
    def calculate_growth(self, company_name: str):
        revenue_json = RevenueTool().get_company_revenue(company_name)

        # ✅ Check if the return is valid JSON
        if not revenue_json.strip().startswith("{"):
            return None, None, f"RevenueTool error: {revenue_json}"

        try:
            data = json.loads(revenue_json.replace("'", '"'))
        except Exception as e:
            return None, None, f"Error parsing revenue data: {e}"

        # Sort and take last 3 values
        sorted_data = sorted(data.items(), reverse=True)
        dates = [k for k, _ in sorted_data[:3]]
        values = [v for _, v in sorted_data[:3]]

        if len(values) < 2:
            return data, None, "Not enough data to calculate growth."

        growth = {}
        for i in range(1, len(values)):
            rate = ((values[i-1] - values[i]) / values[i]) * 100
            growth[f"{dates[i]} → {dates[i-1]}"] = round(rate, 2)

        avg_growth = round(sum(growth.values()) / len(growth), 2)
        return data, avg_growth, None

    # Tool definition for LangChain
    def get_tool(self) -> Tool:
        return Tool(
            name=self.name,
            func=self.custom_growth,
            description=self.description
        )