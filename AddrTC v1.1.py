'''
v1.1 待完善点：
1.启动时软件各个窗口居中显示（留1.2解决）
    解决方案：获取屏幕分辨率，计算中心位置并设置
2.菜单添加‘重新开始’按钮（留2.1解决）
    解决方案：用面向对象的方法重写软件
3.'使用帮助'窗口待完成（留1.2解决）
    解决方法：编写使用说明
4.更新日志超出窗口显示范围（留1.2解决）
    解决方法：用tkinter scrolledtext存放更新日志
5.分页模型和段页模型中，如果页面过多，页表显示不完全（留2.0解决解决）
    解决方法：用tkinter scrolledtext存放更新日志
'''
from tkinter import *
from datetime import datetime
import random
import math

'''全局变量区'''
memsize = 1024 * 1024  # 内存大小，1M~4M
processsize = 320 * 1024  # 进程大小，16K~1M
pagesize = 32 * 1024  # 页面大小1K~64K,缺省值32K
segnum = 5  # 进程分段数量4~7，缺省值5
schedule = 0

state = ('初始化系统参数', '选择内存管理模型', '分段模型', '分页模型', '段页式模型')
mycolor = ('blue', 'purple', 'red', 'black', 'brown', 'gray', 'silver')

'''逻辑代码区'''


def seg():
    '''将进程分段，每段分配合适的内存区域，返回段表'''
    '''
    +------+------+------+
    \段号  \段长  \基址  \
    +------+------+------+
    \      \      \      \
    +------+------+------+
    \      \      \      \
    +------+------+------+
    '''
    global memsize, processsize, segnum

    segs = []
    segs.append(processsize)
    for i in range(segnum - 1):
        l = random.randint(100, max(segs) - 100)
        s = max(segs) - l
        del segs[segs.index(max(segs))]
        segs.append(l)
        segs.append(s)

    holes = []
    if processsize == memsize:
        for i in range(segnum + 1):
            holes.append(0)
    else:
        holes.append(memsize - processsize)
        for i in range(segnum):
            l = random.randint(0, max(holes) - 1)
            s = max(holes) - l
            del holes[holes.index(max(holes))]
            holes.append(l)
            holes.append(s)

    segtable = []
    base = 0
    for i in range(segnum):
        length = segs[i]
        base = base + holes[i]
        segtable.append((i, length, base))
        base = base + length
    return segtable


def page():
    '''
    页表结构
    +------+------+
    \页号  \帧长  \
    +------+------+
    \      \      \
    +------+------+
    \      \      \
    +------+------+
    '''
    global memsize, processsize, pagesize
    freeframelist = [x for x in range(math.ceil(memsize / pagesize))]
    pagelist = []
    for i in range(math.ceil(processsize / pagesize)):
        chosenone = random.randint(0, len(freeframelist) - 1)
        myframe = freeframelist[chosenone]
        del freeframelist[chosenone]
        pagelist.append((i, myframe))
    return pagelist


def segpage():
    '''
    段页表结构
    +------+------+------+
    \段号  \页号  \块号  \
    +------+------+------+
    \      \      \      \
    +------+------+------+
    \      \      \      \
    +------+------+------+
    '''
    global memsize, processsize, pagesize

    segpagetable = []  # 段页表
    freeframelist = [x for x in range(math.ceil(memsize / pagesize))]  # 空闲帧号

    segs = []
    segs.append(processsize)
    for i in range(segnum - 1):
        l = random.randint(100, max(segs) - 100)
        s = max(segs) - l
        del segs[segs.index(max(segs))]
        segs.append(l)
        segs.append(s)

    for i in range(segnum):
        pagenum = math.ceil(segs[i] / pagesize)  # 每一段需要的页数
        pagelist = []
        # 为当前段分配所需要的页面，生成当前段的页表
        for pn in range(pagenum):
            # 从空闲帧中选择一帧分配给当前页
            chosenone = random.randint(0, len(freeframelist) - 1)
            myframe = freeframelist[chosenone]
            del freeframelist[chosenone]
            pagelist.append((pn, myframe))
        segpagetable.append((i, pagelist))

    return segpagetable


