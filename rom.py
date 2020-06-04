import ctypes
import mmap
import os
import shutil
import subprocess
import threading

from itemspawn import *

dungeonMemory = []
pokemonMemory = []
moveMemory = []
overlay13Memory = []

sTextMemory = []
eTextMemory = []
iTextMemory = []
gTextMemory = []
fTextMemory = []
textMemory = [sTextMemory, eTextMemory, iTextMemory, gTextMemory, fTextMemory]

portraitMemory = []

pmd_version = ""


def bytes2int(b):
    return int.from_bytes(b, "little")


def int2bytes(i, n):
    return i.to_bytes(n, 'little')


def signedint2bytes(i, n):
    return i.to_bytes(n, 'little', signed=True)


def pmd_sky_eu(memory):
    global pmd_version
    code = b'POKEDUN SORAC2SP'
    for index in range(0, 16):
        if memory[index] != int2bytes(code[index], 1):
            return False
    pmd_version = "eu"
    return True


def pmd_sky_us(memory):
    global pmd_version
    code = b'POKEDUN SORAC2SE'
    for index in range(0, 16):
        if memory[index] != int2bytes(code[index], 1):
            return False
    pmd_version = "us"
    return True


def unpack(my_args, ui):
    subprocess.Popen(my_args, creationflags=subprocess.CREATE_NO_WINDOW).wait()  # Ejecutamos ndstool

    memory = []
    ret = True

    if not load_file("rom/header.bin", memory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open header.bin", "Fail!", 0x10)
        ret = False

    if not pmd_sky_eu(memory) and not pmd_sky_us(memory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: ROM must be Pokemon Mystery Dungeon - Explorers of Sky (US or EU)",
                                         "Fail!", 0x10)
        ret = False

    if ret:
        load_all_files()

    ui[0].setEnabled(ret)  # randomize
    ui[1].setEnabled(True)  # actionOpen


def pack(my_args, ui):
    subprocess.Popen(my_args, creationflags=subprocess.CREATE_NO_WINDOW).wait()  # Ejecutamos ndstool

    if os.path.exists("rom"):
        shutil.rmtree("rom", ignore_errors=True)

    ui[1].setEnabled(True)  # actionOpen


def open_rom(filename, ui):
    if filename[0]:

        ui[0].setEnabled(False)  # randomize
        ui[1].setEnabled(False)  # actionOpen

        if os.path.exists("rom"):
            shutil.rmtree("rom", ignore_errors=True)

        os.mkdir("rom")  # Creamos carpeta rom para poner los ficheros generados por el ndstool

        my_args = [
            "ndstool.exe",
            "-x",
            filename[0],
            "-9",
            "rom/arm9.bin",
            "-7",
            "rom/arm7.bin",
            "-y9",
            "rom/y9.bin",
            "-y7",
            "rom/y7.bin",
            "-d",
            "rom/data",
            "-y",
            "rom/overlay",
            "-t",
            "rom/banner.bin",
            "-h",
            "rom/header.bin"
        ]

        thread = threading.Thread(target=unpack, args=(my_args, ui))
        thread.start()


def save_rom(filename, ui):
    if filename[0]:

        my_args = [
            "ndstool.exe",
            "-c",
            filename[0],
            "-9",
            "rom/arm9.bin",
            "-7",
            "rom/arm7.bin",
            "-y9",
            "rom/y9.bin",
            "-y7",
            "rom/y7.bin",
            "-d",
            "rom/data",
            "-y",
            "rom/overlay",
            "-t",
            "rom/banner.bin",
            "-h",
            "rom/header.bin"
        ]

        thread = threading.Thread(target=pack, args=(my_args, ui))
        thread.start()


def load_file(filename, memory):
    if filename:
        with open(filename, 'r') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                memory.clear()
                for index in range(0, m.size()):
                    memory.append(m.read(1))
                m.close()
                return True
    return False


def save_file(filename, memory):
    if filename:
        with open(filename, 'r+') as f:
            with mmap.mmap(f.fileno(), 0) as m:
                m.seek(0)
                for byte in memory:
                    m.write(byte)
                m.close()
                return True
    return False


def load_all_files():
    global pmd_version

    if not load_file("rom/data/BALANCE/mappa_s.bin", dungeonMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open mappa_s.bin", "Fail!", 0x10)

    if not load_file("rom/data/BALANCE/monster.md", pokemonMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open monster.md", "Fail!", 0x10)

    if not load_file("rom/data/BALANCE/waza_p.bin", moveMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open waza_p.bin", "Fail!", 0x10)

    if not load_file("rom/overlay/overlay_0013.bin", overlay13Memory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open overlay_0013.bin", "Fail!", 0x10)

    if not load_file("rom/data/FONT/kaomado.kao", portraitMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open kaomado.kao", "Fail!", 0x10)

    if not load_file("rom/data/MESSAGE/text_e.str", eTextMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_e.str", "Fail!", 0x10)

    if pmd_version == "eu":

        if not load_file("rom/data/MESSAGE/text_s.str", sTextMemory):
            ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_s.str", "Fail!", 0x10)

        if not load_file("rom/data/MESSAGE/text_i.str", iTextMemory):
            ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_i.str", "Fail!", 0x10)

        if not load_file("rom/data/MESSAGE/text_g.str", gTextMemory):
            ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_g.str", "Fail!", 0x10)

        if not load_file("rom/data/MESSAGE/text_f.str", fTextMemory):
            ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_f.str", "Fail!", 0x10)


def save_all_files():
    global pmd_version

    save_file("rom/data/BALANCE/mappa_s.bin", dungeonMemory)
    save_file("rom/data/BALANCE/monster.md", pokemonMemory)
    save_file("rom/data/BALANCE/waza_p.bin", moveMemory)
    save_file("rom/overlay/overlay_0013.bin", overlay13Memory)
    save_file("rom/data/FONT/kaomado.kao", portraitMemory)
    save_file("rom/data/MESSAGE/text_e.str", eTextMemory)

    if pmd_version == "eu":
        save_file("rom/data/MESSAGE/text_s.str", sTextMemory)
        save_file("rom/data/MESSAGE/text_i.str", iTextMemory)
        save_file("rom/data/MESSAGE/text_g.str", gTextMemory)
        save_file("rom/data/MESSAGE/text_f.str", fTextMemory)


def rand_pokemon(legendary):
    maxPokemonId = 0x219

    excludedPokemon = [
        0x0000,  # No pokemon/end of list
        0x0019,  # Pikachu
        0x0025,  # Vulpix
        0x0090,  # Articuno
        0x0091,  # Zapdos
        0x0092,  # Moltres
        0x0096,  # Mewtwo
        0x0097,  # Mew
        0x00AC,  # Pichu
        0x00C9,  # Unown A
        0x00CA,  # Unown B
        0x00CB,  # Unown C
        0x00CC,  # Unown D
        0x00CD,  # Unown E
        0x00CE,  # Unown F
        0x00CF,  # Unown G
        0x00D0,  # Unown H
        0x00D1,  # Unown I
        0x00D2,  # Unown J
        0x00D3,  # Unown K
        0x00D4,  # Unown L
        0x00D5,  # Unown M
        0x00D6,  # Unown N
        0x00D7,  # Unown O
        0x00D8,  # Unown P
        0x00D9,  # Unown Q
        0x00DA,  # Unown R
        0x00DB,  # Unown S
        0x00DC,  # Unown T
        0x00DD,  # Unown U
        0x00DE,  # Unown V
        0x00DF,  # Unown W
        0x00E0,  # Unown X
        0x00E1,  # Unown Y
        0x00E2,  # Unown Z
        0x00E3,  # Unown !
        0x00E4,  # Unown ?
        0x0102,  # Phanpy
        0x0103,  # Donphan
        0x010E,  # Raikou
        0x010F,  # Entei
        0x0110,  # Suicune
        0x0114,  # Lugia
        0x0115,  # Ho-oh
        0x0116,  # Celebi
        0x0117,  # Celebi(shiny)
        0x017B,  # Castform(form a)
        0x017C,  # Castform(form b)
        0x017D,  # Castform(form c)
        0x017E,  # Castform(form d)
        0x017F,  # Kecleon
        0x0180,  # Kecleon(shiny)
        0x0199,  # Regirock
        0x019A,  # Regice
        0x019B,  # Registeel
        0x019C,  # Latias
        0x019D,  # Latios
        0x019E,  # Kyogre
        0x019F,  # Groudon
        0x01A0,  # Rayquaza
        0x01A1,  # Jirachi
        0x01A2,  # Deoxys(form a)
        0x01A3,  # Deoxys(form b)
        0x01A4,  # Deoxys(form c)
        0x01A5,  # Deoxys(form d)
        0x01B7,  # Shinx
        0x01B8,  # Luxio
        0x01B9,  # Luxray
        0x01E9,  # Riolu
        0x0207,  # Dusknoir
        0x0208,  # Froslass
        0x020A,  # Uxie
        0x020B,  # Mesprit
        0x020C,  # Azelf
        0x020D,  # Dialga
        0x020E,  # Palkia
        0x020F,  # Heatran
        0x0210,  # Regigigas
        0x0211,  # Giratina
        0x0212,  # Cresselia
        0x0213,  # Phione
        0x0214,  # Manaphy
        0x0215,  # Darkrai
        0x0216,  # Shaymin
        0x0217,  # Shaymin Sky
        0x0218,  # Giratina O
        0x0229   # Decoy
    ]

    if legendary:
        excludedPokemon = fix_legendary()

    choosables = []

    for index in range(0, maxPokemonId):
        if index not in excludedPokemon:
            choosables.append(index)

    for index in range(0, 14229):
        entry = 0x000177D0 + index * 8
        value = bytes2int(dungeonMemory[entry + 6] + dungeonMemory[entry + 7])
        if value not in excludedPokemon:
            rand = int2bytes(random.choice(choosables), 2)
            dungeonMemory[entry + 6] = int2bytes(rand[0], 1)
            dungeonMemory[entry + 7] = int2bytes(rand[1], 1)


def rand_terrain():
    maxTerrainId = 0x91

    excludedTerrains = [
        0x0D,  # Invalid
        0x15,  # Invalid
        0x29,  # Invalid
        0x2F,  # Invalid
        0x3C,  # Invalid
        0x46,  # Invalid
        0x47,  # Invalid
        0x48,  # Invalid
        0x49,  # Invalid
        0x4D,  # Invalid
        0x56,  # Invalid
        0x59,  # Invalid
        0x5C,  # Invalid
        0x5D,  # Invalid
        0x5F,  # Invalid
        0x59,  # Invalid
        0x62,  # Invalid
        0x64,  # Invalid
        0x6B,  # Invalid
        0x78,  # Invalid
        0x79,  # Invalid
        0x90   # Invalid
    ]

    choosables = []
    terrains = []

    for index in range(0, maxTerrainId):
        if index not in excludedTerrains:
            choosables.append(index)

    for index in range(0, 250):
        terrains.append(int2bytes(random.choice(choosables), 1))

    count = 0
    last = 0

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32

        current = bytes2int(dungeonMemory[entry + 2])

        if last != current:
            count += 1

        last = current
        dungeonMemory[entry + 2] = terrains[count]


def rand_music():
    maxMusicId = 0x81

    excludedMusic = [
        0x00,  # No music
        0x36,  # No music
        0x76,  # No music
        0x77,  # No music
        0x78,  # No music
        0x79,  # No music
        0x7A,  # No music
        0x7B,  # No music
        0x7C,  # No music
        0x7D,  # No music
        0x7E,  # No music
        0x7F   # No music
    ]

    choosables = []
    music = []

    for index in range(0, maxMusicId):
        if index not in excludedMusic:
            choosables.append(index)

    for index in range(0, 250):
        music.append(int2bytes(random.choice(choosables), 1))

    count = 0
    last = 0

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32

        current = bytes2int(dungeonMemory[entry + 2])  # terrain

        if last != current:
            count += 1

        last = current
        dungeonMemory[entry + 3] = music[count]


def rand_weather():
    maxWeatherId = 0x8

    choosables = []
    weather = []

    for index in range(0, maxWeatherId):
        choosables.append(index)

    for index in range(250):
        weather.append(int2bytes(random.choice(choosables), 1))

    count = 0
    last = 0

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32

        current = bytes2int(dungeonMemory[entry + 2])  # terrain

        if last != current:
            count += 1

        last = current
        dungeonMemory[entry + 4] = weather[count]


def rand_darkness():
    maxDarknessId = 0x3

    choosables = []
    darkness = []

    for index in range(0, maxDarknessId):
        choosables.append(index)

    for index in range(250):
        darkness.append(int2bytes(random.choice(choosables), 1))

    count = 0
    last = 0

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32

        current = bytes2int(dungeonMemory[entry + 2])  # terrain

        if last != current:
            count += 1

        last = current
        dungeonMemory[entry + 22] = darkness[count]


def rand_enemyiq():
    maxEnemyiqId = 1000

    choosables = []
    enemyiq = []

    for index in range(0, maxEnemyiqId):
        choosables.append(index)

    for index in range(250):
        enemyiq.append(int2bytes(random.choice(choosables), 2))

    count = 0
    last = 0

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32

        current = bytes2int(dungeonMemory[entry + 2])  # terrain

        if last != current:
            count += 1

        last = current
        dungeonMemory[entry + 28] = int2bytes(enemyiq[count][0], 1)
        dungeonMemory[entry + 29] = int2bytes(enemyiq[count][1], 1)


def rand_kecleon_shop_percentage():
    choosables = []

    for index in range(0, 51):
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 7] = int2bytes(random.choice(choosables), 1)


def set_kecleon_shop_percentage(percent):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 7] = int2bytes(percent, 1)


def rand_monster_house_percentage():
    choosables = []

    for index in range(0, 26):
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 8] = int2bytes(random.choice(choosables), 1)


def set_monster_house_percentage(percent):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 8] = int2bytes(percent, 1)


def rand_water_room_percentage():
    choosables = []

    for index in range(0, 26):
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 12] = int2bytes(random.choice(choosables), 1)


def set_water_room_percentage(percent):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 12] = int2bytes(percent, 1)


def rand_hidden_stairs_percentage():
    choosables = []

    for index in range(0, 51):
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 27] = int2bytes(random.choice(choosables), 1)


