import streamlit as st
from web3 import Web3
import json

st.set_page_config(page_title="CowFarm DApp", layout="centered")
st.title("🐮 CowFarm Smart Contract Interface")

# ------------------------------
# Step 1: Connect to Web3 provider
# ------------------------------
infura_url = "https://rpc.sepolia.org"  # Change this if using a different provider
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    st.success("✅ Connected to Ethereum network")
else:
    st.error("❌ Failed to connect to Ethereum")

# ------------------------------
# Step 2: Load ABI and Contract
# ------------------------------
with open("CowFarm.json") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# Deployed contract address
contract_address = "0xd9145CCE52D386f254917e481eB44e9943F39138"

# Contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# ------------------------------
# Step 3: Show current cow counter
# ------------------------------
if st.button("Check Total Cows"):
    try:
        cow_count = contract.functions.cowCounter().call()
        st.info(f"🐄 Total Cows Stored: {cow_count}")
    except Exception as e:
        st.error(f"Error fetching cow count: {e}")

# ------------------------------
# Step 4: Interact with `storeCow`
# ------------------------------
st.subheader("📦 Store a New Cow")

with st.form("store_cow_form"):
    farm_address = st.text_input("Farm Address", placeholder="0x...")
    monthly_fee = st.number_input("Monthly Fee (wei)", min_value=0)
    milk_commission = st.number_input("Milk Commission (wei)", min_value=0)
    submitted = st.form_submit_button("Store Cow")

    if submitted:
        try:
            # Replace with actual account and private key if signing is needed
            st.warning("This will only work with Web3 wallet integration or backend signing.")
            st.code(f"contract.functions.storeCow('{farm_address}', {monthly_fee}, {milk_commission}).transact(...)")
            st.success("Mock call generated. Add transaction logic for full deployment.")
        except Exception as e:
            st.error(f"Error: {e}")

# ------------------------------
# Step 5: Display Contract Events (Optional)
# ------------------------------
st.subheader("🧾 Smart Contract Info")
st.write(f"📍 Contract Address: `{contract_address}`")
st.write("🔧 Contract ABI Loaded:", type(abi))
