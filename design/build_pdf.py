from pathlib import Path
from xml.sax.saxutils import escape
import os
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable, KeepTogether
from math import atan2, sin, cos

root = Path(__file__).resolve().parents[1]
out = root / 'output/pdf'
out.mkdir(parents=True, exist_ok=True)
font = os.environ.get('LABMATE_CJK_FONT', 'C:/Windows/Fonts/msyh.ttc')
pdfmetrics.registerFont(TTFont('CJK', font, subfontIndex=0))
navy = colors.HexColor('#193548')
teal = colors.HexColor('#087c75')
mist = colors.HexColor('#ebf6f4')
ink = colors.HexColor('#253943')
pale = colors.HexColor('#dde9ed')

def style(name, size, leading, before=0, after=0, color=ink):
    return ParagraphStyle(name, fontName='CJK', fontSize=size, leading=leading, keepWithNext=name=='h2',
                          wordWrap='CJK', spaceBefore=before, spaceAfter=after, textColor=color)
title = style('title', 27, 39, after=6, color=navy)
h2 = style('h2', 15, 22, 13, 5, teal)
body = style('body', 10.3, 15, after=4)
small = style('small', 9, 14)
sub = style('sub', 9.5, 16, after=15, color=teal)

def para(txt, s=body):
    return Paragraph(escape(txt), s)

figs = [
 ('图 1  使用者与管理人员用例', [('使用者',58,91),('核验身份与培训',235,115),('开打前检查',235,75),('请求视觉指导',405,75),('协会管理人员',58,29),('查看记录与现场复核',235,29)], [(0,1,''),(0,2,''),(2,3,'可选'),(4,5,'')]),
 ('图 2  准入与检查活动图', [('入口锁定',60,130),('身份与资格均通过？',232,130),('保持锁定并指引',402,130),('进入检查及可选指导',232,79),('必要条件满足？',232,27),('说明缺项／转复核',60,27),('保存通过记录',402,27)], [(0,1,''),(1,2,'否'),(1,3,'是'),(3,4,''),(4,5,'否'),(4,6,'是')]),
 ('图 3  服务与会话类关系', [('准入服务',63,132),('检查服务',232,132),('设备状态适配器',400,132),('检查会话',142,79),('视觉指导服务',320,79),('资料目录',232,27),('摄像头工具',400,27)], [(0,3,''),(1,3,''),(1,2,'只读'),(4,3,'读上下文'),(4,5,''),(4,6,'')]),
 ('图 5  关键对象协作图', [('页面对象',61,141),('准入对象',228,141),('记录库',402,141),('视觉指导对象',61,83),('摄像头工具',228,83),('资料目录',402,83),('检查对象',61,25),('设备适配器',228,25)], [(0,1,'1 核验'),(1,2,'1.1 查培训'),(0,3,'2 指导'),(3,4,'2.1 取帧'),(4,5,''),(3,6,''),(6,7,'3.1 读状态'),(7,2,'3.2 结果')]),
 ('图 1  核心实体关系图（连线 1:N，指导引用资料可空）', [('用户',55,187),('培训结果',227,187),('设备',402,187),('检查会话',227,125),('检查项结果',58,90),('状态快照',398,104),('指导记录',227,63),('审计事件',58,32),('知识条目',398,38)], [(0,1,'1:N'),(2,1,'1:N'),(0,3,'1:N'),(2,3,'1:N'),(3,4,'1:N'),(3,5,'1:N'),(3,6,'1:N'),(3,7,'1:N'),(2,8,'1:N'),(8,6,'0..1:N')])
]
# The collaboration diagram shows independent calls to the tool and knowledge catalog.
figs[3] = (figs[3][0], [('页面对象',61,172),('准入对象',228,172),('记录库',402,172),('视觉指导对象',228,112),('摄像头工具',402,128),('资料目录',402,84),('检查对象',61,48),('设备适配器',228,48)], [(0,1,'1 核验'),(1,2,'1.1 查培训'),(0,3,'2 指导'),(3,4,'2.1 取帧'),(3,5,'2.2 查资料'),(0,6,'3 提交'),(6,7,'3.1 读状态')])

