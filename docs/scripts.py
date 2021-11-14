""" Copyright aldoniel 2021

contact électronique : new issue -> https://github.com/aldoniel/radcalc/issues 

Ce logiciel est un programme informatique servant à faciliter des calculs radiologiques.

Ce logiciel est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA 
sur le site "http://www.cecill.info".

En contrepartie de l'accessibilité au code source et des droits de copie,
de modification et de redistribution accordés par cette licence, il n'est
offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
seule une responsabilité restreinte pèse sur l'auteur du programme,  le
titulaire des droits patrimoniaux et les concédants successifs.

A cet égard  l'attention de l'utilisateur est attirée sur les risques
associés au chargement,  à l'utilisation,  à la modification et/ou au
développement et à la reproduction du logiciel par l'utilisateur étant 
donné sa spécificité de logiciel libre, qui peut le rendre complexe à 
manipuler et qui le réserve donc à des développeurs et des professionnels
avertis possédant  des  connaissances  informatiques approfondies.  Les
utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
logiciel à leurs besoins dans des conditions permettant d'assurer la
sécurité de leurs systèmes et ou de leurs données et, plus généralement, 
à l'utiliser et l'exploiter dans les mêmes conditions de sécurité. 

Le fait que vous puissiez accéder à cet en-tête signifie que vous avez 
pris connaissance de la licence CeCILL, et que vous en avez accepté les
termes. """

# from typing import Callable !! ne pas importer, ça ralentit à mort l'initialisation de brython: plus 4s. Anoter seulement les types élémentaires.
from browser import document, html,window
#from browser.widgets.dialog import InfoDialog #infodialog bugue sur android
#from typing_extensions import TypeVarTuple
#from math import e as math_e #utiliser le module Math de javascript pour économiser un import
#from math import log as ln
from javascript import Math,Number,NULL
from javascript import Date # on gagne environ un ordre de grandeur en vitesse par rapport à l'objet python
#from browser import  alert # pour les tests
from browser.local_storage import storage
#from browser.session_storage import storage as session_storage #bugue ?

# openonglet

""" def cachecontenudecolore():
    classonglet = document.select('.onglet')
    for onglet in classonglet:
        onglet.style.display = "none" #cacher tout le contenu (chaque rubrique)
    classtablink = document.select('.tablink')
    for tablink in classtablink:
        tablink.className=tablink.className.replace(" w3-green", "") """ # cette fonction génialement écrite est lente et écrite en js
    #c'est un peu bourrin mais ça décolore le texte partout

#cachecontenudecolore()

#plutot qu'utiliser bind, on va ajouter la fonction brython au js namespace https://brython.info/static_doc/en/jsobjects.html
#ev.target.attrs["onglet"]
""" def brython_openonglet(ev,nomonglet:str):
    cachecontenudecolore()
    document.getElementById(nomonglet).style.display = "block"
    ev.currentTarget.className += " w3-green"
    if nomonglet!="DFG":
        ev.currentTarget.closest(".w3-dropdown-hover").children[0].className += " w3-green"
 """ # cette fonction génialement écrite est lente et gardée en js

#window.brython_openonglet = brython_openonglet
#document <= html.H5('Brython Ready! :)')


def cecillacceptefunc(ev):
    # enregistre l'acceptation et affiche le menu
    storage['cecillaccepte']="1"
    document["menu"].style.display="block"
    window.scroll(0,0) #js, scroll en haut
    for item in document.select('[licence]'): #crash debug meu je sais pas pourquoi 
        togcollapse(item) # replier licences
    del document["cecillaccepter"]
    del document["defile"]
    document["assistance"]<="Les icônes du haut permettent d'accéder aux différents calculateurs. Il est souvent possible de passer à la valeur suivante en appuyant sur entrée."

def togcollapse(bouton):
    #fonction redéfinie à partir du js que je maitrise pas.
    bouton.classList.toggle("collapseactive")
    content = bouton.nextElementSibling
    if content.style.maxHeight:
        content.style.maxHeight = None # c'est assez étrange mais c'était null en js, mais NULL plante brython et d'ailleurs cette valeur est mal documentée ?
    else:
        content.style.maxHeight = "max-content" # str(content.scrollHeight+10) + "px" # l'expression en js donne un résultat différent et moindre depuis brython ?? mais max content marche


def cecilladd(ev):
    #charge dynamiquement la licence


    def load_script2(req):
       document["cecill"].html=req.responseText
    
    SCRIPT_PATH = 'cecill21fr.html'
    
    request = window.XMLHttpRequest.new()
    request.onload = lambda e:load_script2(request)
    request.open('GET', SCRIPT_PATH, False)
    request.send()

    #document["cecill"].html=open('cecill21fr.html').read() # marche sur le navigateur mais pas sous cordova où open plante avec une erreur de 404 et erreur protocole file://
    document["evapropos"].unbind("click", cecilladd) #une fois que c'est chargé la fonction se déréférence toute seule

if window.current_onglet=="apropos": # si on charge d'emblée sur le légal
    cecilladd(None)
else:
    document["evapropos"].bind("click", cecilladd) # si on charge pas sur le légal, on ajoute le chargement par le menu

try:
#essaie de lire l'acceptation ds local storage et sinon charge la licence etc.
    assert storage['cecillaccepte']=="1"
