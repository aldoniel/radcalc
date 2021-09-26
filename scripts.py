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
from browser.local_storage import storage
from browser.widgets.dialog import InfoDialog
#from typing_extensions import TypeVarTuple
#from math import e as math_e #utiliser le module Math de javascript pour économiser un import
#from math import log as ln
from javascript import Math,Number,NULL
from javascript import Date # on gagne environ un ordre de grandeur en vitesse par rapport à l'objet python
from browser import  alert # pour les tests
from browser.local_storage import storage

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
 """ # cette fonction génialement écrite est lente et écrite en js

#window.brython_openonglet = brython_openonglet
#document <= html.H5('Brython Ready! :)')

def cecillacceptefunc(ev):
    # enregistre l'acceptation et affiche le menu
    storage['cecillaccepte']="1"
    document["menu"].style.display="block"
    window.scroll(0,0) #js, scroll en haut

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
for item in document.select(f'[name="ucr"]'):
    item.bind("change",calcdfg)

def infomdrd(ev):
    InfoDialog("MDRD","ici, MDRD=186*(creat*.0113)<sup>-1.154</sup>*age<sup>-.203</sup>*ethnie*genre) où ethnie=1.212 pour les Afro-Américain et 1 sinon ; où genre=0.742 pour les femmes et 1 sinon.",left=0,ok=True)

document["infomdrd"].bind("click", infomdrd)

def infococ(ev):
    InfoDialog("Cockcroft-Gault","HAS 2012 : la formule de Cockcroft et Gault estime, non le DFG (en mL/min/1,73 m2), mais la clairance de la créatinine (en mL/min). Formule historique pour l'adaptation des posologies des médicaments. Formule : MDRD=round(((140-age)/creat)*poids*k) où k=1.23 pour hommes et 1.04 sinon.",left=0,ok=True)

document["infococ"].bind("click", infococ)

def infockd(ev):
    InfoDialog("CKD-EPI","HAS 2012 : Estimation du DFG : CKD-EPI est l’équation la plus fiable. Ici, CKD=round( 141*  min(creat/k, 1)^(-0.411 si homme sinon -0.329) * max(creat/k, 1)^-1.209 * 0.993^age * (1 si homme sinon 1.018) * (1.159 si Afro-Américain sinon 1) ) ; k = 0.9 si homme sinon 0.7 ; creat : 113,1179 g/mol pour la conversion en mg/dl.",left=0,ok=True)

document["infockd"].bind("click", infockd)

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

#collection[0].select()


def infobrock(ev):
    InfoDialog('&nbsp;', 'McWilliams A, Tammemagi M, Mayo J, Roberts H, Liu G, Soghrati K, Yasufuku K, Martel S, Laberge F. et al. Probability of cancer in pulmonary nodules detected on first screening computed tomography. <a href="https://www.nejm.org/doi/10.1056/NEJMoa1214726" target="_blank">New England Journal of Medicine</a> 2013;369;10.',left=0,ok=True)

document["infobrock"].bind("click", infobrock)

def infoBTS(ev):
    InfoDialog('&nbsp;', '<a href="https://www.brit-thoracic.org.uk/quality-improvement/guidelines/pulmonary-nodules/" target="_blank">BTS Guidelines for the Investigation and Management of Pulmonary Nodules</a><br><a href="https://radiologyassistant.nl/chest/plumonary-nodules/bts-guideline" target="_blank">Résumé sur Radiology Assistant.</a>',left=0,ok=True)

document["infoBTS"].bind("click", infoBTS)
document["infoBTS2"].bind("click", infoBTS)


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

def infoherder(ev):
    InfoDialog('&nbsp;', """<p>106 patients avec un seul nodule pulmonaire de moins de 30 mm furent inclus. Les patients ayant un ATCD de cancer dans les 5 ans précédant la TEP, etc. avaient été exclus. Le coefficient de corrélation interobservateur de l'analyse visuelle du résultat TEP était de 0,87. </p><p>Herder GJ et al. Clinical prediction model to characterize pulmonary nodules: validation and added value of 18F-fluorodeoxyglucose positron emission tomography. <a href="https://doi.org/10.1378/chest.128.4.2490" target="_blank">Chest</a></p>""",left=0,ok=True)

document["infoherder"].bind("click", infoherder)

def infoherder_fixe(ev):
    InfoDialog('&nbsp;', "<ul><li><b>Aucune</b> : fixation indiscernable de celle du parenchyme pulmonaire.</li><li><b>Faible</b> : Fixation ≤ à celle du secteur vasculaire médiastinal.</li><li><b>Modérée</b> : Fixation > à celle du secteur vasculaire médiastinal.</li><li><b>Modérée</b> : Fixation nettement > à celle du secteur vasculaire médiastinal.</li></ul><p>Remarque : de manière surprenante, l'étude Herder ne définit pas les termes de son échelle de fixation. L'échelle donnée ici est celle-proposée par les recommandations BTS à fin de standardisation (grade D).",left=0,ok=True)

document["infoherder_fixe"].bind("click", infoherder_fixe)

