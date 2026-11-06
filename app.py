import re,math,sys,unittest
from collections import Counter
from pathlib import Path
def vectors(texts):
    counts=[Counter(re.findall(r'\b\w{2,}\b',s.casefold()))for s in texts];df=Counter(w for c in counts for w in c)
    result=[]
    for c in counts:
        v={w:n*(math.log((1+len(texts))/(1+df[w]))+1)for w,n in c.items()};norm=math.sqrt(sum(x*x for x in v.values()));result.append({w:x/norm for w,x in v.items()}if norm else{})
    return result
def compare(texts):
    v=vectors(texts);return sorted([(sum(value*v[j].get(w,0)for w,value in v[i].items()),i,j)for i in range(len(v))for j in range(i+1,len(v))],reverse=True)
def clusters(size,pairs,threshold):
    parent=list(range(size))
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    for score,a,b in pairs:
        if score>=threshold:parent[root(a)]=root(b)
    return [root(i)for i in range(size)]
class Tests(unittest.TestCase):
    def test_similarity(self):
        pairs=compare(['red apple fruit','red apple fruit','network socket']);self.assertAlmostEqual(pairs[0][0],1);self.assertEqual(pairs[0][1:],(0,1));self.assertEqual(clusters(3,pairs,.8)[0],clusters(3,pairs,.8)[1]);self.assertNotEqual(clusters(3,pairs,.8)[0],clusters(3,pairs,.8)[2]);self.assertEqual(vectors([''])[0],{})
def ui():
    import tkinter as tk
    from tkinter import ttk,filedialog,messagebox
    r=tk.Tk();r.title('Document Similarity Explorer');r.geometry('1000x680');panel=ttk.Frame(r,padding=18);panel.pack(fill='both',expand=True);ttk.Label(panel,text='Find related documents.',font=('Segoe UI',24)).pack(anchor='w');threshold=tk.StringVar(value='0.5');ttk.Label(panel,text='Cluster cosine threshold 0–1').pack(anchor='w');ttk.Entry(panel,textvariable=threshold).pack(fill='x');tree=ttk.Treeview(panel,columns=('score','a','b'),show='headings');[tree.heading(c,text=c)for c in tree['columns']];tree.pack(fill='both',expand=True);status=tk.StringVar();ttk.Label(panel,textvariable=status).pack(anchor='w')
    def openfolder():
        folder=filedialog.askdirectory()
        if not folder:return
        try:
            value=float(threshold.get())
            if not 0<=value<=1:raise ValueError('Threshold must be 0–1')
            paths=sorted(p for p in Path(folder).iterdir()if p.suffix.lower()in('.txt','.md')and p.is_file())
            if len(paths)>200:raise ValueError('Limit: 200 files')
            if any(p.stat().st_size>1024*1024 for p in paths):raise ValueError('Limit: 1 MiB per file')
            texts=[p.read_text(encoding='utf-8')for p in paths];pairs=compare(texts);groups=clusters(len(paths),pairs,value);tree.delete(*tree.get_children())
            for score,a,b in pairs[:500]:tree.insert('','end',values=(f'{score:.3f}',paths[a].name,paths[b].name))
            status.set(f'{len(paths)} files · {len(set(groups))} connected clusters at {value} · top 500 pairs')
        except (OSError,ValueError)as e:messagebox.showerror('Compare',str(e))
    ttk.Button(panel,text='Compare folder',command=openfolder).pack(pady=10);r.mainloop()
if __name__=='__main__':unittest.main(argv=[sys.argv[0]])if '--self-test'in sys.argv else ui()