'''图形界面代码区'''


def help():
    '''
    此函数用于创建并显示帮助窗口
    '''
    addlog('查看使用帮助')
    helpWindow = Toplevel()
    helpWindow.title('使用帮助')
    helpWindow.geometry('600x400')


def whatsnew():
    '''
    此函数用于创建并显示版本更新记录
    '''
    addlog('查看更新日志')
    whatsnewWindow = Toplevel()
    whatsnewWindow.title('更新日志')
    whatsnewWindow.geometry('600x400')

    content = '''
    \t\tAddr v1.1更新记录:\n
    1.页面大小设置项添加‘内存可以分为xx块’字段
    2.选择内存管理模型界面添加每种模型的介绍
    3.系统日志区更新，滚动条始终最下
    4.系统日志区字体调大，提高界面友好性
    5.修复了如果内存分的页面过多，画布中数字重叠的bug
    6.添加输入框初次点击清空功能
    7.输入框提示字体调整为灰色，提高用户体验
    \n
    \t\tAddr v1.0更新记录:\n
    
    1.实现了模拟内存分段、生成段表、正确地址转换的功能\n
    2.实现了模拟内存分页、生成页表、正确地址转换的功能\n
    3.实现了模拟内存分段再分页、生成段页表、正确地址转换的功能\n
    4.制作了简单的图形界面,基本操作依靠鼠标完成\n
    4.实现了内存的图形化展示\n
    5.实现了软件的操作日志显示\n
    6.实现了软件的状态与进度条显示\n
    '''

    text = Label(whatsnewWindow, bg='#F0F0F0', text=content, justify=LEFT)
    text.pack(expand='yes', fill=BOTH)


def license():
    '''
    此函数用于创建并显示隐私条款
    '''
    addlog('查看许可证')
    licenseWindow = Toplevel(rootWindow)
    licenseWindow.title('许可证')
    licenseWindow.geometry('600x400')

    content ='GNU General Public License (GPL) version 3 或更新版本\n\n在尊重 GPLv3 许可证的前提下，你可以随意分发，修改或者出售此软件。\n\nAddrTC 项目使用 ' \
             '100% 透明的方式进行开发，对公众开放 源代码，使用 python3.6 环境。\n\n源代码： https://pan.baidu.com/s/14zivrP3Gbt5ZTqNi-QtFag  密码3ges  '

    text = Label(licenseWindow, bg='#F0F0F0', text=content)
    text.pack(expand='yes', fill=BOTH)



def about():
    '''
    此函数用于创建并显示关于窗口
    '''
    addlog('查看关于')
    aboutWindow = Toplevel()
    aboutWindow.title('关于')
    aboutWindow.geometry('300x200')

    content = 'AddrTC \n\nV1.1\n\n2018年9月10日'

    text = Label(aboutWindow, bg='#F0F0F0', text=content)
    text.pack(expand='yes', fill=BOTH)


def updateprogressbar():
    '''更新进度条'''
    global schedule, fill_line
    if schedule < 4:
        schedule = schedule + 1
    progressbar.delete(fill_line)
    fill_line = progressbar.create_rectangle(0, 0, 383 * schedule, 30, width=0, fill="blue")
    rootWindow.update()


def addlog(msg):
    log.config(state=NORMAL)
    now = datetime.now()
    log.insert(END, str(now) + '\t' + msg + '\n')
    log.config(state=DISABLED)
    log.yview_moveto(1)




def setmemsize(text):
    mb = pow(2, int(text))
    global memsize
    memsize = mb * 1024 * 1024
    v1.config(text=str(mb) + 'MB')
    graph.itemconfig(maxmem, text=str(hex(memsize - 1)))


def setprocesssize(text):
    global processsize
    processsize = int(text)
    kb = processsize / 1024
    v2.config(text=str(kb) + 'KB' + '\t内存占用率' + str(int(processsize / memsize * 100)) + '%')


