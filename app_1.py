import streamlit as st
from web3 import Web3
import json
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="CowFarm DApp", layout="centered")
st.title("🐮 CowFarm Smart Contract Interface")

# ------------------------------
# Step 0: MetaMask Wallet Connection (JS-based)
# ------------------------------
st.subheader("🦊 Connect MetaMask Wallet")

wallet_address = streamlit_js_eval(js_expressions="window.ethereum.selectedAddress", key="wallet")
if wallet_address:
    st.success(f"🦊 Connected Wallet: {wallet_address}")
else:
    st.info("🔌 Please connect your MetaMask wallet below.")

st.markdown("""
    <button onclick="window.ethereum.request({ method: 'eth_requestAccounts' })">
        👉 Connect MetaMask
    </button>
""", unsafe_allow_html=True)

# ------------------------------
# Step 1: Connect to Infura Ethereum Mainnet
# ------------------------------
infura_url = "https://mainnet.infura.io/v3/40915988fef54b268deda92af3e2ba66"
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    st.success("✅ Connected to Ethereum Mainnet via Infura")
else:
    st.error("❌ Failed to connect to Ethereum network")

# ------------------------------
# Step 2: Load ABI and Contract
# ------------------------------
try:
    with open("CowFarm.json") as f:
        contract_json = json.load(f)
        abi = contract_json["abi"]
except Exception as e:
    st.error(f"Error loading ABI: {e}")
    st.stop()

# Deployed contract address
contract_address = "0xd9145CCE52D386f254917e481eB44e9943F39138"

# Contract instance
try:
    contract = web3.eth.contract(address=contract_address, abi=abi)
except Exception as e:
    st.error(f"Error creating contract instance: {e}")
    st.stop()

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
    monthly_fee = st.number_input("Monthly Fee (in wei)", min_value=0)
    milk_commission = st.number_input("Milk Commission (in wei)", min_value=0)
    submitted = st.form_submit_button("Store Cow")

    if submitted:
        if not wallet_address:
            st.warning("⚠️ Please connect MetaMask first.")
        else:
            st.warning("⚠️ Transactions cannot yet be signed in browser (MetaMask connected, no signer).")
            st.code(f"contract.functions.storeCow('{farm_address}', {monthly_fee}, {milk_commission}).transact(from={wallet_address})")
            st.success("🔄 MetaMask address connected. Frontend signing can now be added.")

# ------------------------------
# Step 5: Display Contract Info
# ------------------------------
st.subheader("🧾 Smart Contract Info")
st.write(f"📍 Contract Address: `{contract_address}`")
st.write("🔧 ABI Loaded:", isinstance(abi, list))
