import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(".."))
from ai_model import forecast_price
import pandas as pd
from web3 import Web3
import json

st.title("🐄 Decentralized Cow Farming + AI Price Forecasting")

# Connect to Blockchain
infura_url = 'https://rpc-mumbai.maticvigil.com'
web3 = Web3(Web3.HTTPProvider(infura_url))

contract_address = "0xYOUR_CONTRACT_ADDRESS"
with open('CowFarm.json') as f:
    abi = json.load(f)

contract = web3.eth.contract(address=contract_address, abi=abi)

# Wallet connection
private_key = st.text_input("Enter your private key:", type="password")
wallet_address = web3.eth.account.privateKeyToAccount(private_key).address if private_key else None

# Features
tab1, tab2, tab3 = st.tabs(["📦 Store Cow", "💵 Payments", "📈 Forecast Prices"])

with tab1:
    st.subheader("📦 Store Your Cow on a Farm")
    farm_address = st.text_input("Farm Wallet Address")
    monthly_fee = st.number_input("Monthly Fee", min_value=0)
    milk_fee = st.number_input("Milk Commission Fee", min_value=0)
    if st.button("Store Cow"):
        nonce = web3.eth.get_transaction_count(wallet_address)
        txn = contract.functions.storeCow(farm_address, monthly_fee, milk_fee).build_transaction({
            'chainId': 80001,
            'gas': 3000000,
            'gasPrice': web3.to_wei('5', 'gwei'),
            'nonce': nonce
        })
        signed = web3.eth.account.sign_transaction(txn, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
        st.success(f"Cow stored! TxHash: {tx_hash.hex()}")

with tab2:
    st.subheader("💵 Make or Receive Payments")
    cow_id = st.number_input("Cow ID", min_value=0)
    amount = st.number_input("Payment Amount in ETH", min_value=0.001)
    tx_type = st.selectbox("Payment Type", ["Pay Farm", "Pay Owner"])
    if st.button("Send Payment"):
        nonce = web3.eth.get_transaction_count(wallet_address)
        if tx_type == "Pay Farm":
            txn = contract.functions.payFarm(cow_id).build_transaction({
                'chainId': 80001,
                'gas': 3000000,
                'gasPrice': web3.to_wei('5', 'gwei'),
                'nonce': nonce,
                'value': web3.to_wei(amount, 'ether')
            })
        else:
            txn = contract.functions.payMilkCommission(cow_id).build_transaction({
                'chainId': 80001,
                'gas': 3000000,
                'gasPrice': web3.to_wei('5', 'gwei'),
                'nonce': nonce,
                'value': web3.to_wei(amount, 'ether')
            })

        signed = web3.eth.account.sign_transaction(txn, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
        st.success(f"Payment sent! TxHash: {tx_hash.hex()}")

with tab3:
    st.subheader("📈 AI-Based Cow Price Forecast")
    forecast = forecast_price()
    st.line_chart(forecast)