def setpagesize(text):
    global pagesize
    pagesize = pow(2, int(text))
    kb = pagesize / 1024
    v3.config(text=str(kb) + 'KB' + '\t此进程需要' + str(processsize / pagesize) + '个页面\n'+'\t内存可分为' + str(memsize / pagesize) + '个页面')


def setsegnum(text):
    global segnum
    segnum = int(text)
    v4.config(text=str(segnum) + '个')


def init():
    global schedule
    updateprogressbar()
    status.config(text=state[1])
    cleartable()
    addlog('设置内存大小：' + str(memsize))
    addlog('设置页面大小：' + str(pagesize))
    addlog('设置分段数量' + str(segnum))
    addlog('设置进程大小' + str(processsize))
    #       选择内存管理模型
    Label(table, text='选择内存管理模型', font=("Arial, 12")).place(x=20, y=20)

    Button(table, text='分段式内存管理模型', command=selectseg).place(x=100, y=100)
    segsummary = '''
    按照用户进程中的自然段划分逻辑空间
    例如：用户的进程由主程序、两个子程序、栈和一段数据组成，五部分划分为 5 个段，
    每段都从 0 开始编址，并分配一段连续的地址空间（段内要求连续、段间不要求连续）
    其逻辑地址由段号 S 和偏移地址 W 两部分组成
    在段式系统中，段号和段内偏移量必须由用户提供，高级程序语言中，这个工作由编译程序完成'''
    Label(table, text=segsummary, justify=LEFT).place(x=230, y=60)

    Button(table, text='分页式内存管理模型', command=selectpage).place(x=100, y=200)
    pagesummary = '''
    将虚拟内存空间和物理内存空间皆划分为大小相同的页面，如4KB、8KB或16KB等，
    并以页面作为内存空间的最小分配单位，一个程序的一个页面可以存放在任意一个物理页面里。
    避免了产生外部碎片，提高了内存的利用率，提升了计算机的性能，以分页通过硬件机制实现，对用户透明'''
    Label(table, text=pagesummary, justify=LEFT).place(x=230, y=180)

    Button(table, text='段页式内存管理模型', command=selectsegpage).place(x=100, y=300)
    segpagesummary = '''
    在段页式存储中，每个分段又被分成若干个固定大小的页。'''
    Label(table, text=segpagesummary, justify=LEFT).place(x=230, y=280)

def cleartable():
    global table
    table.destroy()
    table = Frame(controlPanel, width=841, height=418)
    table.pack(side=BOTTOM)


def selectseg():
    # 更新界面
    updateprogressbar()
    status.config(text=state[2])
    cleartable()
    # 添加日志
    addlog('选择分段式内存管理模型')
    # 分页
    segtable = seg()
    # 更新界面
    addlog('生成段表：' + str(segtable))
    drawsegtable(segtable)
    drawseg(segtable)

    def cleardh(event):
        if dh.get() == '输入段号：':
            dh.set('')

    dh = StringVar()
    duanhao = Entry(table, textvariable=dh, fg=mycolor[5])
    duanhao.bind('<Button-1>', cleardh)
    dh.set('输入段号：')
    duanhao.place(x=300, y=130)

    def cleardpy(event):
        if dpy.get() == '输入段内地址：':
            dpy.set('')

    dpy = StringVar()
    duanpianyi = Entry(table, textvariable=dpy, fg=mycolor[5])
    duanpianyi.bind('<Button-1>', cleardpy)
    dpy.set('输入段内地址：')
    duanpianyi.place(x=300, y=180)

    def segtc():
        try:
            sn = int(duanhao.get())
            so = int(duanpianyi.get())
        except ValueError:
            return

        if sn >= segnum or sn < 0 or so < 0 or so >= segtable[sn][1]:
            addlog('输入逻辑地址：' + str(sn) + ':' + str(so) + ',越界！！')
            dz.set('地址越界')
        else:
            addr = segtable[sn][2] + so
            # 更新界面
            dz.set('物理地址：' + str(addr) + '    (' + str(hex(addr)) + ')')
            updateprogressbar()
            # 记录日志
            addlog('输入逻辑地址：' + str(sn) + ':' + str(so) + ',转换后得到物理地址：' + str(addr))
            # 映射图上标记
            graph.create_line(120,
                              550 - addr / memsize * 490,
                              290,
                              550 - addr / memsize * 490,
                              fill='red')
            graph.create_text(120, 550 - addr / memsize * 490, anchor=E, text=str(hex(addr)), font=("Arial, 10"))

    Button(table, text='>>>', command=segtc).place(x=470, y=150)

    dz = StringVar()
    dizhi = Entry(table, textvariable=dz, width=30, fg=mycolor[5])
    dizhi.config(state='readonly')
    dz.set('此处显示物理地址：')
    dizhi.place(x=550, y=150)


