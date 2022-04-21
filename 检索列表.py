from  Market_baipan import Getbaipan

df=Getbaipan('HK.00700')
x=df['ask_price']!=348
# def tf(x):
#     if x.iloc[:5]== True:
#         return True
#
print(x)
print(x.iloc[:5].all()==False)
def test(x):
    if (x.iloc[:5].all()==False) == True:
        return True
    else:
        return False
print(test(x))