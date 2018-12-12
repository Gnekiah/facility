#-------------------------------------------------------------------------------
# Name:        watermark
#
# Author:      Ekira
#
# Created:     12/10/2018
# Copyright:   (C) Ekira 2017
# Licence:     <GNU Lesser General Public License>
#-------------------------------------------------------------------------------

# -*- coding: utf-8 -*- #

import os, time
import wx
from wx import FontEnumerator
import platform
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def txt_to_wm(txt, font, fontsize, fontcolor):
    imgfont = ImageFont.truetype(font=font, size=fontsize)
    x = 5
    y = 5
    width = 10
    height = 10
    for i in txt:
        w,h = imgfont.getsize(i)
        width += w
        height += h
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    for i in txt:
        draw.text(xy=(x,y), text=i, fill=fontcolor, font=imgfont)
        w,h = imgfont.getsize(i)
        x += w
    return img
    
    
def embed_img(srcpath, tgtpath, wmimg, transp, pos, prop, lr, tb):
    filename = srcpath.split('/')[-1].split('\\')[-1]
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
        
    targetpath = os.path.join(tgtpath, _filename + _filetype)
    while os.path.exists(targetpath):
        targetpath = os.path.join(tgtpath,  _filename + "-" + str(int(time.time())) + _filetype)

    srcimg = Image.open(srcpath)
    tgtimg = Image.new('RGBA', srcimg.size, (0, 0, 0, 0))
    
    srcw = srcimg.size[0]
    srch = srcimg.size[1]
    owmw = wmimg.size[0]
    owmh = wmimg.size[1]
    twmw = round(srcw * prop)
    twmh = round((owmh * srcw * prop) / owmw)
    lr = round(lr * srcw)
    tb = round(tb * srch)
    region = None
    if pos == 1:        ## 左上
        region = [lr, tb, lr+twmw, tb+twmh]
    elif pos == 2:      ## 左下
        region = [lr, srch-tb-twmh, lr+twmw, srch-tb]
    elif pos == 3:      ## 右上
        region = [srcw-lr-twmw, tb, srcw-lr, tb+twmh]
    elif pos == 4:      ## 右下
        region = [srcw-lr-twmw, srch-tb-twmh, srcw-lr, srch-tb]
    else:
        return "位置选择出错\n\r"
        
    wmimg = wmimg.convert("RGBA")
    r,g,b,alpha = wmimg.split()
    alpha = alpha.point(lambda i: i>0 and round(255*transp))
    wmimg.putalpha(alpha)
    wmimg = wmimg.resize((twmw, twmh))
    tgtimg.paste(srcimg,(0,0))
    tgtimg.paste(wmimg,region,wmimg)
    if _filetype.lower != ".png":
        tgtimg = tgtimg.convert("RGB")
    tgtimg.save(targetpath)
    return "嵌入成功：%s\n\r" % srcpath
    