def drawsegtable(segtable):
    '''在控制面板绘制生成的段表'''
    head = ('段号', '段长', '段基址')
    # Label(table, text='段基址').place(x=40, y=40)
    for i in head:
        Label(table, text=i).place(x=40 + 60 * head.index(i), y=40)
    for item in segtable:
        Label(table, text=str(item[0])).place(x=45, y=60 + 20 * segtable.index(item))
        Label(table, text=str(item[1])).place(x=95, y=60 + 20 * segtable.index(item))
        Label(table, text=str(item[2])).place(x=160, y=60 + 20 * segtable.index(item))


def drawseg(segtable):
    '''在图形画布上画出分配的段'''
    global mycolor
    cl = mycolor[2]
    for item in segtable:
        graph.create_rectangle(140,
                               550 - int(item[1] + item[2]) / memsize * 490,
                               290,
                               550 - int(item[2] / memsize * 490),
                               fill=cl)

    graph.create_rectangle(260, 700, 280, 720, fill=cl, outline='black')
    graph.create_text(290, 710, anchor=W, text='本进程进程地址空间', font=("Arial, 9"))


def selectpage():
    updateprogressbar()
    status.config(text=state[3])
    cleartable()
    addlog('选择分页式内存管理模型')
    pagelist = page()
    addlog('生成页表：' + str(pagelist))
    drawpagetable(pagelist)
    drawpage(pagelist)

    def cleare(event):
        if e.get() == '此处输入逻辑地址：':
            e.set('')

    e = StringVar()
    logicaddr = Entry(table, textvariable=e, fg=mycolor[5])
    e.set('此处输入逻辑地址：')
    logicaddr.bind('<Button-1>', cleare)
    logicaddr.place(x=250, y=153)

    def pagetc():
        try:
            la = int(logicaddr.get())
        except ValueError:
            return

        if la >= processsize or la < 0:
            addlog('输入逻辑地址：' + str(la) + ',越界！！')
            yh.set('地址越界')
            py.set('地址越界')
            kh.set('地址越界')
            p.set('地址越界')
        else:
            pagenum = int(la / pagesize)  # 页号
            pageoffsets = la % pagesize  # 页内偏移
            framenum = pagelist[pagenum][1]  # 帧号
            addr = framenum * pagesize + pageoffsets
            # 更新界面
            yh.set('页号：' + str(pagenum))
            py.set('页内偏移：' + str(pageoffsets))
            kh.set('物理帧号：' + str(framenum))
            p.set('物理地址：' + str(addr) + '  (' + str(hex(addr)) + ')')
            updateprogressbar()
            # 记录日志
            addlog('输入逻辑地址：' + str(la) + ',转换后得到物理地址：' + str(addr))
            # 图形画布标记
            graph.create_line(120,
                              550 - addr / memsize * 490,
                              290,
                              550 - addr / memsize * 490,
                              fill='red')
            graph.create_text(120, 550 - addr / memsize * 490, anchor=E, text=str(hex(addr)), font=("Arial, 10"))

    Button(table, text='>>>', command=pagetc).place(x=420, y=150)

    yh = StringVar()
    yehao = Entry(table, textvariable=yh, width=30, fg=mycolor[5])
    yehao.config(state='readonly')
    yh.set('此处显示页号：')
    yehao.place(x=500, y=90)

    py = StringVar()
    yepianyi = Entry(table, textvariable=py, width=30, fg=mycolor[5])
    yepianyi.config(state='readonly')
    py.set('此处显示页内偏移：')
    yepianyi.place(x=500, y=130)

    kh = StringVar()
    kuaihao = Entry(table, textvariable=kh, width=30, fg=mycolor[5])
    kuaihao.config(state='readonly')
    kh.set('此处显示块号：')
    kuaihao.place(x=500, y=170)

    p = StringVar()
    physicaladdress = Entry(table, textvariable=p, width=30, fg=mycolor[5])
    physicaladdress.config(state='readonly')
    p.set('此处显示物理地址：')
    physicaladdress.place(x=500, y=210)


