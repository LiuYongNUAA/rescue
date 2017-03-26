# -*- coding: utf-8 -*-

import math
PI = math.pi
Men_DWL = 0.0114
Men_CWL = 0.0054

Wind_Speed = float(input('windspeed'))
Wind_Angle = float(input('windangle'))
Sea_Speed = float(input('seaspeed'))
Sea_Angle = float(input('seaangle'))
Time = float(input('time')) * 3600


class Men(object):
    def Get_Loc(self):
        self.long = float(input('请输入经度'))
        self.lat = float(input('请输入纬度'))
    def Transfor(self):
        self.x = self.long * 20037508.34 / 180
        self.y = math.log(math.tan((90 + self.lat) * PI / 360))/(PI / 180)
        self.y = self.y * 20037508.34 / 180
    def Float(self):
        self.DWL = Men_DWL * Wind_Speed
        self.CWL = Men_CWL * Wind_Speed
        if Wind_Speed < 9.25:
            self.Wc_Speed = 0.09
        else:
            self.Wc_Speed = (0.230446 + 0.0070957 * Wind_Speed * 0.514) ** 2 + 0.09
        self.Wc_Angle = -35.338 + 3587.98 / (0.514 * Wind_Speed) + Wind_Angle
        self.xfloat = self.DWL * math.sin(Wind_Angle * PI / 180) + self.CWL * math.cos(Wind_Angle * PI / 180) + Sea_Speed * math.sin(Sea_Angle *PI /180) + self.Wc_Speed * math.sin(self.Wc_Angle * PI /180)
        self.x = self.x + self.xfloat * Time
        self.yfloat = self.DWL * math.cos(Wind_Angle * PI / 180) - self.CWL * math.cos(Wind_Angle * PI / 180) + Sea_Speed * math.cos(Sea_Angle *PI /180) + self.Wc_Speed * math.cos(self.Wc_Angle * PI /180)
        self.y = self.y + self.yfloat * Time
    def TransBack(self):
        self.x = self.x / 20037508.34 * 180
        self.y = self.y / 20037508.34 * 180
        self.y = 180 / PI * (2 * math.atan(math.exp(self.y * PI / 180)) - PI / 2)
test = Men()
test.Get_Loc()
test.Transfor()
test.Float()
test.TransBack()
print(test.x, test.y)








