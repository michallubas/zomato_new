import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la
# from build import Hello
# from sim import Simulation

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))

######################################################################################################################
# CREATE DATA Base
# exec(open('create_table.py').read())
######################################################################################################################
#


class Simulation():
    def __init__(self):

        self.loops = 100
        self.dt = 0.1
        self.V_max = 27.7
        self.V_min = 0
        self.s_max = 100000
        self.s_min = 0
        self.V_start = 19.446
        # V_start = 0
        self.F_brake = 4000
        # F_brake = 0

        # initiation of objects

        # format for below instances: dataIn,dataOut, dataOut_max, method
        self.speed = Integral('V', 'speed', 0, self.V_start, self.V_max, 'trapezoid',
                              self.dt)                   # a     =>  V  [m/s]
        self.road = Integral('s', 'road', 0, 0, self.s_max, 'trapezoid',
                             self.dt)                       # V     =>  s [m]

        # format for below instances:  name, data in: axis x , data in: axis y
        self.track_profile = Table('TP', 'tr_profile', 0, [0, 1, 10, 100, 1000, 10000, 1000000], [
            0, 0, 0, 0, 0, 0, 0])                                        # s     =>  i
        self.tracking_force = Table('RF', 'tr_force', 0, [0, 9.72, 11.12, 15.3, 22.22, 30.56, 33.4], [
            0, 0, 0, 0, 0, 0, 0])                                       # V     =>  F
        # tracking_force = Table('RF', 'tr_force', 0, [0, 9.72, 11.12, 15.3, 22.22, 30.56, 33.4], [
        #                        3000, 3000, 2800, 2000, 1400, 1000, 900])                                       # V     =>  F

        # data in=0 for start, for polynomial ax2 + bx + c:  [a,b,c] , positive or negative: 1 or -1
        self.resistance = Polynomial('Wz', 'fundamental_resistance', 0, [
            1300*9.81*0.00065 + 0.6*0.3*0.9*1.6*1.48, 0, 0.012*1300*9.81], -1.0, self.dt)   # V  => Wz

        # train:
        # resistance = Polynomial('Wz', 'fundamental_resistance', 0, [
        #                         0.6*0.35*0.9*1.6*1.48, 0, 0.012+(1200*9.81)], -1.0, dt)  # V  => Wz

        # last number is brake
        self.summary = Summary('sum', 'summary', self.F_brake, 0, 0, 0)   # F     =>  sum

        # train
        # tracking_force = Table('tr_force' , 0,[0,21,30,44], [300,265,190,125] )             # V     =>  F

        # Check for min & max
        self.check_V_s = Check('c', 'check_V_s', self.V_max, self.s_max, self.V_min, self.s_min)

        # format for below gains/instances:  name, data in: x, data in: y, divide/multiply by..
        self.gain_a = Gain('Ga', 'conv: force_to_a', 0, 1300, 1.085,
                           '1/(xy)')                        # F     =>  a
        self.gain_Wi = Gain('GWi', 'conv: i_to_w', 0, 1300, 9.81,
                            'xy')                            # i     =>  Wi

        # options for actions in GainUnit: 1*1000 or 1/1000
        self.gain_Wi1000 = GainUnit('GWi1000', 'divide_1000', 0,
                                    '1/1000')                          # Wi => F
        self.gain_Wz1000 = GainUnit('GWz1000', 'divide_1000', 0,
                                    '1/1000')                          # Wz => F

        self.gain_a_records = []
        self.speed_records = []
        self.road_records = []
        self.tracking_force_records = []
        self.summary_records = []
        self.t_records = []

    #####################################################################################################################
    # symulacja

    # initial time t=0
        self.t = 0
        self.id = 0

        while self.id < self.loops:
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

            self.speed.calculate()
            self.road.updateDataIn(self.speed.getdataOut())                   # V => road
            self.tracking_force.updateDataIn(self.speed.getdataOut())         # V => tracking_force
            self.resistance.updateDataIn(self.speed.getdataOut())             # V => resistance

            self.road.calculate()
            self.track_profile.updateDataIn(self.road.getdataOut())

            self.track_profile.calculate()
            self.gain_Wi.updateDataIn(self.track_profile.getdataOut())

            self.gain_Wi.calculate()

            # for car no gain for road profile !!!
            # gain_Wi1000.updateDataIn(gain_Wi.getdataOut())
            # gain_Wi1000.calculate()

            self.tracking_force.calculate()

            self.resistance.calculate()

            # for car no gain for resitance !!!
            # gain_Wz1000.updateDataIn(resistance.getdataOut())
            # gain_Wz1000.calculate()
            # summary.updateDataIn(gain_Wi1000.getdataOut(), gain_Wz1000.getdataOut(),
            #                      tracking_force.getdataOut())

            self.summary.updateDataIn(self.gain_Wi.getdataOut(), self.resistance.getdataOut(),
                                      self.tracking_force.getdataOut())

            self.summary.calculate()
            self.gain_a.updateDataIn(self.summary.getdataOut())

            self.gain_a.calculate()
            # gain_a.updateDataOut(-5)

            self.speed.updateDataIn(self.gain_a.getdataOut())

          # check
            self.check_V_s.updateDataIn(self.speed.getdataOut(), self.road.getdataOut())
            if (self.check_V_s.calculate() and self.id > 4):
                self.check_V_s.updateDataIn(self.speed.getdataOut(), self.road.getdataOut())
                break

        #     print('XXXXXXXX END  LOOP   XXXXXXXXXX')

            # records
            self.gain_a_records.append(self.gain_a.getdataOut())
            self.speed_records.append(self.speed.getdataOut())
            self.road_records.append(self.road.getdataOut())
            self.tracking_force_records.append(self.tracking_force.getdataOut())
            self.summary_records.append(self.summary.getdataOut())
            self.t_records.append(self.t)

            self.t = self.t+self.dt

            self.id += 1
            # finish loop

        plt.rcParams.update({'font.size': 8})
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(15, 15))
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.4)
        # plt.rcParams['figure.constrained_layout.use'] = True
        # fig.tight_layout()

        ax1.plot(self.t_records, self.speed_records, 'b')
        ax1.set(xlabel='time [s]', ylabel='speed [m/s]')
        ax1.set_xlim(xmin=0)
        ax1.set_ylim(ymin=0)

        ax2.plot(self.t_records, self.tracking_force_records, 'r')
        ax2.set(xlabel='time [s]', ylabel='tracking_force [N]')
        ax2.set_xlim(xmin=0)
        ax2.set_ylim(ymin=-0.1)

        ax3.plot(self.t_records, self.road_records, 'y')
        ax3.set(xlabel='time [s]', ylabel='road [m]')
        ax3.set_xlim(xmin=0)
        ax3.set_ylim(ymin=0)

        ax4.plot(self.t_records, self.gain_a_records, 'r')
        ax4.set(xlabel='time [s]', ylabel='a [m/s2]')
        ax4.set_xlim(xmin=0)
        ax4.set_ylim(ymin=-10)

        ax5.plot(self.road_records, self.speed_records, 'y')
        ax5.set(xlabel='road [m]', ylabel='speed [m/s]')
        ax5.set_xlim(xmin=0)
        ax5.set_ylim(ymin=0)

        # plt.show()