def drawpagetable(pagelist):
    '''在控制面板绘制生成的页表
    对多显示前式16项'''
    head = ('页号', '帧号')
    for i in head:
        Label(table, text=i).place(x=40 + 60 * head.index(i), y=40)
    for item in pagelist:
        Label(table, text=str(item[0])).place(x=45, y=60 + 20 * pagelist.index(item))
        Label(table, text=str(item[1])).place(x=105, y=60 + 20 * pagelist.index(item))
        if pagelist.index(item) == 15:
            break


def drawpage(pagelist):
    '''在图形画布上画出分配的页面'''
    global mycolor
    cl = mycolor[2]
    for i in range(int(memsize / pagesize)):
        graph.create_line(140,
                          60 + i * (pagesize / memsize * 490),
                          290,
                          60 + i * (pagesize / memsize * 490),
                          fill=mycolor[5])
        # 最多标记32块
        if int(memsize / pagesize) <= 32 :
            graph.create_text(292,
                              60 + (i + 0.5) * (pagesize / memsize * 490),
                              anchor=W,
                              text=str(int(memsize / pagesize) - i - 1),
                              font=("Arial, 8"))
        elif i % int(memsize / pagesize / 32) == 0:
            graph.create_text(292,
                              60 + (i + 0.5) * (pagesize / memsize * 490),
                              anchor=W,
                              text=str(int(memsize / pagesize) - i - 1),
                              font=("Arial, 8"))

    for item in pagelist:
        graph.create_rectangle(140,
                               550 - pagesize / memsize * 490 * (item[1] + 1),
                               290,
                               550 - pagesize / memsize * 490 * item[1],
                               fill=cl,
                               outline='')
    # 添加图例
    graph.create_rectangle(260, 700, 280, 720, fill=cl, outline='black')
    graph.create_text(290, 710, anchor=W, text='本进程进程地址空间', font=("Arial, 9"))


def selectsegpage():
    # 更新界面
    updateprogressbar()
    status.config(text=state[4])
    cleartable()
    # 添加日志
    addlog('选择段页式内存管理模型')

    segpagetable = segpage()
    addlog('生成段页表：'+str(segpagetable))
    drawsegpagetable(segpagetable)
    drawsegpage(segpagetable)

    def cleardh(event):
        if dh.get()=='输入段号：':
            dh.set('')

    dh = StringVar()
    duanhao = Entry(table, textvariable=dh, fg=mycolor[5])
    duanhao.bind('<Button-1>', cleardh)
    dh.set('输入段号：')
    duanhao.place(x=300, y=130)

    def cleardpy(event):
        if dpy.get()=='输入段内地址：':
            dpy.set('')

    dpy = StringVar()
    duanpianyi = Entry(table, textvariable=dpy, fg=mycolor[5])
    duanpianyi.bind('<Button-1>', cleardpy)
    dpy.set('输入段内地址：')
    duanpianyi.place(x=300, y=180)

    def segpagetc():
        try:
            sn = int(duanhao.get())
            so = int(duanpianyi.get())
        except ValueError:
            return

        if sn >= segnum or sn < 0 or so < 0 or so >= len(pagesize*segpagetable[sn][1]):
            addlog('输入逻辑地址：' + str(sn) + ':' + str(so) + ',越界！！')
            dz.set('地址越界')
        else:
            tt = int(so / pagesize)  # 段内子页表的页号
            tn = so % pagesize  # 页内偏移
            addr = segpagetable[sn][1][tt][1] * pagesize + tn
            # 更新界面
            dz.set('物理地址：' + str(addr) + '    (' + str(hex(addr)) + ')')
            updateprogressbar()
            # 记录日志
            addlog('输入逻辑地址：' + str(sn) + ':' + str(so) + ',转换后得到物理地址：' + str(addr))
            # 映射图上标记
            graph.create_line(120,
                              550 - addr / memsize * 490,
                              290,
                              550 - addr / memsize * 490,
                              fill='red')
            graph.create_text(120, 550 - addr / memsize * 490, anchor=E, text=str(hex(addr)), font=("Arial, 10"))

    Button(table, text='>>>', command=segpagetc).place(x=470, y=150)

    dz = StringVar()
    dizhi = Entry(table, textvariable=dz, width=30, fg=mycolor[5])
    dizhi.config(state='readonly')
    dz.set('此处显示物理地址：')
    dizhi.place(x=550, y=150)


