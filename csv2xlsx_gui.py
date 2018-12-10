#-------------------------------------------------------------------------------
# Name:        csv2xlsx GUI
# Purpose:     csv to xlsx
#
# Author:      Ekira
#
# Created:     09/02/2017
# Modified:    12/10/2018
# Copyright:   (C) Ekira 2017
# Licence:     <GNU Lesser General Public License>
#-------------------------------------------------------------------------------

# -*- coding: utf-8 -*- #

import xlwt, csv, os
import codecs, chardet
import wx
import time


def csv_to_xlsx(filepath, tgtdirpath):
    filename = filepath.split('/')[-1].split('\\')[-1]
    _filename = filename[:-4]
    targetpath = os.path.join(tgtdirpath, _filename + ".xlsx")
    while os.path.exists(targetpath):
        targetpath = os.path.join(tgtdirpath,  _filename + "-" + str(int(time.time())) + ".xlsx")
    ret = str()

    f = open(filepath, "rb")
    encoding = chardet.detect(f.read(1024))["encoding"]
    if encoding == "GB2312":
        encoding = "gbk"
    f.close()

    with codecs.open(filepath, 'r', encoding=encoding) as f:
        read = csv.reader(f)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(_filename)
        l = 0
        for line in read:
            r = 0
            for i in line:
                sheet.write(l, r, i)
                r += 1
            l += 1
        workbook.save(targetpath)
        ret = "成功，原始文件编码：%s，文件 %s 转换为 %s\n\r" % (encoding, filepath, targetpath)
    return ret


class Csv2XlsWindow(wx.Dialog):
    def __init__(self, parent, title, size):
        wx.Dialog.__init__(self, parent, title=title, size=size)
        self.InitUI()


    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL))

        p_origin = wx.Button(parent=panel, label="选择文件(夹)", pos=(10,10))
        p_origin_path = wx.StaticText(parent=panel, label="", pos=(160,10))
        p_target = wx.Button(parent=panel, label="选择保存路径", pos=(10,45))
        p_target_path = wx.StaticText(parent=panel, label="", pos=(160,50))
        p_run = wx.Button(parent=panel, label="开始转换", pos=(310,80))
        p_log = wx.TextCtrl(parent=panel, pos=(10,115), size=(465, 240), style=wx.TE_READONLY | wx.TE_MULTILINE)

        self.panel = panel
        self.p_origin = p_origin
        self.p_target = p_target
        self.p_run = p_run
        self.p_origin_path = p_origin_path
        self.p_target_path = p_target_path
        self.p_log = p_log
        self.paths = list()
        self.tgtpath = str()

        self.Bind(wx.EVT_BUTTON, self.OnOriginButton, p_origin)
        self.Bind(wx.EVT_BUTTON, self.OnTargetButton, p_target)
        self.Bind(wx.EVT_BUTTON, self.OnRunButton, p_run)

        
    def OnOriginButton(self, event):
        filesFilter = "Csv (*.csv)|*.csv"
        dlg = wx.FileDialog(parent=self.panel, message="选择原始文件", wildcard=filesFilter, style=wx.FD_OPEN|wx.FD_MULTIPLE)
        dialogResult = dlg.ShowModal()
        if dialogResult !=  wx.ID_OK:
            return
        paths = dlg.GetPaths()
        self.p_origin_path.SetLabel('')
        pathstr = str()
        self.paths.clear()
        for path in paths:
            pathstr += path + "|"
            self.paths.append(path)
        self.p_origin_path.SetLabel(pathstr)


    def OnTargetButton(self, event):
        dlg = wx.DirDialog (parent=self.panel, message="选择保存路径", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dialogResult = dlg.ShowModal()
        if dialogResult !=  wx.ID_OK:
            return
        path = dlg.GetPath()
        self.p_target_path.SetLabel(path)
        self.tgtpath = path


    def OnRunButton(self, event):
        paths = self.paths
        tgtpath = self.tgtpath
        log = self.p_log
        if len(paths) == 0 or not os.path.exists(tgtpath):
            return 

        self.p_origin.Enable(False)
        self.p_target.Enable(False)
        self.p_run.Enable(False)
        for path in paths:
            try:
                ret = csv_to_xlsx(path, tgtpath)
                log.AppendText(ret)
            except Exception as e:
                log.AppendText("===转换失败===%s\n\r" % path)
        self.p_origin.Enable(True)
        self.p_target.Enable(True)
        self.p_run.Enable(True)

    