except (KeyError,AssertionError):
    storage['cecillaccepte']="0"
    document["menu"].style.display="none"
    link = html.CENTER(html.A(html.BUTTON("↓ Défiler vers Accepter ↓", Class="w3-button w3-red"),href="#cecillaccepter"))
    document["defile"]<=link
    accepte = html.CENTER(html.BUTTON("J'accepte la licence CeCILL", Class="w3-button w3-red w3-large"))
    accepte.bind("click",cecillacceptefunc)
    document["cecillaccepter"]<=accepte
    for item in document.select('[licence]'): # déplier licences après avoir inséré sinon le contect n'a pas la bonne taille...
        togcollapse(item)


class glob_var:
    nextInput_maxint:dict={}

# fonctions communes

def getradiovalue(name):
    collection=document.select(f"[name={name}]") #elt.get(name=name)
    for elem in collection:
        if elem.checked:
            return elem.value

def nextInput(ev,code:str,maxint:int):
    # permet de passer d'un input à l'autre avec entrée pour des float
    if ev.type=="keypress" and ev.keyCode==13:
        try:
            if ev.target.getAttribute("type")=="number": # valider input. je fais l'hypothèse vraie ici mais peut être pas toujours que seuls les inputs ont type==number
                value:float=float(ev.target.value)
                min=ev.target.getAttribute("min")
                if min: #si existe (je ne vérifie pas si min est bien un chiffre...)
                    if value < float(min):
                        raise ValueError(f'{value}<{min}')
            i:int=int(ev.target.getAttribute(code)) #target permet d'accéder à l'élément d'où vient l'évènement 
            if i<(maxint):
                i+=1
                nextitem=document.select(f'[{code}="{i}"]')
                nextitem[0].focus()
                nextitem[0].select()
            else:
                ev.target.click()
        except Exception:
            ev.target.value=""
    ev.stopPropagation()

def formulaire_anime(code:str,calcfunc,nocalc:bool=False):
    #met l'événement nextinput si keypress sur les éléments dont le nom est i+nomducalcul (section)=n
    #met l'événement de calcul sur tous les input si event change
    collection=document.select(f'[i{code}]')
    #print(collection)
    lencollection:int=len(collection)
    if nocalc:
        for elem in collection: #le dernier élément est le bouton calc
            elem.bind("keypress", lambda ev:nextInput(ev,code='i'+code,maxint=lencollection))
    else:
        for elem in collection[:-1]: #le dernier élément est le bouton calc
            elem.bind("keypress", lambda ev:nextInput(ev,code='i'+code,maxint=lencollection))
        collection[lencollection-1].bind("click", calcfunc) #bind to calcfunc

    #code classique buggué : semble marcher mais sélectionne les attributs contenant {code} et non les attributs =={code} collection=document.select(f'#{code} input')
    for elem in document.select(f'input[i{code}]'): #sélection de input et [attribut]
        elem.bind("change", calcfunc)

def radio_anime(name:str,calcfunc):
#name : valeur de name du radio. Sert à animer les boutons radio mal animés par formulaire_anime. Un élément peut recevoir bind 2x mais ça a pas l'air grave.
    for elem in document.select(f'[name="{name}"]'):
        elem.bind("change",calcfunc)

#DFG

def calcdfg(ev):
    err:str="-"
    try:
        IDMS:bool =  document["IDMS"].checked
        kidms:float=.95 if IDMS else 1
        creat:float=float(document["creat"].value)
        if document["mgdl"].checked:
            creatmol:float=creat/0.1131179
            creatmgdl:float=creat/10
        else:
            creatmol:float=creat
            creatmgdl=0.01131179*creat
        age:float=float(document["age"].value)
        MDRD:int=0
        genre=float(getradiovalue("genre"))
        ethnie=float(getradiovalue("ethnie"))
        MDRD=round(186*(creatmol*.0113)**-1.154*age**-.203*ethnie*genre*kidms)
        document["MDRD"].textContent =MDRD

        genre=int(genre) #ça me gène de faire des tests d'égalité sur des float. cette ligne suppose qu'on teste toujours vs 1
        ethnie=True if ethnie > 1 else False #idem. True == African American
        if IDMS:
            k :float= .9 if genre == 1 else .7
            CKD:int=round( 141*  min(creatmgdl/k, 1)**(-0.411 if genre ==1 else -0.329) * max(creatmgdl/k, 1)**-1.209 * 0.993**age * (1 if genre==1 else 1.018) * (1.159 if ethnie else 1) )
            document["CKD"].textContent =CKD
        else:
            document["CKD"].textContent =err
    except:
        document["MDRD"].textContent = err
        document["CKD"].textContent = err
        return
    try:
        k:float=1.23 if genre==1 else 1.04
        poids:float=float(document["poids"].value)
        cock:int=round(((140-age)/creat)*poids*k)
        document["dfgcg"].textContent =cock
    except:
        document["dfgcg"].textContent =err


formulaire_anime("DFG",calcdfg)
radio_anime("ucr",calcdfg)
document["IDMS"].bind("change",calcdfg)

# modèle de brock

