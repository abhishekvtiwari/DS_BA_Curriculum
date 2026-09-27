# Generates the SVG figures for Chapter 53. Run: python3 make_figs53.py
# fig53-1 is drawn from the real generated images; the rest use the chapter's measured numbers.
import pathlib, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
DATA = pathlib.Path(__file__).resolve().parents[1] / "companion" / "ch53" / "defect_data"

def fig_images():
    images = np.load(DATA / "images.npy"); kinds = np.load(DATA / "defect_types.npy")
    picks = [("good", 0), ("good", 1), ("good", 2), ("scratch", 0), ("void", 0), ("short_shot", 0)]
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 5.0))
    for ax, (kind, which) in zip(axes.ravel(), picks):
        index = np.where(kinds == kind)[0][which]
        ax.imshow(images[index], cmap="gray", vmin=0, vmax=1, interpolation="nearest")
        ax.set_title(kind.replace("_", " "), fontsize=10, color=("#2f7d6d" if kind == "good" else "#b23b3b"))
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("What the model sees: 32x32 images of moulded lids", fontsize=12, y=0.98)
    fig.tight_layout()
    fig.savefig(__file__.replace("make_figs53.py", "fig53-1-defect-images.svg"), format="svg")
    plt.close(fig)

def fig_training_step():
    o=[text(30,32,"One training step, with the numbers from section 53.2",14,INK,"bold",family=HEAD)]
    boxes=[(40,"inputs","x = [1.0, 2.0]",ACC),(250,"hidden layer","z1 = [2.1, 0.2]\nafter ReLU the same",PURPLE),
           (470,"output","z2 = 1.420",ACC),(690,"loss","(1.420 - 1.0)² = 0.176",RED)]
    for x,title,detail,c in boxes:
        o.append(rect(x,70,190,80,fill="#fff",stroke=c,sw=1.8,rx=8))
        o.append(text(x+95,96,title,12.5,c,"bold",anchor="middle"))
        for i,line in enumerate(detail.split("\n")):
            o.append(text(x+95,120+i*18,line,11.5,INK,anchor="middle",family=MONO))
        if x<690:
            o.append(path(f"M{x+190},110 H{x+248}",stroke=INK,sw=2)); o.append(path(f"M{x+240},104 L{x+250},110 L{x+240},116",stroke=INK,sw=2))
    o.append(text(40,178,"forward pass: predict, then measure how wrong",12,MUTED))
    back=[(690,"dloss/dz2 = 0.840",RED),(470,"dW2 = [1.764, 0.168]",ORANGE),(250,"dz1 = [0.588, -0.420]",ORANGE),(40,"dW1 = [[0.588, -0.420],\n       [1.176, -0.840]]",ORANGE)]
    for x,detail,c in back:
        o.append(rect(x,220,190,72,fill="#fdf3dc",stroke=c,sw=1.6,rx=8))
        for i,line in enumerate(detail.split("\n")):
            o.append(text(x+95,250+i*16,line,11,INK,anchor="middle",family=MONO))
        if x>40:
            o.append(path(f"M{x},256 H{x-58}",stroke=ORANGE,sw=2)); o.append(path(f"M{x-50},250 L{x-60},256 L{x-50},262",stroke=ORANGE,sw=2))
    o.append(text(40,318,"backward pass: pass the blame back, in proportion to each input",12,MUTED))
    o.append(rect(40,345,840,58,fill="#e2f3ee",stroke=GREEN,sw=1.6,rx=8))
    o.append(text(60,370,"update:  W = W - 0.05 x gradient",12.5,GREEN,"bold",family=MONO))
    o.append(text(60,390,"prediction 1.420 -> 1.019,  loss 0.176 -> 0.000.  Repeat a few million times.",12,INK))
    return svg(1040,420,"".join(o))

