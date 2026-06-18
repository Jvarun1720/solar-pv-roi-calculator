# ☀️ Interactive Solar PV Forecasting & ROI Dashboard

An engineering-backed, interactive financial and spatial modeling application designed to size residential/commercial solar arrays, forecast long-term energy yields, and map 15-year return on investment (ROI) lifecycles. 

Built using **Streamlit** and **Plotly**, the tool incorporates realistic solar physical constraints—such as panel degradation rates, geographical peak sun hours (PSH), performance ratios (PR), and spatial roof limitations—to deliver cross-currency financial forecasting.

<img width="1913" height="986" alt="Screenshot 2026-06-16 143928" src="https://github.com/user-attachments/assets/49aafec8-fb28-47a5-afd5-2539ca8c20b2" />


---

## 🚀 Features

* **Dynamic Spatial Sizing:** Automatically bounds recommended system size based on available rooftop physical area (assuming ~100 sq ft per 1 kW).
* **Dual-Currency Financial Modeling:** Seamlessly toggles between USD ($) and INR (₹) with dynamically adjusting regional default metrics (e.g., base utility rates, infrastructure costs per kW).
* **15-Year Cash Flow Forecasting:** Simulates compound yearly degradation alongside cumulative savings to accurately isolate the project break-even year.
* **Interactive Visualizations:** Leverages Plotly for an adaptive, real-time updated waterfall/bar chart reflecting net financial positions over time.
* **Environmental Accounting:** Tracks green impact by calculating projected annual $CO_2$ offsets based on net clean energy production.
* **Hybrid Deployment Architecture:** Fully operational as both a responsive web application and a native desktop environment.

---

## 📊 Core Mathematical Model

The application utilizes standardized solar engineering formulas to maintain analytical accuracy:

1. **Energy Generation Demand:** $$\text{Monthly Demand (kWh)} = \frac{\text{Monthly Bill}}{\text{Cost per kWh}}$$
2. **Ideal System Size Calculation:** $$\text{Required Size (kW)} = \frac{\text{Monthly Demand (kWh)}}{30 \times \text{Peak Sun Hours} \times \text{Performance Ratio (0.75)}}$$
3. **Physical Constraint Sizing:** $$\text{Actual Size (kW)} = \min\left(\text{Required Size}, \frac{\text{Roof Area (sq ft)}}{100}\right)$$
4. **Annual Degradation Yield Factor:** $$\text{Yearly Generation}_t = \text{Initial Generation} \times (1 - 0.005)^{t-1}$$

---

## 🛠️ Tech Stack

* **Frontend & UI Framework:** Streamlit
* **Data Visualization:** Plotly (Graph Objects)
* **Data Manipulation:** Pandas
* **Desktop App Wrapper:** PyWebView
* **Language:** Python 3.x

---

## ⚙️ Installation & Usage

### 🌐 Running the Web Application Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/solar-pv-roi-calculator.git](https://github.com/your-username/solar-pv-roi-calculator.git)
   cd solar-pv-roi-calculator
