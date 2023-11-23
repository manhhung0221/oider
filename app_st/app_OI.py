import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from manage_engine import engine_public

def draw_oi(data,vn30,reTicker):
    # Tạo một biểu đồ với hai trục y
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Thêm các dòng cho 'cOI_TD', 'cOI_NN', 'cOI_other' trên trục y chính
    fig.add_trace(go.Scatter(x=data['DateTime'], y=data['cOI_TD'], name='OI Tự doanh'), secondary_y=False)
    fig.add_trace(go.Scatter(x=data['DateTime'], y=data['cOI_NN'], name='OI Nước Ngoài'), secondary_y=False)
    fig.add_trace(go.Scatter(x=data['DateTime'], y=data['cOI_other'], name='OI Nhóm khác'), secondary_y=False)

    # Thêm dòng cho 'VNINDEX' trên trục y thứ cấp
    fig.add_trace(go.Scatter(x=vn30['DateTime'], y=vn30['Close'], name='VN30'), secondary_y=True)

    # Đặt tiêu đề cho biểu đồ
    fig.update_layout(title_text=reTicker,xaxis=dict(tickformat='%d/%m/%Y'),)

    # Đặt tiêu đề cho trục x
    fig.update_xaxes(title_text="DateTime")

    # Đặt tiêu đề cho trục y1
    fig.update_yaxes(title_text="OI", secondary_y=False)

    # Đặt tiêu đề cho trục y2
    fig.update_yaxes(title_text="Chỉ số", secondary_y=True)
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]), #hide weekends

        ])
    # Hiển thị biểu đồ
    return fig

def get_data(reTicker):

    data_td=pd.read_sql(f"""SELECT re.reTicker AS Ticker,re.DateTime,BuyVolTD,SellVolTD 
                    FROM re_ticker AS re
                    INNER JOIN eod_td_derivative AS td
                    ON re.Ticker=td.Ticker AND re.DateTime=td.DateTime
                    WHERE re.reTicker='{reTicker}'""",engine_public)
    data_nn=pd.read_sql(f"""SELECT re.reTicker AS Ticker,re.DateTime,BuyVolForeign,SellVolForeign
                    FROM re_ticker AS re
                    INNER JOIN eod_nn_derivative AS nn
                    ON re.Ticker=nn.Ticker AND re.DateTime=nn.DateTime
                    WHERE re.reTicker='{reTicker}'""",engine_public)
    data_eod=pd.read_sql(f"""SELECT re.reTicker AS Ticker,re.DateTime,der.OI 
                    FROM re_ticker AS re
                    INNER JOIN eod_derivative AS der
                    ON re.Ticker=der.Ticker AND re.DateTime=der.DateTime
                    WHERE re.reTicker='{reTicker}'""",engine_public)
    data_eod.sort_values("DateTime",inplace=True)
    data_td.sort_values("DateTime",inplace=True)
    data_nn.sort_values("DateTime",inplace=True)

    data_td['OI_TD']=data_td['BuyVolTD']-data_td['SellVolTD']
    data_td['cOI_TD']=data_td['OI_TD'].cumsum()
    data_td['pct_OI_TD']=data_td['cOI_TD'].pct_change(1)

    data_nn['OI_NN']=data_nn['BuyVolForeign']-data_nn['SellVolForeign']
    data_nn['cOI_NN']=data_nn['OI_NN'].cumsum()
    data_nn['pct_OI_NN']=data_nn['cOI_NN'].pct_change(1)

    data=data_eod.merge(data_td[['Ticker','DateTime','cOI_TD','pct_OI_TD']],on=['Ticker','DateTime'],how='left')
    data=data.merge(data_nn[['Ticker','DateTime','cOI_NN','pct_OI_NN']],on=['Ticker','DateTime'],how='left')
    data['cOI_TD'].ffill(inplace=True)
    data['cOI_NN'].ffill(inplace=True)
    data.fillna(0,inplace=True)
    data['ratioTD']=data['cOI_TD']/data['OI']
    data['ratioNN']=data['cOI_NN']/data['OI']

    data['cOI_other']=data['OI']-abs(data['cOI_TD'])-abs(data['cOI_NN'])
    data['ratioOther']=data['cOI_other']/data['OI']

    min_date=data.DateTime.min()
    vn=pd.read_sql(f"SELECT Ticker,DateTime,Close FROM eod_index WHERE DateTime>='{min_date:%Y-%m-%d}'",engine_public)
    vn30=vn.loc[vn['Ticker']=='VN30']
    vn30.sort_values("DateTime",inplace=True)
    fig=draw_oi(data,vn30,reTicker)
    return fig
def OI():
    st.title('OI PHAI SINH')
    col1, col2 = st.columns([0.3, 0.7])  # Số trong list đại diện cho tỷ lệ chiều rộng của mỗi cột

    # Sử dụng cột đầu tiên cho hộp nhập liệu thứ nhất
    with col1:
        reTicker = st.text_input('Nhập mã phái sinh')
    if reTicker:
        reTicker=reTicker.upper()
        fig=get_data(reTicker)
        st.plotly_chart(fig,use_container_width=True)
