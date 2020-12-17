"""
Rules:
IF Suhu Ruangan IS Rendah AND Kelembaban IS Rendah AND Jumlah Orang IS Sedikit  THEN Suhu Thermostat IS Sangat Tinggi
IF Suhu Ruangan IS Rendah AND Kelembaban IS Rendah AND Jumlah Orang IS Banyak   THEN Suhu Thermostat IS Tinggi
IF Suhu Ruangan IS Rendah AND Kelembaban IS Sedang                              THEN Suhu Thermostat IS Tinggi
IF Suhu Ruangan IS Rendah AND Kelembaban IS Tinggi                              THEN Suhu Thermostat IS Agak Tinggi
IF Suhu Ruangan IS Sedang AND Kelembaban IS Rendah AND Jumlah Orang IS Sedikit  THEN Suhu Thermostat IS Agak Sedang
IF Suhu Ruangan IS Sedang AND Kelembaban IS Rendah AND Jumlah Orang IS Banyak   THEN Suhu Thermostat IS Sedang
IF Suhu Ruangan IS Sedang AND Kelembaban IS Sedang                              THEN Suhu Thermostat IS Sangat Sedang
IF Suhu Ruangan IS Sedang AND Kelembaban IS Tinggi AND Jumlah Orang IS Sedikit  THEN Suhu Thermostat IS Sedang
IF Suhu Ruangan IS Sedang AND Kelembaban IS Tinggi AND Jumlah Orang IS Banyak   THEN Suhu Thermostat IS Agak Sedang
IF Suhu Ruangan IS Tinggi AND Kelembaban IS Rendah AND Jumlah Orang IS Sedikit  THEN Suhu Thermostat IS Agak Rendah
IF Suhu Ruangan IS Tinggi AND Kelembaban IS Rendah AND Jumlah Orang IS Banyak   THEN Suhu Thermostat IS Rendah
IF Suhu Ruangan IS Tinggi AND Kelembaban IS Sedang                              THEN Suhu Thermostat IS Rendah
IF Suhu Ruangan IS Tinggi AND Kelembaban IS Tinggi AND Jumlah Orang IS Sedikit  THEN Suhu Thermostat IS Rendah
IF Suhu Ruangan IS Tinggi AND Kelembaban IS Tinggi AND Jumlah Orang IS Banyak   THEN Suhu Thermostat IS Sangat Rendah

"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def sqrt(num):
    return num**0.5
    
def square(num):
    return num**2
    
# Generate semesta dari fuzzy set sebagai numpy array
suhu       = ctrl.Antecedent(np.arange(15, 36, 1), 'suhu')
lembab     = ctrl.Antecedent(np.arange(0, 101, 1), 'lembab')
orang      = ctrl.Antecedent(np.arange(0, 31, 1),  'orang')
thermostat = ctrl.Consequent(np.arange(15, 36, 1), 'thermostat')

#Generate nilai-nilai membership function dengan trimf untuk membuat triangular membership function
suhu['rendah']   = fuzz.trimf(suhu.universe,   [15, 15, 25])
suhu['sedang']   = fuzz.trimf(suhu.universe,   [23, 25, 29])
suhu['tinggi']   = fuzz.trimf(suhu.universe,   [27, 35, 36])
lembab['rendah'] = fuzz.trimf(lembab.universe, [0, 0, 41])
lembab['sedang'] = fuzz.trimf(lembab.universe, [35, 55, 76])
lembab['tinggi'] = fuzz.trimf(lembab.universe, [70, 100, 101])
orang['sedikit'] = fuzz.trimf(orang.universe,  [0, 0, 21])
orang['banyak']  = fuzz.trimf(orang.universe,  [10, 30, 31])
thermostat['agak rendah']   = np.array(list(map(sqrt,   fuzz.trimf(suhu.universe, [15, 15, 25]))))
thermostat['rendah']        =                           fuzz.trimf(suhu.universe, [15, 15, 25])
thermostat['sangat rendah'] = np.array(list(map(square, fuzz.trimf(suhu.universe, [15, 15, 25]))))
thermostat['agak sedang']   = np.array(list(map(sqrt,   fuzz.trimf(suhu.universe, [23, 26, 30]))))
thermostat['sedang']        =                           fuzz.trimf(suhu.universe, [23, 26, 30])
thermostat['sangat sedang'] = np.array(list(map(square, fuzz.trimf(suhu.universe, [23, 26, 30]))))
thermostat['agak tinggi']   = np.array(list(map(sqrt,   fuzz.trimf(suhu.universe, [27, 35, 36]))))
thermostat['tinggi']        =                           fuzz.trimf(suhu.universe, [27, 35, 36])
thermostat['sangat tinggi'] = np.array(list(map(square, fuzz.trimf(suhu.universe, [27, 35, 36]))))



# Buat list of fuzzy rules menggunakan ctrl.Rule
rulebase = [ctrl.Rule(suhu['rendah'] & lembab['rendah'] & orang['sedikit']  , thermostat['sangat tinggi']),
            ctrl.Rule(suhu['rendah'] & lembab['rendah'] & orang['banyak']   , thermostat['tinggi']),
            ctrl.Rule(suhu['rendah'] & lembab['sedang']                     , thermostat['tinggi']),
            ctrl.Rule(suhu['rendah'] & lembab['tinggi']                     , thermostat['agak tinggi']),
            ctrl.Rule(suhu['sedang'] & lembab['rendah'] & orang['sedikit']  , thermostat['agak sedang']),
            ctrl.Rule(suhu['sedang'] & lembab['rendah'] & orang['banyak']   , thermostat['sedang']),
            ctrl.Rule(suhu['sedang'] & lembab['sedang']                     , thermostat['sangat sedang']),
            ctrl.Rule(suhu['sedang'] & lembab['tinggi'] & orang['sedikit']  , thermostat['sedang']),
            ctrl.Rule(suhu['sedang'] & lembab['tinggi'] & orang['banyak']   , thermostat['agak sedang']),
            ctrl.Rule(suhu['tinggi'] & lembab['rendah'] & orang['sedikit']  , thermostat['agak rendah']),
            ctrl.Rule(suhu['tinggi'] & lembab['rendah'] & orang['banyak']   , thermostat['rendah']),
            ctrl.Rule(suhu['tinggi'] & lembab['sedang']                     , thermostat['rendah']),
            ctrl.Rule(suhu['tinggi'] & lembab['tinggi'] & orang['sedikit']  , thermostat['rendah']),
            ctrl.Rule(suhu['tinggi'] & lembab['tinggi'] & orang['banyak']   , thermostat['sangat rendah'])]


# Buat Control System untuk variabel Consequent dan Simulation-nya
thermostat_ctrl = ctrl.ControlSystem(rulebase)
thermostat_ctrl_sim = ctrl.ControlSystemSimulation(thermostat_ctrl)

# Terima input
inp_suhu = float(input('Suhu ruangan (15-35) : '))
inp_lembab = float(input('Kelembaban (0-100) : '))
inp_orang = float(input('Jumlah orang (0-30) : '))

# Masukkan input ke dalam simulation
thermostat_ctrl_sim.input['suhu'] = inp_suhu
thermostat_ctrl_sim.input['lembab'] = inp_lembab
thermostat_ctrl_sim.input['orang'] = inp_orang

# Lakukan perhitungan
thermostat_ctrl_sim.compute()

# Tampilkan nilai hasil defuzzifikasi (metode centroid)
print('Suhu thermostat : {:.2f}'.format(thermostat_ctrl_sim.output['thermostat']))
thermostat.view(sim = thermostat_ctrl_sim)
input('Tekan tombol apapun untuk keluar...')