import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd

# GUI code
sg.theme('DarkGreen')

#excel code
EXCEL_FILE = '3-DOF ARTICULATED MANIPULATOR - Forward Kinematics.xlsx'
df = pd.read_excel(EXCEL_FILE)

#LAYOUT CODE
layout = [
    [sg.Text('Fll out the following fields: ')],
    [sg.Text('a1 ='), sg.InputText(key='a1', size=(20,10)), sg.Text('T1 ='), sg.InputText(key='T1', size=(20,10))],
    [sg.Text('a2 ='), sg.InputText(key='a2', size=(20,10)), sg.Text('T2 ='), sg.InputText(key='T2', size=(20,10))],
    [sg.Text('a3 ='), sg.InputText(key='a3', size=(20,10)), sg.Text('T3 ='), sg.InputText(key='T3', size=(20,10))],
    [sg.Button('Solve Forward Kinematics')],

    [sg.Frame('Position Vector: ',[[
        sg.Text('X ='), sg.InputText(key='X', size=(10,1)),
        sg.Text('Y ='), sg.InputText(key='Y', size=(10,1)),
        sg.Text('Z ='), sg.InputText(key='Z', size=(10,1))]])],

    [sg.Frame('H0_3 Transformation Matrix = ',[[
        sg.Output(size=(60,10))]])],

    [sg.Submit(), sg.Button('Clear Input'), sg.Exit()]
]
#window code
window = sg.Window('3-DOF ARTICULATED MANIPULATOR - Forward Kinematics', layout)

def clear_input():
    for key in values:
        window[key](' ')
    return None

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event =='Clear Input':
        clear_input()

#Forward kinematics code
    if event == 'Solve Forward Kinematics':
        #link lengths in cm
        a1 = values['a1']
        a2 = values['a2']
        a3 = values['a3']

        #joint variable thetas in degrees
        T1 = values['T1']
        T2 = values['T2']
        T3 = values['T3']

        #joint variable thetas in radians
        T1 = (float(T1)/180.0)*np.pi
        T2 = (float(T2)/180.0)*np.pi
        T3 = (float(T3)/180.0)*np.pi

        #if joint variable are ds, don't need to convert

        ## DH Parameter Table - DHPT (ONLY EDIT for every new manipulator)
        #Rows = no. of HTM
        #Columns + no. of parameters
        #Theta, alpha, r, d

        DHPT = [[float(T1),(90.0/180.0)*np.pi,0,float(a1)],
            [float(T2),(0.0/180.0)*np.pi,float(a2),0],
            [float(T3),(0.0/180.0)*np.pi,float(a3),0]]
        
        # np.trigo function (DHPT[ROW][COLUMN])

        i = 0
        H0_1 = [[np.cos(DHPT)[i][0], -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
                [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
                [0,0,0,1]]

        i = 1
        H1_2 = [[np.cos(DHPT)[i][0], -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
                [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
                [0,0,0,1]]

        i = 2
        H2_3 = [[np.cos(DHPT)[i][0], -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
                [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
                [0,0,0,1]]

        #transformation matrices from base to end effector
        #print("H0_1 = ")
        #print(np.matrix(H0_1))
        #print("H1_2 = ")
        #print(np.matrix(H1_2))
        #print("H2_3 = ")
        #print(np.matrix(H2_3))

        #dot product of H0_3 = H0_1*H1_2*H2_3
        H0_2 = np.dot(H0_1, H1_2)
        H0_3 = np.dot(H0_2, H2_3)

        #transformation matrix of the manipulator
        print("H0_3 =")
        print(np.matrix(H0_3))

        #position vector x y z
        X0_3 = H0_3[0,3]
        print("X =")
        print(X0_3)

        Y0_3 = H0_3[1,3]
        print("Y =")
        print(Y0_3)

        Z0_3 = H0_3[2,3]
        print("Z =")
        print(Z0_3)

    if event == 'Submit':
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!')
        clear_input()
window.close()