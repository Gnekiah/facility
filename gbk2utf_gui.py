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
import codecs, chardet
import wx
import time


def gbk_to_utf(filepath, tgtdirpath, encoding):
    filename = filepath.split('/')[-1].split('\\')[-1]
    _fnamelist = filename.split(".")
    _filename = str()
    _filetype = str()
    targetpath = str()
    ret = str()
    if len(_fnamelist) == 1:
        _filename = filename
        _filetype = ""
    elif len(_fnamelist) == 2:
        _filename = _fnamelist[0]
        _filetype = "." + _fnamelist[-1]
    else:
        _filename = ".".join(_fnamelist[:-1])
        _filetype = "." + _fnamelist[-1]

    targetpath = os.path.join(tgtdirpath, _filename + _filetype)
    while os.path.exists(targetpath):
        targetpath = os.path.join(tgtdirpath,  _filename + "-" + str(int(time.time())) + _filetype)

    f = open(filepath, "rb")
    from_encoding = chardet.detect(f.read(1024))["encoding"]
    if from_encoding == "GB2312":
        from_encoding = "gbk"
    f.close()

    data = None
    with open(filepath, encoding=from_encoding) as f:
        data = f.read()
    with open(targetpath, 'w', encoding=encoding) as f:
        f.write(data)

    ret = "成功，文件 %s 转换为 %s\n\r" % (filepath, targetpath)
    return ret


class Gbk2UtfWindow(wx.Dialog):
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
        filesFilter = "所有文件|*.*"
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
                ret = gbk_to_utf(path, tgtpath, encoding)
                log.AppendText(ret)
            except Exception as e:
                log.AppendText("===转换失败===%s\n\r" % path)
        self.p_origin.Enable(True)
        self.p_target.Enable(True)
        self.p_run.Enable(True)
        self.p_format.Enable(True)

    