def set_hidden_stairs_percentage(percent):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 27] = int2bytes(percent, 1)


def rand_water():
    maxWaterId = 0x2

    choosables = []
    water = []

    for index in range(0, maxWaterId):
        choosables.append(index)

    for index in range(250):
        water.append(int2bytes(random.choice(choosables), 1))

    count = 0
    last = 0

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32

        current = bytes2int(dungeonMemory[entry + 2])  # terrain

        if last != current:
            count += 1

        last = current
        dungeonMemory[entry + 13] = water[count]


def rand_floor():
    maxFloorId = 12

    excludedFloor = [
        0x02,  # One room monster house
        0x05   # Two room monster house
    ]

    choosables = []

    for index in range(0, maxFloorId):
        if index not in excludedFloor:
            choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry] = int2bytes(random.choice(choosables), 1)


def rand_hallway_length():
    choosables = []

    for index in range(6, 51):
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 5] = int2bytes(random.choice(choosables), 1)


def rand_room_density():
    choosables = []

    for index in range(4, 21):
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 1] = int2bytes(random.choice(choosables), 1)


def set_room_density(value):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 1] = int2bytes(value, 1)


def rand_hallway_density():
    choosables = []

    for index in range(0, 41):
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 19] = int2bytes(random.choice(choosables), 1)


