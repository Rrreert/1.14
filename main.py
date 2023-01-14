import pandas as pd
import streamlit as st
import joblib

model = joblib.load('model.pkl')


def preprocessing(inp):
    lis = []
    for item in inp:
        if item in ['偏瘦', '无', '边缘规则', '无包膜外侵', '无点状强回声', '无基因突变', '小于等于1cm', '无中央区淋巴结转移', '<0.5',
                    '<=55']:
            lis.append(0)
        elif item in ['男', '正常', '有', '否', '非低回声', '<=1', '有基因突变', '1', '大于1cm小于等于2cm', '上极', '单侧',
                      '有中央区淋巴结转移', '>=0.5', '>55']:
            lis.append(1)
        elif item in ['女', '肥胖', '是', '低回声', '边缘不规则', '2', '大于2cm小于等于4cm', '中极/下极', '双侧']:
            lis.append(2)
        elif item in ['0', '>1', '包膜外侵', '点状强回声', '>=3', '大于4cm']:
            lis.append(3)
    return pd.DataFrame(lis)


with st.sidebar:
    with st.form("my_form", clear_on_submit=False):
        st.write("Forecast parameters")

        Sex_val = st.radio("性别", ('男', '女'))
        Age_val = st.radio("年龄", ('<=55', '>55'))
        BMI_val = st.selectbox("身体质量指数", ('偏瘦', '正常', '肥胖'))
        Diabetes_val = st.radio("有无糖尿病", ('无', '有'))
        CLT_val = st.radio("有无桥本氏甲状腺炎", ('无', '有'))
        Solid_val = st.radio("是否实性", ('否', '是'))
        Hypoechogenicity_val = st.radio("回声", ('非低回声', '低回声'))
        AT_val = st.radio("纵横比", ('<=1', '>1'))
        Irregular_shape_val = st.radio("边缘", ('边缘规则', '边缘不规则'))
        ETE_val = st.radio("包膜是否外侵", ('无包膜外侵', '包膜外侵'))
        Microcalcification_val = st.radio("有无点状强回声", ('无点状强回声', '点状强回声'))
        BRAF_val = st.radio("braf基因状况", ('无基因突变', '有基因突变'))
        Number_val = st.selectbox("瘤体数目", ('1', '2', '>=3'))
        Size_val = st.selectbox("瘤体直径", ('小于等于1cm', '大于1cm小于等于2cm',
                                         '大于2cm小于等于4cm', '大于4cm'))
        Location_val = st.radio("瘤体位置", ('上极', '中极/下极'))
        Bilaterality_val = st.radio("是否是双侧肿瘤", ('单侧', '双侧'))
        CLNM_val = st.radio("中央区淋巴结状况", ('无中央区淋巴结转移', '有中央区淋巴结转移'))
        CLNR_val = st.radio("中央区淋巴结转移比率", ('<0.5', '>=0.5'))

        submitted = st.form_submit_button("Submit")

st.title(
    'A machine learning-based predictive model for predicting  lateral lymph node metastasis in patients with '
    'papillary thyroid carcinoma')

if submitted:
    df = preprocessing([Sex_val, Age_val, BMI_val, Diabetes_val, CLT_val, Solid_val, Hypoechogenicity_val,
                        AT_val, Irregular_shape_val, ETE_val, Microcalcification_val, BRAF_val, Number_val,
                        Size_val, Location_val, Bilaterality_val, CLNM_val, CLNR_val])
    pred = model.predict_proba(df.T.values)
    if pred[:, 1][0] <= 0.5:
        st.header('Risk grouping for LNM: High Risk Probability of LNM: {}%'.format(round(pred[:, 1][0]*100, 2)))
    elif pred[:, 1][0] > 0.5:
        st.header('Risk grouping for LNM: High Risk Probability of LNM: {}%'.format(round(pred[:, 1][0]*100, 2)))
