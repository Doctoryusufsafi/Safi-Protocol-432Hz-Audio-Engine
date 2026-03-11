# SAFI PROTOCOL DSP ENGINE v5.0 - GUI
# Omerta Music Research - Casablanca - 2026
# ASCII-pure - Python 3.8+
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess, sys, os, json, tempfile, threading, base64, math, wave
import numpy as np

BG='#060608'; GOLD='#c9a84c'; GOLD2='#e8c97a'; GDIM='#7a6030'
RED='#cc1111'; DK2='#0e0f11'; DK3='#141618'
FM=('Courier New',9); FS=('Courier New',8); FL=('Courier New',10,'bold')

def lbl(p,t,fg=GOLD,font=FM,**k):
    return tk.Label(p,text=t,bg=BG,fg=fg,font=font,**k)

def ent(p,tv=None,**k):
    k.setdefault('width',20)
    e=tk.Entry(p,textvariable=tv,bg=DK3,fg=GOLD2,
               insertbackground=GOLD,relief='flat',font=FM,
               highlightbackground=GDIM,highlightthickness=1,**k)
    return e

def gbtn(p,t,cmd,w=14,**k):
    return tk.Button(p,text=t,command=cmd,width=w,bg=DK2,fg=GOLD,
                     activebackground=GDIM,activeforeground=BG,
                     relief='flat',font=FM,cursor='hand2',
                     highlightbackground=GOLD,highlightthickness=1,**k)

def rbtn(p,t,cmd,**k):
    return tk.Button(p,text=t,command=cmd,
                     bg=RED,fg='white',activebackground='#ff3333',
                     activeforeground='white',relief='flat',
                     font=('Courier New',10,'bold'),cursor='hand2',**k)

def chk(p,t,var,**k):
    return tk.Checkbutton(p,text=t,variable=var,bg=BG,fg=GDIM,
                          selectcolor=DK2,activebackground=BG,
                          activeforeground=GOLD,font=FS,anchor='w',**k)

def sep(p,**k):
    return tk.Frame(p,bg=GDIM,height=1,**k)

# -- LED ------------------------------------------------------
class LED(tk.Canvas):
    def __init__(self,parent,size=10,**k):
        super().__init__(parent,width=size,height=size,
                         bg=BG,highlightthickness=0,**k)
        self.s=size; self.on(False)
    def on(self,active,color=None):
        self.delete('all'); s=self.s
        c=(color or GOLD) if active else '#1a1a1a'
        self.create_oval(1,1,s-1,s-1,fill=c,
                         outline=GDIM if active else '#222')

