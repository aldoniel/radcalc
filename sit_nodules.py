# todo : je suis à peu près sûr de m'être planté dans le tuple unpacking des appels de edge, d'ailleurs quand on utilise yesno on a edge.args=('n',) au lieu de ('n')

try:
    import graphviz
    graphvizok:bool=True
except:
    print("require grapviz ; sudo apt install grapviz ; pip install graphviz")
    graphvizok=False
    
from typing_extensions import Self #from typing si python > 3.11

class edgeclass():
    def __init__(self,destination:str,func:str,args):
        self.func:str=func
        self.args:tuple=args
        self.destination:str=destination
        
#class logicgraph():
#    pass

class nodeclass():
# name (nom interne),msg (nom affiché) un noeud de diagramme. Contient un défi, un lien vers les noeuds d'après, un message
#le noeud renvoie le nom du noeud suivant et stop si fin
    def __init__(self,parentgraph,name:str,msg:str): #debug ajouter :logicgraph
        self.name:str=name # nom interne
        self.msg:str=msg # nom affiché
        self.edges:list[edgeclass]=[]
        self.parentgraph=parentgraph #c'est pas malin mais ya pas d'autre moyen d'accéder que d'ajouter l'adresse #debug ajouter :logicgraph
    def run(self)->str:
        # -> stop si fin ; nom node suivant
        print(self.msg)
        if "stop" in self.name:
            return "stop" #les nodes de fin affichent leur nom et stopent l'arbre
        for i_edge in range(len(self.edges)):#retourne l'index du 1er lien qui valide sa condition (!! faire liens exclusifs)
            next_node:str=getattr(self,self.edges[i_edge].func)(i_edge) #c'est méga dangeureux...faut tester pcq passe l'analyseur. c'est un appel de la fonction par nom en str
            if next_node!="":# "" est le msg echec test
                return next_node
        raise RuntimeError("erreur de logique, aucun lien n'est valide") #debug, ça implique de lancer le graphe dans un try catch en prod
    def edge(self,destination:str,func:str,*args)->Self:
        # fait un lien depuis soi-même vers un node
        self.edges.append(edgeclass(destination, func,args))
        return self
    def yes(self,i_edge:int)->str:
        # renvoie le lien sans condition. c'est la fonction vérité.
        # debug self.edges[i_edge].isvalidated == True
        return self.edges[i_edge].destination
    def switch(self,i_edge:int)->str:
        #va lister les nodes pointés par un edge de fonction switch pour demander à user d'en choisir un
        switchnodedest:list[str]=[]
        for edge in self.edges:
            if edge.func == "switch":
                switchnodedest.append(edge.destination)
        #debug bon là c'est temporaire
        i:int=0
        for inode in switchnodedest:
            i+=1
            print(f"{i}:{self.parentgraph.getnodemsg(inode)}")
        i=int(input("n° destination ?"))
        return switchnodedest[i-1]
    def yesno(self,i_edge:int)->str:
        # liste les deux nodes pointés par une question
        yesnonodedest:list[str]=["",""]
        count:int=0
        for edge in self.edges:
            if edge.func == "yesno":
                count+=1
                #print(f"{edge.args=}") debug
                if "y" in edge.args:
                    yesnonodedest[0]=edge.destination
                    count+=4
                elif "n" in edge.args:
                    yesnonodedest[1]=edge.destination
                    count+=8
        assert count == 14 , f"{yesnonodedest=}. Un node qui utilise yesno doit l'utiliser 2 fois exactement, un yes un no"
        #debug bon là c'est temporaire
        s:str=input("oui/non ?")
        if "o" in s.lower():
            return yesnonodedest[0]
        else:
            return yesnonodedest[1]
    def no(self,i_edge:int)->str:
        # je trace le graphe avec, faudra réfléchir à l'implémentation de yes,no... ou faire un if(bool)
        return self.edges[i_edge].destination
    def eq(self,i_edge:int)->str:
        # arg0 == arg1
        if self.edges[i_edge].args[0] == self.edges[i_edge].args[1]: #c'est villain comme POO...
            return self.edges[i_edge].destination
        else:
            return ""
    def le(self,i_edge:int)->str:
        # arg0 <= arg1
        if self.edges[i_edge].args[0] <= self.edges[i_edge].args[1]:
            return self.edges[i_edge].destination
        else:
            return ""
    def l(self,i_edge:int)->str:
        # arg0 < arg1
        if self.edges[i_edge].args[0] < self.edges[i_edge].args[1]:
            return self.edges[i_edge].destination
        else:
            return ""
    def g(self,i_edge:int)->str:
        # arg0 > arg1
        if self.edges[i_edge].args[0] > self.edges[i_edge].args[1]:
            return self.edges[i_edge].destination
        else:
            return ""
    def ge(self,i_edge:int)->str:
        # arg0 >= arg1
        if self.edges[i_edge].args[0] >= self.edges[i_edge].args[1]:
            return self.edges[i_edge].destination
        else:
            return ""