# plt.tight_layout()


class Integral():
    def __init__(self, name, text, dataIn, dataOut, dataOut_max, method, dt=0.1):
        self.dataIn = dataIn
        self.dt = dt
        self.dataOut = dataOut
        self.name = name
        self.text = text
        self.dataOut_max = dataOut_max
        self.method = method
        self.dataInPrev = 0

    def updateDataIn(self, new_dataIn):
        self.dataIn = new_dataIn

    def updateDataInPrev(self, new_dataIn):
        self.dataInPrev = new_dataIn

    def updateDataOut(self, new_dataIn):
        self.dataOut = new_dataIn

    def calculate(self):

        # if self.method == 'rectangle':
        #     self.dataOut = self.dataOut + self.dataIn * self.dt
        #     if self.dataOut >= self.dataOut_max:
        #         self.dataOut = self.dataOut_max
        #         return self.dataOut_max
        #     return self.dataOut

        if self.method == 'trapezoid':
            self.dataOut = self.dataOut + 0.5 * (self.dataInPrev + self.dataIn) * self.dt
            if self.dataOut >= self.dataOut_max:
                self.dataOut = self.dataOut_max
                self.dataInPrev = self.dataIn
                return self.dataOut

            self.dataInPrev = self.dataIn
            return self.dataOut

    def getdataOut(self):
        return self.dataOut

    def __repr__(self):
        return (f'Name: {self.name}, dataIn: {self.dataIn}, dataOut: {self.dataOut}')