class Diagram(Flowable):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.width = 466
        self.height = max(y for _, _, y in data[1]) + 39 if data else 213

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor('#f8fbfc'))
        c.setStrokeColor(pale)
        c.roundRect(0, 0, self.width, self.height, 8, stroke=1, fill=1)
        if not self.data:
            self.sequence()
            return
        label, boxes, edges = self.data
        for i,j,t in edges:
            _,x,y = boxes[i]
            _,xx,yy = boxes[j]
            dx,dy = xx-x,yy-y
            cut = min(57/abs(dx) if dx else 99, 11/abs(dy) if dy else 99)
            a,b,d,e = x+dx*cut,y+dy*cut,xx-dx*cut,yy-dy*cut
            self.arrow(a,b,d,e)
            if t:
                c.setFont('CJK', 8)
                c.setFillColor(teal)
                c.drawCentredString((a+d)/2+ (12 if not dx else 0),(b+e)/2+4,t)
        for t,x,y in boxes:
            c.setFillColor(mist)
            c.setStrokeColor(pale)
            c.roundRect(x-54,y-11,108,22,5,stroke=1,fill=1)
            c.setFillColor(navy)
            c.setFont('CJK',9)
            c.drawCentredString(x,y-3,t)
        self.caption(label)

    def caption(self,label):
        self.canv.setFillColor(navy)
        self.canv.setFont('CJK',10)
        self.canv.drawString(13,self.height-16,label)

    def arrow(self,x,y,a,b):
        c=self.canv
        c.setStrokeColor(teal)
        c.setLineWidth(.65)
        c.line(x,y,a,b)
        angle=atan2(b-y,a-x)
        for d in (-.5,.5):
            c.line(a,b,a-5*cos(angle+d),b-5*sin(angle+d))

    def sequence(self):
        self.caption('图 4  准入、视觉指导与检查提交时序')
        c=self.canv
        xs=[49,137,227,324,412]
        for x,n in zip(xs,['使用者','页面','准入服务','检查服务','视觉指导']):
            c.setFillColor(mist)
            c.roundRect(x-39,165,78,20,4,fill=1,stroke=0)
            c.setFillColor(navy); c.setFont('CJK',9); c.drawCentredString(x,172,n)
            c.setStrokeColor(pale); c.line(x,165,x,14)
        for i,j,y,t in [(0,1,150,'开始核验'),(1,2,132,'核对资格'),(2,1,114,'锁定／发放会话'),(1,4,96,'通过且需指导时请求'),(4,1,78,'提示／无法判断'),(1,3,60,'提交确认项'),(3,2,42,'重核资格'),(3,1,24,'返回检查结果')]:
            self.arrow(xs[i],y,xs[j],y)
            c.setFillColor(navy); c.setFont('CJK',8); c.drawCentredString((xs[i]+xs[j])/2,y+3,t)

def footer(c, doc):
    c.setStrokeColor(pale); c.line(54,43,541,43)
    c.setFont('CJK',8.5); c.setFillColor(teal)
    c.drawString(54,29,'LABMATE / 啊对对队 / 设计评审')
    c.drawRightString(541,29,f'{doc.page:02d}')

def build(src, name):
    story, idx = [], 0
    lines = iter(src.read_text(encoding='utf-8').splitlines())
    for l in lines:
        if l.startswith('```'):
            for x in lines:
                if x.startswith('```'): break
            d = Diagram(figs[4]) if src.stem == 'database' else Diagram(None if idx == 3 else figs[idx if idx < 3 else 3])
            story += [d, Spacer(1,8)]; idx+=1
        elif l.startswith('# '):
            story.append(para(l[2:],title))
        elif l.startswith('## '):
            story.append(para(l[3:],h2))
        elif l.startswith('啊对对队'):
            story.append(para(l,sub))
        elif l.startswith('| 实体'):
            rows=[[para(v.strip(),small) for v in l.strip('|').split('|')]]
            for x in lines:
                if not x.startswith('|'): break
                if not x.startswith('|---'):
                    rows.append([para(v.strip(),small) for v in x.strip('|').split('|')])
            t=Table(rows,colWidths=[155,312],repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),mist),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.4,pale),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            story.append(t)
        elif l.strip():
            story.append(para(l))
    SimpleDocTemplate(str(out/name),pagesize=A4,leftMargin=54,rightMargin=54,
                      topMargin=48,bottomMargin=59,title=name[:-4],author='LabMate').build(story,onFirstPage=footer,onLaterPages=footer)

build(root/'design/system.md','啊对对队_系统设计说明书.pdf')
build(root/'design/database.md','啊对对队_数据库设计说明书.pdf')
