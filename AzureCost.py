import argparse
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

def generate_tree_chart(files):
    data = {}

    # 遍历所有文件
    for file in files:
        # 读取Excel文件
        sheet = pd.read_excel(file)

        # 提取第一列作为分类标签
        categories = sheet.iloc[:, 0].tolist()

        # 提取第二列的数值
        values = sheet.iloc[:, 1].tolist()

        # 将数据加入字典
        for category, value in zip(categories, values):
            if category not in data:
                data[category] = [0] * len(files)
            data[category][files.index(file)] += value

    # 准备数据用于绘图
    categories = sorted(data.keys())
    values = [[data[category][i] for category in categories] for i in range(len(files))]

    # 提取文件名作为图例标签
    file_names = [os.path.basename(file).split('.')[0] for file in files]

    # 格式化数值
    values_formatted = [[f'{value:.2f} RMB' for value in file_values] for file_values in values]

    # 创建 Plotly 图表
    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'xy'}]])

    for i in range(len(files)):
        fig.add_trace(go.Bar(x=categories, y=values[i], text=values_formatted[i], name=file_names[i]), row=1, col=1)

    # 设置布局
    fig.update_layout(title='Comparison of Azure Cost',
                      xaxis=dict(title='Service Name', tickangle=-90),
                      yaxis=dict(title='Cost (RMB)'),
                      hovermode='closest')

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_html = f"output_{timestamp}.html"

    # 保存为 HTML 文件
    fig.write_html(output_html)

    return output_html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comparison chart from Excel files.")
    parser.add_argument("files", metavar="FILE", nargs="+", help="Excel file paths")
    args = parser.parse_args()

    # Convert paths starting with .\ to absolute paths
    files = [os.path.abspath(file) if file.startswith('.\\') else file for file in args.files]

    output_file = generate_tree_chart(files)
    print("Output HTML file:", output_file)