# Interpolation version 3, linear interpolation
class Table():
    def __init__(self, name, text, dataIn, dataIn_x, dataIn_y):
        self.dataIn = dataIn
        self.dataIn_x = dataIn_x
        self.dataIn_y = dataIn_y
        self.name = name
        self.text = text
        self.dataOut = 0

    def updateDataIn(self, new_dataIn):
        self.dataIn = new_dataIn

    def updateDataOut(self, new_dataIn):
        self.dataOut = new_dataIn

#           [0,21,30,44, >44], [300,265,190,125, 0]

    def calculate(self):
        counter = 1
        for numb in self.dataIn_x[1:]:
            if self.dataIn <= numb:
                self.dataOut = self.dataIn_y[counter-1] + (self.dataIn_y[counter]-self.dataIn_y[counter-1])/(
                    self.dataIn_x[counter]-self.dataIn_x[counter-1])*(self.dataIn-self.dataIn_x[counter-1])
                return self.dataOut
            counter += 1

        self.dataOut = 0
        return self.dataOut

    def getdataOut(self):
        return self.dataOut

    def __repr__(self):
        return (f'Name: {self.name}, dataIn: {self.dataIn}, dataOut: {self.dataOut} ')


class Summary():
    def __init__(self, name, text, dataIn_brake, dataIn_1, dataIn_2, dataIn_3):
        self.dataIn_1 = dataIn_1
        self.dataIn_2 = dataIn_2
        self.dataIn_3 = dataIn_3
        self.dataIn_brake = dataIn_brake
        self.dataOut = self.dataIn_1 + self.dataIn_2 + self.dataIn_3 - self.dataIn_brake
        self.name = name
        self.text = text

    def updateDataIn(self, new_dataIn_1, new_dataIn_2, new_dataIn_3):
        self.dataIn_1 = new_dataIn_1
        self.dataIn_2 = new_dataIn_2
        self.dataIn_3 = new_dataIn_3

    def updateDataOut(self, new_dataIn):
        self.dataOut = new_dataIn

    def calculate(self):
        self.dataOut = self.dataIn_1+self.dataIn_2 + self.dataIn_3 - self.dataIn_brake
        return self.dataOut

    def getdataOut(self):
        return self.dataOut

    def __repr__(self):
        return (f'Name: {self.name}, dataIn1: {self.dataIn_1}, dataIn2: {self.dataIn_2}, dataIn3: {self.dataIn_3}, dataOut: {self.dataOut}')


class Polynomial():
    def __init__(self, name, text,  dataIn, dataIn_abc, dataIn_sign,  dt=0):
        self.dataIn = dataIn
        self.dataIn_abc = dataIn_abc
        self.dataIn_sign = dataIn_sign
        self.name = name
        self.dataOut = 0
        self.p = np.poly1d([dataIn_abc[0], dataIn_abc[1], dataIn_abc[2]])

    def updateDataIn(self, new_dataIn):
        self.dataIn = new_dataIn

    def updateDataOut(self, new_dataIn):
        self.dataOut = new_dataIn

    def calculate(self):
        # self.dataOut = self.dataIn**2 * self.dataIn_abc[0] + \
        #     self.dataIn * self.dataIn_abc[1] + self.dataIn_abc[2]

        self.dataOut = self.p(self.dataIn)

        self.dataOut *= self.dataIn_sign
        return self.dataOut

    def getdataOut(self):
        return self.dataOut

    def __repr__(self):
        return (f'Name: {self.name}, dataIn: {self.dataIn},dataIn abc: {self.dataIn_abc}, sign is: {self.dataIn_sign}, dataOut: {self.dataOut}')