def set_hallway_density(value):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 19] = int2bytes(value, 1)


def rand_water_density():
    choosables = []

    for index in range(0, 41):
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 21] = int2bytes(random.choice(choosables), 1)


def set_water_density(value):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 21] = int2bytes(value, 1)


def rand_pokemon_density():
    choosables = []

    for index in range(3, 21):  # (3, 14)
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 6] = int2bytes(random.choice(choosables), 1)


def set_pokemon_density(value):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 6] = int2bytes(value, 1)


def rand_item_density():
    choosables = []

    for index in range(1, 21):  # (1, 8)
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 15] = int2bytes(random.choice(choosables), 1)


def set_item_density(value):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 15] = int2bytes(value, 1)


def rand_traps():
    maxTrapsId = 25

    choosables = []

    for index in range(1, maxTrapsId):
        choosables.append(index)

    for index in range(0, 106):
        entry = 0x000343CC + index * 50

        traps = []

        for it in range(len(choosables)):
            dungeonMemory[entry + ((it + 1) * 2)] = int2bytes(0, 1)
            dungeonMemory[entry + ((it + 1) * 2) + 1] = int2bytes(0, 1)
            if random.randint(1, 100) <= 25:  # 25% all traps
                traps.append(choosables[it])

        percentage = 0

        for it in range(0, len(traps)):

            if it == (len(traps) - 1):
                percentage = 10000
            else:
                percentage += 10000//len(traps)

            dungeonMemory[entry + traps[it] * 2] = int2bytes(int2bytes(percentage, 2)[0], 1)
            dungeonMemory[entry + (traps[it] * 2) + 1] = int2bytes(int2bytes(percentage, 2)[1], 1)


