#-------------------------------------------------------------------------------
# Name:        xls2csv GUI
# Purpose:     xls to csv & csv to xls
#
# Author:      Ekira
#
# Created:     09/02/2017
# Modified:    12/10/2018
# Copyright:   (C) Ekira 2017
# Licence:     <GNU Lesser General Public License>
#-------------------------------------------------------------------------------

# -*- coding: utf-8 -*- #

import xlrd, csv, os
import codecs
import wx
import time


def xlsx_to_csv(filepath, tgtdirpath, encoding):
    workbook = xlrd.open_workbook(filepath)
    filename = filepath.split('/')[-1].split('\\')[-1]
    _filename = filename[:-5] if filename[-1]=='x' else filename[:-4]
    ret = str()
    sheetnames = workbook.sheet_names()
    for i in range(len(sheetnames)):
        sheetname = sheetnames[i]
        sheetname = sheetname.replace("/","").replace("\\","").strip()
        if len(sheetnames) != 1:
            _filename += ('-' + sheetname)
        targetpath = os.path.join(tgtdirpath,  _filename + ".csv")
        table = workbook.sheet_by_index(i)
        while os.path.exists(targetpath):
            targetpath = os.path.join(tgtdirpath,  _filename + "-" + str(int(time.time())) + ".csv")

        with codecs.open(targetpath, 'w', encoding=encoding) as f:
            write = csv.writer(f)
            for row_num in range(table.nrows):
                row_value = table.row_values(row_num)
                write.writerow(row_value)
        ret += "成功，文件 %s 的表格 %s 转换为 %s\n\r" % (filepath, sheetname, targetpath)
    return ret


class Xls2CsvWindow(wx.Dialog):
    def __init__(self, parent, title, size):
        wx.Dialog.__init__(self, parent, title=title, size=size)
        self.InitUI()


    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL))

        p_origin = wx.Button(parent=panel, label="选择文件", pos=(10,10))
        p_origin_path = wx.StaticText(parent=panel, label="", pos=(125,15))
        p_target = wx.Button(parent=panel, label="保存路径", pos=(10,45))
        p_target_path = wx.StaticText(parent=panel, label="", pos=(125,50))
        p_format = wx.RadioBox(parent=panel, label="目标编码:", pos=(10,80), choices=['gbk','utf-8'], majorDimension=2)
        p_run = wx.Button(parent=panel, label="开始转换", pos=(290,100))
        p_log = wx.TextCtrl(parent=panel, pos=(10,160), size=(465, 190), style=wx.TE_READONLY | wx.TE_MULTILINE)

        self.panel = panel
        self.p_origin = p_origin
        self.p_target = p_target
        self.p_run = p_run
        self.p_origin_path = p_origin_path
        self.p_target_path = p_target_path
        self.p_format = p_format
        self.p_log = p_log
        self.paths = list()
        self.tgtpath = str()

        self.Bind(wx.EVT_BUTTON, self.OnOriginButton, p_origin)
        self.Bind(wx.EVT_BUTTON, self.OnTargetButton, p_target)
        self.Bind(wx.EVT_BUTTON, self.OnRunButton, p_run)

        
    def OnOriginButton(self, event):
        filesFilter = "所有文件|*.*|Excel (*.xlsx)|*.xlsx|Excel (*.xls)|*.xls"
        dlg = wx.FileDialog(parent=self.panel, message="选择原始文件", wildcard=filesFilter, style=wx.FD_OPEN|wx.FD_MULTIPLE)
        dialogResult = dlg.ShowModal()
        if dialogResult !=  wx.ID_OK:
            dlg.Destroy()
            return
        paths = dlg.GetPaths()
        self.p_origin_path.SetLabel('')
        pathstr = str()
        self.paths.clear()
        for path in paths:
            pathstr += path + "|"
            self.paths.append(path)
        self.p_origin_path.SetLabel(pathstr)
        dlg.Destroy()


    def OnTargetButton(self, event):
        dlg = wx.DirDialog (parent=self.panel, message="选择保存路径", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dialogResult = dlg.ShowModal()
        if dialogResult !=  wx.ID_OK:
            dlg.Destroy()
            return
        path = dlg.GetPath()
        self.p_target_path.SetLabel(path)
        self.tgtpath = path
        dlg.Destroy()


    def OnRunButton(self, event):
        paths = self.paths
        tgtpath = self.tgtpath
        encoding = self.p_format.GetStringSelection()
        log = self.p_log
        if len(paths) == 0 or not os.path.exists(tgtpath):
            return 

        self.p_origin.Enable(False)
        self.p_target.Enable(False)
        self.p_run.Enable(False)
        self.p_format.Enable(False)

        for path in paths:
            try:
                ret = xlsx_to_csv(path, tgtpath, encoding)
                log.AppendText(ret)
            except:
                log.AppendText("===转换失败===%s\n\r" % path)
        self.p_origin.Enable(True)
        self.p_target.Enable(True)
        self.p_run.Enable(True)
        self.p_format.Enable(True)

    
