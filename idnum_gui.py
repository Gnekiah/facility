#-------------------------------------------------------------------------------
# Name:        IDnum GUI
# Purpose:     Generate a legal Chinese id number & Check out the opponent of Chinese id number
#
# Author:      Ekira
#
# Created:     12/10/2018
# Copyright:   (C) Ekira 2017
# Licence:     <GNU Lesser General Public License>
#-------------------------------------------------------------------------------

# -*- coding: utf-8 -*- #

import wx
import os, sys, time
from random import randint
import idnum_code2area


# calculate for checkbit
def getcheckbit(s):
    checkbit = 0
    weight = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    checkbitmap = ['1','0','X','9','8','7','6','5','4','3','2']
    for i in range(0, 17):
        checkbit += weight[i] * int(s[i])
    return checkbitmap[checkbit % 11]


# check out oponent of id format
def format_check(s):
    if len(s) != 18:
        return 2
    for i in s[0:17]:
        if not i.isdigit():
            return 3
    if getcheckbit(s[0:17]) != s[17]:
        return 1
    return 0


# check out the opponent of id number
def brth_check(s):
    pre = "19000101"
    now = time.strftime('%Y%m%d', time.localtime(time.time()))
    if s < pre or s > now:
        return 1
    if s[4:6] == "00" or s[4:6] > "12":
        return 2
    if s[6:8] == "00" or s[6:8] > "31":
        return 3
    if (s[4:6] == "04" or s[4:6] == "06" or s[4:6] == "09" or s[4:6] == "11") and s[6:8] > "30":
            return 3
    if s[4:6] == "02" and s[6:8] > "29":
            return 3
    if int(s[2:4]) % 4 != 0 and s[4:6] == "02" and s[6:8] > "28":
        return 3
    if int(s[0:4])%100 == 0 and  int(s[0:4])%400 != 0 and s[4:6] == "02" and s[6:8] > "28":
        return 3
    return 0


class IdNumWindow(wx.Dialog):
    def __init__(self, parent, title, size):
        wx.Dialog.__init__(self, parent, title=title, size=size)
        self.InitUI()


    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL))

        p_input = wx.TextCtrl(parent=panel, pos=(10, 10), size=(280,30))
        p_check = wx.Button(parent=panel, label="检查", pos=(290,10))
        p_gentor = wx.Button(parent=panel, label="生成", pos=(290,60))

        wx.StaticText(parent=panel, label="身份证号:", pos=(10,100))
        p_id = wx.StaticText(parent=panel, label="", pos=(100,100))
        wx.StaticText(parent=panel, label="所属地区:", pos=(10,130))
        p_area = wx.StaticText(parent=panel, label="", pos=(100,130))
        wx.StaticText(parent=panel, label="出生年月:", pos=(10,160))
        p_birth = wx.StaticText(parent=panel, label="", pos=(100,160))
        wx.StaticText(parent=panel, label="号码序列:", pos=(10,190))
        p_no = wx.StaticText(parent=panel, label="", pos=(100,190))
        wx.StaticText(parent=panel, label="尾校验码:", pos=(10,220))
        p_bit = wx.StaticText(parent=panel, label="", pos=(100,220))
        

        self.p_input = p_input
        self.p_check = p_check
        self.p_gentor = p_gentor
        self.p_id = p_id
        self.p_area = p_area
        self.p_birth = p_birth
        self.p_no = p_no
        self.p_bit = p_bit
        self.Bind(wx.EVT_BUTTON, self.OnCheckButton, p_check)
        self.Bind(wx.EVT_BUTTON, self.OnGentorButton, p_gentor)

        
    def OnCheckButton(self, event):
        idnum = self.p_input.GetValue()
        area = str()
        brth = str()
        num = str()
        self.p_id.SetLabel("")
        self.p_area.SetLabel("")
        self.p_birth.SetLabel("")
        self.p_no.SetLabel("")
        self.p_bit.SetLabel("")

        if len(idnum) == 0: return

        fmtck = format_check(idnum)
        if fmtck != 0:
            if fmtck == 1:
                self.p_bit.SetLabel("尾部校验码错误")
            elif fmtck == 2:
                self.p_id.SetLabel("输入的号码长度错误")
            else:
                self.p_id.SetLabel("存在非法字符")
            return
        dicts =  idnum_code2area.code2area()
        
        if idnum[0:6] not in dicts.keys():
            self.p_area.SetLabel("地区代码非法")
            return

        area = dicts[idnum[0:6]]
        brth = idnum[6:14]
        num = idnum[14:17]
        brthck =  brth_check(brth)
        if brthck != 0:
            if brthck == 1:
                self.p_birth.SetLabel("年份越界")
            elif brthck == 2:
                self.p_birth.SetLabel("月份越界")
            else:
                self.p_birth.SetLabel("日期越界")
            return
        self.p_id.SetLabel(idnum)
        self.p_area.SetLabel(area)
        self.p_birth.SetLabel(brth)
        self.p_no.SetLabel(num)
        self.p_bit.SetLabel(idnum[-1:])
        return


    def OnGentorButton(self, event):
        idnum = str()
        dicts = idnum_code2area.code2area()
        lists = list(dicts.keys())
        areacode = lists[randint(0, len(lists))]
        area = dicts[areacode]
        idnum += areacode
        randstamp = randint(0, int(time.time()))
        date = time.strftime("%Y%m%d", time.localtime(randstamp))
        idnum += date
        num = str(randint(1, 999))
        if len(num) == 1:
            num = '00'+num
        if len(num) == 2:
            num = "0"+num
        idnum += num
        checkbit = getcheckbit(idnum)
        idnum += checkbit
        self.p_id.SetLabel(idnum)
        self.p_area.SetLabel(area)
        self.p_birth.SetLabel(date)
        self.p_no.SetLabel(num)
        self.p_bit.SetLabel(checkbit)
        return

