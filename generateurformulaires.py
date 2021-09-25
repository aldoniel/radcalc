import easygui
import pyperclip

class glob_var:
    #Modifié le 08/7/21 : il faut maintenant initialiser nom_compteur sinon ça fera une erreur de type
    html:str=""
    python:str=""
    value_python_pas_init:bool=True
    p_ouvert:bool=True
    nom_compteur:str
    i:int=0

    @staticmethod
    def geti()->int:
        glob_var.i+=1
        return glob_var.i

def input_float(titre:str,varname:str):
    # attention, le code est valeur mini ==1
    html:str=f"""<p><label class="w3-text-teal"><b>{titre}</b></label>
<input required class="w3-input w3-border w3-light-grey" {glob_var.nom_compteur}={glob_var.geti()} type="number" min="1" step="any" id="{varname}" title="Seulement des chiffres S.V.P."></p>"""
    python:str=f'{varname}:float=float(document["{varname}"].value)'
    glob_var.html+=html+"\n"
    glob_var.python+=python+"\n"

#version avec placeholder, à tester sur safari
# def input_date(titre:str,varname:str):
#     # attention, le code est valeur mini ==1 ; Le 20/02/2021 à 15h46 : aucune idée de ce que ce commentaire signifie. Ai dérivé ce code de input_float sans trop comprendre ce que ça fait.
#     html:str=f"""<p><label class="w3-text-teal"><b>{titre}</b></label>
# <input required class="w3-input w3-border w3-light-grey" {glob_var.nom_compteur}={glob_var.geti()} type="date" placeholder="yyyy-mm-dd" id="{varname}" title="Date au format AAAA-MM-JJ"></p>"""
#     python:str=f'{varname}:float=float(document["{varname}"].value)'
#     glob_var.html+=html+"\n"
#     glob_var.python+=python+"\n"

def input_date(titre:str,varname:str):
    # Le 20/02/2021 à 15h46 : aucune idée de ce que ce commentaire signifie. Ai dérivé ce code de input_float sans trop comprendre ce que ça fait.
    html:str=f"""<p><label class="w3-text-teal"><b>{titre}</b></label>
<input required class="w3-input w3-border w3-light-grey" {glob_var.nom_compteur}={glob_var.geti()} type="date" id="{varname}" title="Date au format AAAA-MM-JJ"></p>"""
    python:str=f'{varname}:str=str(document["{varname}"].value)'
    glob_var.html+=html+"\n"
    glob_var.python+=python+"\n"

def input_checked(name_varname:str,label:str,checked:bool=False,compteur:bool=False):
    #attention, qd on crée des checkbox, commencer par cette fonction puis suivre par input_checked_decoy et input_checked_decoy fin sinon ça finit pas la balise p
    if compteur:
        html:str=f"""<input class="w3-radio"  {glob_var.nom_compteur}={glob_var.geti()}  type="radio" name="{name_varname}" id="{name_varname}" {"checked" if checked else ""} >
<label>{label}</label>"""
    else:
        html:str=f"""<input class="w3-radio"  type="radio" name="{name_varname}" id="{name_varname}" {"checked" if checked else ""} >
<label>{label}</label>"""
    python:str=f'{name_varname}:bool =  document["{name_varname}"].checked'
    glob_var.html+=html+"\n"
    glob_var.python+=python+"\n"



def input_checked_decoy(name:str,label:str,checked:bool=False,compteur:bool=False):
    if compteur:
        html:str=f"""<input class="w3-radio"  {glob_var.nom_compteur}={glob_var.geti()}  type="radio" name="{name}" {"checked" if checked else ""} >
<label>{label}</label>"""
    else:
        html:str=f"""<input class="w3-radio"  type="radio" name="{name}" {"checked" if checked else ""} >
<label>{label}</label>"""
    glob_var.html+=html+"\n"

def input_checked_value(label:str,varname:str,value:float,checked:bool=False,compteur:bool=False):
    if compteur:
        html:str=f"""<input class="w3-radio"  {glob_var.nom_compteur}={glob_var.geti()}  type="radio" name="{varname}" value="{value}" {"checked" if checked else ""} >
<label>{label}</label>"""
    else:
        html:str=f"""<input class="w3-radio"  type="radio" name="{varname}" value="{value}" {"checked" if checked else ""} >
<label>{label}</label>"""
    python:str=f'{varname}:float =float(getradiovalue("{varname}"))'
    glob_var.html+=html+"\n"
    # if glob_var.value_python_pas_init==True: j'ai écrit cette ligne pour éviter la duplication mais ça supprime les utilisations suivantes de la fonction donc je vais lier ça au compteur vu que je l'appelle qu'une fois
    #     glob_var.python+=python+"\n"
    #     glob_var.value_python_pas_init=False
    if compteur:
        glob_var.python+=python+"\n"

def label(titre:str):
    html=f'<label class="w3-text-teal"><b>{titre}</b></label>'
    glob_var.html+=html+"\n"

def p():
    #input_float/html gère son p. Label n'en a pas besoin. input_checked_value c'est en manuel car on sait pas trop quand on saute les lignes.
    glob_var.html+="<p>" if glob_var.p_ouvert else "</p>"
    glob_var.p_ouvert= not glob_var.p_ouvert

   
