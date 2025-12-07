import csv  
import random  
import numpy as np  
  
def sample_vital(lo, hi, sigma=0.0):  
    return round(random.uniform(lo, hi) + np.random.randn()*sigma, 1)  
  
def sample_pair(lo, hi, sigma=0.0):  
    return (sample_vital(lo, hi, sigma), sample_vital(lo, hi, sigma))  
  
def generate_record(pid):  
    # 1) Demographics  
    # gender: one-hot [F, M, Other]  
    gender = random.choices(  
        [(1,0,0),(0,1,0),(0,0,1)],  
        weights=[0.48,0.48,0.04]  
    )[0]  
    age = random.randint(20, 90)  
    # ethnicity: 6 categories  
    eth = random.choices(  
        [(1,0,0,0,0,0),(0,1,0,0,0,0),(0,0,1,0,0,0),  
         (0,0,0,1,0,0),(0,0,0,0,1,0),(0,0,0,0,0,1)],  
        weights=[0.5,0.2,0.15,0.1,0.03,0.02]  
    )[0]  
  
    # 2) Vitals / labs  
    # Base vitals  
    temp1, temp2 = sample_pair(36.5,37.5,0.1)  
    hr1, hr2     = sample_pair(60,100,5)  
    rr1, rr2     = sample_pair(12,22,2)  
    # Pressures  
    if age>65:  
        sbp_lo, sbp_hi = 110,160  
        dbp_lo, dbp_hi = 60,90  
        cr_lo, cr_hi   = 0.9,1.8  
        alb_lo,alb_hi  = 2.5,3.5  
    else:  
        sbp_lo, sbp_hi = 90,140  
        dbp_lo, dbp_hi = 55,85  
        cr_lo, cr_hi   = 0.6,1.2  
        alb_lo,alb_hi  = 3.0,4.5  
  
    sysS1, sysS2 = sample_pair(sbp_lo, sbp_hi, 5)  
    sysD1, sysD2 = sample_pair(dbp_lo, dbp_hi, 5)  
    sysM1 = round((sysS1 + 2*sysD1)/3.,1)  
    sysM2 = round((sysS2 + 2*sysD2)/3.,1)  
  
    paS1, paS2 = sample_pair(25,40,2)  
    paD1, paD2 = sample_pair(10,25,2)  
    paM1 = round((paS1 + 2*paD1)/3.,1)  
    paM2 = round((paS2 + 2*paD2)/3.,1)  
  
    sao21, sao22 = sample_pair(90,100,2)  
    # repeat temperature as “temp” per schema  
    temp3, temp4 = sample_pair(36.5,37.5,0.1)  
    # labs  
    be1, be2       = sample_pair(-2,2,0.5)  
    ca1, ca2       = sample_pair(8.4,10.2,0.2)  
    pao21, pao22   = sample_pair(80,100,5)  
    paco21, paco22 = sample_pair(35,45,3)  
    co21, co22     = sample_pair(20,30,2)  
    alb1, alb2     = sample_pair(alb_lo,alb_hi,0.3)  
    bun1, bun2     = sample_pair(8,25,3)  
    bic1, bic2     = sample_pair(20,28,2)  
    bil1, bil2     = sample_pair(0.2,1.5,0.3)  
    cr1  = round(random.uniform(cr_lo,cr_hi),2)  
    cr2  = round(random.uniform(cr_lo,cr_hi),2)  
    lac1, lac2     = sample_pair(0.5,3.0,0.5)  
    plt1, plt2     = sample_pair(150,400,50)  
    k1, k2         = sample_pair(3.5,5.0,0.2)  
    na1, na2       = sample_pair(135,145,2)  
    wbc1, wbc2     = sample_pair(4,12,2)  
  
    # 3) Outcome/stays  
    sbp_f = int(sysS1)  
    sbp_l = int(sysS2)  
    urine1 = random.randint(200,2000)  
    urine2 = urine1 + random.randint(-200,200)  
    mortality = int(age>80 and random.random()<0.3)  # older have slightly higher risk  
  
    return [  
        pid,  
        *gender,  
        age,  
        *eth,  
        temp1, temp2,  
        hr1, hr2,  
        rr1, rr2,  
        sysS1, sysS2,  
        sysD1, sysD2,  
        sysM1, sysM2,  
        paS1, paS2,  
        paD1, paD2,  
        paM1, paM2,  
        sao21, sao22,  
        temp3, temp4,  
        be1, be2,  
        ca1, ca2,  
        pao21, pao22,  
        paco21, paco22,  
        co21, co22,  
        alb1, alb2,  
        bun1, bun2,  
        bic1, bic2,  
        bil1, bil2,  
        cr1, cr2,  
        lac1, lac2,  
        plt1, plt2,  
        k1, k2,  
        na1, na2,  
        wbc1, wbc2,  
        sbp_f, sbp_l,  
        urine1, urine2,  
        mortality  
    ]  
  
# Column header  
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
    "sbp_first","sbp_last",  
    "urine_first","urine_last",  
    "mortality0"  
]  
  
writer = csv.writer(open("synthetic_100_more.csv","w", newline=""))  
writer.writerow(header)  
  
for pid in range(300011, 300111):  
    writer.writerow(generate_record(pid))  
  
print("100 synthetic records written to synthetic_100_more.csv")  