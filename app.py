import streamlit as st
from fpdf import FPDF

# Set up the web page title and icon
st.set_page_config(page_title="3D Print Cost & ROI Calculator", page_icon="🖨️", layout="centered")

# --- PDF GENERATION FUNCTION ---
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Header / Branding
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "3D PRINTING JOB QUOTE", ln=True, align="C")
    pdf.ln(10)
    
    # Job Details Section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "1. Operational Specifications", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Estimated Print Time: {data['print_time']} Hours", ln=True)
    pdf.cell(0, 8, f"Model Print Weight: {data['print_weight']} Grams", ln=True)
    pdf.cell(0, 8, f"Hands-on Labor Setup: {data['labor_time']} Hours", ln=True)
    pdf.ln(5)
    
    # Financial Breakdown Table/List
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "2. Line-Item Cost Breakdown", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Material Cost: ${data['material_cost']:.2f}", ln=True)
    pdf.cell(0, 8, f"Electricity Cost: ${data['electricity_cost']:.2f}", ln=True)
    pdf.cell(0, 8, f"Machine Wear & Maintenance: ${data['machine_wear_cost']:.2f}", ln=True)
    pdf.cell(0, 8, f"Hands-on Labor Cost: ${data['labor_cost']:.2f}", ln=True)
    pdf.cell(0, 8, f"Risk Protection (Failed Print Buffer): ${data['failure_buffer_cost']:.2f}", ln=True)
    pdf.ln(5)
    
    # Final Pricing Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Final Pricing Summary", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Total Manufacturing Cost: ${data['total_manufacturing_cost']:.2f}", ln=True)
    pdf.cell(0, 8, f"Net Profit Margin Tagged: ${data['profit_margin_value']:.2f}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Recommended Retail Client Price: ${data['recommended_retail_price']:.2f}", ln=True)
    
    return pdf.output(dest="S")

# --- APP HEADER ---
st.title("🖨️ 3D Print Cost & ROI Calculator")
st.markdown("Calculate the *true* cost of your 3D prints, protect your business from failed prints, and set profitable retail prices.")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ Global Rates Setup")
electricity_rate = st.sidebar.number_input("Electricity Rate ($ per kWh)", min_value=0.00, value=0.15, step=0.01, format="%.2f")
labor_rate = st.sidebar.number_input("Your Labor Rate ($ per Hour)", min_value=0.00, value=20.00, step=1.00, format="%.2f")
printer_wattage = st.sidebar.number_input("Printer Power Consumption (Watts)", min_value=0, value=150, step=10)
printer_depreciation = st.sidebar.number_input("Machine Wear/Depreciation ($ per Hour)", min_value=0.00, value=0.25, step=0.05, format="%.2f")

# --- MONETIZATION SIDEBAR HOOK ---
st.sidebar.markdown("---")
st.sidebar.subheader("🌟 Upgrade to Pro")
st.sidebar.write("Unlock history saving, multi-material calculations, and cloud inventory tracking tools.")
st.sidebar.link_button("🚀 Go Premium", "https://buy.stripe.com/mock_link_id")

# --- MAIN DASHBOARD GRID ---
col1, col2 = st.columns(2)

with col1:
    st.header("📦 Material & Print Specs")
    spool_cost = st.number_input("Filament Spool Cost ($)", min_value=0.00, value=25.00, step=1.00, format="%.2f")
    spool_weight = st.number_input("Spool Total Weight (Grams)", min_value=1, value=1000, step=100)
    print_weight = st.number_input("Model Print Weight (Grams)", min_value=0.0, value=150.0, step=5.0)
    print_time = st.number_input("Estimated Print Time (Hours)", min_value=0.0, value=6.5, step=0.5)

with col2:
    st.header("💼 Business Variables")
    labor_time = st.number_input("Post-Processing / Setup Labor (Hours)", min_value=0.0, value=0.5, step=0.1)
    failure_rate = st.slider("Buffer for Failed Prints (%)", min_value=0, max_value=50, value=10, step=5)
    markup = st.slider("Desired Profit Margin Markup (%)", min_value=0, max_value=300, value=50, step=10)

st.markdown("---")

# --- MATHEMATICAL LOGIC ---
cost_per_gram = spool_cost / spool_weight
material_cost = print_weight * cost_per_gram
electricity_consumed = (printer_wattage / 1000) * print_time
electricity_cost = electricity_consumed * electricity_rate
machine_wear_cost = print_time * printer_depreciation
labor_cost = labor_time * labor_rate

base_production_cost = material_cost + electricity_cost + machine_wear_cost + labor_cost
failure_buffer_cost = base_production_cost * (failure_rate / 100)
total_manufacturing_cost = base_production_cost + failure_buffer_cost
profit_margin_value = total_manufacturing_cost * (markup / 100)
recommended_retail_price = total_manufacturing_cost + profit_margin_value

# --- DISPLAYING RESULTS ---
st.header("📊 Price Summary & Cost Breakdown")

metric_col1, metric_col2 = st.columns(2)
with metric_col1:
    st.metric(label="Total Production Cost", value=f"${total_manufacturing_cost:.2f}")
with metric_col2:
    st.subheader(f"Suggested Retail Price: **${recommended_retail_price:.2f}**")

st.markdown("### 🔍 Line-Item Breakdown")
st.write(f"- **Material Cost:** ${material_cost:.2f}")
st.write(f"- **Electricity Cost:** ${electricity_cost:.2f}")
st.write(f"- **Machine Wear:** ${machine_wear_cost:.2f}")
st.write(f"- **Labor Cost:** ${labor_cost:.2f}")
st.write(f"- **Risk Protection Buffer:** ${failure_buffer_cost:.2f}")

st.markdown("---")

# --- PDF GENERATION ENGINE BUTTON ---
# Package data dict for clean processing
job_data = {
    'print_time': print_time, 'print_weight': print_weight, 'labor_time': labor_time,
    'material_cost': material_cost, 'electricity_cost': electricity_cost,
    'machine_wear_cost': machine_wear_cost, 'labor_cost': labor_cost,
    'failure_buffer_cost': failure_buffer_cost, 'total_manufacturing_cost': total_manufacturing_cost,
    'profit_margin_value': profit_margin_value, 'recommended_retail_price': recommended_retail_price
}

pdf_bytes = generate_pdf(job_data)

st.download_button(
    label="📥 Download Professional PDF Invoice",
    data=pdf_bytes,
    file_name="3d_print_job_quote.pdf",
    mime="application/pdf",
    use_container_width=True
)
