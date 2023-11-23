import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from manage_engine import engine_public
from draw.draw_oi_reTicker import get_data
from draw.draw_oi_Ticker import get_data_ticker

def OI():
    st.title('OI PHAI SINH')
    col1, col2,col3 = st.columns([0.1, 0.15,0.8])  # Số trong list đại diện cho tỷ lệ chiều rộng của mỗi cột
    col1_row2_chart, col2_row2_chart = st.columns([0.5, 0.5])  
    # Sử dụng cột đầu tiên cho hộp nhập liệu thứ nhất
    with col1:
        nearDerivative=engine_public.execute("SELECT reTicker FROM re_ticker WHERE Ticker='VN30F1M' ORDER BY DateTime DESC LIMIT 1").fetchone()[0]
        reTicker = st.text_input(label='Nhập mã phái sinh',value=nearDerivative)
    with col2:
        Ticker = st.text_input(label='Nhập mã phái sinh theo kỳ hạn',value='VN30F1M')
        Ticker=Ticker.upper()
    if reTicker:
        reTicker=reTicker.upper()
        fig_reTicker,min_date=get_data(reTicker)
        if fig_reTicker is not None:
            with col1_row2_chart:
                st.plotly_chart(fig_reTicker,use_container_width=True)
            fig_ticker=get_data_ticker(Ticker,min_date)
            if fig_ticker is not None:
                with col2_row2_chart:
                    st.plotly_chart(fig_ticker,use_container_width=True)