def infoAUC(ev):
    InfoDialog('&nbsp;', """Brock : 0,902 ; IC95%[0,856–0,948] , AUC Herder 0,924, IC95%[0,875–0,974] Risk of malignancy in pulmonary nodules: A validation study of four prediction models, Ali Al-Ameri et al., <a href="https://doi.org/10.1016/j.lungcan.2015.03.018">Chest 2015 </a>
<p>AUC Herder (publication initiale) : AUC 0,92 ; IC 95% [0,87–0.97] Herder GJ et al. Clinical prediction model to characterize pulmonary 
nodules: validation and added value of 18F-fluorodeoxyglucose positron 
emission tomography. <a href="https://doi.org/10.1378/chest.128.4.2490" target="_blank">Chest</a></p>
<p>AUC Brock : 0,96 ; IC95%[0,93–0,98] McWilliams A et al. Probability of cancer in pulmonary nodules detected on first screening CT. <a href="https://doi.org/10.1056/nejmoa1214726">N Engl J Med</a></p>""",left=0,ok=True)

document["infoAUC"].bind("click", infoAUC)

# VTD

def vtd_approxvol(formule:str)->float:
    #calcule volume à partir de string 5 ou 5x6 ou 5x6x7
    motif:str="*" #ne peut être "" sinon split->Valuerror
    print("vtd_approxvol1")
    if "-" in formule:
        motif="-"
    elif "x" in formule:
        motif="x"
    elif ' ' in formule:
        motif=' '
    
    try:
        print("vtd_approxvol2")
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

def infovtd(ev):
    InfoDialog('&nbsp;', """Si le champ "Volume du nodule" est rempli, il sera utilisé en priorité.<br>
    Le champ "volume approximatif" admet une valeur en mm (ex pour 5 mm saisir "5" ; pour 5*6 mm saisir "5*6" ; pour 5x6x7 mm saisir "5-6-7". On peut utiliser " *-x" comme séparateur.).<br>
    Avec une dimension, on peut estimer le volume par X³/2.<br>
    En 2D, par X*Y*((X+Y)/2)/2).<br>
    En 3D, par le volume du prisme X*Y*Z/2.""",left=0,ok=True)

document[f"infovtd1"].bind("click", infovtd)
document[f"infovtd2"].bind("click", infovtd)

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

def infoDFGabs(ev):
    InfoDialog('&nbsp;',"Calul simple à partir de l'équation de Dubois et Dubois : DFGabs=DFGrel/1.73*0.007184 * taillecm<sup>0.725</sup> * poidskg<sup>0.425</sup>",left=0,ok=True)

document["infoDFGabs"].bind("click", infoDFGabs)

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


def infosch(ev):
    InfoDialog("équation de Schwartz",'<p>DFG = 0.413*taillecm/creatmgdl</p><p><a href="https://pubmed.ncbi.nlm.nih.gov/19158356/ target="_blank">Schwartz, article original</a></p><p>Le DFG normal avant 2 ans pourra être consulté sur <a href="http://pedsinreview.aappublications.org/content/pedsinreview/14/2/local/back-matter.pdf" target="_blank">Pediatrics in review</a></p>',left=0,ok=True)

document["infosch"].bind("click", infosch)

# sauvegarder dans le browser storage le dernier onglet
def code2sortie(ev):
    storage['last_onglet'] = window.current_onglet #importation de la variable javascript
    return NULL #return javascript NULL pour enlever la popup de sortie https://stackoverflow.com/questions/13443503/run-javascript-code-on-window-close-or-page-refresh

window.onbeforeunload = code2sortie

#recist

def isnumber(s)->bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def calcrecist(ev):
    try:
        l_A:list=[]
        l_B:list=[]
        i:int=0
        lirecist:list=document.select('[irecist]')
        lirecist.pop() #le dernier item c'est le bouton qui n'a pas de valeur
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

        suma:float=sum(l_A)
        sumb:float=sum(l_B)
        recist:float=round(100/suma*sumb-100,1)
        document["recist_suma"].textContent = suma
        document["recist_sumb"].textContent = sumb
        document["recist_recist"].textContent ='SPD {:+.1f} % : {}'.format(recist,"progression" if recist>=20 else ("réponse complète" if recist==-100 else "réponse partielle" if recist<=-30 else "maladie stable")) #1 chiffre après , et signé
    except ZeroDivisionError:
        document["recist_recist"].textContent = "division par zéro : il doit y avoir une erreur de saisie de la colone 1..."
    except TypeError as e:
        ermsg:str="erreur de saisie"
        if len(e.args)==1:
            ermsg=f"{ermsg} ligne {e.args[0]}"
        document["recist_recist"].textContent = ermsg
    except Exception:
        document["recist_recist"].textContent = "erreur générique"

formulaire_anime("recist",calcrecist)

def recist_clear(ev):
    lirecist:list=document.select('[irecist]')
    lirecist.pop()
    for item in lirecist:
        item.value=""

document["recist_clear"].bind("click", recist_clear)

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
        document["testisvol"].textContent ='{:.1f} mL'.format(.00071*float(document["testix"].value)*float(document["testiy"].value)*float(document["testiz"].value))
    except Exception:
        document["testisvol"].textContent = '-'

formulaire_anime("testis",calctestis)