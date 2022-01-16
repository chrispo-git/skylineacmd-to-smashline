import os
import tkinter as tk
from tkinter import filedialog

print(" Make sure to check your dependencies!")
root = tk.Tk()
root.withdraw()

#uncomment this
input_file = filedialog.askopenfilename()

#comment this
#input_file = "acmd.rs"
i = []
o = []

def inputter():
  global i
  with open(input_file) as f:
    i = f.readlines()
  f.close()

def acmd2smashline():
  global i
  global o
  script_type = 0
  is_acmd_script = False
  is_acmd_use = False
  for f in i:
    w_f = f
    acmd_func = '#[acmd_func('
    bocf = 'BATTLE_OBJECT_CATEGORY_FIGHTER'
    bocw = 'BATTLE_OBJECT_CATEGORY_WEAPON'
    fighter_kind = '    battle_object_kind = '
    fightermut = ': &mut L2CFighterCommon'
    weaponmut = ': &mut L2CFighterBase'
    anim = '    animation ='
    animcmd = '    animcmd ='
    acmd = '    acmd!({'
    acmdadd = 'acmd::add_hooks!'
    hookadd = 'acmd::add_custom_hooks!'
    use = 'use'
    acmd_use = 'acmd'
    lua2cpp = 'use smash::lua2cpp::'
    lua2cpp_use = 'use smash::lua2cpp::*;\n'
    dependencies = '''use smashline::*;
use smash_script::*;'''
    
    if script_type != 0:
      if script_type == 1:
        o.append("    category = ACMD_GAME)]\n")
      elif script_type == 2:
        o.append("    category = ACMD_EFFECT)]\n")
      elif script_type == 3:
        o.append("    category = ACMD_SOUND)]\n")
      elif script_type == 4:
        o.append("    category = ACMD_EXPRESSION)]\n")
      script_type = 0
    
    if acmd_func in w_f:
      o.append("#[acmd_script(\n")
      is_acmd_script = True
    elif fightermut in w_f :
      if is_acmd_script == True:
        is_acmd_script = False
        beginning = "pub fn "
        end = "(fighter: &mut L2CFighterCommon) {"
        isolate = w_f[len(beginning):((len(end)*-1))-1]
        isolate = isolate.lower()
        w_f = "unsafe fn " + str(isolate) + "(fighter: &mut L2CAgentBase) {" + "\n"
        o.append(w_f)
      else:
        o.append("#[fighter_frame_callback]\n" + w_f)
    elif weaponmut in w_f :
      if is_acmd_script == True:
        is_acmd_script = False
        beginning = "pub fn "
        end = "(fighter: &mut L2CFighterBase) {"
        isolate = w_f[len(beginning):((len(end)*-1))-1]
        isolate = isolate.lower()
        w_f = "unsafe fn " + str(isolate) + "(fighter: &mut L2CAgentBase) {" + "\n"
        o.append(w_f)
      else:
        o.append("#[weapon_frame_callback]\n" + w_f)
    elif acmdadd in w_f:
        isolate = w_f
        isolate = isolate.replace("acmd::add_hooks!", "smashline::install_acmd_scripts!")
        o.append(isolate)
    elif hookadd in w_f:
        isolate = w_f
        isolate = isolate.replace("acmd::add_custom_hooks!", "smashline::install_agent_frame_callbacks!")
        o.append(isolate)
    elif "acmd::add_custom_weapon_hooks!" in w_f:
        isolate = w_f
        isolate = isolate.replace("acmd::add_custom_weapon_hooks!", "smashline::install_agent_frame_callbacks!")
        o.append(isolate)
    elif acmd in w_f:
      o.append("    let lua_state = fighter.lua_state_agent;\n    acmd!(lua_state, {\n")
    elif use in w_f and acmd_use in w_f:
      if is_acmd_use == False:
        o.append(dependencies)
        is_acmd_use = True
    elif lua2cpp in w_f:
      o.append(lua2cpp_use)
    elif bocf in w_f:
      o.append("")
    elif bocw in w_f:
      o.append("")
    elif anim in w_f:
      o.append("")
    elif fighter_kind in w_f and "FIGHTER_KIND_" in w_f:
      beginning = fighter_kind + "FIGHTER_KIND_"
      end = "aa"
      isolate = w_f[len(beginning):((len(end)*-1))-1]
      isolate = isolate.lower()
      w_f = '    agent = "' + str(isolate) + '",\n'
      o.append(w_f)
    elif fighter_kind in w_f:
      beginning = fighter_kind + "WEAPON_KIND_"
      end = "aa"
      isolate = w_f[len(beginning):((len(end)*-1))-1]
      isolate = isolate.lower()
      w_f = '    agent = "' + str(isolate) + '",\n'
      o.append(w_f)
    elif animcmd in w_f:
      beginning = animcmd
      end = "aa"
      isolate = w_f[len(beginning):((len(end)*-1))-1]
      isolate = isolate.lower()
      w_f = '    script = ' + str(isolate) + ',\n'
      o.append(w_f)
      if "effect" in w_f:
        script_type = 2
      elif "sound" in w_f:
        script_type = 3
      elif "expression" in w_f:
        script_type = 4
      else:
        script_type = 1
    else:
      o.append(w_f)

inputter()
acmd2smashline()


if os.path.exists("mod.rs"):
  os.remove("mod.rs")
with open('mod.rs', 'a') as f:
  for x in o:
    f.write(x)
f.close()

print("Done!")