def fig_attention():
    o=[text(30,32,'Attention on four tokens: who listens to whom',14,INK,"bold",family=HEAD)]
    tokens=["the","crate","was","cracked"]
    weights=[[0.347,0.244,0.212,0.197],[0.315,0.290,0.202,0.193],[0.262,0.264,0.238,0.236],[0.226,0.396,0.186,0.192]]
    x0,y0,cell=260,80,86
    for j,t in enumerate(tokens):
        o.append(text(x0+j*cell+cell/2,y0-12,t,12,MUTED,"bold",anchor="middle"))
    o.append(text(x0+2*cell,y0-38,"attended to",12,INK,"bold",anchor="middle"))
    for i,t in enumerate(tokens):
        o.append(text(x0-16,y0+i*cell+cell/2+5,t,12,MUTED,"bold",anchor="end"))
        for j,w in enumerate(weights[i]):
            shade=int(255-(w-0.18)/0.24*120)
            o.append(rect(x0+j*cell,y0+i*cell,cell-4,cell-4,fill=f"rgb({shade},{min(255,shade+18)},{shade+6})",stroke=RULE,rx=5))
            o.append(text(x0+j*cell+(cell-4)/2,y0+i*cell+(cell-4)/2+5,f"{w:.3f}",12,INK,"bold" if w>0.34 else "normal",anchor="middle",family=MONO))
    o.append(text(60,y0+2*cell,"the token",12,INK,"bold",anchor="middle")); o.append(text(60,y0+2*cell+18,"doing the",12,INK,anchor="middle")); o.append(text(60,y0+2*cell+36,"looking",12,INK,anchor="middle"))
    notes=["Each row sums to 1: it is how one token divides","its attention over the sentence.","",
           "'cracked' puts 0.396 on 'crate', more than on any","other token, including itself. Nothing told the model","about grammar: the learned query of 'cracked' simply","lines up with the learned key of 'crate'.","",
           "Queries and keys decide who is listened to.","Values decide what is heard."]
    for i,l in enumerate(notes):
        o.append(text(640,y0+10+i*22,l,12,INK if i<2 or i>6 else MUTED))
    return svg(1040,y0+4*cell+40,"".join(o))

def fig_threshold():
    o=[text(30,32,"The threshold is a business decision, not a modelling one",14,INK,"bold",family=HEAD)]
    rows=[(0.50,109,10,2,40080),(0.30,111,8,2,32080),(0.10,113,6,6,24240),(0.05,114,5,15,20600),
          (0.02,115,4,28,17120),(0.01,116,3,46,13840),(0.005,116,3,93,15720),(0.002,116,3,205,20200)]
    x0,x1,y0,y1=120,620,330,80
    costs=[r[4] for r in rows]
    def px(i): return x0+i*(x1-x0)/(len(rows)-1)
    def py(c): return y0-(c-12000)/30000*(y0-y1)
    o.append(path(f"M{x0},{y0} H{x1+20}",stroke=MUTED,sw=1.4)); o.append(path(f"M{x0},{y0} V{y1-10}",stroke=MUTED,sw=1.4))
    for c in (15000,20000,30000,40000):
        o.append(path(f"M{x0},{py(c)} H{x1+20}",stroke=RULE,sw=0.8,dash="3,4")); o.append(text(x0-10,py(c)+4,f"₹{c//1000}k",11,MUTED,anchor="end"))
    o.append(path("M"+" L".join(f"{px(i)},{py(c)}" for i,c in enumerate(costs)),stroke=ACC,sw=2.5))
    for i,(t,tp,fn,fp,c) in enumerate(rows):
        col = GREEN if c==min(costs) else ACC
        o.append(rect(px(i)-5,py(c)-5,10,10,fill=col,stroke=col,rx=5))
        o.append(text(px(i),y0+20,f"{t:g}",11,MUTED,anchor="middle"))
    best=costs.index(min(costs))
    o.append(text(px(best),py(min(costs))-16,"cheapest: ₹13,840",12,GREEN,"bold",anchor="middle"))
    o.append(text(370,y0+42,"decision threshold",12,INK,anchor="middle"))
    o.append(rect(700,80,310,250,fill="#f6f9fc",stroke=RULE,rx=8))
    for i,l in enumerate(["A missed defect costs ₹4,000.","A false alarm costs ₹40.","",
                          "At 0.50: 10 missed, 2 re-inspected","At 0.01: 3 missed, 46 re-inspected","",
                          "Same model, same data.","Only the threshold changed, and the","bill fell by two thirds.","",
                          "Accuracy is 92% at every row,","which is why nobody should quote it."]):
        o.append(text(718,108+i*20,l,11.5,INK if i in (0,1,7,8) else MUTED,"bold" if i in (10,11) else "normal"))
    return svg(1040,y0+60,"".join(o))

if __name__=="__main__":
    fig_images()
    for name,fn in [("fig53-2-training-step.svg",fig_training_step),("fig53-3-attention.svg",fig_attention),
                    ("fig53-4-threshold-cost.svg",fig_threshold)]:
        open(name,"w").write(fn())
    print("ok53")