def calcbrock(ev):
    try:
        brock_age:float=float(document["brock_age"].value)
        brock_sexe:float =float(getradiovalue("brock_sexe"))
        brock_kcfam:bool =  document["brock_kcfam"].checked
        brock_emphyseme:bool =  document["brock_emphyseme"].checked
        brock_taille_nodule:float=float(document["brock_taille_nodule"].value)
        brock_nodule_type:float =float(getradiovalue("brock_nodule_type"))
        brock_LS:bool =  document["brock_LS"].checked
        brock_spicule:bool =  document["brock_spicule"].checked
        brock_nb_nodule:float=float(document["brock_nb_nodule"].value)

        t:list=[]
        t.append(0.0286687*(brock_age-62))
        t.append(brock_sexe)
        if brock_kcfam:
            t.append(0.296109)
        if brock_emphyseme:
            t.append(0.2953112)
        t.append(-5.385484*(((brock_taille_nodule)/10)**(-0.5)-1.58113883))
        t.append(brock_nodule_type)
        if brock_LS:
            t.append(0.6581383)    
        if brock_spicule:
            t.append(0.7729335)
        t.append(-0.0824156*(brock_nb_nodule-4))
        t.append(-6.78917)
        exp:float=Math.E**sum(t)
        brock_proba_kc:float=100*exp/(1+exp)
        if Number.isNaN(brock_proba_kc):
            raise ValueError
        document["brock_proba_kc"].textContent=round(brock_proba_kc,1)
        brock_comment:str="Recommandations BTS : "
        if brock_nodule_type==0:
            if brock_taille_nodule< 5:
                brock_comment+="Ne pas suivre les nodules <5 mm de découverte fortuite. (Mais selon Fleischner 2017, un suivi à 1 an est optionnel si le patient est à haut risque.)"
            elif brock_taille_nodule>=5 and brock_taille_nodule <6:
                brock_comment+="Surveillance à 1 an."
            elif brock_taille_nodule>=6 and brock_taille_nodule<8:    
                brock_comment+="Surveillance à 3 mois et volumétrie."
            elif brock_taille_nodule>=8:
                if brock_proba_kc<10:
                    brock_comment+="Surveillance à 3 mois et volumétrie."
                else:
                    brock_comment+="Faire un TEP-scanner avec calcul du risque selon le modèle de Herder."
        else:#nodules "subsolid"
            brock_comment+="En cas de nodule de découverte récente, stable sur le contrôle à 3 mois : "
            if brock_proba_kc<10:
                brock_comment+="contrôle en TDM 1, 2, 4 ans après le baseline."
            else:
                brock_comment+="discuter avec le patient un contrôle en TDM 1, 2, 4 ans après le baseline ; ou une biopsie guidée en imagerie ; ou un traitement (exérèse ou non-chirurgical)."
            brock_comment+=" Une morphologie suspecte du nodule (taille de la portion solide ; indentation pleurale ; aspect en bulles) doit faire discuter un traitement."
        document["brock_avis"].textContent=brock_comment
    except:# Exception as err:
        #print(err.args)
        document["brock_proba_kc"].textContent="-"
        document["brock_avis"].textContent="-"
        

formulaire_anime("brock",calcbrock)
document["brock_clear"].bind("click", lambda ev:iclear("ibrock"))


# modèle de herder

def herder_calc(ev):
    try:
        herder_age:float=float(document["herder_age"].value)
        herder_tabac:float =float(getradiovalue("herder_tabac"))
        herder_kc:float =float(getradiovalue("herder_kc"))
        herder_LS:float =float(getradiovalue("herder_LS"))
        herder_mm:float=float(document["herder_mm"].value)
        herder_spicule:float =float(getradiovalue("herder_spicule"))
        herder_fdg:float =float(getradiovalue("herder_fdg"))

        x:float=.0391*herder_age+.1274*herder_mm+herder_tabac+herder_kc+herder_LS+herder_spicule-6.8272
        probakcsanstep:float=1/(1+Math.E**-x) #100*math_e**x/(1+math_e**x)
        y:float=-4.739+3.691*probakcsanstep+herder_fdg
        herder_proba_kc:float=100/(1+Math.E**-y)
        if Number.isNaN(herder_proba_kc):
            raise ValueError
        document["herder_proba_kc"].textContent=round(herder_proba_kc,1)
        herder_comment:str="Recommandations BTS : "
        if herder_mm<8:
            herder_comment+="""<div class="w3-panel w3-red">Avertissement : dans l'algorythme de la BTS, le modèle de Herder en TEP concerne exclusivement les nodules ≥ 8mn. Comme la population dans l'étude de Herder a été rétrospectivement incluse entre 1997 et 2001, il est vraissemblable que les nodules de petite taille n'ont pas été inclus et que donc la probabilité calculée sera d'autant moins valide que le nodule est petit (utiliser alors plutôt le modèle de Brock). Ci-après, pour information, voici quelles auraient été les recommandations si le nodule mesurait au moins 8mm. Ces recommandations sont à interpréter selon le bon sens.</div>"""
        if herder_proba_kc<10:
            if herder_mm>=6:
                herder_comment+="Surveillance à 3 mois."
            elif herder_mm>=5:
                herder_comment+="Surveillance à 1 an."
            elif herder_mm<5:
                herder_comment+="Ne pas suivre les nodules <5 mm de découverte fortuite. (Mais selon Fleischner 2017, un suivi à 1 an est optionnel si le patient est à haut risque.)"
        elif herder_proba_kc<=70:
            herder_comment+="Selon le risque individuel et la préférence du patient, envisager une biopsie guidée par l'imagerie ; ou sinon, une biopsie-exérèse ou une surveillance en TDM."
        elif herder_proba_kc>70:
            herder_comment+="Envisager une exérèse ou un traitement non-chirurgical (± une biopsie guidée par l'imagerie)."
        document["herder_avis"].html=herder_comment
    except Exception:
        document["herder_proba_kc"].textContent="-"
        document["herder_avis"].textContent="-"