def rand_trap_density():
    choosables = []

    for index in range(1, 21):  # (3, 15)
        choosables.append(index)

    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 16] = int2bytes(random.choice(choosables), 1)


def set_trap_density(value):
    for index in range(0, 1873):
        entry = 0x00008DB0 + index * 32
        dungeonMemory[entry + 16] = int2bytes(value, 1)


def pokemon_name(value, language):
    entry = 0x00008880 + value * 4
    pointer = bytes2int(textMemory[language][entry] + textMemory[language][entry + 1] +
                        textMemory[language][entry + 2] + textMemory[language][entry + 3])

    pokemon_name = b''
    count = 0
    finish = False
    while not finish:
        byte = textMemory[language][pointer + count]
        if byte == int2bytes(0, 1):
            finish = True
        else:
            pokemon_name += byte
        count += 1

    return pokemon_name


def pokemon_message(value, k):
    global pmd_version
    entry = 0x000019F0 + k * 4

    sPersonalityMessage = '¡[CS:K]'.encode('ansi') + pokemon_name(value, 0) + '[CR]!'.encode('ansi')
    ePersonalityMessage = 'Will be a [CS:K]'.encode('ansi') + pokemon_name(value, 1) + '[CR]!'.encode('ansi')
    iPersonalityMessage = 'Sarà il Pokémon [CS:K]'.encode('ansi') + pokemon_name(value, 2) + '[CR]!'.encode('ansi')
    gPersonalityMessage = 'wird ein [CS:K]'.encode('ansi') + pokemon_name(value, 3) + '[CR]!'.encode('ansi')
    fPersonalityMessage = '... un [CS:K]'.encode('ansi') + pokemon_name(value, 4) + '[CR]!'.encode('ansi')
    personalityMessages = [sPersonalityMessage, ePersonalityMessage, iPersonalityMessage,
                           gPersonalityMessage, fPersonalityMessage]

    for language in range(0, 5):
        if pmd_version == "eu" or language == 1:
            pointer = bytes2int(textMemory[language][entry] + textMemory[language][entry + 1] +
                                textMemory[language][entry + 2] + textMemory[language][entry + 3])

            count = 0
            finish = False
            while not finish:
                byte = textMemory[language][pointer + count]
                if byte == int2bytes(0, 1):
                    finish = True
                elif count < len(personalityMessages[language]):
                    textMemory[language][pointer + count] = int2bytes(personalityMessages[language][count], 1)
                else:
                    textMemory[language][pointer + count] = int2bytes(32, 1)
                count += 1


def fix_portraits():
    for index in range(0, 1154):
        entry = 0x000000A0 + index * 160
        first_pointer = (portraitMemory[entry] + portraitMemory[entry + 1] +
                         portraitMemory[entry + 2] + portraitMemory[entry + 3])

        byte = portraitMemory[entry + 7]
        if byte == int2bytes(255, 1):
            first_pointer += (portraitMemory[entry + 4] + portraitMemory[entry + 5] +
                              portraitMemory[entry + 6] + portraitMemory[entry + 7])
        else:
            first_pointer += signedint2bytes(-bytes2int(portraitMemory[entry + 4] + portraitMemory[entry + 5] +
                                                        portraitMemory[entry + 6] + portraitMemory[entry + 7]), 4)

        for it in range(2, 40, 2):
            offset = entry + it * 4
            byte = portraitMemory[offset + 3]
            if byte == int2bytes(255, 1):
                portraitMemory[offset] = int2bytes(first_pointer[0], 1)
                portraitMemory[offset + 1] = int2bytes(first_pointer[1], 1)
                portraitMemory[offset + 2] = int2bytes(first_pointer[2], 1)
                portraitMemory[offset + 3] = int2bytes(first_pointer[3], 1)
                portraitMemory[offset + 4] = int2bytes(first_pointer[4], 1)
                portraitMemory[offset + 5] = int2bytes(first_pointer[5], 1)
                portraitMemory[offset + 6] = int2bytes(first_pointer[6], 1)
                portraitMemory[offset + 7] = int2bytes(first_pointer[7], 1)


