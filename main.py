import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from gui.gui import Ui_MainWindow

from rom import *

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

new_filename = None
write_finish = False


def increase_step():
    if ui.actionOpen.isEnabled():
        timer.stop()
        if ui.randomize.isEnabled():
            ui.progressBar.setValue(100)
            ctypes.windll.user32.MessageBoxW(0, "Success: file opened!", "Info", 0x40)
        ui.progressBar.setValue(0)
    elif ui.progressBar.value() < 90:
        if os.path.exists("rom/data/"):
            if os.path.exists("rom/data/SCRIPT/"):
                if os.path.exists("rom/data/SCRIPT/D30P21A/"):
                    if os.path.exists("rom/data/SCRIPT/D70P41A/"):
                        if os.path.exists("rom/data/SCRIPT/S00P01A/"):
                            ui.progressBar.setValue(90)
                        else:
                            ui.progressBar.setValue(70)
                    else:
                        ui.progressBar.setValue(50)
                else:
                    ui.progressBar.setValue(30)
            else:
                ui.progressBar.setValue(10)


def finish():
    global write_finish
    if write_finish:
        write_finish = False
        ui.progressBar.setValue(50)
        save_all_files()
        save_rom(new_filename, [ui.randomize, ui.actionOpen])
    if ui.actionOpen.isEnabled():
        timer2.stop()
        ui.progressBar.setValue(100)
        ctypes.windll.user32.MessageBoxW(0, "Randomization complete!", "Complete", 0x40)
        ui.progressBar.setValue(0)


def open_file():
    open_rom(choose_open_file(), [ui.randomize, ui.actionOpen])
    if not ui.actionOpen.isEnabled():
        ui.progressBar.setValue(0)
        timer.start(1000)


def choose_open_file():
    return QFileDialog.getOpenFileName(None, "Choose a ROM", "", "NDS Files (*.nds)")


def about():
    ctypes.windll.user32.MessageBoxW(0, "Developers:\n     -Tenma\n\n"
                                        "Credits:\n     -Aissurteivos\n     -Psy_commando\n     "
                                        "-OgreGunner\n     -Nhahtdh",
                                        "About", 0x40)


def create_file():
    global new_filename
    new_filename = choose_save_file()
    if new_filename[0]:
        ui.progressBar.setValue(0)
        ui.randomize.setEnabled(False)
        ui.actionOpen.setEnabled(False)

        thread = threading.Thread(target=write_data)
        thread.start()

        timer2.start(1000)


def write_data():
    if ui.pokemon_spawns.isChecked():
        rand_pokemon(ui.legendary.isChecked())
    if ui.music.isChecked():
        rand_music()
    if ui.weather.isChecked():
        rand_weather()
    if ui.darkness.isChecked():
        rand_darkness()
    if ui.enemy_iq.isChecked():
        rand_enemyiq()
    if ui.water.isChecked():
        rand_water()
    if ui.floor_structure.isChecked():
        rand_floor()
    if ui.hallway_length.isChecked():
        rand_hallway_length()
    if ui.trap_spawns.isChecked():
        rand_traps()
    if ui.item_spawns.isChecked():
        rand_items()

    if ui.setPokemon.isChecked():
        set_pokemon_density(ui.spinBoxPokemonDensity.value())
    elif ui.pokemon_density.isChecked():
        rand_pokemon_density()
    if ui.setItem.isChecked():
        set_item_density(ui.spinBoxItemDensity.value())
    elif ui.item_density.isChecked():
        rand_item_density()
    if ui.setTrap.isChecked():
        set_trap_density(ui.spinBoxTrapDensity.value())
    elif ui.trap_density.isChecked():
        rand_trap_density()
    if ui.setRoom.isChecked():
        set_room_density(ui.spinBoxRoomDensity.value())
    elif ui.room_density.isChecked():
        rand_room_density()
    if ui.setHallway.isChecked():
        set_hallway_density(ui.spinBoxHallwayDensity.value())
    elif ui.hallway_density.isChecked():
        rand_hallway_density()
    if ui.setWater.isChecked():
        set_water_density(ui.spinBoxWaterDensity.value())
    elif ui.water_density.isChecked():
        rand_water_density()

    if ui.kecleon_percentage.isChecked():
        set_kecleon_shop_percentage(ui.spinBoxKecleonShop.value())
    if ui.monster_house.isChecked():
        set_monster_house_percentage(ui.spinBoxMonsterHouse.value())
    if ui.water_percentage.isChecked():
        set_water_room_percentage(ui.spinBoxWaterRoom.value())
    if ui.hidden_stairs.isChecked():
        set_hidden_stairs_percentage(ui.spinBoxHiddenStairs.value())

    if ui.terrain_appearance.isChecked():
        rand_terrain()

    if ui.type.isChecked():
        rand_types(ui.spinBoxTypes.value())
    if ui.abilities.isChecked():
        rand_abilities(ui.spinBoxAbilities.value())
    if ui.iq_group.isChecked():
        rand_iqgroups()
    if ui.mobility.isChecked():
        rand_mobility()
    if ui.moveset.isChecked():
        rand_moveset()

    if ui.player_starters.isChecked():
        rand_player()
    if ui.partner_starters.isChecked():
        rand_partner()

    if ui.portraits.isChecked():
        fix_portraits()
    if ui.body_size.isChecked():
        set_body_size()
    if ui.recruit_rate.isChecked():
        set_recruit_rate(ui.spinBoxRecruit.value())

    global write_finish
    write_finish = True


def choose_save_file():
    return QFileDialog.getSaveFileName(None, "Choose a Destination", "", "NDS Files (*.nds)")


ui.actionOpen.triggered.connect(open_file)
ui.actionAbout.triggered.connect(about)

ui.randomize.clicked.connect(create_file)

timer = QTimer()
timer.timeout.connect(increase_step)

timer2 = QTimer()
timer2.timeout.connect(finish)

window.show()
sys.exit(app.exec_())