formulaire_anime("herder",herder_calc)
document["herder_clear"].bind("click", lambda ev:iclear("iherder"))

# VTD

def vtd_approxvol(formule:str)->float:
    #calcule volume à partir de string 5 ou 5x6 ou 5x6x7
    motif:str="*" #ne peut être "" sinon split->Valuerror
    if "-" in formule:
        motif="-"
    elif "x" in formule:
        motif="x"
    elif ' ' in formule:
        motif=' '
    
    try:
        t:tuple=tuple(map(float,formule.lower().split(motif))) #conversion en tuple de float d'une string au format
        result:float=0
        lt:int=len(t)
        if lt==3:
            result=t[0]*t[1]*t[2]/2
        elif lt==2:
            result=(t[0]*t[1]*(t[0]+t[1])/2)/2
        elif lt==1:
            result=t[0]**3/2
        return result
    except ValueError:
        raise ValueError

def vtd_calc(ev):
    try:
        vtd_date1:str=str(document["vtd_date1"].value)
        try:
            vtd_vol1:float=float(document["vtd_vol1"].value)
        except ValueError:
            vtd_vol1:float=vtd_approxvol(document["vtd_vol1b"].value)
            document["vtd_vol1c"].textContent=f"Soit environ {vtd_vol1} mm³"
        try:
            vtd_vol2:float=float(document["vtd_vol2"].value)
        except ValueError:
            vtd_vol2:float=vtd_approxvol(document["vtd_vol2b"].value)
            document["vtd_vol2c"].textContent=f"Soit environ {vtd_vol2} mm³"
        vtd_date2:str=str(document["vtd_date2"].value)
        vtd_delta:float=Math.abs((Date.new(vtd_date2).getTime()-Date.new(vtd_date1).getTime())/86400000) # /nb ms par jour ; Date.new("YYYY.MM.DD") est une initialisation au format iso
        document["vtd_delta"].textContent=f" ({vtd_delta} jours après le 1er scanner.)" #print(f"nb de jours : {vtd_delta}")
        vtd_vdt:float=Math.LN2*vtd_delta/Math.log(vtd_vol2/vtd_vol1)
        vtd_vol_delta:float=100/vtd_vol1*(vtd_vol2-vtd_vol1)
        if Number.isNaN(vtd_vdt):
            print("isNaN")
            raise ValueError
        document["vtd_vdt"].textContent=f"{round(vtd_vdt)} jours (volume {round(vtd_vol_delta):+}%)"
        vtd_avis:str="Selon la BTS : "
        if abs(vtd_vol_delta)<25:
            vtd_avis+='la différence de volume est non significative (nodule "stable"). '
            vtd_tmpstr1:str="Contrôler à 1 an si on vient de faire le contrôle à 3 mois. "
            vtd_tmpstr2:str="Arrêt du suivi si la probabilité de cancer est <10% (Brock ± Herder) ET si on vient de faire le contrôle à 1 an en volumétrie automatisée. Si la volumétrie est manuelle, les contrôles sont à 3 mois ; 1 an ; 2 ans (avec une gestion à 2 ans comme à 1 an)."
            if vtd_delta<120:
                vtd_avis+=vtd_tmpstr1
            elif vtd_delta>210:
                vtd_avis+=vtd_tmpstr2
            else:
                vtd_avis+=(vtd_tmpstr1+vtd_tmpstr2)
        else:
            if vtd_vdt<0:
                vtd_avis+="""Les recommandation BTS ne proposent pas de conduite à tenir pour les nodules diminuant significativement de taille. Cependant, certains cancers peuvent diminuer de taille. Il est "d'usage" (contactez-moi si vous avez une référence) de suspecter une cause infectieuse/inflammatoire dans ce cas et de surveiller."""
            elif vtd_vdt<=400:
                vtd_avis+="poursuivre les investigations diagnostiques (biopsie, imagerie, résection)."
                if vtd_vdt<30 and vtd_delta<100:
                    vtd_avis+="""<div class="w3-panel w3-orange">Remarque : Les nodules à croissance rapide avec un temps de doublement <30 jours sont plutôt infectieux. (Cette information n'est pas reprise dans l'algorythme BTS).</div>"""
            elif vtd_vdt >400 and vtd_vdt<=600:
                vtd_avis+='Envisager la biopsie ou la surveillance selon la préférence du patient.'
            elif vtd_vdt>600:
                vtd_avis+="Envisager d'arrêter la surveillance (seulement en cas de volumétrie automatisée) ou de la poursuivre selon la préférence du patient."
        document["vtd_avis"].html=vtd_avis
    except Exception:
        document["vtd_vdt"].textContent="-"
        document["vtd_avis"].textContent="-"
        document["vtd_delta"].textContent=""
        document["vtd_vol1c"].textContent=""
        document["vtd_vol2c"].textContent=""

