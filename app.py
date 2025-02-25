import streamlit as st
import google.generativeai as genai

# Set page configuration at the very beginning
st.set_page_config(page_title="Smart Converter & AI", layout="wide")

def initialize_gemini():
    genai.configure(api_key="AIzaSyD2pu_pjTzWVhy9nqJ0hp1DBhzSQMe8ZHA")

def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        ('meters', 'kilometers'): 0.001,
        ('kilometers', 'meters'): 1000,
        ('grams', 'kilograms'): 0.001,
        ('kilograms', 'grams'): 1000,
        ('celsius', 'fahrenheit'): lambda c: (c * 9/5) + 32,
        ('fahrenheit', 'celsius'): lambda f: (f - 32) * 5/9
    }
    if (from_unit, to_unit) in conversion_factors:
        factor = conversion_factors[(from_unit, to_unit)]
        return factor(value) if callable(factor) else value * factor
    return None

def get_gemini_response(query):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(query)
    return response.text if response else "No response from Gemini."

def main():
    # Inject custom CSS (using data-testid selectors for reliability)
    st.markdown(
        """
        <style>
            /* Set app background */
            .stApp { 
                background-color: #818FB4;
            }
            /* Title and subtitle styling */
            .title {
                font-size: 32px;
                font-weight: bold;
                text-align: center;
                color: #222;
            }
            .subtitle {
                font-size: 20px;
                text-align: center;
                color: #444;
            }
            /* Container box styling */
            .box {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                color: #222;
            }
            /* Widget text color overrides using data-testid selectors */
            div[data-testid="stTextInput"] * {
                color: #222 !important;
            }
            div[data-testid="stNumberInput"] * {
                color: #222 !important;
            }
            div[data-testid="stSelectbox"] * {
                color: #222 !important;
            }
            div[data-testid="stTextArea"] * {
                color: #222 !important;
            }
            /* Ensure text areas have a white background */
            div[data-testid="stTextArea"] textarea {
                background-color: #fff !important;
                color: #222 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header Section
    st.markdown("<p class='title'>Smart Unit Converter & AI Assistant</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Easily convert units and get AI-powered answers</p>", unsafe_allow_html=True)
    
    # Layout with two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        st.subheader("🔢 Unit Converter")

        unit_types = {
            "Length": ["meters", "kilometers"],
            "Mass": ["grams", "kilograms"],
            "Temperature": ["celsius", "fahrenheit"]
        }
        category = st.selectbox("Select unit category", list(unit_types.keys()))
        from_unit = st.selectbox("From", unit_types[category])
        to_unit = st.selectbox("To", unit_types[category])
        value = st.number_input("Enter value", min_value=0.0, format="%.2f")

        if st.button("Convert", use_container_width=True):
            result = convert_units(value, from_unit, to_unit)
            if result is not None:
                st.success(f"✅ {value} {from_unit} = {result:.2f} {to_unit}")
            else:
                st.error("❌ Conversion not available")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        st.subheader("🤖 Ask Gemini AI")
        user_query = st.text_area("Enter your question", placeholder="Ask anything...")
        if st.button("Get AI Response", use_container_width=True):
            with st.spinner("Thinking..."):
                initialize_gemini()
                response = get_gemini_response(user_query)
                st.info(response)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
