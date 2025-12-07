import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Schema based on your header
cols = [
    'patientunitstay','gender0','gender1','gender2','age','ethnicity0','ethnicity1','ethnicity2',
    'ethnicity3','ethnicity4','ethnicity5','temperature_first', 'temperature_last', 'heartrate_first', 'heartrate_last', 'respiration_first', 'respiration_last',
    'systemicsystolic_first','systemicsystolic_last','systemicdiastolic_first','systemicdiastolic_last','systemicmean_first','systemicmean_last','pasystolic_first','pasystolic_last',
    'padiastolic_first','padiastolic_last','pamean_first','pamean_last','sao2_first','sao2_last','temp_first','temp_last','base_excess_first','base_excess_last',
    'calcium_first','calcium_last','pao2_first','pao2_last','paco2_first','paco2_last','co2_first','co2_last','alb_first','alb_last','bun_first','bun_last','bicarb_first','bicarb_last',
    'bilirubin_first','bilirubin_last','creatinine_first','creatinine_last','lactate_first','lactate_last','platelet_first','platelet_last','potassium_first','potassium_last',
    'sodium_first','sodium_last','wbc_first','wbc_last','hr_first','hr_last','sbp_first','sbp_last','dbp_first','dbp_last','mbp_first','mbp_last','rsp_first','rsp_last','sap_first','sap_last','urine_first','urine_last','mortality0'
]

def sample_ethnicity():
    one_hot = np.zeros(6)
    idx = np.random.choice(6, p=[0.70,0.10,0.10,0.04,0.03,0.03])
    one_hot[idx] = 1.0
    return one_hot.tolist()

def sample_gender():
    probs = [0.48, 0.50, 0.02] # based on typical ICU distributions
    idx = np.random.choice(3, p=probs)
    one_hot = [0.0, 0.0, 0.0]
    one_hot[idx] = 1.0
    return one_hot

