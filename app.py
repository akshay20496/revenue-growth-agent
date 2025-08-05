import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from revenue import RevenueTool
from growth_calculation import CalculationTool
from dotenv import load_dotenv
import json
import os
import time
import random
import re

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("groq_api")

# Initialize tools
revenue_tool = RevenueTool().get_tool()
calculation_tool = CalculationTool().get_tool()

# Function to initialize and run the agent
def run_agent_with_query(query: str):
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama3-8b-8192",
        temperature=0
    )
    agent = initialize_agent(
        tools=[revenue_tool, calculation_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        early_stopping_method="generate",
        verbose=True
    )
    return agent.run(query)

# Retry mechanism for Groq overcapacity errors
def run_agent_with_retries(query: str, retries=5):
    for attempt in range(retries):
        try:
            return run_agent_with_query(query)
        except Exception as e:
            error_msg = str(e).lower()
            if "over capacity" in error_msg or "503" in error_msg:
                wait = 2 ** attempt + random.uniform(0, 1)
                st.warning(f"Groq over capacity. Retrying in {wait:.1f} seconds...")
                time.sleep(wait)
            else:
                return f"❌ Error: {e}"
    return "❌ Error: Groq API is currently unavailable after multiple attempts."

# Streamlit UI
st.set_page_config(page_title="Revenue Growth Agent", page_icon="📈")

# 🖼️ App title and description
st.title("📊 Revenue Growth Rate Calculator for the Last 3 Quarters")
st.markdown(
    "Ask a question like:\n"
    "`Get apple last 3 quarterly revenues and calculate the average growth rate.`"
)

# Company input
company_input = st.text_input(
    "Enter company name:",
    placeholder="e.g. Apple, Microsoft, Infosys"
)

# Submit button
if st.button("Submit"):
    if company_input:
        user_input = f"Get {company_input} last 3 quarterly revenues and calculate the average growth rate."

        with st.spinner(f"🔄 Processing query: '{user_input}'"):
            try:
                response = run_agent_with_retries(user_input)

                # Show raw response
                st.markdown("### ✅ Response")
                st.write(response)

                # Extract average growth rate
                match = re.search(r"average growth rate.*?(-?\d+(?:\.\d+)?)\s*%", response, re.IGNORECASE)

                if match:
                    avg_growth = float(match.group(1))

                    st.markdown("### 📈 Insight")
                    if avg_growth > 0:
                        st.info(f"📈 Positive growth: Revenue is **increasing** by an average of **{avg_growth}%**.")
                    elif avg_growth < 0:
                        st.warning(f"📉 Negative growth: Revenue is **decreasing** by an average of **{abs(avg_growth)}%**.")
                    else:
                        st.info("➖ Stable revenue: The average growth rate is **0%**.")
                else:
                    # Fallback: use manual calculation if agent response doesn't include avg growth
                    data, avg_growth_manual, error = CalculationTool().calculate_growth(company_input)

                    if error:
                        st.error(f"⚠️ Could not extract average growth rate: {error}")
                    elif avg_growth_manual is not None:
                        st.markdown("### 📈 Fallback Insight")
                        if avg_growth_manual > 0:
                            st.info(f"📈 Positive growth: Revenue is **increasing** by an average of **{avg_growth_manual}%**.")
                        elif avg_growth_manual < 0:
                            st.warning(f"📉 Negative growth: Revenue is **decreasing** by an average of **{abs(avg_growth_manual)}%**.")
                        else:
                            st.info("➖ Stable revenue: The average growth rate is **0%**.")

                # Now get revenue data directly for plotting
                data, avg_growth_value, error = CalculationTool().calculate_growth(company_input)

                if error:
                    st.error(f"📛 {error}")
                else:
                    st.markdown("debug: Data for plotting")
                    st.json(data)
                    plot_img = RevenueTool().plot_revenue_from_data(company_input, json.dumps(data))
                    if plot_img:
                        st.markdown("### 📊 Revenue Trend")
                        st.image(f"data:image/png;base64,{plot_img}", use_container_width=True)
                    else:
                        st.warning("📉 Could not generate revenue chart.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a company name.")