def drawsegpagetable(segpagelist):
    '''在控制面板绘制生成的段页表'''

    # 画表头
    head = ('段号', '页号', '内存块号')
    for i in head:
        Label(table, text=i).place(x=40 + 60 * head.index(i), y=40)

    # 画段页表
    hig = 60  # 起始高度，每次增加20
    dt = 0
    for item in segpagelist:
        cl = mycolor[item[0]]
        Label(table, text=str(item[0]), fg=cl).place(x=45, y=hig + dt * 20)
        for itm in item[1]:
            Label(table, text=str(itm[0]), fg=cl).place(x=105, y=hig + dt * 20)  # 页号
            Label(table, text=str(itm[1]), fg=cl).place(x=175, y=hig + dt * 20)  # 块号
            dt += 1


def drawsegpage(segpagelist):
    '''在图形画布上画出分配的页面'''
    global mycolor
    # 内存分割成帧，并标记块号
    for i in range(int(memsize / pagesize)):
        graph.create_line(140,
                          60 + i * (pagesize / memsize * 490),
                          290,
                          60 + i * (pagesize / memsize * 490),
                          fill=mycolor[5])
        # 最多标记32块
        if int(memsize / pagesize) <= 32 :
            graph.create_text(292,
                              60 + (i + 0.5) * (pagesize / memsize * 490),
                              anchor=W,
                              text=str(int(memsize / pagesize) - i - 1),
                              font=("Arial, 8"))
        elif i % int(memsize / pagesize / 32) == 0:
            graph.create_text(292,
                              60 + (i + 0.5) * (pagesize / memsize * 490),
                              anchor=W,
                              text=str(int(memsize / pagesize) - i - 1),
                              font=("Arial, 8"))

    # 画每段的内存映射图
    for item in segpagelist:
        # 设置颜色
        cl = mycolor[item[0]]
        # 画该段内每一个内存页
        for itm in item[1]:
            graph.create_rectangle(140,
                                   550 - pagesize / memsize * 490 * (itm[1] + 1),
                                   290,
                                   550 - pagesize / memsize * 490 * itm[1],
                                   fill=cl,
                                   outline='')

    # 修改图例
    for i in range(segnum):
        cl = mycolor[i]
        graph.create_rectangle(260-i*30, 700, 280-i*30, 720, fill=cl, outline='black')

    graph.create_text(290, 710, anchor=W, text='本进程进程地址空间', font=("Arial, 9"))


'''主界面'''

rootWindow = Tk()
rootWindow.title('内存地址转换模拟器')

# 设定窗口大小
rootWindow.geometry('1280x800')
rootWindow.resizable(False, False)

# 设置窗口图标
rootWindow.iconbitmap('.\\Conversion_128px.ico')

# 设置菜单栏
manubar = Menu()
manubar.add_command(label='使用帮助', command=help)
manubar.add_command(label='更新日志', command=whatsnew)
manubar.add_command(label='许可', command=license)
manubar.add_command(label='关于', command=about)
rootWindow['menu'] = manubar

