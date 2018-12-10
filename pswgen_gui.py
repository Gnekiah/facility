#-------------------------------------------------------------------------------
# Name:        pswgen GUI
# Purpose:     Package pswgen to provide GUI.
#
# Author:      Ekira
#
# Created:     09/02/2017
# Modified:    12/10/2018
# Copyright:   (C) Ekira 2017
# Licence:     <GNU Lesser General Public License>
#-------------------------------------------------------------------------------

# -*- coding: utf-8 -*- #

import wx, random

SYMBOL = ["0123456789","ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz","""`~!@#$%^&*()-=_+[]\{}|;':",./<>?"""]

class PswGenWindow(wx.Dialog):
    def __init__(self, parent, title, size):
        wx.Dialog.__init__(self, parent, title=title, size=size)
        self.InitUI()


    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
   
        wx.StaticText(parent=panel, label="符号类型:", pos=(10,10))
        p_string = wx.CheckListBox(parent=panel, pos=(10,33), size=(200,90),
            choices=["数字","大写字母","小写字母","符号"])
        p_string.SetChecked([0])

        p_format = wx.RadioBox(parent=panel, label="格式:", pos=(225,25), choices=['间隔','随机'], majorDimension=2)
        wx.StaticText(parent=panel, label="长度:", pos=(250,110))
        p_length = wx.SpinCtrl(parent=panel, value="10", min=1, max=256, pos=(325, 105), size=(70,-1))

        wx.StaticText(parent=panel, label="随机口令:", pos=(10,180))
        p_passwd = wx.TextCtrl(parent=panel, pos=(100, 177), size=(300,30))
        p_gentor = wx.Button(parent=panel, label="生成", pos=(270,220))

        self.p_string = p_string
        self.p_format = p_format
        self.p_length = p_length
        self.p_passwd = p_passwd
        self.p_gentor = p_gentor
        self.Bind(wx.EVT_BUTTON, self.OnButton, p_gentor)

        
    def OnButton(self, event):
        v_string = self.p_string.GetChecked()
        v_format = self.p_format.GetStringSelection()
        v_length = self.p_length.GetValue()
        passwd = ""
        symbol = []
        for i in v_string:
            symbol.append(SYMBOL[i])
        if v_format == '间隔':
            size = len(v_string)
            for i in range(v_length):
                passwd += random.choice(symbol[i%size])
        elif v_format == '随机':
            new_string = "".join(symbol)
            for i in range(v_length):
                passwd += random.choice(new_string)
        else:
            pass
        self.p_passwd.SetValue(passwd)
        