formulaire_anime("vtd",vtd_calc)
formulaire_anime("vtd2",vtd_calc) # astuce pour découpler les champs volume et volume approx
document["vtd_clear"].bind("click", lambda ev:iclear("ivtd"))
document["vtd_clear"].bind("click", lambda ev:iclear("ivtd2"))

def vtd_ajd(ev):
    document["vtd_date2"].value=Date.new().toISOString()[0:10]

document["vtd_ajd"].bind("click", vtd_ajd)

def vtd_3m(ev):
    #calculter today-3m
    a=Date.new()
    a.setMonth(a.getMonth() - 3)
    document["vtd_date1"].value=a.toISOString()[0:10]


document["vtd_3m"].bind("click", vtd_3m)
document["vtd_ajd"].bind("click", vtd_calc)
document["vtd_3m"].bind("click", vtd_calc)

# modal

modal=document["modal_id"]
modalImg=document["img01"]
modal_captionText=document["caption"]
zm=None

def modal_show(ev):
    global zm
    zm = window.Zoom.new(document["img01"], {'pan': True, 'rotate': False })
    modal.style.display = "block"
    modalImg.src = ev.target.getAttribute("src")
    modal_captionText.innerHTML = ev.target.getAttribute("alt")

def modal_hide(ev):
    global zm
    del zm #la biblio de zoom lie des événements, faut les libérer.
    modal.style.display = "none"


collection=document.select("[modalbouton]")
for item in collection:
    item.bind("click", modal_show)

document.select('.modal_close')[0].bind("click", modal_hide)

# DFGabs


def DFGabs_calc(ev):
    try:
        DFGrel:float=float(document["DFGrel"].value)
        taillecm:float=float(document["taillecm"].value)
        poidskg:float=float(document["poidskg"].value)

        DFGabs:float=DFGrel/1.73*0.007184 * pow(taillecm,0.725) * pow(poidskg,0.425)
        if Number.isNaN(DFGabs):
            raise ValueError
        document["DFGabs"].textContent=round(DFGabs)
    except:
        document["DFGabs"].textContent="-"


formulaire_anime("DFGabs",DFGabs_calc,True)

# schwartz

def calcschwartz(ev):
    try:
        creatsch:float=float(document["creatsch"].value)
        taillecmsch:float=float(document["taillecmsch"].value)
        if document["mmolsch"].checked:
            #creatmol:float=creatsch/0.1131179
            creatmgdl:float=creatsch/10
        else:
            #creatmol:float=creatsch
            creatmgdl=0.01131179*creatsch
        document["dfgsch"].textContent = round(0.413*taillecmsch/creatmgdl)
    except:
        document["dfgsch"].textContent = "-"
        return

formulaire_anime("schwartz",calcschwartz)
for item in document.select(f'[name="usch"]'):
    item.bind("change",calcschwartz)

# sauvegarder dans le browser storage le dernier onglet
def code2sortie(ev):
    storage['last_onglet'] = window.current_onglet #importation de la variable javascript
    return NULL #return javascript NULL pour enlever la popup de sortie https://stackoverflow.com/questions/13443503/run-javascript-code-on-window-close-or-page-refresh

window.onbeforeunload = code2sortie # enregistre la sortie sur navigateur sur android, ce code ne marche jamais (ni en pause, ni au kill)
document.addEventListener("pause", code2sortie, False) # enregistre l'événement pause d'android via cordova 

lderniersonglets:list=[]
try: 
    lderniersonglets.append(window.current_onglet) # si js a gangé la course, alors current_onglet a été initialisé et try{dernierongletclic(ongletName);} a échoué donc j'initialise
except:
    print("tiens, brython a été plus rapide que js!")

def dernierongletclic(onglet:str):
    global lderniersonglets
    lderniersonglets.append(onglet)
    
window.dernierongletclic=dernierongletclic #ajout de la fonction brython au js namespace

def onBackKeyDown(ev):
    # ajoute le comportement android normal si presse back
    try:
        del lderniersonglets[-1] #supprime la page actuelle
        window.openonglet(NULL,lderniersonglets.pop())
    except IndexError:
        window.navigator.app.exitApp()

document.addEventListener("backbutton", onBackKeyDown, False)

#recist 