class logicgraph():
# une classe de gestions des noeuds. Doit les enregistrer !!! à lancer ds un try
    def __init__(self):
        self.stack:list[nodeclass]=[] #la liste des noeud
        self.dico:dict[str,int]={} #le nom des noeuds(chq noeud s'enregistre là):index
        self.lastdestination:str=""
    def push(self,inode:nodeclass):
        # ajoute un noeud
        self.stack.append(inode)
        if inode.name in self.dico.keys():
            raise IndexError("node homonyme dans stack !")
        self.dico[inode.name]=self.stacklen()-1
    def stacklen(self)->int:
        return len(self.stack)
    def pop(self)->nodeclass:
        #attention, cette fonction ne doit servir qu'à poper le dernier ajout pour le détruire en cas de remontée dans le diagramme sinon on aura des pb d'index
        #non testé
        try:
            return self.stack.pop()
        except IndexError as e:
            print("erreur : logicgraph vide")
            raise e
    def clear(self):
        #efface le stack, je sais pas si ça servira un jour
        self.stack.clear()
    def run(self,index:int=0):
        # exécute le diagrame àp de 0 et s'arrête quand un node renvoie le message "stop" réservé, qui n'est pas un nom de node (ou un node qui arrête l'arbre...)
        if self.stacklen()==0:
            raise RuntimeError("erreur stack vide")
        while True:
            next_node:str=self.stack[index].run()
            if next_node=="stop":
                break
            else:
                index=self.dico[next_node] #index est màj pour savoir quel noeud s'exécute à iternation +1
    def testnodes(self,entrypoints:int=1):
        liste_suivants:list[str]=[]
        list_name:list[str]=[]
        for inode in self.stack:
            ret:str=inode.run() #danger, ça teste seulement que le truc pointe vers un noeud, mais ça teste par toutes les connections... refaire
            list_name.append(inode.name)
            liste_suivants.append(ret)
            assert type(ret)==str
            assert ret!=""
            assert ret in self.dico or 'stop' in ret #vérifie que le noeud suivant existe ou est une fin
                
        set_noms:set=set(list_name)
        assert len(set_noms)==self.stacklen() #pas de noms doublons
        depart:set=set_noms-set(liste_suivants) #
        assert len(depart)==entrypoints,f"error {len(depart)=}" # n point de sépart
        inom:str
        for inom in depart:
            assert "begin" in inom # les points d'entrée doivent s'appeler begin&qc
        """
        todo : tester les liens vers des noeuds inexistants...
        """
    def lastnode(self):
        #revoie le dernier node dans la stack
        return self.stack[-1]
    def node(self,name:str,msg:str)->nodeclass:
        # sucre syntaxique pour créer un noeud dans le graphe
        xnode:nodeclass=nodeclass(self,name,msg)
        self.push(xnode)
        return xnode
    def massnodeadd(self,nodes:tuple[tuple[str,str],...]):
        for item in nodes:
            self.push(nodeclass(self,item[0],item[1]))
    def massedge(self,origin:str,destnodes:tuple[str,...],func:str,*args:str):
        #crée les liens d'un node vers un tuple de destnodes avec la même fonction
        nodeorigin:nodeclass=self.getnode(origin)
        for destnode in destnodes:
            nodeorigin.edge(destnode,func,*args)
    def edgeod(self,origine:str,destination,func:str,*args:str)->Self:
        # fait un lien de origine vers destination vers un node et renvoie le graphe. Est la manière d'ajouter les liens après massnode...
        nodeorigin:nodeclass=self.stack[self.dico[origine]]
        nodeorigin.edge(destination, func,*args)
        self.lastdestination=destination
        #nodeorigin.edges.append(edgeclass(destination, func,args))
        #return self.stack[self.dico[destination]]
        return self
    def edged(self,destination,func:str,*args)->Self:
        # fait un lien depuis self.lastdestination vers un node. Est la manière d'ajouter les liens après massnode...
        assert self.lastdestination!="", "edged doit être utilisé après edgeod"
        self.stack[self.dico[self.lastdestination]].edge(destination,func,*args) #debug *args?
        self.lastdestination=destination
        return self
    def getnode(self,nodename:str)->nodeclass:
        return self.stack[self.dico[nodename]]
    def getnodemsg(self,nodename:str)->str:
        return self.stack[self.dico[nodename]].msg
    def makegraph(self):
        # dessine le graphe avec grapviz
        if graphvizok == False:
            print("missing graphviz")
            return
        g = graphviz.Digraph('G', filename='algo.gv')
        for inode in self.stack:
            g.node(inode.name,label=inode.msg)
            for iedge in inode.edges:
                g.edge(inode.name, iedge.destination, label=f"{iedge.func}{iedge.args}")
        g.view()

