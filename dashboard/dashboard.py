import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the RFM dataset
file_path = os.path.join(os.path.dirname(__file__), 'main_data.csv')

with st.spinner('Memuat dataset, harap tunggu...'):
    rfm_df = pd.read_csv(file_path)

# Streamlit App
st.title('E-Commerce RFM Analysis Dashboard')

# Sidebar for filtering RFM metrics
st.sidebar.header('Filter RFM Metrics')

# Filter Recency
recency_filter = st.sidebar.slider('Recency (days)', min_value=int(rfm_df['Recency'].min()), max_value=int(rfm_df['Recency'].max()), value=(int(rfm_df['Recency'].min()), int(rfm_df['Recency'].max())))

# Filter Frequency
frequency_filter = st.sidebar.slider('Frequency (orders)', min_value=int(rfm_df['Frequency'].min()), max_value=int(rfm_df['Frequency'].max()), value=(int(rfm_df['Frequency'].min()), int(rfm_df['Frequency'].max())))

# Filter Monetary
monetary_filter = st.sidebar.slider('Monetary (amount)', min_value=float(rfm_df['Monetary'].min()), max_value=float(rfm_df['Monetary'].max()), value=(float(rfm_df['Monetary'].min()), float(rfm_df['Monetary'].max())))

# Filter data based on selections
filtered_rfm = rfm_df[(rfm_df['Recency'] >= recency_filter[0]) & (rfm_df['Recency'] <= recency_filter[1]) &
                    (rfm_df['Frequency'] >= frequency_filter[0]) & (rfm_df['Frequency'] <= frequency_filter[1]) &
                    (rfm_df['Monetary'] >= monetary_filter[0]) & (rfm_df['Monetary'] <= monetary_filter[1])]

# Show filtered data
st.write('Filtered RFM Data:', filtered_rfm)

# Visualizations
st.write("### Recency, Frequency, Monetary Distribution")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Recency Plot
sns.histplot(filtered_rfm['Recency'], kde=True, ax=axes[0])
axes[0].set_title('Recency Distribution')

# Frequency Plot
sns.histplot(filtered_rfm['Frequency'], kde=True, ax=axes[1])
axes[1].set_title('Frequency Distribution')

# Monetary Plot
sns.histplot(filtered_rfm['Monetary'], kde=True, ax=axes[2])
axes[2].set_title('Monetary Distribution')

st.pyplot(fig)