def isnumber(s)->bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def calcrecist(ev):
    sumb_manuel=None #super hackish... sert à désactiver les vérifications de tableau
    suma_manuel=None
    recist_warning:str=""
    try:
            suma_manuel=float(document["recist_suma_manuel"].value)
            recist_warning="(somme manuelle en colone 1)"
    except:
        pass
    try:
        sumb_manuel=float(document["recist_sumb_manuel"].value)
        recist_warning="(somme manuelle en colone 2)" if not recist_warning else "(somme manuelle en colone 1 & 2)"
    except:
        pass
    try:
        l_A:list=[]
        l_B:list=[]
        i:int=0
        lirecist:list=document.select('[irecist]')
        #lirecist.pop()
        del lirecist[-1]  #le dernier item c'est le bouton qui n'a pas de valeur
        for i in range(1,11):
            item=lirecist.pop()
            if i%2==0:
                l_A.append(item.value)
            else:
                l_B.append(item.value)
        # attention, à ce stade les listes sont non validées et de type string peut être non castable en réel
        i=6
        for (a,b) in zip(l_A,l_B):
            i-=1 # en popant la liste je l'ai inversée, du coup le compteur aussi...
            if sumb_manuel or suma_manuel:
                if a=='':
                    l_A[i-1]=0
                else:
                    if isnumber(a):
                        l_A[i-1]=float(a)
                    else:
                        raise TypeError(i)
                if b=='':
                    l_B[i-1]=0
                else:
                    if isnumber(b):
                        l_B[i-1]=float(b)
                    else:
                        raise TypeError(i)
            else:
                if (isnumber(a) and isnumber(b)) or (a=='' and b==''):
                    #élimine les lignes à moitié nulles ou contenant du texte
                    if a=='' and b=='': # met à zéro les lignes vides (rq : firefox renvoie '' si on tappe du texte ds le champ nombre)
                        l_A[i-1]=0
                        l_B[i-1]=0
                    else:
                        l_A[i-1]=float(a)
                        l_B[i-1]=float(b)
                else:
                    raise TypeError(i) # ex, si un navigateur accepte du texte ds un champ nombre...
        sumlA:float=sum(l_A)
        sumlB:float=sum(l_B)
        suma:float=suma_manuel if suma_manuel else sumlA
        sumb:float=sumb_manuel if sumb_manuel else sumlB
        document["recist_suma"].textContent = sumlA
        document["recist_sumb"].textContent = sumlB
        recist:float=round(100/suma*sumb-100,1)
        document["recist_recist"].textContent ='SPD {:+.1f} % : {} {}'.format(recist,"progression" if recist>=20 and (sumb-suma) >=5 else ("réponse complète" if recist==-100 else "réponse partielle" if recist<=-30 else "maladie stable"),recist_warning) #1 chiffre après , et signé
    except ZeroDivisionError:
        document["recist_recist"].textContent = "division par zéro : il doit y avoir une erreur de saisie de la colone 1..."
        document["recist_suma"].textContent ="-"
        document["recist_sumb"].textContent ="-"
    except TypeError as e:
        ermsg:str="erreur de saisie"
        if len(e.args)==1:
            ermsg=f"{ermsg} ligne {e.args[0]}"
        document["recist_recist"].textContent = ermsg
    except Exception:
        document["recist_recist"].textContent = "erreur générique"

formulaire_anime("recist",calcrecist)
document["recist_suma_manuel"].bind("change",calcrecist)
document["recist_sumb_manuel"].bind("change",calcrecist)

def iclear(inom:str):
    champs:list=document.select(f'[{inom}].w3-input')
    for item in champs:
        item.value=""
    radio:list=document.select(f'[{inom}].w3-radio')
    for item in radio:
        item.checked=False

def recistleftoverclear(ev):
    document["recist_suma"].textContent ="-"
    document["recist_sumb"].textContent ="-"
    document["recist_suma_manuel"].value =""
    document["recist_sumb_manuel"].value =""
    document["recist_recist"].textContent ='-'

document["recist_clear"].bind("click", lambda ev:iclear("irecist"))
document["recist_clear"].bind("click", recistleftoverclear)

#washout

def calcwashout(ev):
    try:
        uh0:float=float(document["uh0"].value)
        uh70:float=float(document["uh70"].value)
        uh15:float=float(document["uh15"].value)
        worel:float= 100*(uh70-uh15)/uh70
        woabs:float=100*(uh70-uh15)/(uh70-uh0)

        document["washout_avis"].html="Remarque : la densité spontanée est entre -30 et -115 U.H., ne s'agit-il pas d'un myélolipome ? ...</p>" if (uh0<=-30 and uh0>=-115) else "<p>Remarque : la densité spontanée est ≤ à 10 U.H., en faveur d'un adénome. Le calcul du lavage n'était pas nécessaire.</p>" if uh0<=10 else "erreur de saisie ?" if uh0>200 else ""
        document["washout_relatif"].textContent ='{:+.1f} % : {}'.format(worel,"en faveur d'un adénome" if worel>=40 else "indéterminé")
        document["washout_absolu"].textContent = '{:+.1f} % : {}'.format(woabs,"en faveur d'un adénome" if woabs>=60 else "indéterminé")

    except Exception:
        document["washout_relatif"].textContent = "-"
        document["washout_absolu"].textContent = "-"

formulaire_anime("washout",calcwashout)

# chuteirm

def calcchuteirm(ev):
    try:
        insur:float=float(document["insur"].value)
        outsur:float=float(document["outsur"].value)
        chutesurr:float=100*(insur-outsur)/insur
        document["chuteirm_sur"].textContent ='{:+.1f} % {}'.format(chutesurr,"> 16,5% en faveur d'un adénome" if chutesurr>16.5 else "indéterminé")
        
        try:
            inrat:float=float(document["inrat"].value)
            outrat:float=float(document["outrat"].value)
            chuterat=(outsur/outrat)*(inrat/insur)
            document["chuteirm_rat"].textContent = '{:+.2f} {}'.format(chuterat,"< 0,71 en faveur d'un adénome" if chuterat<0.71 else "indéterminé")
        except Exception:
            document["chuteirm_rat"].textContent = '-'

    except Exception:
        document["chuteirm_rat"].textContent = '-'
        document["chuteirm_sur"].textContent = "-"

