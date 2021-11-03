import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import kstest,anderson
from scipy.stats import friedmanchisquare
from rpy2.robjects.packages import importr
import rpy2.robjects as ro


df_full=pd.read_csv('000001.csv',usecols=[0,3,4,5,6,7,8,9],index_col='日期',
                header=0,encoding='ANSI',parse_dates=True)
# 选取1991-01-01至2020-12-31之间日数据,并计算对数收益率
df_full=df_full.iloc[::-1]                                  # 反转df
df_full=df_full['1991-01-01':'2020-12-31']                  # 选取30年数据
df_full['lgrtn']=np.log(df_full['收盘价']/df_full['前收盘'])  # 添加对数收益率
df_full['weekday']=df_full.index.weekday                    # 添加星期标志

df=df_full[['lgrtn','weekday']]              # 选取新的df，只包括日期索引.lgrtn.weekday
df.index.name=None                                          # 去除索引名字

# 对对数收益率进行正态分布检验
# 画图
sns.set_style('darkgrid')
plt.figure(figsize=(4,3))
sns.histplot(df,x='lgrtn',bins=200)
plt.show()
# qqplot
sm.qqplot(df['lgrtn'])
plt.show()
df.drop(index='1992-05-21',inplace=True)  # 去除异常值
# 重做qqplot
sm.qqplot(df['lgrtn'],line='s')
plt.show()                                # 非正态分布

# 检验数据正态性
anderson(df['lgrtn'])              # 拒绝原假设，不服从正太
kstest(df['lgrtn'],'norm')         # 同上

# 去除不完整数据周，保留balanced data，做Friedman test
for i in range(3):                 # 删除前三行不完整数据
    df.drop(index=df.index[0],inplace=True)
i=0
tdelta=df.index[5]-df.index[0]     # 一周的timedelta
while i < (df.shape[0]-5):         # 当5期之后数据不是0或者不是一周之后，则删除
    while df['weekday'].iloc[i+5]!=0 or df.index[i+5]-df.index[i]!= tdelta:
        df.drop(index=df.index[i],inplace=True)
    i+=5
for i in range(4):                 # 删除最后4个不完整数据
    df.drop(index=df.index[-1],inplace=True)

df_1=df[df['weekday']==0]         # 分类
df_rtn1=np.array(df_1['lgrtn'])
df_2=df[df['weekday']==1]
df_rtn2=np.array(df_2['lgrtn'])
df_3=df[df['weekday']==2]
df_rtn3=np.array(df_2['lgrtn'])
df_4=df[df['weekday']==3]
df_rtn4=np.array(df_4['lgrtn'])
df_5=df[df['weekday']==4]
df_rtn5=np.array(df_5['lgrtn'])
# friedman test 结果显示存在星期效应
# 正确
friedmanchisquare(df_rtn1,df_rtn2,df_rtn3,df_rtn4,df_rtn5)



# skillings-mack test
# 分类unbalanced data
mon_index=pd.date_range(start='1991-01-05',end='2020-12-27',freq='W-MON')
df_mon=pd.DataFrame(df_full['lgrtn'],index=mon_index)
tue_index=pd.date_range(start='1991-01-05',end='2020-12-27',freq='W-TUE')
df_tue=pd.DataFrame(df_full['lgrtn'],index=tue_index)
wed_index=pd.date_range(start='1991-01-05',end='2020-12-27',freq='W-WED')
df_wed=pd.DataFrame(df_full['lgrtn'],index=wed_index)
thu_index=pd.date_range(start='1991-01-05',end='2020-12-27',freq='W-THU')
df_thu=pd.DataFrame(df_full['lgrtn'],index=thu_index)
fri_index=pd.date_range(start='1991-01-05',end='2020-12-27',freq='W-FRI')
df_fri=pd.DataFrame(df_full['lgrtn'],index=fri_index)

# 转换为array
mon_ary=np.array(df_mon['lgrtn'])
tue_ary=np.array(df_tue['lgrtn'])
wed_ary=np.array(df_wed['lgrtn'])
thu_ary=np.array(df_thu['lgrtn'])
fri_ary=np.array(df_fri['lgrtn'])

# 保存为csv在R中继续使用skllingsmack检验
np.savetxt('mon_ary.txt',mon_ary)
np.savetxt('tue_ary.txt',tue_ary)
np.savetxt('wed_ary.txt',wed_ary)
np.savetxt('thu_ary.txt',thu_ary)
np.savetxt('fri_ary.txt',fri_ary)



