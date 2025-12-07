import csv  
import random  
  
def one_hot(idx, length):  
    v = [0]*length  
    v[idx] = 1  
    return v  
  
def rand_float(low, high, dp=1):  
    return round(random.uniform(low, high), dp)  
  
def rand_int(low, high):  
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
  
writer = csv.writer(open("synthetic_eicu_100more.csv","w", newline=""))  
writer.writerow(header)  
  
start_id = 210012  
for i in range(100):  
    pid = start_id + i  
  
    # 1. gender  
    gender = one_hot(random.randrange(3), 3)  
    # 2. age 18–90  
    age = rand_int(18, 90)  
    # 3. ethnicity  
    ethnicity = one_hot(random.randrange(6), 6)  
  
    # 4. Vitals: temp (36.0–38.5), hr (50–110), resp (12–25)  
    t1, t2 = rand_float(36.0, 38.5), rand_float(36.0, 38.5)  
    hr1, hr2 = rand_int(50, 110), rand_int(50, 110)  
    rsp1, rsp2 = rand_int(12, 25), rand_int(12, 25)  
  
    # 5. Systemic BP  
    sys_s1, sys_s2 = rand_int(90, 160), rand_int(90, 160)  
    sys_d1, sys_d2 = rand_int(50, 95), rand_int(50, 95)  
    sys_m1 = round((sys_s1 + 2*sys_d1)/3)  
    sys_m2 = round((sys_s2 + 2*sys_d2)/3)  
  
    # 6. Pulmonary pressures  
    pas1, pas2 = sys_s1 + rand_int(-10, 10), sys_s2 + rand_int(-10, 10)  
    pad1, pad2 = sys_d1 + rand_int(-5, 5), sys_d2 + rand_int(-5, 5)  
    pam1 = round((pas1 + 2*pad1)/3)  
    pam2 = round((pas2 + 2*pad2)/3)  
  
    # 7. Sao2  
    sao1, sao2 = rand_int(88, 100), rand_int(88, 100)  
    # 8. Repeat temp  
    tb1, tb2 = rand_float(36.0, 38.5), rand_float(36.0, 38.5)  
    # 9. Base excess  
    be1, be2 = rand_float(-5.0, 5.0), rand_float(-5.0, 5.0)  
    # 10. Calcium  
    ca1, ca2 = rand_float(8.0, 10.5), rand_float(8.0, 10.5)  
    # 11. Blood gases  
    pao1, pao2 = rand_int(60, 120), rand_int(60, 120)  
    pac1, pac2 = rand_int(30, 50), rand_int(30, 50)  
    co21, co22 = rand_int(20, 50), rand_int(20, 50)  
    # 12. Albumin, BUN  
    alb1, alb2 = rand_float(2.5, 4.5), rand_float(2.5, 4.5)  
    bun1, bun2 = rand_int(8, 30), rand_int(8, 30)  
    # 13. Bicarb  
    bic1, bic2 = rand_int(18, 28), rand_int(18, 28)  
    # 14. Bilirubin  
    bil1, bil2 = rand_float(0.3, 2.5), rand_float(0.3, 2.5)  
    # 15. Creatinine  
    cr1, cr2 = rand_float(0.5, 2.5), rand_float(0.5, 2.5)  
    # 16. Lactate  
    lac1, lac2 = rand_float(0.5, 5.0), rand_float(0.5, 5.0)  
    # 17. Platelets  
    plt1, plt2 = rand_int(100, 400), rand_int(100, 400)  
    # 18. Electrolytes  
    k1, k2 = rand_float(3.0, 5.5), rand_float(3.0, 5.5)  
    na1, na2 = rand_int(130, 150), rand_int(130, 150)  
    # 19. WBC  
    wbc1, wbc2 = rand_int(3, 15), rand_int(3, 15)  
  
    # 20. Secondary HR, BP, etc.  
    hr1b, hr2b = rand_int(50, 110), rand_int(50, 110)  
    sbp1b, sbp2b = rand_int(90, 160), rand_int(90, 160)  
    dbp1b, dbp2b = rand_int(50, 95), rand_int(50, 95)  
    mbp1b = round((sbp1b + 2*dbp1b)/3)  
    mbp2b = round((sbp2b + 2*dbp2b)/3)  
    rsp1b, rsp2b = rand_int(12, 25), rand_int(12, 25)  
    sap1b, sap2b = rand_int(80, 140), rand_int(80, 140)  
    urine1, urine2 = rand_int(200, 3000), rand_int(200, 3000)  
  
    # 21. Mortality  
    mortality = 1 if random.random() < 0.1 else 0  
  
    row = [  
        pid,  
        *gender,  
        age,  
        *ethnicity,  
        t1, t2,  
        hr1, hr2,  
        rsp1, rsp2,  
        sys_s1, sys_s2,  
        sys_d1, sys_d2,  
        sys_m1, sys_m2,  
        pas1, pas2,  
        pad1, pad2,  
        pam1, pam2,  
        sao1, sao2,  
        tb1, tb2,  
        be1, be2,  
        ca1, ca2,  
        pao1, pao2,  
        pac1, pac2,  
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
        hr1b, hr2b,  
        sbp1b, sbp2b,  
        dbp1b, dbp2b,  
        mbp1b, mbp2b,  
        rsp1b, rsp2b,  
        sap1b, sap2b,  
        urine1, urine2,  
        mortality  
    ]  
    writer.writerow(row)  
  
print("Wrote 100 synthetic records to synthetic_eicu_100more.csv") 