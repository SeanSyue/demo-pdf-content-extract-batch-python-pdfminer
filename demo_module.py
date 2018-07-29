"""
https://zhuanlan.zhihu.com/p/34819237
https://github.com/wshuyi/demo-pdf-content-extract-batch-python-pdfminer
分析流程整理成函数，以便于将来更方便地调用
"""
import glob
from pdf_extractor import extract_pdf_content
import pandas as pd
import matplotlib.pyplot as plt


def get_mydict_from_pdf_path(mydict_, pdf_path_):
    """
    整合pdf内容提取到字典的模块
    输入是已有词典和pdf文件夹路径，输出为新的词典
    """
    pdfs = glob.glob("{}/*.pdf".format(pdf_path_))
    for pdf in pdfs:
        key = pdf.split('/')[-1]
        if key not in mydict_:
            print("Extracting content from {} ...".format(pdf))
            mydict_[key] = extract_pdf_content(pdf)
    return mydict_


def make_df_from_mydict(mydict_):
    """ 把词典转换成数据框 """
    df_ = pd.DataFrame.from_dict(mydict_, orient='index').reset_index()
    df_.columns = ["path", "content"]
    return df_


def draw_df(df_):
    """ 绘制统计出来的字符数量 """
    df_["length"] = df_.content.apply(lambda x: len(x))
    plt.figure(figsize=(14, 6))
    df_.set_index('path').length.plot(kind='bar')
    plt.xticks(rotation=45)


if __name__ == '__main__':
    # 在运行之前，先将演示目录下的newpdf子目录中的2个pdf文件，移动到pdf目录下面
    pdf_path = "pdf/"
    mydict = dict()
    mydict = get_mydict_from_pdf_path(mydict, pdf_path)
    print(mydict)

    df = make_df_from_mydict(mydict)
    draw_df(df)
