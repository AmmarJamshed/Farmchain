import streamlit as st
from web3 import Web3
import json
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle

# ------------------ Page Config ------------------ #
st.set_page_config(page_title="🧠 CowFarm AI Forecast DApp", layout="centered")

# ------------------ Custom Styling ------------------ #
st.markdown("""
    <style>
    body {
        background-color: #0d0c1d;
    }
    .stApp {
        background-color: #0d0c1d;
        color: #00FFAA;
    }
    h1, h2, h3, h4 {
        color: #B388EB;
    }
    .stButton>button {
        background-color: #00FFAA;
        color: black;
        font-weight: bold;
        border-radius: 10px;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1f1f2e;
        color: #00FFAA;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 CowFarm AI + Blockchain Forecasting DApp")

# ------------------ MetaMask Wallet Connection ------------------ #
st.subheader("🦊 Connect MetaMask Wallet")

wallet_address = streamlit_js_eval(
    js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' }).then(accounts => accounts[0]);",
    key="wallet_connect"
)

if wallet_address:
    st.success(f"🦊 Wallet Connected: {wallet_address}")
else:
    st.info("🔌 Please connect your MetaMask wallet below.")

st.markdown("""
    <button onclick="window.ethereum.request({ method: 'eth_requestAccounts' })">
        👉 Connect MetaMask
    </button>
""", unsafe_allow_html=True)

# ------------------ Ethereum Network Connection ------------------ #
infura_url = "https://sepolia.infura.io/v3/40915988fef54b268deda92af3e2ba66"
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    st.success("✅ Connected to Sepolia Testnet via Infura")
else:
    st.error("❌ Failed to connect to Ethereum")

# ------------------ Load ABI ------------------ #
try:
    with open("CowFarm.json") as f:
        contract_json = json.load(f)
        abi = contract_json["abi"]
except Exception as e:
    st.error(f"Error loading ABI: {e}")
    st.stop()

# ------------------ Contract Address ------------------ #
contract_address = "0x0C5996E38D7B3b00e15F916AafF7Ef987a1A90f1"

try:
    contract = web3.eth.contract(address=contract_address, abi=abi)
except Exception as e:
    st.error(f"Error creating contract instance: {e}")
    st.stop()

# ------------------ Farm and Vendor Onboarding ------------------ #
st.header("🏡 Onboard Farm & Vendor")

with st.form("onboard_form"):
    farm_name = st.text_input("Farm Name")
    location = st.text_input("Location (GPS or City)")
    capacity = st.number_input("Total Capacity", min_value=1)
    maintenance_cost = st.number_input("Monthly Maintenance Cost", min_value=0)
    vendor_name = st.text_input("Vendor Name")
    vendor_id = st.text_input("Vendor CNIC/ID")
    submitted = st.form_submit_button("Register Farm + Vendor")

    if submitted:
        st.success(f"Registered {farm_name} and Vendor {vendor_name}")

# ------------------ Cow Price Forecast ------------------ #
st.header("📈 AI Forecast Cow Price")

st.markdown("Fill in cow details to predict market price using AI model:")

with st.form("forecast_form"):
    breed = st.selectbox("Breed", ["Sahiwal", "Friesian", "Jersey", "Crossbred"])
    age = st.slider("Age (months)", 6, 120)
    weight = st.slider("Weight (kg)", 100, 800)
    health_score = st.slider("Health Score (0 - 10)", 0.0, 10.0, step=0.1)
    milk_output = st.slider("Milk Output (liters/day)", 0, 50)
    submit_forecast = st.form_submit_button("🔮 Predict Price")

    if submit_forecast:
        try:
            # Simulated model (replace with actual model)
            features = pd.DataFrame([[breed, age, weight, health_score, milk_output]],
                                    columns=["breed", "age", "weight", "health", "milk"])
            breed_map = {"Sahiwal": 0, "Friesian": 1, "Jersey": 2, "Crossbred": 3}
            features["breed"] = features["breed"].map(breed_map)
            model = RandomForestRegressor()
            model.fit(np.array([[0, 24, 300, 8.0, 10]]), [70000])  # Dummy fit
            prediction = model.predict(features)[0]
            st.success(f"💰 Predicted Cow Price: PKR {int(prediction):,}")
        except Exception as e:
            st.error(f"Prediction error: {e}")

# ------------------ Cow Count ------------------ #
st.header("🐄 Total Cows on Blockchain")
if st.button("Check Cow Counter"):
    try:
        cow_count = contract.functions.cowCounter().call()
        st.info(f"🐄 Total Cows Registered: {cow_count}")
    except Exception as e:
        st.error(f"Error: {e}")
