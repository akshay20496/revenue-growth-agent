# 📈 Revenue Growth Rate Analyzer (LangChain + Groq + LLaMA3)

This app calculates and visualizes the **average quarterly revenue growth** of any public company using the power of **LangChain agents**, **Groq's ultra-fast LLaMA3 models**, and **real-time financial data** from Yahoo Finance.

<p align="center">
  <img src="https://img.shields.io/badge/Built_with-LangChain-blue?logo=langchain">
  <img src="https://img.shields.io/badge/Powered_by-Groq-ff69b4?logo=groq">
  <img src="https://img.shields.io/badge/Model-LLaMA3_8b_8192-orange?logo=meta">
  <img src="https://img.shields.io/badge/Made_with-Streamlit-ff4b4b?logo=streamlit">
</p>

---

## ✨ Features

- 🔍 **Natural Language Query**: Just enter a company name (e.g. `Apple`) — the app understands and builds the full query behind the scenes.
- 📊 **Graphical Insights**: Displays a bar chart of the company’s last 3 quarterly revenues.
- 📉 **Growth Calculation**: Computes QoQ (Quarter-over-Quarter) growth rates and the average growth rate.
- 🤖 **Agent-powered**: Uses LangChain's zero-shot ReAct agent with multiple tools.
- ⚡ **Groq LLaMA3**: Utilizes Groq's blazing fast inference on Meta’s LLaMA3 8B model.

---

## 🧠 Powered By

- **[LangChain Agents](https://www.langchain.com/)** – for orchestrating tools
- **[Groq API](https://groq.com/)** – for running LLaMA3 at high speed
- **[yfinance + yahooquery](https://pypi.org/project/yfinance/)** – for fetching revenue data
- **[Matplotlib](https://matplotlib.org/)** – for rendering bar charts
- **[Streamlit](https://streamlit.io/)** – for the interactive frontend

---

## 📽️ Demo

https://github.com/your-username/repo-name/assets/your-demo-video.mp4  
*(Replace this with your actual video link)*

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/revenue-growth-agent.git
cd revenue-growth-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file and add your **Groq API key**:
```
groq_api=your_groq_api_key
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🗂️ Project Structure

```
📦 revenue-growth-agent/
│
├── app.py                      # Streamlit frontend
├── revenue.py                  # RevenueTool: fetch & plot revenue
├── growth_calculation.py       # CalculationTool: compute average growth
├── .env                        # Environment file for Groq API key
├── requirements.txt            # Python dependencies
```

---

## 🧠 How It Works

1. You enter just a **company name**.
2. The app builds a query like:  
   👉 _"Get Apple last 3 quarterly revenues and calculate the average growth rate."_
3. LangChain's agent:
   - Uses the **RevenueTool** to fetch revenue data.
   - Uses the **CalculationTool** to compute growth.
4. It displays:
   - 📉 Average growth rate
   - 📊 Revenue chart

---

## ✅ Example Queries

- `Apple`
- `Infosys`
- `Tata Motors`
- `Microsoft`
- `Nvidia`
- `Alphabet Inc.`
- `Toyota`

---

## 🧪 Sample Output

```
The average growth rate for Apple's last 3 quarterly revenues is -12.34%.

📉 Negative growth: Revenue is decreasing by an average of 12.34%.
```

![Bar chart example](path-to-screenshot.png)

---

## 📌 Future Ideas

- Add CSV download support  
- Support for more financial metrics (net income, EPS, etc.)  
- GPT-4o/Gemini/Claude integration

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgments

- Thanks to [Groq](https://groq.com/) for free LLaMA3 API access  
- Inspired by agentic AI concepts from [LangChain](https://www.langchain.com/)
