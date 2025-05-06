import streamlit as st
from web3 import Web3
import json
from streamlit_js_eval import streamlit_js_eval

# ------------------ Page Config ------------------ #
st.set_page_config(page_title="🧠 CowFarm AI Blockchain DApp", layout="centered")

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
    .stTextInput>div>div>input {
        background-color: #1f1f2e;
        color: #00FFAA;
    }
    .stNumberInput>div>div>input {
        background-color: #1f1f2e;
        color: #00FFAA;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 CowFarm AI + Blockchain DApp")

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

# ------------------ Cow Counter ------------------ #
st.header("🐄 View Total Cows Stored")

if st.button("Check Cow Counter"):
    try:
        cow_count = contract.functions.cowCounter().call()
        st.info(f"🐄 Total Cows Registered on Chain: {cow_count}")
    except Exception as e:
        st.error(f"Error fetching cow count: {e}")

# ------------------ Store Cow ------------------ #
st.header("📦 Register a New Cow to the Blockchain")

st.markdown("Provide the **Farm's Public Ethereum Address**, monthly hosting fee, and milk commission:")

with st.form("store_cow_form"):
    farm_address = st.text_input("Farm Address (Public Wallet Key)", placeholder="0x...")
    monthly_fee = st.number_input("Monthly Hosting Fee (in wei)", min_value=0)
    milk_commission = st.number_input("Milk Commission (in wei)", min_value=0)
    submitted = st.form_submit_button("📦 Store Cow")

    if submitted:
        if not wallet_address:
            st.warning("⚠️ Please connect MetaMask first.")
        else:
            st.warning("⚠️ Transactions not signed yet – implement eth_sendTransaction to proceed.")
            st.code(
                f"contract.functions.storeCow('{farm_address}', {monthly_fee}, {milk_commission}).transact(from={wallet_address})"
            )
            st.success("🔄 Transaction setup complete. Add JS signer to process on-chain.")

# ------------------ Contract Info ------------------ #
st.header("🔧 Smart Contract Info")
st.write(f"📍 Contract Address: `{contract_address}`")
st.write("✅ ABI Loaded:", isinstance(abi, list))
