import csv  
import random  
  
def one_hot(n_classes):  
    v = [0]*n_classes  
    v[random.randrange(n_classes)] = 1  
    return v  
  
def rnd_float(low, high, decimals=1):  
    return round(random.uniform(low, high), decimals)  
  
def rnd_int(low, high):  
    return random.randint(low, high)  
  
header = [  
    "patientunitstay",  
    "gender0","gender1","gender2",  
    "age",  
    "ethnicity0","ethnicity1","ethnicity2","ethnicity3","ethnicity4","ethnicity5",  
    "temperature_first","temperature_last",  
    "heartrate_first","heartrate_last",  
    "respiration_first","respiration_last",  
    "systemicsystolic_first","systemicsystolic_last",  
    "systemicdiastolic_first","systemicdiastolic_last",  
    "systemicmean_first","systemicmean_last",  
    "pasystolic_first","pasystolic_last",  
    "padiastolic_first","padiastolic_last",  
    "pamean_first","pamean_last",  
    "sao2_first","sao2_last",  
    "temp_first","temp_last",  
    "base_excess_first","base_excess_last",  
    "calcium_first","calcium_last",  
    "pao2_first","pao2_last",  
    "paco2_first","paco2_last",  
    "co2_first","co2_last",  
    "alb_first","alb_last",  
    "bun_first","bun_last",  
    "bicarb_first","bicarb_last",  
    "bilirubin_first","bilirubin_last",  
    "creatinine_first","creatinine_last",  
    "lactate_first","lactate_last",  
    "platelet_first","platelet_last",  
    "potassium_first","potassium_last",  
    "sodium_first","sodium_last",  
    "wbc_first","wbc_last",  
    "hr_first","hr_last",  
    "sbp_first","sbp_last",  
    "dbp_first","dbp_last",  
    "mbp_first","mbp_last",  
    "rsp_first","rsp_last",  
    "sap_first","sap_last",  
    "urine_first","urine_last",  
    "mortality0"  
]  
  
writer = csv.writer(open("synthetic_eicu_100.csv","w", newline=""))  
writer.writerow(header)  
  
start_id = 300011  
for i in range(100):  
    pid = start_id + i  
    gender = one_hot(3)  
    age = rnd_int(18, 90)  
    ethnicity = one_hot(6)  
    temp1, temp2 = rnd_float(36.0, 38.5,1), rnd_float(36.0, 38.5,1)  
    hr1, hr2 = rnd_int(60,110), rnd_int(60,110)  
    resp1, resp2 = rnd_int(12,25), rnd_int(12,25)  
    sys_s1, sys_s2 = rnd_int(100,150), rnd_int(100,150)  
    sys_d1, sys_d2 = rnd_int(60, 95), rnd_int(60, 95)  
    sys_m1 = round((sys_s1 + 2*sys_d1)/3)  
    sys_m2 = round((sys_s2 + 2*sys_d2)/3)  
    pas1, pas2 = rnd_int(100,160), rnd_int(100,160)  
    pad1, pad2 = rnd_int(60,100), rnd_int(60,100)  
    pam1 = round((pas1 + 2*pad1)/3)  
    pam2 = round((pas2 + 2*pad2)/3)  
    sao1, sao2 = rnd_int(90,100), rnd_int(90,100)  
    t1, t2 = rnd_float(36.0, 38.5,1), rnd_float(36.0, 38.5,1)  
    be1, be2 = rnd_float(-5.0,5.0,1), rnd_float(-5.0,5.0,1)  
    ca1, ca2 = rnd_float(8.0,10.5,1), rnd_float(8.0,10.5,1)  
    pao1, pao2 = rnd_int(60,120), rnd_int(60,120)  
    pac1, pac2 = rnd_int(30,50), rnd_int(30,50)  
    co21, co22 = rnd_int(20,50), rnd_int(20,50)  
    alb1, alb2 = rnd_float(2.5,4.5,1), rnd_float(2.5,4.5,1)  
    bun1, bun2 = rnd_int(10,30), rnd_int(10,30)  
    bic1, bic2 = rnd_int(20,28), rnd_int(20,28)  
    bil1, bil2 = rnd_float(0.5,2.0,1), rnd_float(0.5,2.0,1)  
    cr1, cr2 = rnd_float(0.6,2.0,1), rnd_float(0.6,2.0,1)  
    lac1, lac2 = rnd_float(0.5,4.0,1), rnd_float(0.5,4.0,1)  
    plt1, plt2 = rnd_int(150,350), rnd_int(150,350)  
    k1, k2 = rnd_float(3.5,5.0,1), rnd_float(3.5,5.0,1)  
    na1, na2 = rnd_int(135,145), rnd_int(135,145)  
    wbc1, wbc2 = rnd_int(4,12), rnd_int(4,12)  
    hr1b, hr2b = rnd_int(60,110), rnd_int(60,110)  
    sbp1b, sbp2b = rnd_int(100,150), rnd_int(100,150)  
    dbp1b, dbp2b = rnd_int(60,95), rnd_int(60,95)  
    mbp1b = round((sbp1b + 2*dbp1b)/3)  
    mbp2b = round((sbp2b + 2*dbp2b)/3)  
    rsp1b, rsp2b = rnd_int(12,25), rnd_int(12,25)  
    sap1b, sap2b = rnd_int(90,140), rnd_int(90,140)  
    urine1, urine2 = rnd_int(500,2000), rnd_int(500,2000)  
    mortality = 1 if random.random()<0.10 else 0  
  
    row = (  
        [pid] +  
        gender +  
        [age] +  
        ethnicity +  
        [temp1,temp2,hr1,hr2,resp1,resp2,  
         sys_s1,sys_s2,sys_d1,sys_d2,sys_m1,sys_m2,  
         pas1,pas2,pad1,pad2,pam1,pam2,  
         sao1,sao2,t1,t2,be1,be2,ca1,ca2,  
         pao1,pao2,pac1,pac2,co21,co22,alb1,alb2,  
         bun1,bun2,bic1,bic2,bil1,bil2,cr1,cr2,  
         lac1,lac2,plt1,plt2,k1,k2,na1,na2,wbc1,wbc2,  
         hr1b,hr2b,sbp1b,sbp2b,dbp1b,dbp2b,mbp1b,mbp2b,  
         rsp1b,rsp2b,sap1b,sap2b,urine1,urine2,mortality]  
    )  
    writer.writerow(row)  
  
print("Generated synthetic_eicu_100.csv with 100 records.")  