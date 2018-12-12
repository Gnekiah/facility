#-------------------------------------------------------------------------------
# Name:        Minitools
# Purpose:     Minitools.
#
# Author:      Ekira
#
# Created:     09/02/2017
# Modified:    12/10/2018
# Copyright:   (C) Ekira 2017
# Licence:     <GNU Lesser General Public License>
#-------------------------------------------------------------------------------

# -*- coding: utf-8 -*- #

import wx, os
import pswgen_gui
import idnum_gui
import xls2csv_gui
import csv2xlsx_gui
import gbk2utf_gui
import watermark_gui

class MainWindow(wx.App):
    def __init__(self):
        self.HOME_PATH = os.path.join(os.path.expanduser('~'), ".facility")
        self.APP_NAME = "minitools-gui"
        self.VERSION = "0.0.1"
        self.UPDATE_URL = "http://www.xxiong.me/"
        if not os.path.isdir(self.HOME_PATH):
            os.mkdir(self.HOME_PATH)
        wx.App.__init__(self)

    
    def OnInit(self):
        framestyle=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN
        frame = wx.Frame(parent=None, title=self.APP_NAME, size=(600,400), style=framestyle)
        frame.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        bg = wx.Panel(frame)

        xls2csvButton = wx.Button(bg, label="xls(x) 转 csv")
        csv2xlsButton = wx.Button(bg, label="csv 转 xlsx")
        gbk2utfButton = wx.Button(bg, label="gbk <=> utf-8")
        passwdgenButton = wx.Button(bg, label="随机密码生成器")
        chsidgenButton = wx.Button(bg, label="身份证号码生成器")
        watermarkButton = wx.Button(bg, label="批量图片嵌水印")
        updateButton = wx.Button(bg, label="正在检查更新...")
        updateButton.Enable(False)

        grid = wx.GridSizer(rows=6, cols=3, vgap=10, hgap=5)
        grid.AddMany([
            (xls2csvButton,0,wx.EXPAND),
            (csv2xlsButton,0,wx.EXPAND),
            (gbk2utfButton,0,wx.EXPAND),
            (passwdgenButton,0,wx.EXPAND),
            (chsidgenButton,0,wx.EXPAND),
            (watermarkButton,0,wx.EXPAND),
            (updateButton,0,wx.EXPAND),
            ])
        bg.SetSizer(grid)

        self.bg = bg
        self.frame = frame
        self.xls2csvButton = xls2csvButton
        self.csv2xlsButton = csv2xlsButton
        self.gbk2utfButton = gbk2utfButton
        self.passwdgenButton = passwdgenButton
        self.chsidgenButton = chsidgenButton
        self.watermarkButton = watermarkButton
        self.updateButton = updateButton

        self.Bind(wx.EVT_BUTTON, self.OnXls2csvButton, xls2csvButton)
        self.Bind(wx.EVT_BUTTON, self.OnCsv2xlsButton, csv2xlsButton)
        self.Bind(wx.EVT_BUTTON, self.OnGbk2utfButton, gbk2utfButton)
        self.Bind(wx.EVT_BUTTON, self.OnPasswdgenButton, passwdgenButton)
        self.Bind(wx.EVT_BUTTON, self.OnChsidgenButton, chsidgenButton)
        self.Bind(wx.EVT_BUTTON, self.OnWatermarkButton, watermarkButton)
        self.Bind(wx.EVT_BUTTON, self.OnUpdateButton, updateButton)
        
        frame.Show()
        return True


    def OnXls2csvButton(self, event):
        try:
            dlg = xls2csv_gui.Xls2CsvWindow(self.bg, "xls(x) 转 csv", (500,400))
            self.frame.Show(False)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            dlg.Destroy()
            self.frame.Show(True)
        return


    def OnCsv2xlsButton(self, event):
        try:
            dlg = csv2xlsx_gui.Csv2XlsWindow(self.bg, "csv 转 xlsx", (500,400))
            self.frame.Show(False)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            dlg.Destroy()
            self.frame.Show(True)
        return


    def OnGbk2utfButton(self, event):
        try:
            dlg = gbk2utf_gui.Gbk2UtfWindow(self.bg, "gbk <=> utf-8", (500,400))
            self.frame.Show(False)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            dlg.Destroy()
            self.frame.Show(True)
        return


    def OnPasswdgenButton(self, event):
        try:
            dlg = pswgen_gui.PswGenWindow(self.bg, "随机密码生成器", (430,300))
            self.frame.Show(False)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            dlg.Destroy()
            self.frame.Show(True)
        return


    def OnChsidgenButton(self, event):
        try:
            dlg = idnum_gui.IdNumWindow(self.bg, "身份证号码生成器", (430,300))
            self.frame.Show(False)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            dlg.Destroy()
            self.frame.Show(True)
        return


    def OnWatermarkButton(self, event):
        try:
            dlg = watermark_gui.WatermarkWindow(self.bg, "批量图片嵌水印", (600,500))
            self.frame.Show(False)
            dlg.ShowModal()
            dlg.Destroy()
        except Exception as e:
            print(e)
        finally:
            dlg.Destroy()
            self.frame.Show(True)
        return

        


    def OnUpdateButton(self, event):
        pass


def main():
    app = MainWindow()
    app.MainLoop()


if __name__ == '__main__':
    main()