"""
lg:logicgraph=logicgraph()
prix=51
lg.node("begin","début diagramme").edge("test","yes") #syntaxe courte

lg.push(nodeclass(lg,"test","combien ça coûte ?"))
lg.lastnode().edge("msg1","le",prix,50).edge("msg2","g",prix,50)

lg.push(nodeclass(lg,"msg1","c'est bon marché"))
lg.lastnode().edge("end","yes")

lg.push(nodeclass(lg,"msg2","c'est cher"))
lg.lastnode().edge("end","yes")

lg.push(nodeclass(lg,"end","fin diagramme"))
lg.lastnode().edge("stop","yes")
lg.run()

lg.makegraph()
#lg.testnodes(1)
"""

dep:logicgraph=logicgraph()
massenode:tuple=(
    #niveau 1
    ("begin","Type de lésion"),
    #niveau 2
    ("rien","Pas de nodule"),
    ("solide","Nodule solide"),
    ("depo","Nodule en verre dépoli pur"),
    ("mixte","Nodule partiellement solide"),
    ('masse',"Masse hilaire ou miliaire"),
    ("cond","Condensation d'allure infectieuse"),
    #niveau 3
    ("benin","Nodule d'allure bénin\n(entièrement calcifié,\ngraisse intranodulaire,\nganglion intrapulmonaire\n(<1cm, distance à la plèvre <1cm,\nsous la carène)"),
    ("100","<=100mm3 (6mm)"),
    ("250","100-250mm3 (6-8mm)"),
    ("500","250-500mm3 (8-10mm)"),
    ("qsuspect",'Présence de signes suspects ? cf###'),
    ("passpect",""),#semble un moyen simple de créer un noeud vide pour yesno
    ("3m6","<= 3cm et portion solide <= 6mm"),
    ("3m68","portion solide 6-8mm"),
    ("m810","portion solide 8-10mm"),
    ("m10","portion solide >10mm"),
    ("m36",">3cm et portion solide <=6mm"),
    ("i3","<= 3cm"),
    ("s3","> 3cm"),
    #niveau 4
    ("stop1a","Contrôle à 1 an"),
    ("stop6m","Contrôle à 6 mois"),
    ("stop3m","Contrôle à 3 mois"),
    ('stop1m',"Contrôle à 1 mois"),
    ('stoprcp',"RCP"),
    )

dep.massnodeadd(massenode)
dep.massedge(origin="begin",destnodes=("rien","solide","depo","mixte","masse","cond"),func="switch")
dep.edgeod("rien","stop1a","yes")
dep.massedge(origin="solide",destnodes=("benin","100","250","500"),func="switch")
dep.edgeod("benin","stop1a","yes")
dep.edgeod("100","stop1a","yes")
dep.edgeod("250","stop6m","yes")
dep.edgeod("500","stop3m","yes")
dep.edgeod("depo","qsuspect","yes").edged("passpect","yesno","n").edged("i3","switch").edged("stop1a","yes")
dep.edgeod("qsuspect","stoprcp","yesno","y")
dep.edgeod("passpect","s3","switch").edged("stop6m","yes")
dep.massedge(origin="mixte",destnodes=("3m6","3m68","m810","m10","m36"),func="switch")
dep.edgeod("3m6","stop1a","yes")
dep.edgeod("3m68","stop6m","yes")
dep.edgeod("m810","stop3m","yes")
dep.edgeod("m10","stop1m","yes")
dep.edgeod("m36","stop6m","yes")
dep.edgeod("masse","stoprcp","yes")
dep.edgeod("cond","stop3m","yes")
dep.makegraph()
dep.run()