def rand_player():
    maxPokemonId = 0x219

    excludedPokemon = [
        0x0000,  # No pokemon/end of list
        0x00C9,  # Unown A
        0x00CA,  # Unown B
        0x00CB,  # Unown C
        0x00CC,  # Unown D
        0x00CD,  # Unown E
        0x00CE,  # Unown F
        0x00CF,  # Unown G
        0x00D0,  # Unown H
        0x00D1,  # Unown I
        0x00D2,  # Unown J
        0x00D3,  # Unown K
        0x00D4,  # Unown L
        0x00D5,  # Unown M
        0x00D6,  # Unown N
        0x00D7,  # Unown O
        0x00D8,  # Unown P
        0x00D9,  # Unown Q
        0x00DA,  # Unown R
        0x00DB,  # Unown S
        0x00DC,  # Unown T
        0x00DD,  # Unown U
        0x00DE,  # Unown V
        0x00DF,  # Unown W
        0x00E0,  # Unown X
        0x00E1,  # Unown Y
        0x00E2,  # Unown Z
        0x00E3,  # Unown !
        0x00E4,  # Unown ?
    ]

    choosables = []

    for index in range(0, maxPokemonId):
        if index not in excludedPokemon:
            choosables.append(index)

    k = 0
    for index in range(0, 32):
        entry = 0x00001F78 + index * 2

        value = random.choice(choosables)
        choosables.remove(value)

        if k % 3 == 0:
            k += 1

        pokemon_message(value, k)
        k += 1

        if index % 2 == 1:
            value += 600

        overlay13Memory[entry] = int2bytes(int2bytes(value, 2)[0], 1)
        overlay13Memory[entry + 1] = int2bytes(int2bytes(value, 2)[1], 1)


def rand_partner():
    maxPokemonId = 0x219

    excludedPokemon = [
        0x0000,  # No pokemon/end of list
        0x00C9,  # Unown A
        0x00CA,  # Unown B
        0x00CB,  # Unown C
        0x00CC,  # Unown D
        0x00CD,  # Unown E
        0x00CE,  # Unown F
        0x00CF,  # Unown G
        0x00D0,  # Unown H
        0x00D1,  # Unown I
        0x00D2,  # Unown J
        0x00D3,  # Unown K
        0x00D4,  # Unown L
        0x00D5,  # Unown M
        0x00D6,  # Unown N
        0x00D7,  # Unown O
        0x00D8,  # Unown P
        0x00D9,  # Unown Q
        0x00DA,  # Unown R
        0x00DB,  # Unown S
        0x00DC,  # Unown T
        0x00DD,  # Unown U
        0x00DE,  # Unown V
        0x00DF,  # Unown W
        0x00E0,  # Unown X
        0x00E1,  # Unown Y
        0x00E2,  # Unown Z
        0x00E3,  # Unown !
        0x00E4,  # Unown ?
    ]

    choosables = []

    for index in range(0, maxPokemonId):
        if index not in excludedPokemon:
            choosables.append(index)

    for index in range(0, 21):
        entry = 0x00001F4C + index * 2

        value = random.choice(choosables)
        choosables.remove(value)

        if random.randint(0, 1) == 0:
            value += 600

        overlay13Memory[entry] = int2bytes(int2bytes(value, 2)[0], 1)
        overlay13Memory[entry + 1] = int2bytes(int2bytes(value, 2)[1], 1)


def rand_types(percent):
    maxTypeId = 0x13

    excludedTypes = [
        0x00,  # Notype, so excluded
        0x12  # Neutraltype, not usedfor pokemon
    ]

    choosables = []
    pokemonTypes = []

    for index in range(0, maxTypeId):
        if index not in excludedTypes:
            choosables.append(index)

    for index in range(0, 600):
        if random.randint(1, 100) <= percent:
            value1 = random.choice(choosables)
            value2 = random.choice(choosables)
            while value1 == value2:
                value2 = random.choice(choosables)
            pokemonTypes.append({'first': value1, 'second': value2})
        else:
            pokemonTypes.append({'first': random.choice(choosables), 'second': 0})

    for index in range(0, 1155):
        entry = 0x08 + index * 68
        pokemon_id = bytes2int(pokemonMemory[entry + 4] + pokemonMemory[entry + 5])

        pokemonMemory[entry + 20] = int2bytes(pokemonTypes[pokemon_id]['first'], 1)
        pokemonMemory[entry + 21] = int2bytes(pokemonTypes[pokemon_id]['second'], 1)


