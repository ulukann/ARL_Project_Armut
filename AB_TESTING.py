
#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################
# Facebook kısa süre önce mevcut "maximum bidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi ve averagebidding'in maximum bidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testiyapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.

#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna Average Biddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

#####################################################
# Proje Görevleri
#####################################################

#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.


import pandas as pd
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel("ABTesti-221114-234653",sheet_name="Control Group")
dataframe_test = pd.read_excel("ABTesti-221114-234653",sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)

df_control.describe([0, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]).T
df_test.describe([0, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]).T

pd.plotting.scatter_matrix(df_control)
plt.show()

pd.plotting.scatter_matrix(df_test)
plt.show()

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df_control["group"] = "control"
df_test["group"] = "test"
df_control.head()
df = pd.concat([df_control,df_test], axis=0,ignore_index=True)
df


for col in df.columns:
    sns.boxplot(x="group",y=col,hue="group",data=df)
    plt.show()

df.info()
#2.yol
df["grp"]=pd.Series()
df.loc[0:40, ['grp']] = "C"
df.loc[40::, ['grp']] = "T"

#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

# H0 : M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark yoktur.)
# H1 : M1!= M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark vardır.)

df_control["Purchase"].mean()
df_test["Purchase"].mean()

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

df.groupby("group").agg({"Purchase": "mean"})


#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

# Normallik Varsayımı :

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır
# p < 0.05 H0 RED
# p > 0.05 H0 REDDEDİLEMEZ
# Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ?
# Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.5891
# HO reddedilemez. Control grubunun değerleri normal dağılım varsayımını sağlamaktadır.
#2.yol
shapiro(df.loc[df.index[0:40],"Purchase"])

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# HO reddedilemez. Test grubunun değerleri normal dağılım varsayımını sağlamaktadır.


test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.1541
# HO reddedilemez. Control grubunun değerleri normal dağılım varsayımını sağlamaktadır.
#2.yol
shapiro(df.loc[df.index[40::],"Purchase"])

# Varyans Homojenliği :
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir.
# p < 0.05 H0 RED
# p > 0.05 H0 REDDEDİLEMEZ
# Kontrol ve test grubu için varyans homojenliğinin sağlanıp sağlanmadığını Purchase değişkeni üzerinden test ediniz.
# Test sonucuna göre normallik varsayımı sağlanıyor mu? Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.1083
# HO reddedilemez. Control ve Test grubunun değerleri varyans homejenliği varsayımını sağlamaktadır.
# Varyanslar Homojendir.
#2.yol
levene(df.loc[df.index[0:40], "Purchase"],
       df.loc[df.index[40::], "Purchase"])

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

# Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) yapılmaktadır.
# H0: M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark yoktur.)
# H1: M1 != M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark vardır)
# p<0.05 HO RED , p>0.05 HO REDDEDİLEMEZ

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Adım 3: Test sonucunda elde edilen p_valuedeğerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# p-value=0.3493
# HO reddedilemez. Kontrol ve test grubu satın alma ortalamaları arasında istatistiksel olarak anlamlı farklılık yoktur


##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.


# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
"""
def permutation_test(df, num_perm=50000):
    obs_diff = df.loc[df.group == "test"].Purchase.mean() - df.loc[df.group == "control"].Purchase.mean()
    num_of_control = df.loc[df.group == "control"].shape[0]

    poss_diffs = []
    for i in tqdm(range(num_perm)):
        control_index = df.sample(num_of_control).index.values
        test_index = set(df.index.values) - set(control_index)

        poss_diffs.append(df.loc[list(test_index)].Purchase.mean() - df.loc[list(control_index)].Purchase.mean())

    poss_diffs = np.array(poss_diffs)
    fig, ax = plt.subplots()
    sns.histplot(poss_diffs[poss_diffs < obs_diff], ax=ax)
    sns.histplot(poss_diffs[poss_diffs > obs_diff], ax=ax)
    ax.vlines(x=obs_diff, ymin=0, ymax=1200, colors="r")
    ax.annotate(text="Obs. Diff", xy=(obs_diff, 1000), xytext=(obs_diff*2, 1200),
                color="r", arrowprops={"width": 0.5, "color": "r", "headwidth": 5})

    ax.set_xlabel("Gruplar Arası Fark")
    ax.set_ylabel("Gözlem Sayısı")
    ax.set_title("Olası Farklar Simülasyonu")
    fig.set_size_inches(12, 12)
    return (poss_diffs > obs_diff).mean()

p_val_sim = permutation_test(df)
plt.show()
"""
