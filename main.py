#!/usr/bin/env ./venv/bin/python

# data for words gotten from nimi.li

import pygame
import random

pygame.init()

class Program:

    WINDOW_WIDTH: int = 1800
    WINDOW_HEIGHT: int = 900

    FONT = pygame.font.SysFont("Noto Sans", 75)
    FONT_SMALL = pygame.font.SysFont("Noto Sans", 37)

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    fps: int = 60
    clock = pygame.time.Clock()

    game_mode: str = "menu"  # can be menu, words, symbols

    reveal_answer: bool = False
    show_toki_pona: bool = False  # before the answer has been shown, this determines if (in words mode) if the English or toki pona translation should only be shown, and (in symbols mode) if the symbol or toki pona should only be shonw
    chosen_word: str = ""  # the word that will be asked about
    randomizer_bag: list[str] = []

    # user drawing stuff
    current_stroke = []
    strokes = []

    words = {
        "a": {"rarity": "pu", "usage": 0, "translation": "interjection like ah or oh, and placed after something for emphasis or emotion"},
        "akesi": {"rarity": "pu", "usage": 0, "translation": "reptile, amphibian, scaly creature, crawling creature"},
        "ala": {"rarity": "pu", "usage": 0, "translation": "not, nothing, no, zero; forms yes/no question"},
        "alasa": {"rarity": "pu", "usage": 0, "translation": "hunt, forage, search, attempt; (preverb) try to"},
        "ale": {"rarity": "pu", "usage": 0, "translation": "all, every, everything, universe; the number one hundred"},
        "anpa": {"rarity": "pu", "usage": 0, "translation": "bottom, underside; below, beneath; defeated, humble, lowly"},
        "ante": {"rarity": "pu", "usage": 0, "translation": "different, altered; modify, change; other; difference"},
        "anu": {"rarity": "pu", "usage": 0, "translation": "or"},
        "awen": {"rarity": "pu", "usage": 0, "translation": "stay, remain, wait, pause; protect, keep safe; continue; (preverb) continue to"},
        "e": {"rarity": "pu", "usage": 0, "translation": "(mark start of direct object)"},
        "en": {"rarity": "pu", "usage": 0, "translation": "(separates multiple subjects)"},
        "esun": {"rarity": "pu", "usage": 0, "translation": "trade, banter, exchange, swap, buy, sell; market, shop, plaze of business"},
        "ijo": {"rarity": "pu", "usage": 0, "translation": "thing, object, entity, being, matter, phenomenon"},
        "ike": {"rarity": "pu", "usage": 0, "translation": "negative quality, e.g. bad, unpleasant, harmful, unneeded"},
        "ilo": {"rarity": "pu", "usage": 0, "translation": "tool, implement, machine, device"},
        "insa": {"rarity": "pu", "usage": 0, "translation": "inside, center, between, middle, midpoint, internal"},
        "jaki": {"rarity": "pu", "usage": 0, "translation": "disgusting, unclean, unsanitary, toxic, repulsive, rotten"},
        "jan": {"rarity": "pu", "usage": 0, "translation": "human being, person, somebody"},
        "jelo": {"rarity": "pu", "usage": 0, "translation": "yellow, amber, golden, lime yellow, yellowish orange"},
        "jo": {"rarity": "pu", "usage": 0, "translation": "hold, carry, possess, contain, own"},
        "kala": {"rarity": "pu", "usage": 0, "translation": "fish, marine animal, sea creature, swimming creature"},
        "kalama": {"rarity": "pu", "usage": 0, "translation": "to produce sound; sound, e.g.sing, thunder, drum, clap, laugh, beep"},
        "kama": {"rarity": "pu", "usage": 0, "translation": "arriving, coming, future, summoned;  (preverb) to become, manage to, succeed in"},
        "kasi": {"rarity": "pu", "usage": 0, "translation": "plant, vegetation; herb, leaf"},
        "ken": {"rarity": "pu", "usage": 0, "translation": "can, may, ability, permission; possibility, maybe; allow, enable, (preverb) to be able to"},
        "kepeken": {"rarity": "pu", "usage": 0, "translation": "(prepositoin) using, by means of"},
        "kili": {"rarity": "pu", "usage": 0, "translation": "fruit, vegetable, mushroom"},
        "kiwen": {"rarity": "pu", "usage": 0, "translation": "hard object e.g. metal, stone, wood"},
        "ko": {"rarity": "pu", "usage": 0, "translation": "sime-solid, e.g. paste, powder, goo, sand, soil, clay; squishy, moldable; sticky"},
        "kon": {"rarity": "pu", "usage": 0, "translation": "air, breath, wind; essence, spirit, soul, ghost; unseen agent"},
        "kule": {"rarity": "pu", "usage": 0, "translation": "color, pigment; category, genre, flavor; colorful, diverse"},
        "kulupu": {"rarity": "pu", "usage": 0, "translation": "group, community, society, company, nation, collection, team, crowd"},
        "kute": {"rarity": "pu", "usage": 0, "translation": "ear, hearing organ; hear, listen, pay attention to, obey"},
        "la": {"rarity": "pu", "usage": 0, "translation": "(particle marking the previous statement as context to the following statement)"},
        "lape": {"rarity": "pu", "usage": 0, "translation": "sleep, rest, break from an activity or work"},
        "laso": {"rarity": "pu", "usage": 0, "translation": "turquoise, blue, green, cyan, indigo, lime green"},
        "lawa": {"rarity": "pu", "usage": 0, "translation": "head, mind, brain; control, lead, guide; government, leader; rule, law"},
        "len": {"rarity": "pu", "usage": 0, "translation": "cloth, clothing, fabric, textile; covered, hidden, secret, private"},
        "lete": {"rarity": "pu", "usage": 0, "translation": "cold, cool, frozen; freeze, chill; raw, uncooked"},
        "li": {"rarity": "pu", "usage": 0, "translation": "(particle that marks the start of an indicative verb (statement))"},
        "lili": {"rarity": "pu", "usage": 0, "translation": "small, short, young; few; piece, part"},
        "linja": {"rarity": "pu", "usage": 0, "translation": "long flexible thing, e.g. rope, yarn hair, fur, line, strand"},
        "lipu": {"rarity": "pu", "usage": 0, "translation": "flat and bendable object, e.g. paper, card, leaf; written text or document, e.g. book, website, clay tablet"},
        "loje": {"rarity": "pu", "usage": 0, "translation": "red magenta, scarlet, pink, rust-colored, reddish orange"},
        "lon": {"rarity": "pu", "usage": 0, "translation": "present, existing, real, true; (preposition) located at, in, during, in the context of"},
        "luka": {"rarity": "pu", "usage": 0, "translation": "hand, arm, tactile limb, grasping limb; to grasp, interact with, feel using touch; the number five"},
        "lukin": {"rarity": "pu", "usage": 0, "translation": "see, look, view, examine, read, watch; visual; eye, seeing organ; (preverb) try to"},
        "lupa": {"rarity": "pu", "usage": 0, "translation": "hole, pit, cave, doorway, window, portal"},
        "ma": {"rarity": "pu", "usage": 0, "translation": "earth, land, soil; country, territory, world; outdoors"},
        "mama": {"rarity": "pu", "usage": 0, "translation": "parent, ancestor; creator, originator; caretaker, sustainer, guardian"},
        "mani": {"rarity": "pu", "usage": 0, "translation": "money, currency; thing of value e.g. gold, investment, livestock"},
        "mi": {"rarity": "pu", "usage": 0, "translation": "I, me, we, us"},
        "moku": {"rarity": "pu", "usage": 0, "translation": "eat, drink, consume, swallow, ingest; food, edible thing"},
        "moli": {"rarity": "pu", "usage": 0, "translation": "death, dead, die, dying; kill, murder"},
        "monsi": {"rarity": "pu", "usage": 0, "translation": "back, behind, rear"},
        "mu": {"rarity": "pu", "usage": 0, "translation": "(animal noise or communication, onomatopoeia)"},
        "mun": {"rarity": "pu", "usage": 0, "translation": "moon, night sky object, star, celestial body"},
        "musi": {"rarity": "pu", "usage": 0, "translation": "fun, game, entertainment, art, play, amusing, interesting, comical, silly"},
        "mute": {"rarity": "pu", "usage": 0, "translation": "many, several, very; quantity; the number twenty"},
        "nanpa": {"rarity": "pu", "usage": 0, "translation": "number; (particle) [ordinal number], -th"},
        "nasa": {"rarity": "pu", "usage": 0, "translation": "strange, usual, silly, abnormal, unexpected; drunk, intoxicated"},
        "nasin": {"rarity": "pu", "usage": 0, "translation": "method, doctrine, tradition; path, road, way"},
        "nena": {"rarity": "pu", "usage": 0, "translation": "protuberances e.g. bump, button, hill, nose"},
        "ni": {"rarity": "pu", "usage": 0, "translation": "this, that, these, those"},
        "nimi": {"rarity": "pu", "usage": 0, "translation": "word, name"},
        "noka": {"rarity": "pu", "usage": 0, "translation": "foot, leg, organ of locomotion, roots"},
        "o": {"rarity": "pu", "usage": 0, "translation": "(particle) [marks end of a vocative (who is being spoken to)], [marks start of imperative (command, wish, instruction)], should"},
        "olin": {"rarity": "pu", "usage": 0, "translation": "to have strong emotional bond with, e.g. affection, appreciation, compassion, respect; platonic, romantic, familial relationships"},
        "ona": {"rarity": "pu", "usage": 0, "translation": "he, she, it, they"},
        "open": {"rarity": "pu", "usage": 0, "translation": "being, start, open, turn on; beginning"},
        "pakala": {"rarity": "pu", "usage": 0, "translation": "damaged, broken, botched, harmed, messed up; mistake"},
        "pali": {"rarity": "pu", "usage": 0, "translation": "work, activity; create, build, design; put effort toward, take action on"},
        "palisa": {"rarity": "pu", "usage": 0, "translation": "long and hard thing e.g. branch, pole, rod, stick, spine, mast"},
        "pan": {"rarity": "pu", "usage": 0, "translation": "grains, starchy foods, baked goods e.g. rice, bread, noodles, porridge"},
        "pana": {"rarity": "pu", "usage": 0, "translation": "give, send, emit, provide, put, release"},
        "pi": {"rarity": "pu", "usage": 0, "translation": "(particle) [group the following words into one modifier for the previous word]"},
        "pilin": {"rarity": "pu", "usage": 0, "translation": "experience e.g. emotion, feeling, touch; heart (physical or emotional)"},
        "pimeja": {"rarity": "pu", "usage": 0, "translation": "dark, unlit; dark color, e.g. black, purple, brown"},
        "pini": {"rarity": "pu", "usage": 0, "translation": "finish, stop, prevent; close, disable, turn off; ended, past; edge, end, conclusion"},
        "pipi": {"rarity": "pu", "usage": 0, "translation": "insect, bug, spider, tiny crawling creature"},
        "poka": {"rarity": "pu", "usage": 0, "translation": "hip, side; next to, nearby, vicinity"},
        "poki": {"rarity": "pu", "usage": 0, "translation": "container e.g. bag, bowl, box, cup, cupboard, drawer, folder"},
        "pona": {"rarity": "pu", "usage": 0, "translation": "positive quality, e.g. good, pleasant, helpful, friendly, useful, peaceful"},
        "pu": {"rarity": "pu", "usage": 0, "translation": "interacting with the book Toki Pona: The Language of Good by Sonja Lang"},
        "sama": {"rarity": "pu", "usage": 0, "translation": "same, similar, alike; (adjective) peer, fellow, each other; (preposition) similar to, same as"},
        "seli": {"rarity": "pu", "usage": 0, "translation": "hot, warm; heat, fire, flame; burn"},
        "selo": {"rarity": "pu", "usage": 0, "translation": "outer layer, e.g. skin, peel, shell, bark; outer shape, outer form, boundary"},
        "seme": {"rarity": "pu", "usage": 0, "translation": "(particle) [indicate a question by marking missing info in a sentence]; what, which, who"},
        "sewi": {"rarity": "pu", "usage": 0, "translation": "up, top, above, highest part; divine, sacred, supernatural; awesome, inspiring, excelling"},
        "sijelo": {"rarity": "pu", "usage": 0, "translation": "body, shape, physical state, torso, substance, form"},
        "sike": {"rarity": "pu", "usage": 0, "translation": "circle, sphere, spiral, round thing e.g. ball, wheel; repeating thing e.g. cycle, orbit, loop"},
        "sin": {"rarity": "pu", "usage": 0, "translation": "new, fresh, update; repeat, do again"},
        "sina": {"rarity": "pu", "usage": 0, "translation": "you (singular and plural)"},
        "sinpin": {"rarity": "pu", "usage": 0, "translation": "vertical surface e.g. wall, board; front of something e.g. face"},
        "sitelen": {"rarity": "pu", "usage": 0, "translation": "image, picture, representation, symbol, mark, writing"},
        "sona": {"rarity": "pu", "usage": 0, "translation": "knowledge, information, data; know, be skilled in, be wise, about; (preverb) know how to"},
        "soweli": {"rarity": "pu", "usage": 0, "translation": "fuzzy creature, land animal, beast"},
        "suli": {"rarity": "pu", "usage": 0, "translation": "big, heavy, large, long, tall, wide; important, relevant"},
        "suno": {"rarity": "pu", "usage": 0, "translation": "light, shine, glow, radiance; sun, light source; brightness"},
        "supa": {"rarity": "pu", "usage": 0, "translation": "flat horizontal surface, especially to put or rest things on e.g. bed, floor, desk, plate, table, platform, stage"},
        "suwi": {"rarity": "pu", "usage": 0, "translation": "sweet, fragrent; cute, adorable"},
        "tan": {"rarity": "pu", "usage": 0, "translation": "(preposition) from, because of; cause, origin"},
        "taso": {"rarity": "pu", "usage": 0, "translation": "only, exclusively; (particle) [marks a sentence as qualifying or contradictory], but, however"},
        "tawa": {"rarity": "pu", "usage": 0, "translation": "motion, e.g. walking, shaking, flight, travel; (prepositoin) to, for, going to, from the perspective of"},
        "telo": {"rarity": "pu", "usage": 0, "translation": "liquids e.g. water, gasoline, soda, lava, soup, oil, ink"},
        "tenpo": {"rarity": "pu", "usage": 0, "translation": "time, event, situation, moment, period, duration"},
        "toki": {"rarity": "pu", "usage": 0, "translation": "communicate, say, think; conversation, story; language"},
        "tomo": {"rarity": "pu", "usage": 0, "translation": "indoor space or shelter e.g. room, building, home, tent, shack"},
        "tu": {"rarity": "pu", "usage": 0, "translation": "the number two; seperate, divide, split"},
        "unpa": {"rarity": "pu", "usage": 0, "translation": "sex, to have sex with"},
        "uta": {"rarity": "pu", "usage": 0, "translation": "mouth, lips, throat, consuming, orifice"},
        "utala": {"rarity": "pu", "usage": 0, "translation": "fight, compete, battle; competition, challenge; struggle, strive"},
        "walo": {"rarity": "pu", "usage": 0, "translation": "light-colored, white, pale, light, gray, cream"},
        "wan": {"rarity": "pu", "usage": 0, "translation": "the number one; singular; combine, join, mix, fuse"},
        "waso": {"rarity": "pu", "usage": 0, "translation": "bird, flying creature, winged animal"},
        "wawa": {"rarity": "pu", "usage": 0, "translation": "power, energy, strength; confident, intense, forceful; amazing, impressive"},
        "weka": {"rarity": "pu", "usage": 0, "translation": "absent, away, distant; remove, get rid of"},
        "wile": {"rarity": "pu", "usage": 0, "translation": "want, desire, wish, require; (preverb) want to"},
        "kijetesantakalu": {"rarity": "ku", "usage": 75, "translation": "racoon, kinkajou; any procyonid; any musteloid"},
        "kin": {"rarity": "ku", "usage": 83, "translation": "(particle) [after phrase or at sentence start] too, also, as well, additionally"},
        "kipisi": {"rarity": "ku", "usage": 71, "translation": "split, cut, slice; piece, part; sharp, pointy"},
        "ku": {"rarity": "ku", "usage": 67, "translation": "interacting with the book Toki Pona Dictionary (2021) by Sonja Lang"},
        "leko": {"rarity": "ku", "usage": 69, "translation": "square, cube, block, blocky, object e.g. bricks, stairs"},
        "meli": {"rarity": "pu", "usage": 82, "translation": "woman, female, wife, girlfriend"},
        "mije": {"rarity": "pu", "usage": 82, "translation": "man, male, husband, boyfriend"},
        "misikeke": {"rarity": "ku", "usage": 63, "translation": "medical item or practice e.g. prescriptions, meditation, exercise, bandages, therapy"},
        "monsuta": {"rarity": "ku", "usage": 84, "translation": "fear, nervousness, dread; scary, frightening; scary thing e.g. predator, threat, danger"},
        "n": {"rarity": "ku", "usage": 73, "translation": "(interjection) hm, uh, mm, er, umm, [indicate thinking or pause]"},
        "namako": {"rarity": "ku", "usage": 72, "translation": "spice, ornament, adornment, embelishment; extra, additional"},
        "soko": {"rarity": "ku", "usage": 65, "translation": "mushroom, fungus, lichen"},
        "tonsi": {"rarity": "ku", "usage": 82, "translation": "nonbinary, gender noncomforming, genderqueer, transgender*"},
        "epiku": {"rarity": "ku", "usage": 50, "translation": "epic, cool, awesome, amazing"},
        "jasima": {"rarity": "ku", "usage": 43, "translation": "reflect, echo; mirror, duplicate"},
        "lanpan": {"rarity": "ku", "usage": 59, "translation": "take, seize, steal"},
        "linluwi": {"rarity": "nimisin", "usage": 38, "translation": "bonded things which are stronger through their bonds e.g. network, internet, connection; weave, braid, interlace"},
        "majuna": {"rarity": "nimisin", "usage": 46, "translation": "old, aged, ancient"},
        "meso": {"rarity": "ku", "usage": 52, "translation": "midpoint, medium, mediocre; neither one not the other, neither fully is nor isn't"},
        "nimisin": {"rarity": "nimisin", "usage": 38, "translation": "any non-pu word; any new word; any joke word"},
        "oko": {"rarity": "ku", "usage": 52, "translation": "see, look, view, examine, read, watch; visual; eye, seeing organ; (preverb) try to. VERY SIMILAR TO LUKIN(???)"},
        "su": {"rarity": "nimisin", "usage": 50, "translation": "interacting with a book from the official toki pona story books"},
    }

    categories_to_use = []
    with open("selected_categories.txt") as f:
        lines = f.readlines()
        for line in lines:
            if line == "" or line == "\n" or line[0] == "#":
                continue
            categories_to_use.append(line.replace("\n", ""))

    words_to_use = {}
    for word in words:
        if word in categories_to_use:
            words_to_use[word] = words[word]
    words = words_to_use


    # load sitelen pona textures for each word
    for word in words:
        words[word]["texture"] = pygame.image.load(f"images/{word}.png").convert_alpha()

    # make translations that are really long have line breaks
    for word in words:
        if len(words[word]["translation"]) <= 60:
            continue
        char_index = 60
        char = words[word]["translation"][char_index]
        while char != " ":
            char_index -= 1
            char = words[word]["translation"][char_index]
        words[word]["translation"] = words[word]["translation"][:char_index] + "\n" + words[word]["translation"][char_index+1:]



    @staticmethod
    def Logic() -> None:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        events = pygame.event.get()

        # global logic that happens irregardless of current gmae mode
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


        if Program.game_mode == "menu":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        Program.game_mode = "words"
                        Program.ChoseNewWord()
                        return
                    if event.key == pygame.K_s:
                        Program.game_mode = "symbols"
                        Program.ChoseNewWord()
                        return


        if Program.game_mode == "words" or Program.game_mode == "symbols":

            if pygame.mouse.get_pressed()[0]:
                Program.current_stroke.append((mouse_x, mouse_y))

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        if not Program.reveal_answer:
                            Program.reveal_answer = True
                        else:
                            Program.ChoseNewWord()

                if event.type == pygame.MOUSEBUTTONUP:  # save current stroke to list of stroke once mouse is released
                    Program.strokes.append(Program.current_stroke.copy())
                    Program.current_stroke.clear()





    @staticmethod
    def ChoseNewWord() -> None:
        if Program.randomizer_bag == []:
            Program.randomizer_bag = list(Program.words)
            random.shuffle(Program.randomizer_bag)
        Program.chosen_word = Program.randomizer_bag.pop(0)
        Program.reveal_answer = False
        if Program.game_mode == "words":
            Program.show_toki_pona = not Program.show_toki_pona
        else:
            Program.show_toki_pona = True
        Program.strokes.clear()



    @staticmethod
    def Render() -> None:

        Program.window.fill((0, 0, 0))

        if Program.game_mode == "menu":
            Program.window.blit(Program.FONT.render(f"press W to train words", True, (255, 255, 255)), (500, 200))
            Program.window.blit(Program.FONT.render(f"press S to train symbols", True, (255, 255, 255)), (500, 400))


        if Program.game_mode == "words":

            # render English
            if (not Program.show_toki_pona) or Program.reveal_answer:
                lines = Program.words[Program.chosen_word]["translation"].split("\n")
                for i, line in enumerate(lines):
                    Program.window.blit(Program.FONT_SMALL.render(line, True, (255, 255, 255)), (500, 150 + i*37))

            # render toki pona
            if Program.show_toki_pona or Program.reveal_answer:
                word_string = Program.chosen_word
                if word_string == "ale":
                    word_string = "ale (also pronounced ali)"
                Program.window.blit(Program.FONT.render(word_string, True, (255, 255, 255)), (800, 250))

            if Program.reveal_answer:

                # render rarity
                if Program.words[Program.chosen_word]["rarity"] == "ku": rarity_color = (255, 255, 0)
                if Program.words[Program.chosen_word]["rarity"] == "nimisin": rarity_color = (255, 100, 0)
                if Program.words[Program.chosen_word]["rarity"] != "pu":
                    Program.window.blit(Program.FONT_SMALL.render(Program.words[Program.chosen_word]["rarity"], True, rarity_color), (800, 830))
                    Program.window.blit(Program.FONT_SMALL.render(str(Program.words[Program.chosen_word]["usage"])+"%", True, rarity_color), (1050, 830))

                # render symbol
                Program.window.blit(Program.words[Program.chosen_word]["texture"], (725, 400))


        if Program.game_mode == "symbols":

            # render symbol
            if (not Program.show_toki_pona) or Program.reveal_answer:
                Program.window.blit(Program.words[Program.chosen_word]["texture"], (725, 400))

            # render text
            if Program.show_toki_pona or Program.reveal_answer:
                lines = Program.words[Program.chosen_word]["translation"].split("\n")
                for i, line in enumerate(lines):
                    Program.window.blit(Program.FONT_SMALL.render(line, True, (255, 255, 255)), (500, 150 + i*37))
                word_string = Program.chosen_word
                if word_string == "ale":
                    word_string = "ale (also pronounced ali)"
                Program.window.blit(Program.FONT.render(word_string, True, (255, 255, 255)), (800, 250))

            if Program.reveal_answer:

                # render rarity
                if Program.words[Program.chosen_word]["rarity"] == "ku": rarity_color = (255, 255, 0)
                if Program.words[Program.chosen_word]["rarity"] == "nimisin": rarity_color = (255, 100, 0)
                if Program.words[Program.chosen_word]["rarity"] != "pu":
                    Program.window.blit(Program.FONT_SMALL.render(Program.words[Program.chosen_word]["rarity"], True, rarity_color), (800, 830))
                    Program.window.blit(Program.FONT_SMALL.render(str(Program.words[Program.chosen_word]["usage"])+"%", True, rarity_color), (1050, 830))


        # render bounds for where you are intended to draw your own symbol I guess idfk
        if Program.game_mode == "symbols":
            pygame.draw.rect(Program.window, (255, 255, 255), (0, 400, 600, 10))
            pygame.draw.rect(Program.window, (255, 255, 255), (590, 410, 10, 490))


        if Program.game_mode in ("words", "symbols"):

            for stroke in Program.strokes:
                for i in range(len(stroke) - 1):
                    pygame.draw.line(Program.window, (255, 255, 255), stroke[i], stroke[i+1], 25)
                    pygame.draw.circle(Program.window, (255, 255, 255), stroke[i], 10)
                pygame.draw.circle(Program.window, (255, 255, 255), stroke[-1], 10)
            for i in range(len(Program.current_stroke) - 1):
                pygame.draw.line(Program.window, (255, 255, 255), Program.current_stroke[i], Program.current_stroke[i+1], 25)
                pygame.draw.circle(Program.window, (255, 255, 255), Program.current_stroke[i], 10)

        pygame.display.flip()



    @staticmethod
    def Run() -> None:
        while True:
            Program.Logic()
            Program.Render()
            Program.clock.tick(Program.fps)



if __name__ == "__main__":
    Program.Run()
