import pandas as pd 
import numpy as np
from sqlalchemy import MetaData,Table
def value_to_string(x, dtype):
    '''
Chuyển giá trị nan thành NULL
    '''
    if pd.isnull(x) or (isinstance(x, float) and np.isnan(x)):
        return 'NULL'
    if dtype == "TEXT" or ("VARCHAR" in dtype) or dtype=='TIMESTAMP' or dtype=='DATETIME':
        x=str(x).replace("'","''")
        return "'" + x + "'"
    return str(x)
def get_dtype_col_SQL(df, table_name, engine):
    '''
    - df: DataFrame bạn muốn thêm vào bảng.
    - table_name: Tên Bảng SQL cần xác định column và data_types.
    - engine: Truyền engine kết nối SQL.
    '''
    metadata = MetaData()
    my_table = Table(table_name, metadata, autoload=True, autoload_with=engine)

    data_types = []
    column = []
    for col in df.columns:
        if col in my_table.columns:
            column.append(col)
            data_types.append(str(my_table.columns[col].type))
    return column, data_types 
def insert_or_update(df, table_name, engine):
    '''
Thực hiện chức năng update hoặc insert dựa trên duplicate key.
Yêu cầu bảng cần xác định Primary key
- df: DataFrame truyền vào
- table_name: Tên Bảng SQL cần insert or update
- engine: bộ engine kết nối với MYSQL'''
    # Danh sách cột và kiểu dữ liệu tương ứng
    columns,data_types=get_dtype_col_SQL(df,table_name,engine)

    
    # Tạo phần VALUES cho câu truy vấn
    values_list = df.values.tolist()
    values_str_list = ['(' + ', '.join(map(lambda x, dtype: value_to_string(x, dtype), v, data_types)) + ')' for v in values_list]
    values_str = ', '.join(values_str_list)
    
    escaped_columns = [f"`{col}`" for col in columns]
    # Tạo phần ON DUPLICATE KEY UPDATE
    duplicate_str = ', '.join([f'{escaped_col}=VALUES({escaped_col})' for escaped_col in escaped_columns])
    
    query = f"""
        INSERT INTO {table_name} ({', '.join(escaped_columns)}) 
        VALUES {values_str} 
        ON DUPLICATE KEY UPDATE {duplicate_str};
    """
    
    # Thực thi câu truy vấn
    with engine.connect() as conn:
        conn.execute(query)