# input_float("Âge (années)","brock_age")

# label("Sexe ?")
# p()
# input_checked_value("Homme","brock_sexe",0,compteur=True)
# input_checked_value("Femme","brock_sexe",0.6010727)
# p()

# label("Histoire familiale de cancer pulmonaire ?")
# p()
# input_checked("brock_kcfam","Oui",compteur=True)
# input_checked_decoy("brock_kcfam","Non")
# p()

# label("Emphysème associé ?")
# p()
# input_checked("brock_emphyseme","Oui",compteur=True)
# input_checked_decoy("brock_emphyseme","Non")
# p()

# input_float("Taille du nodule ? (mm)","brock_taille_nodule")

# label("Type de nodule ?")
# p()
# input_checked_value("Solide","brock_nodule_type",0,compteur=True)
# input_checked_value("Mixte","brock_nodule_type",0.3769578)
# input_checked_value("Verre-dépoli","brock_nodule_type",-0.1276173)
# p()

# label("Nodule d'un lobe supérieur ?")
# p()
# input_checked("brock_LS","Oui",compteur=True)
# input_checked_decoy("brock_LS","Non")
# p()

# label("Nodule spiculé ?")
# p()
# input_checked("brock_spicule","Oui",compteur=True)
# input_checked_decoy("brock_spicule","Non")
# p()

# input_float("Nombre total de nodules ?","brock_nb_nodule")


#---------------------- herder ---------------------------

# input_float("Âge ?","herder_age")

# label("Tabagisme :")
# p()
# input_checked_value("Fumeur ou ancien fumeur","herder_tabac",0.7917,compteur=True)
# input_checked_value("N'a jamais fumé","herder_tabac",0)
# p()

# label("ATCD de cancer extra-thoracique ?")
# p()
# input_checked_value("Oui","herder_kc",1.3388,compteur=True)
# input_checked_value("Non","herder_kc",0)
# p()

# label("Localisation au lobe supérieur ?")
# p()
# input_checked_value("Oui","herder_LS",0.7838,compteur=True)
# input_checked_value("Non","herder_LS",0)
# p()

# input_float("Taille du nodule (mm) ?","herder_mm")

# label("Nodule spiculé ?")
# p()
# input_checked_value("Oui","herder_spicule",1.0407,compteur=True)
# input_checked_value("Non","herder_spicule",0)
# p()

# label("Avidité pour le FDG ?")
# p()
# input_checked_value("Aucune","herder_fdg",0,compteur=True)
# input_checked_value("Faible","herder_fdg",2.322)
# input_checked_value("Modérée","herder_fdg",4.617)
# input_checked_value("Intense","herder_fdg", 4.771)
# p()

#---------------------- VDT ---------------------------

""" label("Examen 1")
input_date("Date du 1er scanner ?","vtd_date1")
input_float("Volume du nodule en mm³?","vtd_vol1")


label("Examen 2")
input_date("Date du 2e scanner ?","vtd_date2")
input_float("Volume du nodule en mm³?","vtd_vol2") """
#--------------------- DFGa -------------------------
"""glob_var.nom_compteur="iDFGabs"
input_float("DFG relatif en ml/mn/1,73m² ?","DFGrel")
input_float("Taille en cm ?","taillecm")
input_float("poids en kg ?","poidskg")"""

#--------------------- schartz -------------------------
# rq ne pas prendre ce code pr comptant, ya pleins de bugs j'ai du CR à la main
# glob_var.nom_compteur="ischwartz"

# input_float("Créatinine ?","creatsch")
# input_checked("mmolsch","en µmol/l",checked=True,compteur=True)
# input_checked_decoy("mgdlsch"," en mg/l")
# input_float("Taille en cm ?","taillecmsch")

#--------------------- washout -------------------------

# glob_var.nom_compteur="iwashout"
# input_float("Densité sans injection","uh0")
# input_float('Densité au temps portal 70" (60-75")',"uh70")
# input_float("Densité au temps tardif 15'","uh15")

"""
glob_var.nom_compteur="ichuteirm"
input_float("Surrénale : Signal en phase","insur")
input_float('Surrénale : Signal en opposition de phase',"outsur")
input_float("Rate : Signal en phase","inrat")
input_float('Rate : Signal en opposition de phase',"outrat")
"""
# --------------------stenose--------------------------
"""
glob_var.nom_compteur="icstenose"
input_float("Sténose","petitdiam")
input_float('Diamètre normal',"gddiam")
input_checked("steform","NASCET",checked=True,compteur=True)
input_checked_decoy("steform","ECST")
"""
#-----------------testis-------------------
glob_var.nom_compteur="itestis"
label("Dimensions du testicule dans les 3 plans")
input_float("x","testix")
input_float('y',"testiy")
input_float('z',"testiz")

ret:str=""
while ret!="exit" and ret!="None":
    ret=str(easygui.buttonbox("choix ?","",("html","py","exit")))
    if ret=="html":
        pyperclip.copy(glob_var.html)
    elif ret=="py":
        pyperclip.copy(glob_var.python)
