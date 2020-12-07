import numpy as np


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


# Interpolation version 1, two tables
# class Table():
#     def __init__(self,name, dataIn, dataIn_3, dataIn_4):
#         self.dataIn=dataIn
#         self.dataIn_3=dataIn_3
#         self.dataIn_4=dataIn_4
#         self.name = name
#         self.dataOut=0

#     def updateDataIn(self, new_dataIn):
#         self.dataIn = new_dataIn


# #           [21,30,44], [300,265,190,125]

#     def calculate(self):
#         counter=0
#         for numb in self.dataIn_3:
#             if self.dataIn <= numb:
#                 self.dataOut = self.dataIn_4[counter]
#                 return self.dataOut
#             counter+=1

#         self.dataOut = self.dataIn_4[ len(self.dataIn_4) - 1 ]
#         return self.dataOut

#     def getdataOut(self):
#         return self.dataOut

#     def __repr__(self):
#         return (f'Name: {self.name}, dataIn: {self.dataIn}, dataOut: {self.dataOut} ')


# Interpolation version 2, vectors
# class Table():
#     def __init__(self, name, dataIn, dataIn_x, dataIn_y):
#         self.dataIn=dataIn
#         self.x=dataIn_x
#         self.y=dataIn_y
#         self.name = name
#         self.dataOut=0

#         # number of points:
#         self.N = 4

#         # use the numpy.vander, option increasing=True so that powers of  increase left-to-right:
#         self.X = np.vander(self.x,increasing=True)


#         # Compute the vector a of coefficients:
#         self.a = la.solve(self.X,self.y)

#         # Accuracy, only to check
#         self.xs = np.linspace(0,max(self.x),100)
#         self.ys = sum([self.a[k]*self.xs**k for k in range(0,self.N)])
# #         plt.plot(self.xs,self.ys,self.x,self.y,'b.',ms=10)
# #         plt.show()

#     def updateDataIn(self, new_dataIn):
#         self.dataIn = new_dataIn


# #           [21,30,44], [300,265,190,125]

#     def calculate(self):

#         self.dataOut =   self.a[0] + self.a[1]*self.dataIn + self.a[2]*self.dataIn**2 + self.a[3]*self.dataIn**3
#         return self.dataOut

#     def getdataOut(self):
#         return self.dataOut

#     def __repr__(self):
#         return (f'Name: {self.name}, dataIn: {self.dataIn}, dataOut: {self.dataOut} ')