class WatermarkWindow(wx.Dialog):
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
        p_watermark = wx.Button(parent=panel, label="水印图片", pos=(10,80))
        p_watermark_path = wx.StaticText(parent=panel, label="", pos=(125,85))
        
        wx.StaticText(parent=panel, label="横边距", pos=(10,120))
        p_pos_width = wx.TextCtrl(parent=panel, pos=(70,115), size=(50,30))
        wx.StaticText(parent=panel, label="纵边距", pos=(125,120))
        p_pos_height = wx.TextCtrl(parent=panel, pos=(185, 115), size=(50,30))
        
        wx.StaticText(parent=panel, label="透明度", pos=(245,120))
        p_transp = wx.TextCtrl(parent=panel, pos=(305, 115), size=(50,30))
        wx.StaticText(parent=panel, label="占比", pos=(365,120))
        p_prop = wx.TextCtrl(parent=panel, pos=(405, 115), size=(50,30))
        p_imgwm = wx.Button(parent=panel, label="嵌入图片", pos=(465,115))
        p_pos = wx.RadioBox(parent=panel, label="位置", pos=(10,150), choices=['左上','左下','右上','右下'], majorDimension=4)
        
        p_tmp1 = wx.StaticText(parent=panel, label="水印文字", pos=(10,230))
        p_txt = wx.TextCtrl(parent=panel, pos=(90, 225), size=(370,30))
        p_tmp2 = wx.StaticText(parent=panel, label="字体", pos=(300,155))
        ##fontlist = wx.FontEnumerator().GetFacenames()
        fontlist = os.listdir("C:/Windows/Fonts/")
        p_font = wx.ComboBox(panel, -1, pos=(340,150), size=(235,30), choices=fontlist, style=wx.CB_SORT)
        p_tmp3 = wx.StaticText(parent=panel, label="字号", pos=(300,190))
        p_fontsize = wx.TextCtrl(parent=panel, pos=(340, 185), size=(50,30))
        p_tmp4 = wx.StaticText(parent=panel, label="颜色", pos=(395,190))
        p_fontcolor = wx.TextCtrl(parent=panel, pos=(435, 185), size=(135,30))
        p_txtwm = wx.Button(parent=panel, label="嵌入文字", pos=(465,225))
        p_log = wx.TextCtrl(parent=panel, pos=(10,260), size=(565, 195), style=wx.TE_READONLY | wx.TE_MULTILINE)

        p_pos_width.SetValue("0.04")
        p_pos_height.SetValue("0.04")
        p_transp.SetValue("0.3")
        p_prop.SetValue("0.15")
        p_fontsize.SetValue("18")
        p_fontcolor.SetValue("125,125,125")

        if(platform.system() == "Windows"):
            pass
        else:
            p_tmp1.Enable(False)
            p_txt.Enable(False)
            p_tmp2.Enable(False)
            p_font.Enable(False)
            p_tmp3.Enable(False)
            p_fontsize.Enable(False)
            p_tmp4.Enable(False)
            p_fontcolor.Enable(False)
            p_txtwm.Enable(False)
            
        self.panel = panel
        self.p_origin = p_origin
        self.p_origin_path = p_origin_path
        self.p_target = p_target
        self.p_target_path = p_target_path
        self.p_watermark = p_watermark
        self.p_watermark_path = p_watermark_path
        
        self.p_pos_width = p_pos_width
        self.p_pos_height = p_pos_height
        self.p_transp = p_transp
        self.p_prop = p_prop
        self.p_imgwm = p_imgwm
        self.p_pos = p_pos
        
        self.p_txt = p_txt
        self.p_font = p_font
        self.p_fontsize = p_fontsize
        self.p_fontcolor = p_fontcolor
        self.p_txtwm = p_txtwm
        self.p_log = p_log
        
        self.fontdata = None
        self.srcpaths = list()
        self.tgtpath = str()
        self.wmpath = str()

        self.Bind(wx.EVT_BUTTON, self.OnOriginButton, p_origin)
        self.Bind(wx.EVT_BUTTON, self.OnTargetButton, p_target)
        self.Bind(wx.EVT_BUTTON, self.OnWatermarkButton, p_watermark)
        self.Bind(wx.EVT_BUTTON, self.OnImgwmButton, p_imgwm)
        self.Bind(wx.EVT_BUTTON, self.OnTxtwmButton, p_txtwm)

        
    def OnOriginButton(self, event):
        filesFilter = "所有文件|*.*|BMP (*.bmp)|*.bmp|PNG (*.png)|*.png|JPG (*.jpg)|*.jpg|JPEG (*.jpeg)|*.jpeg"
        dlg = wx.FileDialog(parent=self.panel, message="选择原始文件", wildcard=filesFilter, style=wx.FD_OPEN|wx.FD_MULTIPLE)
        dialogResult = dlg.ShowModal()
        if dialogResult !=  wx.ID_OK:
            return
        paths = dlg.GetPaths()
        self.p_origin_path.SetLabel('')
        pathstr = str()
        self.srcpaths.clear()
        for path in paths:
            pathstr += path + "|"
            self.srcpaths.append(path)
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

        
    def OnWatermarkButton(self, event):
        filesFilter = "所有文件|*.*|BMP (*.bmp)|*.bmp|PNG (*.png)|*.png|JPG (*.jpg)|*.jpg|JPEG (*.jpeg)|*.jpeg"
        dlg = wx.FileDialog(parent=self.panel, message="选择水印图片", wildcard=filesFilter, style=wx.FD_OPEN)
        dialogResult = dlg.ShowModal()
        if dialogResult !=  wx.ID_OK:
            dlg.Destroy()
            return
        path = dlg.GetPath()
        self.p_watermark_path.SetLabel(path)
        self.wmpath = path
        dlg.Destroy()
        

    def OnImgwmButton(self, event):
        srcpaths = self.srcpaths
        tgtpath = self.tgtpath
        wmpath = self.wmpath
        log = self.p_log
        transp = self.p_transp.GetValue()
        prop = self.p_prop.GetValue()
        pos_width = self.p_pos_width.GetValue()
        pos_height = self.p_pos_height.GetValue()
        pos = 0
        posval = self.p_pos.GetStringSelection()
        ret = str()
        if posval == '左上': pos = 1
        elif posval == '左下': pos = 2
        elif posval == '右上': pos = 3
        elif posval == '右下': pos = 4
        else: ret += "===位置选择出错===\r"
        if len(srcpaths) == 0: ret += "===未选择原始文件===\r"
        if tgtpath == "": ret += "===未选择保存路径===\r"
        if not os.path.exists(wmpath): ret += "===水印文件不存在===\r"
        
        try:
            transp = float(transp)
            prop = float(prop)
            pos_width = float(pos_width)
            pos_height = float(pos_height)
        except:
            ret += "===边距比例、透明度和占比值介于0-1之间===\r"
            log.AppendText(ret + "\n\r")
            return
            
        if transp < 0 or transp > 1: ret += "===透明度应介于0-1之间===\r"
        if prop <= 0 or prop >= 1: ret += "===占比应介于0-1之间===\r"
        if pos_width <= 0 or pos_width >= 1: ret += "===横边距比值应介于0-1之间===\r"
        if pos_height <= 0 or pos_height >= 1: ret += "===纵边距比值应介于0-1之间===\r"
        if ret:
            log.AppendText(ret + "\n\r")
            return
            
        self.p_origin.Enable(False)
        self.p_target.Enable(False)
        self.p_watermark.Enable(False)
        self.p_imgwm.Enable(False)
        self.p_pos.Enable(False)
        self.p_transp.Enable(False)
        self.p_prop.Enable(False)
        self.p_pos_width.Enable(False)
        self.p_pos_height.Enable(False)

        for srcpath in srcpaths:
            try:
                wmimg = Image.open(wmpath)
                ret = embed_img(srcpath, tgtpath, wmimg, transp, pos, prop, pos_width, pos_height)
                log.AppendText(ret)
            except Exception as e:
                print (e)
                log.AppendText("===嵌入图片水印失败===%s\n\r" % srcpath)
        
        self.p_origin.Enable(True)
        self.p_target.Enable(True)
        self.p_watermark.Enable(True)
        self.p_imgwm.Enable(True)
        self.p_pos.Enable(True)
        self.p_transp.Enable(True)
        self.p_prop.Enable(True)
        self.p_pos_width.Enable(True)
        self.p_pos_height.Enable(True)

    
    def OnTxtwmButton(self, event):
        srcpaths = self.srcpaths
        tgtpath = self.tgtpath
        log = self.p_log
        transp = self.p_transp.GetValue()
        prop = self.p_prop.GetValue()
        pos_width = self.p_pos_width.GetValue()
        pos_height = self.p_pos_height.GetValue()
        pos = None
        posval = self.p_pos.GetStringSelection()
        font = self.p_font.GetStringSelection()
        fontsize = self.p_fontsize.GetValue()
        fontcolorval = self.p_fontcolor.GetValue()
        fontcolor = None
        txt = self.p_txt.GetValue()
        ret = str()
        if posval == '左上': pos = 1
        elif posval == '左下': pos = 2
        elif posval == '右上': pos = 3
        elif posval == '右下': pos = 4
        else: ret += "===位置选择出错===\r"
        if len(srcpaths) == 0: ret += "===未选择原始文件===\r"
        if tgtpath == "": ret += "===未选择保存路径===\r"
        
        try:
            transp = float(transp)
            prop = float(prop)
            pos_width = float(pos_width)
            pos_height = float(pos_height)
        except:
            ret += "===边距比例、透明度和占比值介于0-1之间===\r"
            log.AppendText(ret + "\n\r")
            return
        try:
            fontsize = int(fontsize)
            fontcolor_list = fontcolorval.split(",")
            if len(fontcolor_list) != 3:
                raise Exception
            fontcolor = [int(fontcolor_list[0]), int(fontcolor_list[1]), int(fontcolor_list[2])]
            for i in range(0,3):
                if fontcolor[i] < 0 or fontcolor[i] > 255:
                    raise Exception
        except:
            ret += "===字号值为大于0的整数，颜色为RGB格式===\r"
            log.AppendText(ret + "\n\r")
            return
        
        if transp < 0 or transp > 1: ret += "===透明度应介于0-1之间===\r"
        if prop <= 0 or prop >= 1: ret += "===占比应介于0-1之间===\r"
        if pos_width <= 0 or pos_width >= 1: ret += "===横边距比值应介于0-1之间===\r"
        if pos_height <= 0 or pos_height >= 1: ret += "===纵边距比值应介于0-1之间===\r"
        if not font: ret += "===请选择字体===\r"
        if not txt: ret += "===请输入要嵌入的内容===\r"
        if ret:
            log.AppendText(ret + "\n\r")
            return
        
        self.p_origin.Enable(False)
        self.p_target.Enable(False)
        self.p_watermark.Enable(False)
        self.p_imgwm.Enable(False)
        self.p_pos.Enable(False)
        self.p_transp.Enable(False)
        self.p_prop.Enable(False)
        self.p_pos_width.Enable(False)
        self.p_pos_height.Enable(False)
        self.p_txt.Enable(False)
        self.p_font.Enable(False)
        self.p_fontsize.Enable(False)
        self.p_fontcolor.Enable(False)
        self.p_txtwm.Enable(False)

        font = os.path.join("C:/Windows/Fonts/", font)
        for srcpath in srcpaths:
            try:
                wmimg = txt_to_wm(txt, font, fontsize, tuple(fontcolor))
                if not wmimg:
                    raise Exception
                ret = embed_img(srcpath, tgtpath, wmimg, transp, pos, prop, pos_width, pos_height)
                log.AppendText(ret)
            except Exception as e:
                log.AppendText("===嵌入图片水印失败===%s\n\r" % srcpath)
    
        self.p_origin.Enable(True)
        self.p_target.Enable(True)
        self.p_watermark.Enable(True)
        self.p_imgwm.Enable(True)
        self.p_pos.Enable(True)
        self.p_transp.Enable(True)
        self.p_prop.Enable(True)
        self.p_pos_width.Enable(True)
        self.p_pos_height.Enable(True)
        self.p_txt.Enable(True)
        self.p_font.Enable(True)
        self.p_fontsize.Enable(True)
        self.p_fontcolor.Enable(True)
        self.p_txtwm.Enable(True)
    