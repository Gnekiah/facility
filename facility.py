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

import wx, os, _thread, json, sys, urllib
from urllib import request
from subprocess import Popen
import pswgen_gui
import idnum_gui
import xls2csv_gui
import csv2xlsx_gui
import gbk2utf_gui
import watermark_gui


G_APP_NAME = "facility"
G_VERSION = "0.0.1"
G_UPDATE_URL = "http://www.xxiong.me/facility/"
G_HOME_PATH = os.path.join(os.path.expanduser('~'), ".facility")
G_CONFIG_PATH = os.path.join(G_HOME_PATH, "facility.json")
G_LOG_PATH = os.path.join(G_HOME_PATH, "facility.log")


class MainWindow(wx.App):
    def __init__(self):
        self.HOME_PATH = G_HOME_PATH
        self.APP_NAME = G_APP_NAME
        self.VERSION = G_VERSION
        self.UPDATE_URL = G_UPDATE_URL
        if not os.path.isdir(self.HOME_PATH):
            os.mkdir(self.HOME_PATH)
        try:
            _thread.start_new_thread(self.check_update, ())
        except:
            pass
        wx.App.__init__(self)


    def check_update(self):
        apppath = os.path.abspath(sys.argv[0])
        appname = os.path.split(apppath)[-1]
        updateurl = os.path.join(G_UPDATE_URL, "update")
        data = json.loads(request.urlopen(updateurl).read())
        config_path = G_CONFIG_PATH
        config = dict()
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            config["facility"]["version"] = G_VERSION
            config["facility"]["name"] = appname
            config["facility"]["path"] = apppath
        else:
            config = {
                "update": {
                    "version": "0.0.0",
                    "name": "-",
                    "path": "-"
                }, 
                "facility": {
                    "version": G_VERSION,
                    "name": appname,
                    "path": apppath
                },
                "latest_facility": {
                    "version": G_VERSION,
                    "name": appname,
                    "path": apppath
                }
            }
        remote_update = data["update"]["Windows"]
        remote_latest = data["latest"]
        ## 更新 update 程序
        if remote_update["version"] > config["update"]["version"]:
            _url = os.path.join(G_UPDATE_URL, remote_update["name"])
            _localpath = os.path.join(G_HOME_PATH, remote_update["name"])
            urllib.request.urlretrieve(_url, _localpath)
            
            config["update"]["version"] = remote_update["version"]
            config["update"]["name"] = remote_update["name"]
            config["update"]["path"] = _localpath
            with open(config_path, 'w') as f:
                json.dump(config, f)
        ## 检查预更新版本是否为最新
        if remote_latest["version"] > config["latest_facility"]["version"]:
            _url = os.path.join(G_UPDATE_URL, remote_latest["name"])
            _localpath = os.path.join(G_HOME_PATH, remote_latest["name"])
            urllib.request.urlretrieve(_url, _localpath)
            
            config["latest_facility"]["version"] = remote_latest["version"]
            config["latest_facility"]["name"] = remote_latest["name"]
            config["latest_facility"]["path"] = _localpath
            with open(config_path, 'w') as f:
                json.dump(config, f)
        ## 检查是否更新到最新版本
        if config["latest_facility"]["version"] > config["facility"]["version"]:
            self.updateButton.SetLabel("有新版本，点击更新")
            self.updateButton.Enable(True)
        else:
            self.updateButton.SetLabel("当前已是最新版本")
        self.config = config


    def OnInit(self):
        framestyle=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN
        app_title = "%s-v%s" % (self.APP_NAME, self.VERSION)
        frame = wx.Frame(parent=None, title=app_title, size=(600,400), style=framestyle)
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
        Popen(self.config["update"]["path"])
        wx.Exit()


def main():
    app = MainWindow()
    app.MainLoop()


if __name__ == '__main__':
    main()


