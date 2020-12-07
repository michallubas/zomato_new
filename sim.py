import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la
from blocks import Integral, Summary, Polynomial, Gain, GainUnit, Signal, Check, Table
from flask import Flask, request, jsonify, render_template
import sqlite3

from flask_restful import Resource, reqparse


# user in puts:

# loops = int (input('Podaj liczbe petli: '))
# dt = float (input('Podaj dt [delta time] w sekundach: ')    )
# V_max = int (input('Podaj V max w metrach/sekunde: '))
# V_min = int (input('Podaj V min w metrach/sekunde: '))
# s_max = int (input('Podaj s max w metrach: '))
# s_min = int (input('Podaj s min w metrach: '))
# V_start = int (input('Podaj V na start w metrach/sekunde: '))
# F_brake = int (input('Podaj siłę hamjącą w N: '))


class Simulation():
    def __init__(self):

        # CLEAR database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM readings"
        cursor.execute(query)
        connection.commit()
        connection.close()

        loops = 100
        dt = 0.1
        V_max = 27.7
        V_min = 0
        s_max = 100000
        s_min = 0
        V_start = 19.446
        # V_start = 0
        F_brake = 4000
        # F_brake = 0

        # initiation of objects

        # format for below instances: dataIn,dataOut, dataOut_max, method
        speed = Integral('V', 'speed', 0, V_start, V_max, 'trapezoid',
                         dt)                   # a     =>  V  [m/s]
        road = Integral('s', 'road', 0, 0, s_max, 'trapezoid',
                        dt)                       # V     =>  s [m]

        # format for below instances:  name, data in: axis x , data in: axis y
        track_profile = Table('TP', 'tr_profile', 0, [0, 1, 10, 100, 1000, 10000, 1000000], [
                              0, 0, 0, 0, 0, 0, 0])                                        # s     =>  i
        tracking_force = Table('RF', 'tr_force', 0, [0, 9.72, 11.12, 15.3, 22.22, 30.56, 33.4], [
                               0, 0, 0, 0, 0, 0, 0])                                       # V     =>  F
        # tracking_force = Table('RF', 'tr_force', 0, [0, 9.72, 11.12, 15.3, 22.22, 30.56, 33.4], [
        #                        3000, 3000, 2800, 2000, 1400, 1000, 900])                                       # V     =>  F

        # data in=0 for start, for polynomial ax2 + bx + c:  [a,b,c] , positive or negative: 1 or -1
        resistance = Polynomial('Wz', 'fundamental_resistance', 0, [
            1300*9.81*0.00065 + 0.6*0.3*0.9*1.6*1.48, 0, 0.012*1300*9.81], -1.0, dt)   # V  => Wz

        # train:
        # resistance = Polynomial('Wz', 'fundamental_resistance', 0, [
        #                         0.6*0.35*0.9*1.6*1.48, 0, 0.012+(1200*9.81)], -1.0, dt)  # V  => Wz

        # last number is brake
        summary = Summary('sum', 'summary', F_brake, 0, 0, 0)   # F     =>  sum

        # train
        # tracking_force = Table('tr_force' , 0,[0,21,30,44], [300,265,190,125] )             # V     =>  F

        # Check for min & max
        check_V_s = Check('c', 'check_V_s', V_max, s_max, V_min, s_min)

        # format for below gains/instances:  name, data in: x, data in: y, divide/multiply by..
        gain_a = Gain('Ga', 'conv: force_to_a', 0, 1300, 1.085,
                      '1/(xy)')                        # F     =>  a
        gain_Wi = Gain('GWi', 'conv: i_to_w', 0, 1300, 9.81,
                       'xy')                            # i     =>  Wi

        # options for actions in GainUnit: 1*1000 or 1/1000
        gain_Wi1000 = GainUnit('GWi1000', 'divide_1000', 0,
                               '1/1000')                          # Wi => F
        gain_Wz1000 = GainUnit('GWz1000', 'divide_1000', 0,
                               '1/1000')                          # Wz => F

        # database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO readings VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"

        gain_a_records = []
        speed_records = []
        road_records = []
        tracking_force_records = []
        summary_records = []
        t_records = []

    #####################################################################################################################
    # symulacja

    # initial time t=0
        t = 0
        id = 0

        while id < loops:
            # start loop
            #     print('OOOOOO     START LOOP   OOOOOOOO')

            # print(f'id  {id}')
            # print(f'speed          {speed.getdataOut()}')
            # print(f'road           {road.getdataOut()}')
            # print(f'track_profile  {track_profile.getdataOut()}')
            # print(f'gain_Wi        {gain_Wi.getdataOut()}')
            # print(f'resistance     {resistance.getdataOut()}')
            #
            # print(f'tracking_force {tracking_force.getdataOut()}')
            # print(f'gain_Wi1000    {gain_Wi1000.getdataOut()}')
            # print(f'gain_Wz1000    {gain_Wz1000.getdataOut()}')
            #
            # print(f'sum            {summary.getdataOut()}')
            # print(f'a              {gain_a.getdataOut()}')
            # print()
            # print()

            speed.calculate()
            road.updateDataIn(speed.getdataOut())                   # V => road
            tracking_force.updateDataIn(speed.getdataOut())         # V => tracking_force
            resistance.updateDataIn(speed.getdataOut())             # V => resistance

            road.calculate()
            track_profile.updateDataIn(road.getdataOut())

            track_profile.calculate()
            gain_Wi.updateDataIn(track_profile.getdataOut())

            gain_Wi.calculate()

            # for car no gain for road profile !!!
            # gain_Wi1000.updateDataIn(gain_Wi.getdataOut())
            # gain_Wi1000.calculate()

            tracking_force.calculate()

            resistance.calculate()

            # for car no gain for resitance !!!
            # gain_Wz1000.updateDataIn(resistance.getdataOut())
            # gain_Wz1000.calculate()
            # summary.updateDataIn(gain_Wi1000.getdataOut(), gain_Wz1000.getdataOut(),
            #                      tracking_force.getdataOut())

            summary.updateDataIn(gain_Wi.getdataOut(), resistance.getdataOut(),
                                 tracking_force.getdataOut())

            summary.calculate()
            gain_a.updateDataIn(summary.getdataOut())

            gain_a.calculate()
            # gain_a.updateDataOut(-5)

            speed.updateDataIn(gain_a.getdataOut())

        #####################################################################################################################################
        # (id int PRIMARY KEY, t real, V real, s real, TP real, RF real, Wz real, sum real, Ga real, GWi real, GWi1000 real, GWz1000 real)
        # adding to database
            cursor.execute(query, (id, t, speed.getdataOut(), road.getdataOut(), track_profile.getdataOut(), tracking_force.getdataOut(), resistance.getdataOut(),
                                   summary.getdataOut(), gain_a.getdataOut(),  gain_Wi.getdataOut(), gain_Wi1000.getdataOut(), gain_Wz1000.getdataOut()))
            connection.commit()

          # check
            check_V_s.updateDataIn(speed.getdataOut(), road.getdataOut())
            if (check_V_s.calculate() and id > 4):
                connection.close()
                break

        #     print('XXXXXXXX END  LOOP   XXXXXXXXXX')

            # records
            gain_a_records.append(gain_a.getdataOut())
            speed_records.append(speed.getdataOut())
            road_records.append(road.getdataOut())
            tracking_force_records.append(tracking_force.getdataOut())
            summary_records.append(summary.getdataOut())
            t_records.append(t)

            t = t+dt

            id += 1
            # finish loop

        connection.close()

        plt.rcParams.update({'font.size': 8})
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(15, 15))
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.4)
        # plt.rcParams['figure.constrained_layout.use'] = True
        # fig.tight_layout()

        ax1.plot(t_records, speed_records, 'b')
        ax1.set(xlabel='time [s]', ylabel='speed [m/s]')
        ax1.set_xlim(xmin=0)
        ax1.set_ylim(ymin=0)

        ax2.plot(t_records, tracking_force_records, 'r')
        ax2.set(xlabel='time [s]', ylabel='tracking_force [N]')
        ax2.set_xlim(xmin=0)
        ax2.set_ylim(ymin=-0.1)

        ax3.plot(t_records, road_records, 'y')
        ax3.set(xlabel='time [s]', ylabel='road [m]')
        ax3.set_xlim(xmin=0)
        ax3.set_ylim(ymin=0)

        ax4.plot(t_records, gain_a_records, 'r')
        ax4.set(xlabel='time [s]', ylabel='a [m/s2]')
        ax4.set_xlim(xmin=0)
        ax4.set_ylim(ymin=-10)

        ax5.plot(road_records, speed_records, 'y')
        ax5.set(xlabel='road [m]', ylabel='speed [m/s]')
        ax5.set_xlim(xmin=0)
        ax5.set_ylim(ymin=0)

        # plt.show()
# plt.tight_layout()