def rand_abilities(percent):
    maxAbilityId = 0x7D

    excludedAbilities = [
        0x00,  # No ability
        0x35,  # Wonder Guard, possibly gamebreaking
        0x74  # Unknown ability, named "$$$"
    ]

    choosables = []
    pokemonAbilities = []

    for index in range(0, maxAbilityId):
        if index not in excludedAbilities:
            choosables.append(index)

    for index in range(0, 600):
        if random.randint(1, 100) <= percent:
            value1 = random.choice(choosables)
            value2 = random.choice(choosables)
            while value1 == value2:
                value2 = random.choice(choosables)
            pokemonAbilities.append({'first': value1, 'second': value2})
        else:
            pokemonAbilities.append({'first': random.choice(choosables), 'second': 0})

    for index in range(0, 1155):
        entry = 0x08 + index * 68
        pokemon_id = bytes2int(pokemonMemory[entry + 4] + pokemonMemory[entry + 5])

        pokemonMemory[entry + 24] = int2bytes(pokemonAbilities[pokemon_id]['first'], 1)
        pokemonMemory[entry + 25] = int2bytes(pokemonAbilities[pokemon_id]['second'], 1)


def rand_iqgroups():
    maxIQId = 0x10

    excludedIQs = [
        0x08,  # Unused
        0x09,  # Unused
        0x0C,  # Unused
        0x0D,  # Unused
        0x0E,  # Unused
        0x0F  # Invalid
    ]

    choosables = []
    pokemonIQs = []

    for index in range(0, maxIQId):
        if index not in excludedIQs:
            choosables.append(index)

    for index in range(0, 600):
        pokemonIQs.append(random.choice(choosables))

    for index in range(0, 1155):
        entry = 0x8 + index * 68
        pokemon_id = bytes2int(pokemonMemory[entry + 4] + pokemonMemory[entry + 5])

        pokemonMemory[entry + 23] = int2bytes(pokemonIQs[pokemon_id], 1)


def rand_mobility():
    maxMobilityId = 0x06

    excludedMobilities = [
        0x01,  # Unused
    ]

    choosables = []
    pokemonMobilities = []

    for index in range(0, maxMobilityId):
        if index not in excludedMobilities:
            choosables.append(index)

    for index in range(0, 600):
        pokemonMobilities.append(random.choice(choosables))

    for index in range(0, 1155):
        entry = 0x8 + index * 68
        pokemon_id = bytes2int(pokemonMemory[entry + 4] + pokemonMemory[entry + 5])

        pokemonMemory[entry + 22] = int2bytes(pokemonMobilities[pokemon_id], 1)


def set_body_size():
    for index in range(0, 1155):
        entry = 0x8 + index * 68
        pokemonMemory[entry + 19] = int2bytes(1, 1)


def set_recruit_rate(percent):
    for index in range(0, 1155):
        entry = 0x8 + index * 68
        pokemonMemory[entry + 34] = int2bytes(int2bytes(percent*10, 2)[0], 1)
        pokemonMemory[entry + 35] = int2bytes(int2bytes(percent*10, 2)[1], 1)


def fix_legendary():
    excludedPokemon = [
        0x0000,  # No pokemon/end of list
        0x00C9,  # Unown A
        0x00CA,  # Unown B
        0x00CB,  # Unown C
        0x00CC,  # Unown D
        0x00CD,  # Unown E
        0x00CE,  # Unown F
        0x00CF,  # Unown G
        0x00D0,  # Unown H
        0x00D1,  # Unown I
        0x00D2,  # Unown J
        0x00D3,  # Unown K
        0x00D4,  # Unown L
        0x00D5,  # Unown M
        0x00D6,  # Unown N
        0x00D7,  # Unown O
        0x00D8,  # Unown P
        0x00D9,  # Unown Q
        0x00DA,  # Unown R
        0x00DB,  # Unown S
        0x00DC,  # Unown T
        0x00DD,  # Unown U
        0x00DE,  # Unown V
        0x00DF,  # Unown W
        0x00E0,  # Unown X
        0x00E1,  # Unown Y
        0x00E2,  # Unown Z
        0x00E3,  # Unown !
        0x00E4,  # Unown ?
        0x017B,  # Castform(form a)
        0x017C,  # Castform(form b)
        0x017D,  # Castform(form c)
        0x017E,  # Castform(form d)
        0x017F,  # Kecleon
        0x01A3,  # Deoxys(form b)
        0x01A4,  # Deoxys(form c)
        0x01A5,  # Deoxys(form d)
        0x0229  # Decoy
    ]

    for index in range(0, 1155):
        entry = 0x8 + index * 68
        pokemonMemory[entry + 26] = int2bytes(bytes2int(pokemonMemory[entry + 26]) & 127, 1)
        pokemonMemory[entry + 49] = int2bytes(0, 1)

    return excludedPokemon