data = []
for i in range(1000):
    row = []
    # patientunitstay
    row.append(250000 + i)
    # Genders
    gender_vec = sample_gender()
    row.extend(gender_vec)
    # Age, conditionally
    if gender_vec[0] == 1.0:  # female
        age = np.clip(np.random.normal(68, 15), 18, 96)
    elif gender_vec[1] == 1.0: # male
        age = np.clip(np.random.normal(65, 16), 18, 98)
    else:
        age = np.clip(np.random.normal(60, 20), 18, 95)
    age = np.round(age, 0)
    row.append(age)
    # Ethnicity
    row.extend(sample_ethnicity())

    # Temperature First & Last (conditional drift)
    temp1 = np.round(np.random.normal(36.6, 0.5), 1)
    temp2 = np.round(temp1 + np.random.normal(0, 0.3), 1)
    row.append(temp1)
    row.append(temp2)

    # Heart rate – first (+age dep)
    hr_base = 77 - ((age-60)*0.07) # lower for older
    hr1 = np.round(np.clip(np.random.normal(hr_base, 10), 45, 140),1)
    hr2 = np.round(hr1 + np.random.normal(0, 8),1)
    row.append(hr1)
    row.append(hr2)

    # Respiration
    resp_base = 16 + ((age-70)*0.05)
    resp1 = np.round(np.clip(np.random.normal(resp_base, 3), 10, 35), 1)
    resp2 = np.round(resp1 + np.random.normal(0, 2), 1)
    row.append(resp1)
    row.append(resp2)

    # Systolic/diastolic/mean blood pressures (with plausible drift)
    sys1 = np.round(np.random.normal(125, 22), 1)
    sys2 = np.round(sys1 + np.random.normal(0,9),1) if np.random.rand() > 0.5 else np.nan
    dia1 = np.round(np.random.normal(67, 11), 1)
    dia2 = np.round(dia1 + np.random.normal(0,5),1) if np.random.rand() > 0.5 else np.nan
    mean1 = np.round(sys1*0.4 + dia1*0.6, 1)
    mean2 = np.round(mean1 + np.random.normal(0,6),1) if sys2==sys2 and dia2==dia2 else np.nan
    row.extend([sys1, sys2, dia1, dia2, mean1, mean2])

    # Pulmonary artery pressures
    pa_sys1 = np.round(np.random.normal(27, 7),1) if np.random.rand() < 0.1 else np.nan
    pa_sys2 = np.round(pa_sys1 + np.random.normal(0,5),1) if pa_sys1==pa_sys1 else np.nan
    pa_dia1 = np.round(pa_sys1/2,1) if pa_sys1==pa_sys1 else np.nan
    pa_dia2 = np.round(pa_dia1 + np.random.normal(0,2),1) if pa_dia1==pa_dia1 else np.nan
    pa_mean1 = np.round((pa_sys1+pa_dia1*2)/3,1) if pa_sys1==pa_sys1 and pa_dia1==pa_dia1 else np.nan
    pa_mean2 = pa_mean1 + np.random.normal(0,2) if pa_mean1==pa_mean1 else np.nan
    row.extend([pa_sys1,pa_sys2,pa_dia1,pa_dia2,pa_mean1,pa_mean2])
    
    # sao2_first/last
    sao2_1 = np.round(np.random.normal(97, 2),1)
    sao2_2 = np.round(sao2_1 + np.random.normal(0, 1),1)
    row.append(sao2_1)
    row.append(sao2_2)

    # temp_first/temp_last (likely duplicate with temperature?)
    row.append(temp1+np.random.normal(0,0.1))
    row.append(temp2+np.random.normal(0,0.1))

    # base_excess_first/last
    be1 = np.round(np.random.normal(0, 2),1)
    be2 = np.round(be1 + np.random.normal(0,1),1)
    row.append(be1)
    row.append(be2)

    # Calcium
    ca1 = np.round(np.random.normal(2.3,0.15),2)
    ca2 = np.round(ca1 + np.random.normal(0,0.08),2)
    row.append(ca1)
    row.append(ca2)

    # pao2/paco2/co2
    pao2_1 = np.round(np.clip(np.random.normal(90, 22), 40, 200),1)
    pao2_2 = np.round(pao2_1 + np.random.normal(0,10),1)
    paco2_1 = np.round(np.clip(np.random.normal(38,7),22,75),1)
    paco2_2 = np.round(paco2_1 + np.random.normal(0,3),1)
    co2_1 = np.round(paco2_1 + np.random.normal(1,3),1)
    co2_2 = np.round(co2_1 + np.random.normal(0,1),1)
    
    row.extend([pao2_1,pao2_2,paco2_1,paco2_2,co2_1,co2_2])

    # Albumin
    alb1 = np.round(np.clip(np.random.normal(3.7,0.4),2.6,5.3),2)
    alb2 = np.round(alb1 + np.random.normal(0,0.12),2)
    row.extend([alb1,alb2])

    # BUN, bicarb
    bun1 = np.round(np.clip(np.random.normal(20,7),4,56),1)
    bun2 = np.round(bun1 + np.random.normal(0,4),1)
    bicarb1 = np.round(np.clip(np.random.normal(25,3),14,36),1)
    bicarb2 = np.round(bicarb1 + np.random.normal(0,2),1)
    row.extend([bun1,bun2,bicarb1,bicarb2])

    # Bilirubin
    bili1 = np.round(np.clip(np.random.normal(0.8,0.7),0.2,6.2),2)
    bili2 = np.round(bili1 + np.random.normal(0,0.23),2)
    row.extend([bili1,bili2])

    # Creatinine
    cre1 = np.round(np.clip(np.random.normal(1.02,0.42),0.41,6.1),2)
    cre2 = np.round(cre1 + np.random.normal(0,0.11),2)
    row.extend([cre1, cre2])

    # Lactate
    l1 = np.round(np.clip(np.random.normal(1.6,0.7),0.4,7),2)
    l2 = np.round(l1 + np.random.normal(0,0.5),2)
    row.extend([l1,l2])

    # Platelets
    plat1 = np.round(np.clip(np.random.normal(210,65),15,550),1)
    plat2 = np.round(plat1 + np.random.normal(0,19),1)
    row.extend([plat1,plat2])

    # Potassium
    k1 = np.round(np.clip(np.random.normal(4.1,0.5),2.6,6.2),2)
    k2 = np.round(k1 + np.random.normal(0,0.12),2)
    row.extend([k1,k2])

    # Sodium
    na1 = np.round(np.clip(np.random.normal(139,3),129,155),1)
    na2 = np.round(na1 + np.random.normal(0,1),1)
    row.extend([na1,na2])

    # WBC
    wbc1 = np.round(np.clip(np.random.normal(8.2,2.6),2.2,35),1)
    wbc2 = np.round(wbc1 + np.random.normal(0,2),1)
    row.extend([wbc1,wbc2])

    # hr/sbp/dbp/mbp/rsp/sap/urine (duplicates, can add with drift/new samples as needed)
    # They appear to be duplicate/overlapping - for brevity, fill NAs or resample:
    row.extend([np.nan]*18)

    # mortality0 (random, 10% ICU mortality)
    mortality = float(np.random.rand() < 0.10)
    row.append(mortality)

    data.append(row)

df = pd.DataFrame(data, columns=cols)
df.to_csv('synthetic_ehr_1000.csv', index=False)
print("SYNTHETIC EHR generated as 'synthetic_ehr_1000.csv'!")