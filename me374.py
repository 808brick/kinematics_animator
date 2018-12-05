# Author:   Raymond Andrade
# Email:	ra2439@hawaii.edu
# Date:     12/2/2018
# Program:  4-bar linkage classifier and animator
# For:      ME 374 - Kinematics and Dynamics of Machinery

from math import pi as pi
from math import cos as cos
from math import sin as sin
from math import atan as atan
from math import sqrt as sqrt
from math import acos as acos
from math import radians as radians

import matplotlib.pyplot as plt

## Begin User Prompts
print(chr(27) + "[2J")

print("Enter value for the linkages: \n")

L0 = input("Link 0:  ")
L1 = input("Link 1:  ")
L2 = input("Link 2:  ")
L3 = input("Link 3:  ")

# Convert all inputs to floats, program will crash if non number value is entered 
L0 = float(L0)
L1 = float(L1)
L2 = float(L2)
L3 = float(L3)


# Prompt to check if user put in correct values
print(chr(27) + "[2J")
print("L0 = ", L0, "L1 = ", L1, "L2 = ", L2, "L3 = ", L3)
print("Are these the correct values you want to calculate? (y/n)")
indicator = input()

if indicator != "y" or indicator != "Y":
	assert("Restart the program and enter the correct values")

# Create list of all link lengths, find max and min links
link_list = [L0,L1,L2,L3]

max_link = max(link_list)

min_link = min(link_list)

link_list_without_max = link_list.copy()
link_list_without_max.remove(max_link)

# If not a Grashof Mechanism, kill program)
assert max_link < sum(link_list_without_max), "Not a mechanism"

link_list_without_max_and_min = link_list_without_max.copy()
link_list_without_max_and_min.remove(min_link)

# Classify mechanism based on lengths
if max_link + min_link > sum(link_list_without_max_and_min):
	print("Triple Rocker, Non-Grashof") 
	mechanism = "triple rocker"

elif max_link + min_link == sum(link_list_without_max_and_min):
	print("Mechanism is a Change Points")
	mechanism = "change points"

elif link_list[1] == min_link or link_list[3] == min_link:
	print("Mechanism is a Crank Rocker")
	mechanism = "crank rocker"

elif link_list[2] == min_link:
	print("Mechanism is a Double Rocker")
	mechanism = "double rocker"

else:
	print("Mechanism is a Drag Link")
	mechanism = "drag link"

## Calculate Position of Links
def solve_mechanism(theta):
	dont_plot = False
	theta = radians(theta) #Convert degrees to radians
	r0 =[[0,0],[L0,0]]
	r1x = L1 * cos(theta)
	r1y = L1 * sin(theta)
	r1 = [[0,0],[r1x,r1y]]

	rd = sqrt((r0[1][0]-r1x)**2 + (r0[1][1] - r1y)**2)
	sin_theta_d = r1y/rd
	cos_theta_d = (-1*L0+r1x) / rd

	if sin_theta_d == 0 or sin_theta_d == radians(180):
		theta_d = 0
	else:
		theta_d = 2*atan((1 - cos_theta_d) / sin_theta_d)

	phi_b_calc = (L3**2-L2**2-rd**2)/(2*rd*L2)
	if phi_b_calc < -1:
		while phi_b_calc < -1:
			phi_b_calc += 1
		phi_b = acos(phi_b_calc) + pi/2
	elif phi_b_calc > 1:
		while phi_b_calc > 1:
			phi_b_calc -= 1
		phi_b = acos(phi_b_calc) + pi/2
	else:
		phi_b=acos(phi_b_calc)


	theta2 = theta_d - phi_b
	r2=[[r1x,r1y],[L2*cos(theta2) + r1x,L2*sin(theta2) + r1y]]
	r3 = [[r2[1][0],r2[1][1]],[L0,0]]
	r3_magnitude = sqrt((r3[0][0] -r3[1][0])**2 +(r3[0][1] -r3[1][1])**2)
	r2_magnitude = sqrt((r2[0][0] -r2[1][0])**2 +(r2[0][1] -r2[1][1])**2)

	if r3_magnitude > L3 + L3 * 0.05 or r3_magnitude < L3 - L3*0.05:
		theta2 = theta_d + phi_b
		r2=[[r1x,r1y],[L2*cos(theta2) + r1x,L2*sin(theta2) + r1y]]
		r3 = [[r2[1][0],r2[1][1]],[L0,0]]
		r3_magnitude = sqrt((r3[0][0] -r3[1][0])**2 +(r3[0][1] -r3[1][1])**2)
		r2_magnitude = sqrt((r2[0][0] -r2[1][0])**2 +(r2[0][1] -r2[1][1])**2)

	# If r3_magnitude still does not match the value of L3, then the mechanism has reached it's limiting position. Stop plotting. 
	if r3_magnitude > L3 + L3 * 0.05 or r3_magnitude < L3 - L3*0.05:
		dont_plot = True

	return r0, r1, r2, r3, max_link, dont_plot

## Plotting
fig, ax = plt.subplots(figsize=(9, 8))
ax.set_title(mechanism)
ax = fig.add_axes([0.04, 0.04, 0.94, 0.90])

# will rotate 360 degrees 4 times (360 * 4) in increments of 4 degrees.
for i in range(0,360*4, 4): 
	ax.cla()
	ax.title.set_text(mechanism)
	r0, r1, r2, r3, max_link, dont_plot = solve_mechanism(i)
	if dont_plot == False:
		ax.axis('equal')
		ax.set_xlim([-1* max_link, 1.5* max_link])
		ax.set_ylim([-1* max_link, 1.5* max_link])
		ax.plot([r0[0][0],r0[1][0]], [r0[0][1],r0[1][1]], 'black', linestyle='-')
		ax.plot([r1[0][0],r1[1][0]], [r1[0][1],r1[1][1]], 'black', linestyle='-')
		ax.plot([r2[0][0],r2[1][0]], [r2[0][1],r2[1][1]], 'black', linestyle='-')
		ax.plot([r3[0][0],r3[1][0]], [r3[0][1],r3[1][1]], 'black', linestyle='-')
		ax.plot([r0[1][0],r1[0][0],r2[0][0],r3[0][0]], [r0[1][1],r1[0][1],r2[0][1],r3[0][1]], 'bo', markersize=10)
		plt.pause(0.007)