def rand_moveset():
    maxMoveId = 0x21F

    excludedMoves = [
        0x0000,  # Null move
        0x0160,  # Struggle
        0x0163,  # Regularattack, not a move
        0x0164,  # Debug move "is watching"
        0x0165,  # Debug bide
        0x0166,  # Debug revenge
        0x0167,  # Debug avalanche
        0x0169,  # Null move
        0x016A,  # Null move
        0x016B,  # Item effect move, "See-Trap"
        0x016C,  # Item effect move, "Takeaway"
        0x016D,  # Item effect move, "Rebound"
        0x016E,  # Unused move, "Bloop Slash"
        0x016F,  # Item effect move, "Switcher"
        0x0170,  # Item effect move, "Blowback"
        0x0171,  # Item effect move, "Warp"
        0x0172,  # Item effect move, "Transfer"
        0x0173,  # Item effect move, "Slow Down"
        0x0174,  # Item effect move, "Speed Boost"
        0x0175,  # Item effect move, "Searchlight"
        0x0176,  # Item effect move, "Petrify"
        0x0177,  # Item effect move, "Stay Away"
        0x0178,  # Item effect move, "Pounce"
        0x0179,  # Item effect move, "Trawl"
        0x017A,  # Item effect move, "Cleanse"
        0x017B,  # Item effect move, "Observer"
        0x017C,  # Item effect move, "Decoy Maker"
        0x017D,  # Item effect move, "Siesta"
        0x017E,  # Item effect move, "Totter"
        0x017F,  # Item effect move, "Two-Edge"
        0x0180,  # Item effect move, "No-Move"
        0x0181,  # Item effect move, "Escape"
        0x0182,  # Item effect move, "Scan"
        0x0183,  # Item effect move, "Power-Ears"
        0x0184,  # Item effect move, "Drought"
        0x0185,  # Item effect move, "Trap Buster"
        0x0186,  # Item effect move, "Wild Call"
        0x0187,  # Item effect move, "Invisify"
        0x0188,  # Item effect move, "One-Shot"
        0x0189,  # Item effect move, "HP Gauge"
        0x018B,  # Item effect move, "Reviver"
        0x018C,  # Item effect move, "Shocker"
        0x018D,  # Item effect move, "Echo"
        0x018E,  # Item effect move, "Famish"
        0x018F,  # Item effect move, "One-Room"
        0x0190,  # Item effect move, "Fill-in"
        0x0191,  # Item effect move, "Trapper"
        0x0192,  # Item effect move, "Possess"
        0x0193,  # Item effect move, "Itemize"
        0x0194,  # Null move
        0x0195,  # Item effect move, "projectile"
        0x0196,  # Item effect move, "Hurl"
        0x0197,  # Item effect move, "Mobile"
        0x0198,  # Item effect move, "Item-Toss"
        0x0199,  # Item effect move, "See Stairs"
        0x019A,  # Item effect move, "Long Toss"
        0x019B,  # Null move
        0x019C,  # Item effect move, "Pierce"
        0x019D,  # Null move
        0x019E,  # Null move
        0x019F,  # Null move
        0x01A0,  # Null move
        0x01A1,  # Null move
        0x01A2,  # Null move
        0x01A3,  # Null move
        0x01A4,  # Null move
        0x01A5,  # Null move
        0x01A6,  # Null move
        0x01A7,  # Null move
        0x01A8,  # Null move
        0x01A9,  # Null move
        0x01AA,  # Null move
        0x01AB,  # Null move
        0x01AC,  # Null move
        0x01AD,  # Null move
        0x01D3   # Nullmove
    ]

    class LevelMove:

        move = 0
        level = 0

        def __init__(self, move, level):
            self.move = move
            self.level = level

        def is_large(self):
            return self.move >= 128

        def get_size(self):
            if self.is_large():
                return 3
            else:
                return 2

        def write(self, location):
            if self.is_large():
                moveMemory[location] = int2bytes(((self.move >> 7) & 0x7F) | 0x80, 1)
                moveMemory[location + 1] = int2bytes(self.move & 0x7F, 1)
                moveMemory[location + 2] = int2bytes(self.level, 1)
            else:
                moveMemory[location] = int2bytes(self.move, 1)
                moveMemory[location + 1] = int2bytes(self.level, 1)

        def write2(self, location):
            if self.is_large():
                moveMemory[location] = int2bytes(((self.move >> 7) & 0x7F) | 0x80, 1)
                moveMemory[location + 1] = int2bytes(self.move & 0x7F, 1)
            else:
                moveMemory[location] = int2bytes(self.move, 1)

    choosables = []
    size2Choosables = []
    size3Choosables = []

    for index in range(0, maxMoveId):
        if index not in excludedMoves:
            choosables.append(index)
            m = LevelMove(index, 0)
            if m.is_large():
                size3Choosables.append(index)
            else:
                size2Choosables.append(index)

    entry = 0x10
    position = 0
    for index in range(0, 553):
        levelList = entry + position
        levelSpace = 0

        while (bytes2int(moveMemory[entry + position + levelSpace]) != 0 or
               bytes2int(moveMemory[entry + position + levelSpace - 1]) > 0x7F):
            levelSpace += 1

        j = 0
        level = 1
        spaceRemain = levelSpace
        levelChoosables = choosables.copy()
        while j < (spaceRemain - 4):
            move = random.choice(levelChoosables)
            levelChoosables.remove(move)
            lmove = LevelMove(move, level)

            if lmove.is_large():
                lmove.write(levelList + j)
                j += 3
            else:
                lmove.write(levelList + j)
                j += 2

            level += random.randint(1, 5)
            if level > 50:
                level = 50

        def choose_move(num_list):
            if num_list == 2:
                while True:
                    move = random.choice(size2Choosables)
                    if move in levelChoosables:
                        return move
            elif num_list == 3:
                while True:
                    move = random.choice(size3Choosables)
                    if move in levelChoosables:
                        return move

        if (levelSpace - j) == 4:
            move = choose_move(2)
            levelChoosables.remove(move)
            lmove = LevelMove(move, level)
            lmove.write(levelList + j)
            j += 2
            level += random.randint(1, 5)
            if level > 50:
                level = 50
            move = choose_move(2)
            lmove = LevelMove(move, level)
            lmove.write(levelList + j)
            j += 2
        elif (levelSpace - j) == 3:
            move = choose_move(3)
            lmove = LevelMove(move, level)
            lmove.write(levelList + j)
            j += 3
        elif (levelSpace - j) == 2:
            move = choose_move(2)
            lmove = LevelMove(move, level)
            lmove.write(levelList + j)
            j += 2

        # TMs TODO
        TMList = entry + position + levelSpace + 1
        TMSpace = 0

        while (bytes2int(moveMemory[entry + position + levelSpace + TMSpace + 1]) != 0 or
               bytes2int(moveMemory[entry + position + levelSpace + TMSpace]) > 0x7F):
            TMSpace += 1

        # egg moves TODO
        eggList = entry + position + levelSpace + TMSpace + 2
        eggSpace = 0

        while (bytes2int(moveMemory[entry + position + levelSpace + TMSpace + eggSpace + 2]) != 0 or
               bytes2int(moveMemory[entry + position + levelSpace + TMSpace + eggSpace + 1]) > 0x7F):
            eggSpace += 1

        position += levelSpace + TMSpace + eggSpace + 3


