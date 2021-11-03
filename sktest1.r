library(Skillings.Mack)

mon=read.csv('mon_ary.txt')
tue=read.csv('tue_ary.txt')
wed=read.csv('wed_ary.txt')
thu=read.csv('thu_ary.txt')
fri=read.csv('fri_ary.txt')

df=cbind(mon,tue,wed,thu,fri)
colnames(df)=c('mon','tue','wed','thu','fri')
df.t=t(df)
result=Ski.Mack(df.t)
result$adjustedSum
result$varCovarMatrix
# p-value = 8e-6
# 统计量statistic = 29.08
# covariance matrix
#      [,1]  [,2]  [,3]  [,4]  [,5]
#[1,]  5638 -1436 -1418 -1400 -1384
#[2,] -1436  5744 -1455 -1436 -1417
#[3,] -1418 -1455  5752 -1449 -1430
#[4,] -1400 -1436 -1449  5729 -1444
#[5,] -1384 -1417 -1430 -1444  5675
# adjusted sum
#            [,1]        [,2]         [,3]         [,4]        [,5]               
#[1,] 214.4152105 44.76001373 -36.15830105 -369.5651881 146.5482649