class Gain():

    def __init__(self, name, text, dataIn, var1_to_formula, var2_to_formula, formula):

        self.name = name
        self.text = text
        self.dataIn = dataIn
        self.var1_to_formula = var1_to_formula
        self.var2_to_formula = var2_to_formula
        self.formula = formula
        self.dataOut = 0

    def updateDataIn(self, new_dataIn):
        self.dataIn = new_dataIn

    def updateDataOut(self, new_dataIn):
        self.dataOut = new_dataIn

    def calculate(self):
        if self.formula == '1/(xy)':
            self.dataOut = self.dataIn / (self.var1_to_formula * self.var2_to_formula)
            return self.dataOut
        if self.formula == 'xy':
            self.dataOut = self.dataIn * self.var1_to_formula * self.var2_to_formula
            return self.dataOut

    def getdataOut(self):
        return self.dataOut

    def __repr__(self):
        return (f'Name: {self.name}, dataIn: {self.dataIn}, dataOut: {self.dataOut}')


class GainUnit():

    def __init__(self, name, text, dataIn, formula):

        self.name = name
        self.text = text
        self.dataIn = dataIn
        self.formula = formula
        self.dataOut = 0

    def updateDataIn(self, new_dataIn):
        self.dataIn = new_dataIn

    def updateDataOut(self, new_dataIn):
        self.dataOut = new_dataIn

    def calculate(self):
        if self.formula == '1*1000':
            self.dataOut = self.dataIn*1000
            return self.dataOut
        if self.formula == '1/1000':
            self.dataOut = self.dataIn / 1000
            return self.dataOut

    def getdataOut(self):
        return self.dataOut

    def __repr__(self):
        return (f'Name: {self.name}, dataIn: {self.dataIn}, dataOut: {self.dataOut}')


class Check():

    def __init__(self, name, text, V_max, s_max, V_min, s_min):

        self.name = name
        self.text = text
        self.V_max = V_max
        self.V_min = V_min
        self.s_max = s_max
        self.s_min = s_min

        self.dataIn_V = 0
        self.dataIn_s = 0
        self.dataOut_V = False
        self.dataOut_s = False

    def updateDataIn(self, dataIn_V, dataIn_s):
        self.dataIn_V = dataIn_V
        self.dataIn_s = dataIn_s

    def updateDataOut(self, new_dataIn):
        self.dataOut = new_dataIn

    def calculate(self):
        if (self.dataIn_V <= self.V_min):
            # if (self.dataIn_V >= self.V_max or self.dataIn_V <= self.V_min):
            #             self.dataOut_V = True
            # print(
            #     f'Osiagnieto wartosci graniczne dla predkosci, aktualna predkosc: {round(self.dataIn_V,2)} m/s, Vmax= {round(self.V_max,2)} m/s,Vmin= {round(self.V_min,2)} m/s, droga: {round(self.dataIn_s,2)} m')
            return True

        if (self.dataIn_s >= self.s_max or self.dataIn_s <= self.s_min):
            #             self.dataOut_s = True
            print(
                f'Osiagnieto wartosci graniczne dla drogi, aktualna droga: {round(self.dataIn_s,2)} smax s: {round(self.s_max,2)} m, smin=: {round(self.s_min,2)} m/s, aktualna predkosc: {round(self.dataIn_V,2)} ')
            return False

        return False

#     def getdataOut(self):
#         return self.dataOut

    def __repr__(self):
        return (f'Name: {self.name}, dataIn_V: {self.dataIn_V},dataIn_s: {self.dataIn_s}')


class Signal():

    def __init__(self, name, text, dataIn):

        self.name = name
        self.text = text
        self.dataIn = dataIn
        self.dataOut = False

    def updateDataIn(self, dataIn):
        self.dataIn = dataIn

    def updateDataOut(self, new_dataIn):
        self.dataOut = new_dataIn

    def calculate(self):
        if self.dataIn >= V_max:
            return True
        return False

    def getdataOut(self):
        return self.dataOut

    def __repr__(self):
        return (f'Name: {self.name}, dataIn: {self.dataIn},dataOut: {self.dataOut }')


@app.route('/')
def home():
    return render_template('index.html')


# @test
# nic
# tetst test

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # features = [int(x) for x in request.form.values()]
    # final_features = [np.array(features)]
    # prediction = model.predict(final_features)
    train = Simulation()
    features = [int(x) for x in request.form.values()]

    # prediction = model.suma(features)
    # prediction = Hello()
    prediction = train.road_records[len(road_records)-1]
    # print(prediction)

    output = prediction
    # output = round(prediction[0], 1)

    return render_template('index.html', prediction_text=f'Droga hamownia: {round(output,2} metra')


if __name__ == "__main__":
    app.run(debug=True)