# -- WAVEFORM --------------------------------------------------
class WaveView(tk.Canvas):
    def __init__(self,parent,cw=320,ch=55,label='',**k):
        super().__init__(parent,width=cw,height=ch,bg='#080909',
                         highlightthickness=1,
                         highlightbackground=GDIM,**k)
        self.cw=cw; self.ch=ch; self.label=label
        self._idle()
    def _idle(self):
        self.delete('all')
        m=self.ch//2
        self.create_line(0,m,self.cw,m,fill=GDIM,dash=(2,4))
        self.create_text(self.cw//2,m,text=self.label,fill=GDIM,font=FS)
    def draw(self,samples,color=GOLD):
        self.delete('all')
        if samples is None or len(samples)==0:
            return self._idle()
        m=self.ch//2; n=len(samples); w=self.cw
        step=max(1,n//w)
        pts=[]
        for i in range(0,n,step):
            x=int(i/n*w)
            y=int(m-float(samples[i])*m*0.85)
            pts+=[x,max(0,min(self.ch,y))]
        if len(pts)>=4:
            self.create_line(pts,fill=color,width=1)

# -- KNOB ------------------------------------------------------
class Knob(tk.Canvas):
    def __init__(self,parent,label,var,lo,hi,fmt='%.2f',size=54,**k):
        super().__init__(parent,width=size,height=size+20,
                         bg=BG,highlightthickness=0,**k)
        self.var=var; self.lo=lo; self.hi=hi
        self.fmt=fmt; self.sz=size; self.label=label
        self._dy=None
        self._draw()
        var.trace_add('write',lambda *_:self._draw())
        self.bind('<ButtonPress-1>',  self._p)
        self.bind('<B1-Motion>',      self._d)
        self.bind('<MouseWheel>',     self._w)
        self.bind('<Button-4>',       self._w)
        self.bind('<Button-5>',       self._w)
    def _draw(self):
        self.delete('all')
        s=self.sz; cx=s//2; cy=s//2; r=s//2-4; r2=r-5
        self.create_oval(cx-r,cy-r,cx+r,cy+r,outline=GDIM,width=2,fill='#0d0e10')
        v=self.var.get(); rng=self.hi-self.lo
        pct=(v-self.lo)/rng if rng else 0.
        ang=math.radians(225.-pct*270.)
        ex=cx+r2*math.cos(ang); ey=cy-r2*math.sin(ang)
        self.create_line(cx,cy,int(ex),int(ey),fill=GOLD2,width=2)
        if pct>0:
            self.create_arc(cx-r+3,cy-r+3,cx+r-3,cy+r-3,
                start=-45,extent=int(-pct*270),style='arc',
                outline=GOLD,width=2)
        self.create_text(cx,s+6, text=self.fmt%v,fill=GOLD2,font=FS)
        self.create_text(cx,s+15,text=self.label,fill=GDIM,
                         font=('Courier New',7))
    def _p(self,e): self._dy=e.y
    def _d(self,e):
        if self._dy is None: return
        dy=self._dy-e.y; self._dy=e.y
        step=(self.hi-self.lo)/200.
        self.var.set(max(self.lo,min(self.hi,self.var.get()+dy*step)))
    def _w(self,e):
        d=1 if(e.num==4 or (hasattr(e,'delta') and e.delta>0)) else -1
        step=(self.hi-self.lo)/100.
        self.var.set(max(self.lo,min(self.hi,self.var.get()+d*step)))

# -- SLIDER ROW -----------------------------------------------
def slider_row(parent,label,var,lo,hi,fmt='%.2f',res=0.01):
    f=tk.Frame(parent,bg=BG)
    tk.Label(f,text=label,bg=BG,fg=GDIM,font=FS,width=18,anchor='w').pack(side='left')
    vl=tk.Label(f,bg=BG,fg=GOLD2,font=FS,width=9,anchor='e')
    vl.pack(side='right')
    def upd(v): vl.config(text=fmt%float(v))
    sc=tk.Scale(f,variable=var,from_=lo,to=hi,orient='horizontal',
                bg=BG,fg=GOLD,troughcolor=DK2,highlightthickness=0,
                showvalue=0,resolution=res,command=upd)
    sc.pack(side='left',fill='x',expand=True,padx=4)
    upd(var.get())
    return f

# -- MAIN APP --------------------------------------------------
class SafiApp:
    PRESETS={
        'Spotify':(-14.,-1.),'Apple Music':(-16.,-1.),
        'Tidal HiFi':(-14.,-1.),'YouTube':(-14.,-1.),
        'Deezer':(-14.,-1.),'Amazon':(-14.,-1.),
        'Club DJ':(-6.,-.3),'Radio FM':(-10.,-.5),
        'Beatport':(-8.,-.5),'Vinyl':(-12.,-.5),
        'CD Master':(-10.,-.2),'Custom':(-14.,-1.),
    }

    def __init__(self,root):
        self.root=root
        root.title('SAFI PROTOCOL DSP ENGINE v5.0')
        root.configure(bg=BG)
        root.minsize(1100,700)
        self._cover_data=b''; self._cover_mime=b'image/jpeg'
        self._proc=None; self._tmp_s=None; self._tmp_c=None
        self._vars(); self._ui()

    # -- VARIABLES --------------------------------------------
    def _vars(self):
        S=tk.StringVar; D=tk.DoubleVar; I=tk.IntVar; B=tk.BooleanVar
        self.v_in =S(); self.v_out=S(); self.v_preset=S(value='Custom')
        self.v_src=I(value=440); self.v_dst=I(value=432)
        self.v_tempo=D(value=1.0); self.v_width=D(value=1.25)
        self.v_drive=D(value=0.35); self.v_hbdrv=D(value=0.0)
        self.v_lufs=D(value=-14.); self.v_tp=D(value=-1.)
        self.v_bass=D(value=1.5); self.v_pres=D(value=1.0)
        self.v_air =D(value=2.0)
        self.v_firHz=D(value=120.); self.v_firTp=I(value=4097)
        self.v_hpf =B(value=True);  self.v_strip=B(value=True)
        self.v_pitch=B(value=True);  self.v_clip =B(value=True)
        self.v_eq  =B(value=True);  self.v_comp =B(value=True)
        self.v_ms  =B(value=True);  self.v_lufm =B(value=True)
        self.v_bext=B(value=True)
        self.v_artist=S(value='Doctor YUSUF SAFI')
        self.v_album =S(value='Blueprint 432')
        self.v_year  =S(value='2026')
        self.v_genre =S(value='Drill / Psychoacoustic')
        self.v_track =S(); self.v_comp_=S(value='Yusuf Safi')
        self.v_copy  =S(value='(c) Omerta Music Research & YOUSSEF SAFI')
        self.v_eng   =S(value='Safi Protocol DSP Engine v5.0')
        self.v_isrc  =S(); self.v_upc=S()
        self.v_amid  =S(); self.v_spid=S(); self.v_mbid=S()
        self.v_cover =S()

    # -- UI ---------------------------------------------------
    def _ui(self):
        r=self.root
        # Header
        hf=tk.Frame(r,bg=BG); hf.pack(fill='x',padx=8,pady=(6,2))
        tk.Label(hf,text='SAFI PROTOCOL DSP ENGINE v5.0',bg=BG,fg=GOLD,
                 font=('Courier New',13,'bold')).pack(side='left')
        tk.Label(hf,text='Omerta Music Research',bg=BG,fg=GDIM,
                 font=FM).pack(side='left',padx=12)
        bf=tk.Frame(hf,bg='#121000',highlightbackground=GOLD,highlightthickness=1)
        bf.pack(side='left',padx=6)
        self.led64=LED(bf,size=9); self.led64.pack(side='left',padx=(4,2),pady=3)
        self.led64.on(True)
        tk.Label(bf,text='64-bit Linear Phase Processing Active',bg='#121000',
                 fg=GOLD2,font=FS).pack(side='left',padx=(0,6),pady=3)

        # I/O
        iof=tk.Frame(r,bg=BG); iof.pack(fill='x',padx=8,pady=3)
        lbl(iof,'INPUT:',width=7,anchor='e').pack(side='left')
        ent(iof,self.v_in,width=50).pack(side='left',padx=3)
        gbtn(iof,'...',self._brw_in,w=3).pack(side='left',padx=2)
        lbl(iof,'  OUTPUT:').pack(side='left')
        ent(iof,self.v_out,width=50).pack(side='left',padx=3)
        gbtn(iof,'...',self._brw_out,w=3).pack(side='left',padx=2)

        # Notebook
        st=ttk.Style(); st.theme_use('default')
        st.configure('O.TNotebook',background=BG,borderwidth=0)
        st.configure('O.TNotebook.Tab',background=DK2,foreground=GDIM,
                     font=FM,padding=[10,4])
        st.map('O.TNotebook.Tab',
               background=[('selected','#1c1a10')],
               foreground=[('selected',GOLD)])
        nb=ttk.Notebook(r,style='O.TNotebook')
        nb.pack(fill='both',expand=True,padx=8,pady=3)

        td=tk.Frame(nb,bg=BG); te=tk.Frame(nb,bg=BG)
        tm=tk.Frame(nb,bg=BG); tl=tk.Frame(nb,bg=BG)
        nb.add(td,text='  DSP CHAIN  ')
        nb.add(te,text='  EQ / DYNAMICS  ')
        nb.add(tm,text='  METADATA  ')
        nb.add(tl,text='  CONSOLE  ')
        self._tab_dsp(td); self._tab_eq(te)
        self._tab_meta(tm); self._tab_log(tl)

        # Bottom bar
        bb=tk.Frame(r,bg=BG); bb.pack(fill='x',padx=8,pady=(2,8))
        lbl(bb,'PRESET:',fg=GDIM).pack(side='left')
        pm=tk.OptionMenu(bb,self.v_preset,*self.PRESETS.keys(),
                         command=self._preset)
        pm.config(bg=DK2,fg=GOLD,activebackground=GDIM,relief='flat',
                  font=FM,width=12)
        pm['menu'].config(bg=DK2,fg=GOLD,activebackground=GDIM,font=FM)
        pm.pack(side='left',padx=6)
        self.led_p=LED(bb,size=10); self.led_p.pack(side='left',padx=(14,4))
        self.lbl_st=tk.Label(bb,text='READY',bg=BG,fg=GDIM,font=FM,width=30,anchor='w')
        self.lbl_st.pack(side='left')
        gbtn(bb,'STOP',self._stop,w=8).pack(side='right',padx=4)
        rbtn(bb,'  LANCER LA SEQUENCE - 432Hz  ',self._launch).pack(side='right',padx=8)

    # -- TAB DSP ----------------------------------------------
    def _tab_dsp(self,p):
        L=tk.Frame(p,bg=BG); R=tk.Frame(p,bg=BG)
        L.pack(side='left',fill='y',padx=10,pady=6)
        R.pack(side='left',fill='both',expand=True,padx=10,pady=6)

        # Left: modules
        lbl(L,'DSP MODULES',font=FL).grid(row=0,column=0,columnspan=2,sticky='w',pady=(0,6))
        mods=[
            ('HPF 20Hz  Butterworth 4th order',self.v_hpf),
            ('Strip parasitic chunks',          self.v_strip),
            ('440->432Hz  Pitch Shift',          self.v_pitch),
            ('8x Oversampled  Soft Clipper',     self.v_clip),
            ('EQ  4 bands parametric',           self.v_eq),
            ('Glue Compressor  (high-band)',      self.v_comp),
            ('M/S  Width processing',            self.v_ms),
            ('LUFS  Normalization',              self.v_lufm),
            ('bext  EBU chunk',                  self.v_bext),
        ]
        self._mleds={}
        for i,(t,v) in enumerate(mods,1):
            ld=LED(L,size=9); ld.grid(row=i,column=0,padx=(0,4),pady=2,sticky='w')
            ld.on(v.get())
            cb=chk(L,t,v,command=lambda l=ld,vv=v:l.on(vv.get()))
            cb.grid(row=i,column=1,sticky='w')
            self._mleds[t]=ld

        # Pitch freqs
        r0=len(mods)+1
        pf=tk.Frame(L,bg=BG); pf.grid(row=r0,column=0,columnspan=2,sticky='ew',pady=(8,2))
        lbl(pf,'SRC Hz',fg=GDIM,font=FS).pack(side='left')
        tk.Spinbox(pf,from_=400,to=480,textvariable=self.v_src,width=5,
                   bg=DK3,fg=GOLD2,buttonbackground=DK2,relief='flat',
                   font=FS).pack(side='left',padx=4)
        lbl(pf,'DST Hz',fg=GDIM,font=FS).pack(side='left')
        tk.Spinbox(pf,from_=400,to=480,textvariable=self.v_dst,width=5,
                   bg=DK3,fg=GOLD2,buttonbackground=DK2,relief='flat',
                   font=FS).pack(side='left',padx=4)

        # FIR
        ff=tk.Frame(L,bg=BG); ff.grid(row=r0+1,column=0,columnspan=2,sticky='ew',pady=2)
        lbl(ff,'FIR Hz',fg=GDIM,font=FS).pack(side='left')
        tk.Spinbox(ff,from_=60,to=300,textvariable=self.v_firHz,width=5,
                   bg=DK3,fg=GOLD2,buttonbackground=DK2,relief='flat',
                   font=FS).pack(side='left',padx=4)
        lbl(ff,'Taps',fg=GDIM,font=FS).pack(side='left')
        for v,t in [(2049,'2k'),(4097,'4k'),(8193,'8k')]:
            tk.Radiobutton(ff,text=t,variable=self.v_firTp,value=v,
                           bg=BG,fg=GDIM,selectcolor=DK2,
                           activebackground=BG,font=FS).pack(side='left',padx=2)

        # Tempo
        tf=tk.Frame(L,bg=BG); tf.grid(row=r0+2,column=0,columnspan=2,sticky='ew',pady=6)
        lbl(tf,'TEMPO',fg=GDIM,font=FS,width=6).pack(side='left')
        self._tv_lbl=tk.Label(tf,bg=BG,fg=GOLD2,font=FS,width=6)
        self._tv_lbl.pack(side='right')
        def upd_t(v): self._tv_lbl.config(text='x%.2f'%float(v))
        sc=tk.Scale(tf,variable=self.v_tempo,from_=0.25,to=4.,orient='horizontal',
                    bg=BG,fg=GOLD,troughcolor=DK2,highlightthickness=0,
                    showvalue=0,resolution=0.01,command=upd_t)
        sc.pack(side='left',fill='x',expand=True,padx=4); upd_t(self.v_tempo.get())
        bf2=tk.Frame(L,bg=BG); bf2.grid(row=r0+3,column=0,columnspan=2,sticky='w')
        for v,t in [(0.5,'1/2x'),(1.,'1x'),(2.,'2x')]:
            gbtn(bf2,t,lambda vv=v:self.v_tempo.set(vv),w=4).pack(side='left',padx=2)

        # Right: knobs + waveforms
        lbl(R,'CONTROLS',font=FL).grid(row=0,column=0,columnspan=6,sticky='w',pady=(0,6))
        kdefs=[
            ('LUFS', self.v_lufs,-24.,-5., '%.0f'),
            ('T.PEAK',self.v_tp, -3., 0.,  '%.1f'),
            ('WIDTH', self.v_width,0.,2.,  '%.2f'),
            ('DRIVE', self.v_drive,0.,1.,  '%.2f'),
            ('HB DRV',self.v_hbdrv,0.,1., '%.2f'),
            ('TEMPO', self.v_tempo,0.25,4.,'x%.2f'),
        ]
        for i,(lbl_,var,lo,hi,fmt) in enumerate(kdefs):
            Knob(R,lbl_,var,lo,hi,fmt).grid(row=1,column=i,padx=5,pady=4)

        lbl(R,'WAVEFORM',fg=GDIM,font=FS).grid(row=2,column=0,columnspan=6,sticky='w',pady=(8,2))
        wf=tk.Frame(R,bg=BG); wf.grid(row=3,column=0,columnspan=6,sticky='w')
        self.wv_orig=WaveView(wf,cw=310,ch=55,label='ORIGINAL 440Hz')
        self.wv_orig.pack(side='left',padx=(0,6))
        self.wv_proc=WaveView(wf,cw=310,ch=55,label='PROCESSED 432Hz')
        self.wv_proc.pack(side='left')

        lbl(R,'LEVEL L/R',fg=GDIM,font=FS).grid(row=4,column=0,columnspan=6,sticky='w',pady=(6,2))
        vuf=tk.Frame(R,bg=BG); vuf.grid(row=5,column=0,columnspan=6,sticky='w')
        self.vu_l=tk.Canvas(vuf,width=240,height=10,bg='#080a0c',highlightthickness=0)
        self.vu_l.pack(side='left',padx=(0,6))
        self.vu_r=tk.Canvas(vuf,width=240,height=10,bg='#080a0c',highlightthickness=0)
        self.vu_r.pack(side='left')

    def _vu_set(self,canvas,db):
        canvas.delete('all'); pct=max(0.,min(1.,(db+60)/60.)); px=int(pct*240)
        col='#ff3333' if pct>.9 else '#ffaa00' if pct>.75 else GOLD
        if px>0: canvas.create_rectangle(0,1,px,9,fill=col,outline='')

    # -- TAB EQ -----------------------------------------------
    def _tab_eq(self,p):
        L=tk.Frame(p,bg=BG); R=tk.Frame(p,bg=BG)
        L.pack(side='left',fill='y',padx=12,pady=8)
        R.pack(side='left',fill='both',expand=True,padx=12,pady=8)

        lbl(L,'EQ PARAMETRIC',font=FL).pack(anchor='w',pady=(0,6))
        for lbl_,var,lo,hi,fmt,res in [
            ('BASS  +80Hz shelf',  self.v_bass,-6.,12.,'%.1f dB',0.1),
            ('PRESENCE  3kHz',     self.v_pres,-6.,12.,'%.1f dB',0.1),
            ('AIR  12kHz shelf',   self.v_air, -6.,12.,'%.1f dB',0.1),
        ]:
            slider_row(L,lbl_,var,lo,hi,fmt,res).pack(fill='x',pady=2)

        sep(L).pack(fill='x',pady=8)
        lbl(L,'DYNAMICS',font=FL).pack(anchor='w',pady=(0,6))
        for lbl_,var,lo,hi,fmt,res in [
            ('LUFS  target',    self.v_lufs,-24.,-5., '%.1f LUFS',0.5),
            ('TRUE PEAK  ceil', self.v_tp,  -3., 0.,  '%.1f dBTP',0.1),
            ('M/S  WIDTH',      self.v_width,0., 2.,  '%.2f',0.01),
        ]:
            slider_row(L,lbl_,var,lo,hi,fmt,res).pack(fill='x',pady=2)

        lbl(R,'SATURATION  /  HIGH-BAND COMPRESSION',font=FL).pack(anchor='w',pady=(0,6))
        for lbl_,var,lo,hi,fmt,res in [
            ('SOFT CLIP  DRIVE',  self.v_drive, 0.,1.,'%.2f',0.01),
            ('HIGH-BAND DRIVE',   self.v_hbdrv, 0.,1.,'%.2f  (0=+0dB  1=+6dB)',0.01),
        ]:
            slider_row(R,lbl_,var,lo,hi,fmt,res).pack(fill='x',pady=2)

        sep(R).pack(fill='x',pady=8)
        lbl(R,'FIR LINEAR PHASE CROSSOVER',font=FL).pack(anchor='w',pady=(0,6))
        slider_row(R,'CROSSOVER Hz',self.v_firHz,60.,300.,'%.0f Hz',1.).pack(fill='x',pady=2)
        tf=tk.Frame(R,bg=BG); tf.pack(anchor='w',pady=4)
        lbl(tf,'TAPS:',fg=GDIM,font=FS).pack(side='left')
        for v,t in [(2049,'2049 fast'),(4097,'4097 std'),(8193,'8193 ultra')]:
            tk.Radiobutton(tf,text=t,variable=self.v_firTp,value=v,
                           bg=BG,fg=GDIM,selectcolor=DK2,
                           activebackground=BG,font=FS).pack(side='left',padx=6)

        sep(R).pack(fill='x',pady=8)
        inf=tk.Frame(R,bg='#0c0b07',highlightbackground=GDIM,highlightthickness=1)
        inf.pack(fill='x',padx=2,pady=4)
        for t in [
            'FIR Linear Phase  BlackmanHarris window  -92dB stopband',
            'band_low  (sub / kick):  UNTOUCHED',
            'band_high (>120Hz):  Soft Clip + EQ + Glue Comp',
            'Band recombination sum error:  < 1e-14  (machine precision)',
            '8x Oversampled Soft Clipper  zero aliasing in HF',
            '8x Oversampled True Peak Limiter  IEC 60268-18',
        ]:
            tk.Label(inf,text='  '+t,bg='#0c0b07',fg=GDIM,font=FS,anchor='w').pack(fill='x')

    # -- TAB METADATA -----------------------------------------
    def _tab_meta(self,p):
        cv=tk.Canvas(p,bg=BG,highlightthickness=0)
        sb=tk.Scrollbar(p,orient='vertical',command=cv.yview)
        cv.configure(yscrollcommand=sb.set)
        sb.pack(side='right',fill='y'); cv.pack(side='left',fill='both',expand=True)
        inn=tk.Frame(cv,bg=BG)
        wid=cv.create_window((0,0),window=inn,anchor='nw')
        inn.bind('<Configure>',lambda e:(cv.configure(scrollregion=cv.bbox('all')),
                                         cv.itemconfig(wid,width=cv.winfo_width())))
        cv.bind('<Configure>',lambda e:cv.itemconfig(wid,width=e.width))
        for w in (cv,inn):
            w.bind('<MouseWheel>',lambda e:cv.yview_scroll(-1*(e.delta//120),'units'))
            w.bind('<Button-4>',  lambda e:cv.yview_scroll(-1,'units'))
            w.bind('<Button-5>',  lambda e:cv.yview_scroll(1,'units'))

        q=inn
        def row(label,var,r,w=44):
            tk.Label(q,text=label,bg=BG,fg=GDIM,font=FS,width=16,anchor='e').grid(row=r,column=0,sticky='e',padx=(4,2),pady=2)
            ent(q,var,width=w).grid(row=r,column=1,columnspan=3,sticky='ew',padx=4,pady=2)

        r=0
        lbl(q,'TRACK INFO',font=FL).grid(row=r,column=0,columnspan=4,sticky='w',padx=8,pady=(6,4)); r+=1
        for label,var in [('Artist',self.v_artist),('Album',self.v_album),
            ('Year',self.v_year),('Genre',self.v_genre),('Track #',self.v_track),
            ('Composer',self.v_comp_),('Copyright',self.v_copy),('Engineer',self.v_eng)]:
            row(label,var,r); r+=1

        tk.Label(q,text='',bg=BG).grid(row=r,column=0); r+=1
        lbl(q,'IDENTIFIANTS & DISTRIBUTION',font=FL).grid(row=r,column=0,columnspan=4,sticky='w',padx=8,pady=(4,4)); r+=1
        for label,var in [('ISRC',self.v_isrc),('UPC/EAN',self.v_upc),
            ('Apple Music ID',self.v_amid),('Spotify ID',self.v_spid),
            ('MusicBrainz ID',self.v_mbid)]:
            row(label,var,r); r+=1

        tk.Label(q,text='',bg=BG).grid(row=r,column=0); r+=1
        lbl(q,'POCHETTE (COVER ART - APIC)',font=FL).grid(row=r,column=0,columnspan=4,sticky='w',padx=8,pady=(4,4)); r+=1
        cf=tk.Frame(q,bg=BG); cf.grid(row=r,column=0,columnspan=4,sticky='ew',padx=8); r+=1
        ent(cf,self.v_cover,width=46).pack(side='left')
        gbtn(cf,'Charger .jpg/.png',self._load_cover,w=18).pack(side='left',padx=4)
        self.lbl_cov=tk.Label(cf,text='Aucune',bg=BG,fg=GDIM,font=FS)
        self.lbl_cov.pack(side='left',padx=6)

        tk.Label(q,text='',bg=BG).grid(row=r,column=0); r+=1
        lbl(q,'PAROLES (USLT LYRICS)',font=FL).grid(row=r,column=0,columnspan=4,sticky='w',padx=8,pady=(4,4)); r+=1
        self.txt_ly=scrolledtext.ScrolledText(q,width=70,height=10,
            bg=DK3,fg=GOLD2,insertbackground=GOLD,font=FS,relief='flat',
            highlightbackground=GDIM,highlightthickness=1)
        self.txt_ly.grid(row=r,column=0,columnspan=4,padx=8,pady=4,sticky='ew'); r+=1
        q.columnconfigure(1,weight=1)

    # -- TAB CONSOLE ------------------------------------------
    def _tab_log(self,p):
        cf=tk.Frame(p,bg=BG); cf.pack(fill='x',padx=4,pady=4)
        gbtn(cf,'CLEAR',lambda:self.console.config(state='normal') or
             self.console.delete('1.0','end') or
             self.console.config(state='disabled'),w=8).pack(side='left')
        lbl(cf,'DSP Console - Real Time Output',fg=GDIM,font=FS).pack(side='left',padx=8)
        self.console=scrolledtext.ScrolledText(p,bg='#050507',fg=GOLD2,
            insertbackground=GOLD,font=('Courier New',9),relief='flat',
            highlightbackground=GDIM,highlightthickness=1)
        self.console.pack(fill='both',expand=True,padx=4,pady=4)
        self.console.config(state='disabled')
        self.console.tag_configure('ok', foreground='#44cc44')
        self.console.tag_configure('er', foreground='#ff4444')
        self.console.tag_configure('sp', foreground=GOLD)
        self.console.tag_configure('in', foreground=GOLD2)

    # -- ACTIONS ----------------------------------------------
    def _brw_in(self):
        f=filedialog.askopenfilename(filetypes=[('WAV','*.wav'),('All','*.*')])
        if not f: return
        self.v_in.set(f)
        if not self.v_out.get():
            self.v_out.set(os.path.splitext(f)[0]+'_432Hz.wav')
        self._load_wv(f)

    def _brw_out(self):
        f=filedialog.asksaveasfilename(defaultextension='.wav',
                                       filetypes=[('WAV','*.wav')])
        if f: self.v_out.set(f)

    def _load_wv(self,path):
        try:
            with wave.open(path,'rb') as f:
                nc=f.getnchannels(); sr=f.getframerate()
                n=min(f.getnframes(),sr*2); sw=f.getsampwidth()
                raw=f.readframes(n)
            if sw==2: s=np.frombuffer(raw,np.int16).astype(np.float64)/32768.
            else:     s=np.frombuffer(raw,np.uint8).astype(np.float64)/128.-1.
            if nc>1: s=s[::nc]
            self.wv_orig.draw(s,'#aaaaaa')
        except: pass

    def _load_cover(self):
        f=filedialog.askopenfilename(
            filetypes=[('Image','*.jpg *.jpeg *.png'),('All','*.*')])
        if not f: return
        with open(f,'rb') as fp: data=fp.read()
        self._cover_data=data
        self._cover_mime=(b'image/jpeg'
            if f.lower().endswith(('.jpg','.jpeg')) else b'image/png')
        self.v_cover.set(f)
        self.lbl_cov.config(
            text='%s  (%d KB)'%(os.path.basename(f),len(data)//1024),
            fg=GOLD2)

    def _preset(self,name):
        if name in self.PRESETS:
            l,t=self.PRESETS[name]
            self.v_lufs.set(l); self.v_tp.set(t)
            self._log('Preset -> %s  %.0fLUFS / %.1fdBTP\n'%(name,l,t),'in')

    def _log(self,text,tag=''):
        self.console.config(state='normal')
        if not tag:
            if '[OK]' in text or 'OK' in text: tag='ok'
            elif 'rror' in text or 'ERR' in text: tag='er'
            elif '===' in text or '---' in text: tag='sp'
            else: tag='in'
        self.console.insert('end',text,tag)
        self.console.see('end')
        self.console.config(state='disabled')

    def _build_cfg(self):
        return dict(
            input_path=self.v_in.get(),
            output_path=self.v_out.get(),
            src_freq=self.v_src.get(), dst_freq=self.v_dst.get(),
            target_lufs=self.v_lufs.get(), target_tp=self.v_tp.get(),
            ms_width=self.v_width.get(), tempo_ratio=self.v_tempo.get(),
            fir_freq=self.v_firHz.get(), fir_taps=self.v_firTp.get(),
            use_hpf=bool(self.v_hpf.get()), use_strip=bool(self.v_strip.get()),
            use_pitch=bool(self.v_pitch.get()), use_softclip=bool(self.v_clip.get()),
            softclip_drive=self.v_drive.get(),
            use_eq=bool(self.v_eq.get()),
            eq_bass=self.v_bass.get(), eq_pres=self.v_pres.get(),
            eq_air=self.v_air.get(),
            use_comp=bool(self.v_comp.get()), hb_drive=self.v_hbdrv.get(),
            use_lufs=bool(self.v_lufm.get()), use_bext=bool(self.v_bext.get()),
            meta=dict(
                artist=self.v_artist.get(), album=self.v_album.get(),
                year=self.v_year.get(), genre=self.v_genre.get(),
                track=self.v_track.get(), composer=self.v_comp_.get(),
                copyright=self.v_copy.get(), engineer=self.v_eng.get(),
                isrc=self.v_isrc.get(), upc=self.v_upc.get(),
                apple_music_id=self.v_amid.get(),
                spotify_id=self.v_spid.get(),
                musicbrainz_id=self.v_mbid.get(),
                lyrics=self.txt_ly.get('1.0','end').strip(),
                _cover_b64=base64.b64encode(self._cover_data).decode('ascii'),
                _cover_mime=self._cover_mime.decode('ascii'),
            )
        )

    def _launch(self):
        if self._proc and self._proc.poll() is None:
            messagebox.showwarning('SAFI','Traitement en cours...'); return
        inp=self.v_in.get(); out=self.v_out.get()
        if not inp or not os.path.exists(inp):
            messagebox.showerror('SAFI','Fichier input introuvable'); return
        if not out:
            messagebox.showerror('SAFI','Selectionner output'); return

        cfg=self._build_cfg()
        pipeline=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'safi_pipeline_v5.py')

        # Write cfg json
        tc=tempfile.NamedTemporaryFile(mode='w',suffix='.json',
                                       delete=False,encoding='utf-8')
        json.dump(cfg,tc); tc.close(); self._tmp_c=tc.name

        # Write runner script
        ts=tempfile.NamedTemporaryFile(mode='w',suffix='.py',
                                       delete=False,encoding='utf-8')
        ts.write('''import sys,os,base64,json
sys.path.insert(0,%r)
os.environ["PYTHONIOENCODING"]="utf-8"
with open(%r,encoding="utf-8") as f:
    cfg=json.load(f)
if cfg["meta"].get("_cover_b64"):
    cfg["meta"]["_cover_data"]=base64.b64decode(cfg["meta"]["_cover_b64"])
    del cfg["meta"]["_cover_b64"]
if cfg["meta"].get("_cover_mime"):
    cfg["meta"]["_cover_mime"]=cfg["meta"]["_cover_mime"].encode("ascii")
from safi_pipeline_v5 import run_pipeline
lufs,tp=run_pipeline(**cfg)
print("__DONE__%%.3f__%%.3f__"%%( lufs,tp))
''' % (os.path.dirname(pipeline), tc.name))
        ts.close(); self._tmp_s=ts.name

        env=os.environ.copy(); env['PYTHONIOENCODING']='utf-8'
        kw={}
        if sys.platform=='win32':
            kw['creationflags']=0x00000040|0x08000000
        self._proc=subprocess.Popen(
            [sys.executable,ts.name],
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
            text=True,bufsize=1,env=env,**kw)

        self.led_p.on(True,color=RED)
        self.lbl_st.config(text='PROCESSING...',fg=RED)
        self.btn_launch_ref=None
        self._log('\n'+'='*54+'\n','sp')
        threading.Thread(target=self._read,daemon=True).start()

    def _read(self):
        for line in self._proc.stdout:
            self.root.after(0,self._log,line)
            if '__DONE__' in line:
                try:
                    pts=line.strip().split('__')
                    self.root.after(0,self._done,float(pts[2]),float(pts[3]))
                except: pass
        self._proc.wait()
        if self._proc.returncode not in (0,None):
            self.root.after(0,self._err,self._proc.returncode)
        for p in (self._tmp_s,self._tmp_c):
            try: p and os.unlink(p)
            except: pass

    def _done(self,lufs,tp):
        self.led_p.on(True,color='#44cc44')
        self.lbl_st.config(text='[OK]  LUFS:%.1f  TP:%.1f'%(lufs,tp),fg='#44cc44')
        try:
            path=self.v_out.get()
            with wave.open(path,'rb') as f:
                nc=f.getnchannels(); sr=f.getframerate()
                n=min(f.getnframes(),sr*2); sw=f.getsampwidth()
                raw=f.readframes(n)
            if sw==3:
                b=np.frombuffer(raw,np.uint8); ns=len(b)//3
                x=np.zeros(ns,np.int32)
                x|=b[0::3].astype(np.int32)
                x|=b[1::3].astype(np.int32)<<8
                x|=b[2::3].astype(np.int32)<<16
                x=np.where(x>=(1<<23),x-(1<<24),x)
                s=x.astype(np.float64)/float(1<<23)
            elif sw==2: s=np.frombuffer(raw,np.int16).astype(np.float64)/32768.
            else: s=np.frombuffer(raw,np.uint8).astype(np.float64)/128.-1.
            if nc>1: s=s[::nc]
            self.wv_proc.draw(s,GOLD)
        except: pass

    def _err(self,rc):
        self.led_p.on(True,color=RED)
        self.lbl_st.config(text='[ERR] Code: %d'%rc,fg=RED)

    def _stop(self):
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            self._log('\n[STOP] Arrete par utilisateur\n','er')
            self.led_p.on(False)
            self.lbl_st.config(text='STOPPED',fg=GDIM)

def main():
    root=tk.Tk()
    SafiApp(root)
    root.mainloop()

if __name__=='__main__':
    main()