# 控制面板
controlPanel = Frame(rootWindow, height=450, width=847, bd=3, relief='sunken')
Label(controlPanel, text='控制面板区域').pack(side=TOP, anchor=W)
table = Frame(controlPanel, width=841, height=418)
table.pack(side=BOTTOM)
#       初始化系统参数
Label(table, text='初始化系统参数', font=("Arial, 12")).place(x=20, y=20)

Label(table, text='内存大小').place(x=100, y=70)
s1 = Scale(table, from_=0, to=2, resolution=1, orient=HORIZONTAL, length=400, command=setmemsize)
s1.set(0)
s1.place(x=170, y=50)
v1 = Label(table, text='默认大小1M')
v1.place(x=580, y=65)

Label(table, text='进程大小').place(x=100, y=120)
s2 = Scale(table, from_=16 * 1024, to=1024 * 1024, resolution=1024, orient=HORIZONTAL, length=400,
           command=setprocesssize)
s2.set(320 * 1024)
s2.place(x=170, y=100)
v2 = Label(table, text='默认大小320K')
v2.place(x=580, y=115)

Label(table, text='页面大小').place(x=100, y=170)
s3 = Scale(table, from_=10, to=16, resolution=1, orient=HORIZONTAL, length=400, command=setpagesize)
s3.set(15)
s3.place(x=170, y=150)
v3 = Label(table, text='默认大小32K')
v3.place(x=580, y=165)

Label(table, text='分段数量').place(x=100, y=220)
s4 = Scale(table, from_=4, to=7, resolution=1, orient=HORIZONTAL, length=400, command=setsegnum)
s4.set(5)
s4.place(x=170, y=200)
v4 = Label(table, text='默认数量5个')
v4.place(x=580, y=215)

Button(table, text='下一步', command=init).place(x=600, y=300)
#       选择内存管理模型
controlPanel.place(x=0, y=0)

# 图形展示区域
graphPanel = Frame(rootWindow, height=759, width=430, bd=10, relief='sunken')
graph = Canvas(graphPanel, height=739, width=410, bg='white')
mem = graph.create_rectangle(140, 60, 290, 550, fill='green', outline='white')
top = graph.create_line(120, 60, 290, 60, fill='red')
maxmem = graph.create_text(120, 60, anchor=E, text=str(hex(memsize - 1)), font=("Arial, 10"))
base = graph.create_line(120, 550, 290, 550, fill='red')
graph.create_text(120, 550, anchor=E, text='0x00000', font=("Arial, 10"))
#     图例
graph.create_rectangle(260, 660, 280, 680, fill='green', outline='black')
graph.create_text(290, 670, anchor=W, text='非本进程进程地址空间', font=("Arial, 9"))

graph.place(x=0, y=0)
Label(graphPanel, text='图形展示区域', bg='white').place(x=0, y=0, in_=graph)
graphPanel.place(x=850, y=0)

# 日志面板
logPanel = Frame(rootWindow, bd=3, relief='sunken')# , width=200, height=21
Label(logPanel, text='系统日志区域').pack(side=TOP, anchor=W)
#   滚动条
srl = Scrollbar(logPanel, orient=VERTICAL)
log = Text(logPanel, width=82, height=14, bg='#F0F0F0', relief='flat', state=DISABLED, font=("黑体", 14))
srl.config(command=log.yview)
log.config(yscrollcommand=srl.set)

log.pack(side=LEFT, fill=X)
srl.pack(side=RIGHT, fill=Y)
logPanel.place(x=0, y=450)

# 设置状态栏
status = Label(rootWindow, text=state[0], bd=1, relief='groove', height=1, width=18)
# status.pack(side=BOTTOM, fill=None, anchor=W)
status.place(x=0, y=760)

# 设置进度条
progressbar = Canvas(bg='white', height=30, width=1147)
out_line = progressbar.create_rectangle(0, 0, 1147, 30, width=0, outline="black")
fill_line = progressbar.create_rectangle(0, 0, 383 * schedule, 30, width=0, fill="blue")
progressbar.place(x=130, y=758)

addlog('启动模拟器')
# 父窗口开始事件循环
rootWindow.mainloop()