formulaire_anime("chuteirm",calcchuteirm)

# nascet

def calcnascet(ev):
    try:
        document["nascet_ste"].textContent =f'{round(100*(1-float(document["petitdiam"].value)/float(document["gddiam"].value)))} %'
    except Exception:
        document["nascet_ste"].textContent = '-'

formulaire_anime("cstenose",calcnascet) 

#testis
def calctestis(ev):
    try:
        if document["testisformule"].checked:
            document["testisvol"].textContent ='{:.1f} mL'.format(.00071*float(document["testix"].value)*float(document["testiy"].value)*float(document["testiz"].value))
        else:
            document["testisvol"].textContent ='{:.1f} mL'.format(Math.PI/6000*float(document["testix"].value)*float(document["testiy"].value)*float(document["testiz"].value))
    except Exception:
        document["testisvol"].textContent = '-'

formulaire_anime("testis",calctestis)
radio_anime("testisformule",calctestis)
document["testis_clear"].bind("click", lambda ev:iclear("itestis"))

# lugano

def lugano_pd(formule:str,just_split:bool=False):
    #revoie le produit petit axe * grand axe par défaut et sinon un tuple (petit_axe,grand_axe) si just_split (oui c'est moche)
    if formule=="0":
        if just_split:
            return (0,0)
        else:
            return 0
    if "+" in formule:#par récursivité je traite
        splitformule:list=formule.split('+')
        l_f_split:list=[]
        l_t_split:list=[]
        for item in splitformule:
            l_f_split.append(lugano_pd(item))
        if just_split==False:
            return sum(l_f_split)
        else:
            for item in splitformule:
                l_t_split.append(lugano_pd(item,True))
            return l_t_split[l_f_split.index(max(l_f_split))]#ret le plus gros morceau issu de la frag de la lésion

    #calcule volume à partir de string 5 ou 5x6 ou 5x6x7
    motif:str="*" #ne peut être "" sinon split->Valuerror
    if "-" in formule:
        motif="-"
    elif "x" in formule:
        motif="x"
    elif ' ' in formule:
        motif=' '
    try:
        t:tuple=tuple(map(float,formule.lower().split(motif))) #conversion en tuple de float d'une string au format
        if len(t)!=2:
            raise ValueError
        if not just_split:
            return t[0]*t[1]
        else:
            if t[0]<t[1]:
                return (t[0],t[1])
            else:
                return (t[1],t[0])
    except ValueError:
        raise ValueError

