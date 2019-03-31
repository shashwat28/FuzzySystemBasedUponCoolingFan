# -*- coding: utf-8 -*-
"""
Created on Fri Mar  31 17:33:46 2019

@author: Shashwat
"""
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

x_qual = np.arange(0, 101, 1)
x_serv = np.arange(0, 101, 1)
x_tip  = np.arange(0, 101, 1)

temp_lo    = fuzz.trimf(x_qual, [0, 0, 50])
temp_md    = fuzz.trimf(x_qual, [0, 50, 100])
temp_hi    = fuzz.trimf(x_qual, [50, 100, 100])
hum_lo     = fuzz.trimf(x_serv, [0, 0, 50])
hum_md     = fuzz.trimf(x_serv, [0, 50, 100])
hum_hi     = fuzz.trimf(x_serv, [50, 100, 100])
speed_lo   = fuzz.trimf(x_tip, [0, 0, 25])
speed_md   = fuzz.trimf(x_tip, [0, 25, 50])
speed_hi   = fuzz.trimf(x_tip, [25, 50, 75])
speed_hig  = fuzz.trimf(x_tip, [50, 75, 100])
speed_high = fuzz.trimf(x_tip, [75, 100, 100])
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_qual, temp_lo, 'b', linewidth=1.5, label='low')
ax0.plot(x_qual, temp_md, 'g', linewidth=1.5, label='medium')
ax0.plot(x_qual, temp_hi, 'r', linewidth=1.5, label='high')
ax0.set_title('Temperature')
ax0.legend()

ax1.plot(x_serv, hum_lo, 'b', linewidth=1.5, label='low')
ax1.plot(x_serv, hum_md, 'g', linewidth=1.5, label='medium')
ax1.plot(x_serv, hum_hi, 'r', linewidth=1.5, label='high')
ax1.set_title('Humidity')
ax1.legend()

ax2.plot(x_tip, speed_lo, 'b', linewidth=1.5, label='Low')
ax2.plot(x_tip, speed_md, 'g', linewidth=1.5, label='Medium')
ax2.plot(x_tip, speed_hi, 'r', linewidth=1.5, label='High')
ax2.plot(x_tip, speed_hig, 'm', linewidth=1.5, label='more high')
ax2.plot(x_tip, speed_high, 'c', linewidth=1.5, label='highest')
ax2.set_title('Fan Speed')
ax2.legend()
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
tem=input("enter temp:")
hum=input("enter humidity:")
levt_lo = fuzz.interp_membership(x_qual, temp_lo, tem)
levt_md = fuzz.interp_membership(x_qual, temp_md, tem)
levt_hi = fuzz.interp_membership(x_qual, temp_hi, tem)

levh_lo = fuzz.interp_membership(x_serv, hum_lo, hum)
levh_md = fuzz.interp_membership(x_serv, hum_md, hum)
levh_hi = fuzz.interp_membership(x_serv, hum_hi, hum)

active_rule1 = np.fmax(levt_lo, levh_lo)
active_rule2 = np.fmax(levt_lo, levh_md)
active_rule3 = np.fmax(levt_lo, levh_hi)
active_rule4 = np.fmax(levt_md, levh_lo)
active_rule5 = np.fmax(levt_md, levh_md)
active_rule6 = np.fmax(levt_md, levh_hi)
active_rule7 = np.fmax(levt_hi, levh_lo)
active_rule8 = np.fmax(levt_hi, levh_md)
active_rule9 = np.fmax(levt_hi, levh_hi)

factive_rule1=np.fmin(active_rule1, speed_lo)
factive_rule2=np.fmin(active_rule2, speed_md)
factive_rule3=np.fmin(active_rule3, speed_md)
factive_rule4=np.fmin(active_rule4, speed_hi)
factive_rule5=np.fmin(active_rule5, speed_hi)
factive_rule6=np.fmin(active_rule6, speed_hig)
factive_rule7=np.fmin(active_rule7, speed_hig)
factive_rule8=np.fmin(active_rule8, speed_high)
factive_rule9=np.fmin(active_rule9, speed_high)

aggregated = np.fmax(factive_rule1,
                     np.fmax(factive_rule2,
                             np.fmax(factive_rule3,
                                     np.fmax(factive_rule4,
                                             np.fmax(factive_rule5,
                                                     np.fmax(factive_rule6,
                                                             np.fmax(factive_rule7,
                                                                     np.fmax(factive_rule8,factive_rule9))))))))

output_specifier=['low speed','medium speed','medium speed','high speed','high speed','more high speed','more high speed','highest speed','highest speed']
possible_aggregate=[active_rule1,active_rule2,active_rule3,active_rule4,active_rule5,active_rule6,active_rule7,active_rule8,active_rule9]
print(possible_aggregate)
aggregate = np.argwhere(possible_aggregate == np.amax(possible_aggregate))
aggregate = aggregate.flatten().tolist()
print("Possible values:-")
for i in range(len(aggregate)):
    print(output_specifier[aggregate[i]])

final_speed = fuzz.defuzz(x_tip, aggregated, 'centroid')
print("resultant fan speed : ",final_speed)
