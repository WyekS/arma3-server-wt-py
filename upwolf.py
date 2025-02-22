#!/usr/bin/python3
# coding=utf-8

import os
import os.path
import re
import shutil
import sys
import logging

from datetime import datetime
from urllib import request

# Configuración del logging
logging.basicConfig(filename='update.log', level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Parámetros de entrada  (1) actualiza core y mods, (2) actualiza solo core, (3) actualiza solo mods, (xxxxx) id del mod a actualizar
argument = sys.argv[1]

# Configuracion de SteamCMD
STEAM_CMD_MASTER = "steamcmd"
STEAM_CMD_SLAVES = ["/home/arma302/steamcmd/steamcmd.sh", "/home/arma320/steamcmd/steamcmd.sh", "/home/arma330/steamcmd/steamcmd.sh", "/home/arma340/steamcmd/steamcmd.sh"]
STEAM_USER = sys.argv[2]
STEAM_PASS = sys.argv[3]
A3_SERVER_ID = "233780"

# Grupo de usuario del sistema para la creación de enlaces simbólicos
A3_GROUP_USER = "arma3hc"

# Configuracion de lo servidor maestro
A3_SERVER_MASTER = "arma3hc"
A3_SERVER_DIR_MASTER = "/home/arma3hc/serverfiles"

# Configuración de servidores esclavos. Actualmente usamos 1
A3_SERVER_DIR_SLAVES = {"arma302": "/home/arma302/serverfiles"}

# A3_SERVER_DIR_SLAVES = {"arma302": "/home/arma302/serverfiles",
#                         "arma320": "/home/arma320/serverfiles",
#                         "arma330": "/home/arma330/serverfiles",
#                         "arma340": "/home/arma340/serverfiles"}

# Configuracion para la WORKSHOP
A3_WORKSHOP_ID = "107410"
A3_WORKSHOP_DIR = "{}/steamapps/workshop/content/{}".format(A3_SERVER_DIR_MASTER, A3_WORKSHOP_ID)
PATTERN_MOD = "@"
TO_EXCLUDE = "&"
PATTERN = re.compile(r"workshopAnnouncement.*?<p id=\"(\d+)\">", re.DOTALL)
WORKSHOP_CHANGELOG_URL = "https://steamcommunity.com/sharedfiles/filedetails/changelog"

# Lista de MODS. TODO hacer que lea un fichero o una peticion json/html
#"FFAA MOD": "820994401",
#"FFAA MOD ACE3 Compatibility Addon": "792383905",
#"FFAA Extras": "1303231717",
#"ADV - ACE Medical": "1353873848",
#"advanced_towing": "639837898",
#"advanced_urban_rappelling": "730310357",
#"mlo": "823636749",
#"shacktac_user_interface": "498740884",
#"Project Human 1.2":"1188797395",
#"tac_vests": "779568775",
#"tryk_multiplay-uniform_fix": "741196544",
#"DES Elevator":"708665067",
#"Electronic Warfare":"1568688945",
#"Terrorist Organization Black Order":"654170014",
#"Terrorist Organization Black Order - ACE Compat":"1250708527",
#"Grenade Window Breaker":"1702704179",
#"rhs ace compact":"1835439845",
#"DUI - Squad Radar" : "1638341685",
#"Head Range": "630737877",
#"Sullen Skies CUP": "941263726",
#"Dust efx": "1537745369",
#"ASN Motocycle": "2060066647",
#"CRF 450 SUPERMOTARD": "1545064293",
#"acre2": "751965892",


MODS = {

    "3den_enhanced": "623475643",
    "3den_better_inventory": "1124993203",
    "ace": "463939057",
    "ace_compat_-_rhs_armed_forces_of_the_russian_federation": "773131200",
    "ace_compat_-_rhs_united_states_armed_forces": "773125288",
    "acex": "708250744",
    "ace_optionals": "1189541364",
    "achilles": "723217262",
    "Zeus Enhanced": "1779063631",
    "Advanced Ropes": "2019840605",
    "alive": "620260972",
    "asr_ai3": "642457233",
    "asr_ai3_-_project_opfor_config": "849435425",
    "backpackonchest": "820924072",
    "blastcore_edited_(standalone_version)": "767380317",
    "cba_a3": "450814997",
    "enhanced_movement": "333310405",
    "Enhanced Movement Fix" : "1586691629",
    "gren_evo": "1336178086",
    "Spyder Addons":"579263829",
    "jbad": "520618345",
    "kunduz_afghanistan_-_doors_&_multiplayer_fix": "1623903743",
    "project_opfor": "735566597",
    "rhsafrf": "843425103",
    "rhsusaf": "843577117",
    "rhsgref": "843593391",
    "sma_rhs_compatibility_patch": "1112431110",
    "specialist_military_arms": "699630614",
    "lythium": "909547724",
    "australia": "1182728989",
    "CLA CLAFGHAN": "761349672",
    "CUP Terrains - Maps": "583544987",
    "CUP Terrains - Core": "583496184",
    "CUP Weapons": "497660133",
    "CUP Vehicles": "541888371",
    "CUP Units": "497661914",
    "CUP ACE3 Compatibility Vehicles": "621650475",
    "CUP ACE3 Compatibility Weapons": "549676314",
    "USS Nimitz": "643530417",
    "FIREWILL Aviation Pack": "1381545544",
    "Eurofighter Typhoon AWS": "1625724231",
    "FA-18 Super Hornet": "743099837",
    "G.O.S Al Rayak": "648172507",
    "takistan_cup": "1084720856",
    "Distrikt 41 - Ruegen": "835257174",
    "DS Houses": "1113351114",
    "Em_Buildings": "671539540",
    "Immersion Cigs": "753946944",
    "IFA3_AIO_LITE": "660460283",
    "Secret Weapons": "756352410",
    "Sab Secret Weapons - ACE3 Compatibility": "1436492232",
    "GRAD Trenches": "1224892496",
    "7Y Assets WW2": "1202636528",
    "GEIST-A3 LITE": "773314286",
    "Faces of war": "891433622",
    "Iron Front Faces of War Compatibility": "828493030",
    "Iron Front ACE 3 Compatibility": "773759919",
    "ifa3 highter quality": "2000476173",
    "MBG Buildings 3" : "962932583",
    "Rosche Germany" : "1527410521",
    "DEGA Parachutes" : "929073462",
    "Staszow" : "1421161768",
    "immerse": "825172265",
    "suppress" : "825174634",
    "align": "903134884",
    "VCOM": "721359761",
    "LAMBS Danger": "1858075458",
    "Radio Animations": "1480333388",
    "pandur ii apc": "864124640",
    "Project SFX": "2129532219"

}


def log_head(msg):
    logging.info("")
    logging.info("{{0:=<{}}}".format(len(msg)).format(""))
    logging.info(msg)
    logging.info("{{0:=<{}}}".format(len(msg)).format(""))

def log(msg):
    logging.info(msg)

def call_steamcmd(user, steam_cmd, params):
    '''
    Ejecutará el comando en steamcmd con un usuario determinado

    :user Nombre del usuario de la instancia
    :param steam_cmd La ruta del steamcmd de la instancia a actualizar
    :param params Estos parámetros se pasarán a la consola de Steam
    '''
    command = "su - {} -c \"{} {}\"".format(user, steam_cmd, params)
    # log(command)
    result = os.system(command)
    logging.info("")

    if result != 0:
        logging.error("Error when the steamcmd was executed {} Retry again".format(result))
        return result

    return result

# Create symlink
def create_mod_symlinks(a3_server_dir):
    '''
    Crea enlaces simbólicos en la ruta indicada por parámetro

    :a3_server_dir Ruta donde creará los enlaces simbólicos
    '''
    mod_list=""
    for mod_name, mod_id in MODS.items():
        mod_name=cleanModName(mod_name)
        link_path="{}/{}{}".format(a3_server_dir, PATTERN_MOD, mod_name)
        real_path="{}/{}".format(A3_WORKSHOP_DIR, mod_id)

        # mod_list info all mods to script sh
        mod_list += PATTERN_MOD + mod_name + "\;"

        if os.path.isdir(real_path):
            if not os.path.islink(link_path):
                os.symlink(real_path, link_path)
                logging.info("Creating symlink '{}'...".format(link_path))
        else:
            log("Mod '{}' does not exist! ({})".format(mod_name, real_path))

    return mod_list


# Update server
def update_server(user, steamcmd_path, a3_server_dir):
    '''
    Actualizará el mod según el id que llega por parámetro

    :user Nombre del usuario de la instancia
    :param steam_cmd La ruta del steamcmd de la instancia a actualizar
    :param a3_server_dir Ruta de la instancia de arma para construir los parámetros
    '''
    steam_cmd_params = " +login {} {}".format(STEAM_USER, STEAM_PASS)
    steam_cmd_params += " +force_install_dir {}".format(a3_server_dir)
    steam_cmd_params += " +app_update {} validate".format(A3_SERVER_ID)
    steam_cmd_params += " +quit"

    call_steamcmd(user, steamcmd_path, steam_cmd_params)


def mod_needs_update(mod_id, path):
    '''
    Comprueba si el mod necesita ser actualizado

    :mod_id ID del mod a comprobar
    :path Ruta del mod en el sistema
    '''
    if os.path.isdir(path):
        response = request.urlopen(
            "{}/{}".format(WORKSHOP_CHANGELOG_URL, mod_id)).read()
        response = response.decode("utf-8")
        match = PATTERN.search(response)

        if match:
            updated_at = datetime.fromtimestamp(int(match.group(1)))
            created_at = datetime.fromtimestamp(os.path.getctime(path))

            return (updated_at >= created_at)

    return False


def update_mods():
    '''
    Este método solo será llamado una vez, tiene que haber una instancia maestra para la actualización de mods
    En nuestro caso el usuario maestro es "arma3hc"

    '''

    for mod_name, mod_id in MODS.items():
        path = "{}/{}".format(A3_WORKSHOP_DIR, mod_id)

        # Check if mod needs to be updated
        if os.path.isdir(path):

            if mod_needs_update(mod_id, path):
                # Delete existing folder so that we can verify whether the
                # download succeeded
                log("Update required for \"{}\" ({})... TO DOWNLOAD".format(mod_name, mod_id))
                shutil.rmtree(path)
            else:
                log("No update required for \"{}\" ({})... SKIPPING".format(mod_name, mod_id))
                continue

        else:
            log("New mod detected: \"{}\" ({})... TO DOWNLOAD".format(mod_name, mod_id))

        update_mod(mod_id)

    log("[update_mods] FINISHED UPDATE MODS")


def update_mod(id):
    '''
    Este método solo actualiza un mod por UID

    '''
    log("Updating mod \"{}\"...".format(id))
    
     # Building command to steam
    steam_cmd_params = " +login {} {} ".format(STEAM_USER, STEAM_PASS)
    steam_cmd_params += " +force_install_dir {}".format(A3_SERVER_DIR_MASTER) 
    steam_cmd_params += " +workshop_download_item {} {} validate ".format(
        A3_WORKSHOP_ID,
        id
    )
    steam_cmd_params += " +quit"

    for i in range(3):
        if call_steamcmd(A3_SERVER_MASTER, STEAM_CMD_MASTER, steam_cmd_params) == 0:
            log("[update_mods] Mod {} downloaded successfully".format(id))
            break
        else:
            log("[update_mods] Retry download again mod {}".format(id))

    log("[update_mods] Mod {} updated".format(id))


# No se está usando este método, se ha comprobar y las instancias funcionan sin cambiar permisos
def update_permissions_mods():
    os.system("chmod -R 2777 {}/{}* ".format(A3_WORKSHOP_DIR, PATTERN_MOD))

# Actualiza los permisos de root al usuario del servidor a todos los enlaces simbolicos de mods creados
def update_permissions_links(user, a3_server_dir):
    '''
    Actualizará los permisos de los enlaces simbólicos creados en una ruta determinada

    :param user Usuario propetario del enlace
    :param a3_server_dir Directorio de la instancia
    '''
    # For user specific
    os.system("chown -R {} {}/{}* ".format(user, a3_server_dir, PATTERN_MOD))
    # For user group
    os.system("chgrp -R {} {}/{}* ".format(A3_GROUP_USER, a3_server_dir, PATTERN_MOD))
    # For permissions files
    os.system("chmod -R 2777 {}/{}* ".format(a3_server_dir, PATTERN_MOD))


def lowercase_workshop_dir():
    '''
    Convierte a minúsculas las carpetas y ficheros de todos los mods
    '''
    # os.system("(cd {} && find . -depth -exec rename -v 's/(.*)\/([^\/]*)/$1\/\L$2/' {{}} \;)".format(A3_WORKSHOP_DIR))
    # os.system("su - {} -c \"(cd {} && find . -depth -exec rename -v 's/(.*)\/([^\/]*)/$1\/\L$2/' {{}} \;)\"".format(
    #    A3_SERVER_MASTER, A3_WORKSHOP_DIR))
    os.system("su - {} -c \"cd {} && /usr/bin/python3 ./rename.py .\"".format(A3_SERVER_MASTER, A3_WORKSHOP_DIR))


def cleanModName(modName):
    '''
    Limpia los nombres de los mods para el enlace simbólico(& se excluye y espacio se cambia por _)
    '''
    modName = modName.replace(TO_EXCLUDE, "")
    modName = modName.replace(" ", "_")
    modName = modName.lower()
    return modName


#############################
#      FLUJO DEL SCRIPT     #
#############################

# Actualizar el server maestro
if argument != "":
    if argument == "1" or argument == "2":
        log_head("Updating MASTER A3 server ({})".format(A3_SERVER_ID))
        update_server(A3_SERVER_MASTER, STEAM_CMD_MASTER, A3_SERVER_DIR_MASTER)

    # Iterar las instancias de arma y actualizarlas. Actualmente solo tenemos un esclavo/maestro
    #if argument == "1" or argument == "2":
    #    i=0
    #    for a3_instance, a3_server_dir in A3_SERVER_DIR_SLAVES.items():
    #        log_head("Updating SLAVE {} A3 server ({})".format(i, a3_instance))
    #        update_server(a3_instance, STEAM_CMD_SLAVES[i], a3_server_dir)
    #        i += 1

    if argument == "2":
        sys.exit(0)

    # Actualiza los mods, solo se realiza en master, los esclavos usan esta ruta
    mod_list = ""
    if argument == "1" or argument == "3":
        log_head("Updating mods to MASTER")
        update_mods()
        log("")

        # Una sola llamada para convertir a minusculas
        log_head("Converting uppercase files/folders to lowercase...")
        lowercase_workshop_dir()
        log("End lowercase function")

        # Enlaces simbólicos para el MASTER
        log_head("Symlink to MASTER {}".format(A3_SERVER_DIR_MASTER))
        mod_list = create_mod_symlinks(A3_SERVER_DIR_MASTER)

        # Update permissions symbolic
        log("Updating permissions of symlinks created for \"{}\"".format(A3_SERVER_DIR_MASTER))
        update_permissions_links(A3_SERVER_MASTER, A3_SERVER_DIR_MASTER)
        log("Symblinks created")


        # Enlaces simbólicos para los ESCLAVOS. Actualmente solo usamos un esclavo/maestro
        #for a3_instance, a3_server_dir in A3_SERVER_DIR_SLAVES.items():
        #    log_head("SYMLINK FOR " + a3_instance.upper())
        #    create_mod_symlinks(a3_server_dir)
        #    log("Updating permissions of symlinks created for \"{}\"".format(a3_instance))
        #    update_permissions_links(a3_instance, a3_server_dir)
        #    log("")

        sys.exit(0)

    if argument != "1" or argument != "2" or argument !="3":
        update_mod(argument)
        log_head("Converting uppercase files/folders to lowercase...")
        lowercase_workshop_dir()
        log("End lowercase function")
        log_head("Symlink to MASTER {}".format(A3_SERVER_DIR_MASTER))
        mod_list = create_mod_symlinks(A3_SERVER_DIR_MASTER)
        log("Updating permissions of symlinks created for \"{}\"".format(A3_SERVER_DIR_MASTER))
        update_permissions_links(A3_SERVER_MASTER, A3_SERVER_DIR_MASTER)
        log("Symblinks created")
        
        sys.exit(0)

    log("")
    log_head("Copy this line for load mods : {}".format(mod_list))

    log("")
    log(" by Wolf Team ")

sys.exit(0)