def rand_items():
    maxItemId = 0x016B

    excludedItems = [
        0x0000,  # No item
        0x000B,  # Null item
        0x000C,  # Null item
        0x0062,  # Null item
        0x0071,  # Null item
        0x0072,  # Null item
        0x008A,  # Null item
        0x00A6,  # Null item
        0x00AF,  # Null item
        0x00B0,  # Null item
        0x00B1,  # Null item
        0x00B5,  # Null item
        0x00B8,  # Null item
        0x00B9,  # Null item
        0x00BB,  # Used TM, not a dungeon item
        0x00C2,  # Null item
        0x00C6,  # Null item
        0x00CD,  # Null item
        0x00DB,  # Null item
        0x00E0,  # Null item
        0x00E2,  # Null item
        0x00EC,  # Null item
        0x0102,  # Null item
        0x0103,  # Null item
        0x0125,  # Null item
        0x0126,  # Null item
        0x0127,  # Null item
        0x0128,  # Null item
        0x0129,  # Null item
        0x012A,  # Null item
        0x012B,  # Null item
        0x012C,  # Null item
        0x0144,  # Null item
        0x0153,  # Null item
        0x0159,  # Null item
        0x015D,  # Null item
        0x0161,  # Null item
        0x0168,  # Null item
        0x0169,  # Null item
        0x016B   # Null item
    ]

    groupChoosables = OrderedDict({'THROWN_LINE': [], 'THROWN_ARC': [], 'BERRY_SEED': [], 'FOOD': [], 'HELD': [],
                                   'TM': [], 'COINS': [], 'NOTHING': [], 'OTHER': [], 'ORB': [], 'BOX': []})

    for i in range(0, maxItemId):
        if i not in excludedItems:

            if (0x0001 <= i <= 0x0006) or (i == 0x0009):
                groupChoosables['THROWN_LINE'].append(i)
            elif (0x0007 <= i <= 0x0008) or (i == 0x000A):
                groupChoosables['THROWN_ARC'].append(i)
            elif 0x000D <= i <= 0x0044:
                groupChoosables['HELD'].append(i)
            elif (0x0045 <= i <= 0x006C) or (0x0074 <= i <= 0x0076):
                groupChoosables['BERRY_SEED'].append(i)
            elif (0x006D <= i <= 0x0070) or (0x0077 <= i <= 0x0089) or (i == 0x0073):
                groupChoosables['FOOD'].append(i)
            elif (0x008B <= i <= 0x00BA) and (i != 0x00B7):
                groupChoosables['OTHER'].append(i)
            elif 0x00BC <= i <= 0x0124:
                groupChoosables['TM'].append(i)
            elif 0x012D <= i <= 0x0167:
                groupChoosables['ORB'].append(i)
            elif i == 0x016A:
                groupChoosables['BOX'].append(i)
            elif i == 0x00B7:
                groupChoosables['COINS'].append(i)

    weights = [7, 3, 142, 224, 56, 96, 1, 0, 41, 54, 1]

    ptrList = 0x00041A04
    valueStart = 0x00035A28

    position = 0

    for i in range(0, 216):
        pointer1 = bytes2int(dungeonMemory[ptrList + (i * 4)] + dungeonMemory[ptrList + (i * 4) + 1] +
                             dungeonMemory[ptrList + (i * 4) + 2] + dungeonMemory[ptrList + (i * 4) + 3])
        pointer2 = bytes2int(dungeonMemory[ptrList + (i * 4) + 4] + dungeonMemory[ptrList + (i * 4) + 5] +
                             dungeonMemory[ptrList + (i * 4) + 6] + dungeonMemory[ptrList + (i * 4) + 7])
        size = pointer2 - pointer1

        items_list = ItemSpawn()
        for j in range(0, 11):
            if weights[j] != 0:
                items_list.addCategory(j, weights[j])

                for k in range(0, len(list(list(groupChoosables.items())[j])[1])):
                    items_list.addItem(list(list(groupChoosables.items())[j])[1][k] + 0x10, j)

        items_list.normalize(size)
        items_list.write(dungeonMemory, valueStart + position)
        position += size


