def calclugano(ev):
    sumb_manuel=None #super hackish... sert à désactiver les vérifications de tableau
    suma_manuel=None
    lugano_warning:str=""
    lugano_manuelerr:str="(Somme manuelle en colone {} : Vous devez évaluer manuellement la variation de chaque lésion !)"
    try:
            suma_manuel=float(document["lugano_suma_manuel"].value)
            lugano_warning=lugano_manuelerr.format('"Avant"')
    except:
        pass
    try:
        sumb_manuel=float(document["lugano_sumb_manuel"].value)
        lugano_warning=lugano_manuelerr.format('"Aujourd\'hui"') if not lugano_warning else lugano_manuelerr.format('"Avant" et "Aujourd\'hui"')
    except:
        pass
    try:
        l_A:list=[]
        l_B:list=[]
        l_cmp:list=[]
        i:int=0
        lilugano:list=document.select('[ilugano]')
        lilugano_rate:list=[]
        lugano_ratedefined:bool=False
        lugano_pasadenomegalie:bool=True
        del lilugano[-1] #le dernier item c'est le bouton qui n'a pas de valeur 
        lilugano_rate.append(lilugano.pop())
        lilugano_rate.append(lilugano.pop())
        for i in range(1,13):
            item=lilugano.pop()
            if i%2==0:
                l_A.append(item.value)
            else:
                l_B.append(item.value)
        # attention, à ce stade les listes sont non validées et de type string peut être non castable en réel
        i=7
        for (a,b) in zip(l_A,l_B):
            i-=1 # en popant la liste je l'ai inversée, du coup le compteur aussi...
            if sumb_manuel or suma_manuel:
                if a=='':
                    l_A[i-1]=0
                else:
                    try:
                        l_A[i-1]=lugano_pd(a)
                    except:
                        raise TypeError(i)
                if b=='':
                    l_B[i-1]=0
                else:
                    try:
                        l_B[i-1]=lugano_pd(b)
                    except:
                        raise TypeError(i)
            else:
                if (a=='' and b=='') or (len(a)>0 and len(b)>0):
                    #élimine les lignes à moitié nulles
                    if a=='' and b=='': # met à zéro les lignes vides (rq : firefox renvoie '' si on tappe du texte ds le champ nombre)
                        l_A[i-1]=0
                        l_B[i-1]=0
                        l_cmp.append(None) # vide
                    else:
                        try:
                            l_A[i-1]=lugano_pd(a)
                            l_B[i-1]=lugano_pd(b)
                            if l_A[i-1]==0:
                                l_cmp.append(float("nan")) # /0 (progression)
                            else:
                                l_cmp.append((100/l_A[i-1]*l_B[i-1]-100,lugano_pd(a,True),lugano_pd(b,True)))#dégueu, ajoute ( +%,(a_axe1,a_axe2),(b_axe1,b_axe2) )
                                if lugano_pasadenomegalie:
                                    petit,grand=lugano_pd(b,True)
                                    if petit>10 or grand >15:
                                        lugano_pasadenomegalie=False

                        except:
                            raise TypeError(i)
                else:
                    raise TypeError(i) # ex, si un navigateur accepte du texte ds un champ nombre
        sumlA:float=sum(l_A)
        sumlB:float=sum(l_B)
        suma:float=suma_manuel if suma_manuel else sumlA
        sumb:float=sumb_manuel if sumb_manuel else sumlB
        document["lugano_suma"].textContent = sumlA
        document["lugano_sumb"].textContent = sumlB
        lugano:float=round(100/suma*sumb-100,1)
        lugano_p_justif:list=[]
        lugano_cr:bool=False
        lugano_pr:bool=False
        i=7 #6+1
        for item in l_cmp:
            i-=1
            if item==None:
                continue
            else:
                if not (type(item) is tuple) and Number.isNaN(item):#c'est laid et ça m'apprendra à faire des listes composites car isnan accepte des réels slm
                    lugano_p_justif.append(f"La lésion {i} est apparue.")
                    continue
                else:
                    (percent,axesa,axesb)=item
                    if percent>=50:
                        if axesb[1]>15:#si le grand axe de la lésion actuelle est >15mm
                            diff:float=max(axesb[1]-axesa[1],axesb[0]-axesa[0]) #évolution max des axes
                            if (axesb[1]>20 and diff>=10) or (axesb[1]<20 and diff>=5):
                                lugano_p_justif.append(f"La lésion {i} a augmenté de {round(percent)}%.")
        #conversion de lilugano_rate en liste de str(float)
        lilugano_rate[0]=lilugano_rate[0].value
        lilugano_rate[1]=lilugano_rate[1].value
        if (lilugano_rate[0]!='' and lilugano_rate[1]=='') or (lilugano_rate[0]=='' and lilugano_rate[1]!=''):
            raise TypeError(7)#rate mal saisie
        elif lilugano_rate!=['','']:
            try:#conversion en float
                lilugano_rate[0]=float(lilugano_rate[0])
                lilugano_rate[1]=float(lilugano_rate[1])
                ratehaut:float=lilugano_rate[0]-lilugano_rate[1]
                lugano_ratedefined=True
                if lilugano_rate[1]<=130 and ratehaut>20:
                    lugano_p_justif.append(f'La rate précédemment "normale" a augmenté de {round(ratehaut)}mm.')
                elif lilugano_rate[1]>130:
                    percentevolrate130:float=100/(lilugano_rate[1]-130)*(lilugano_rate[0]-130)-100
                    if percentevolrate130>50:
                        lugano_p_justif.append(f'La splénomégalie a augmenté de {round(percentevolrate130)}%.')
            except:
                raise TypeError(7)
        if not lugano_ratedefined:
            lugano_warning+=" Il manque les mesures de la rate."
        if not lugano_p_justif:
            if lugano<=-50 and lugano_ratedefined and percentevolrate130<=-50:
                lugano_pr=True
                if lilugano_rate[0]<=130 and lugano_pasadenomegalie:
                    lugano_cr=True

        lugano_avis:str=f"Progression : {' '.join(reversed(lugano_p_justif))}" if lugano_p_justif else "Réponse complète (si les non-cibles ont aussi disparu)" if lugano_cr else "Réponse partielle" if lugano_pr else "Maladie stable" if lugano_warning=="" else ""
        document["lugano_lugano"].textContent ='SPD {:+.1f} %. {} {}'.format(lugano,lugano_avis,lugano_warning) #1 chiffre après , et signé
    except ZeroDivisionError as e:
        document["lugano_lugano"].textContent = "division par zéro : il doit y avoir une erreur de saisie de la colone 1 "
        document["lugano_suma"].textContent ="-"
        document["lugano_sumb"].textContent ="-"
    except TypeError as e:
        ermsg:str="erreur de saisie"
        if len(e.args)==1:
            ermsg=f"{ermsg} ligne {e.args[0]}"
        document["lugano_lugano"].textContent = ermsg
    except Exception:
        document["lugano_lugano"].textContent = "erreur générique"

formulaire_anime("lugano",calclugano)
document["lugano_suma_manuel"].bind("change",calclugano)
document["lugano_sumb_manuel"].bind("change",calclugano)

def iclear(inom:str):
    champs:list=document.select(f'[{inom}].w3-input')
    for item in champs:
        item.value=""
    radio:list=document.select(f'[{inom}].w3-radio')
    for item in radio:
        item.checked=False

def luganoleftoverclear(ev):
    document["lugano_suma"].textContent ="-"
    document["lugano_sumb"].textContent ="-"
    document["lugano_suma_manuel"].value =""
    document["lugano_sumb_manuel"].value =""
    document["lugano_lugano"].textContent ='-'

document["lugano_clear"].bind("click", lambda ev:iclear("ilugano"))
document["lugano_clear"].bind("click", luganoleftoverclear)