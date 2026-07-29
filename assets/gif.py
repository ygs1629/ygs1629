from PIL import Image, ImageDraw, ImageFont
from random import seed, random
from math import hypot, sin, cos, pi

W,H,FPS=845,292,20
TEXTS=[
    ["Hi, I'm Yannis ", "wave"],
    ["I'm a ", "es", "gr", " AI/ML engineer"],
    ["Based in Valencia, Spain ", "pin"]
]
WRITE,HOLD,ERASE=1.6,1.8,.8
SEC=(WRITE+HOLD+ERASE)*len(TEXTS)

N,D=58,150
seed(7)
pts=[(random()*W,random()*H,random()*9,random()*2*pi) for _ in range(N)]

font=ImageFont.truetype("arialbd.ttf",43)

icons={
    "es":Image.open("assets/emojis/es.png").convert("RGBA").resize((34,34)),
    "gr":Image.open("assets/emojis/gr.png").convert("RGBA").resize((34,34)),
    "pin":Image.open("assets/emojis/pin.png").convert("RGBA").resize((34,34)),
    "wave":Image.open("assets/emojis/wave.png").convert("RGBA").resize((34,34))
}

frames=[]
for f in range(int(FPS*SEC)):
    t=f/FPS
    img=Image.new("RGB",(W,H),"white")
    d=ImageDraw.Draw(img)

    p=[(x+sin(t*.8+a)*s,y+cos(t*.7+a)*s) for x,y,s,a in pts]

    for i,(x1,y1) in enumerate(p):
        for x2,y2 in p[i+1:]:
            dist=hypot(x1-x2,y1-y2)
            if dist<D:
                c=int(235-dist/D*85)
                d.line((x1,y1,x2,y2),fill=(c,c,c),width=1)

    for x,y in p:
        d.ellipse((x-2,y-2,x+2,y+2),fill=(45,45,45))

    cycle=WRITE+HOLD+ERASE
    i=int(t//cycle)%len(TEXTS)
    local=t%cycle
    parts=TEXTS[i]
    plain="".join(p for p in parts if p not in icons)

    if local<WRITE:
        n=int(len(plain)*local/WRITE)
    elif local<WRITE+HOLD:
        n=len(plain)
    else:
        n=int(len(plain)*(1-(local-WRITE-HOLD)/ERASE))

    cursor="|" if int(t*2)%2==0 else ""
    items=[p for p in parts if p in icons and n==len(plain)]
    text="".join(p for p in parts if p not in icons)[:n]+cursor

    w=d.textbbox((0,0),text,font=font)[2]+len(items)*38
    x=(W-w)/2
    y=H/2-24

    left=n
    for p in parts:
        if p in icons:
            if n==len(plain):
                img.paste(icons[p],(int(x),int(y+8)),icons[p])
                x+=38
        else:
            s=p[:left]
            d.text((x,y),s,font=font,fill="black")
            x+=d.textlength(s,font=font)
            left=max(0,left-len(p))

    if cursor:
        d.text((x,y),cursor,font=font,fill="black")

    frames.append(img)

frames[0].save("assets/header.gif",save_all=True,append_images=frames[1:],duration=1000//FPS,loop=0,optimize=True)