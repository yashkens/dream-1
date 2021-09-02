import logging
import re
import json

from dff.core import Node, Context, Actor


logger = logging.getLogger(__name__)
# ....


def extract_members(node_label: str, node: Node, ctx: Context, actor: Actor, *args, **kwargs):
    slots = ctx.misc.get("slots", {})
    members = ["John", "Len*on", "Ringo", "Star*", "Paul", "McCartn*y", "George", "Har*ison"]
    members_re = "|".join(members)
    extracted_member = re.findall(members_re, ctx.last_request, re.IGNORECASE)
    if re.findall(r'john|len*on', ctx.last_request, re.IGNORECASE) != []:
        slots["beatles_member"] = "John Lennon"
        ctx.misc["slots"] = slots
    elif re.findall(r'paul|mccartne*y', ctx.last_request, re.IGNORECASE) != []:
        slots["beatles_member"] = "Paul McCartney"
        ctx.misc["slots"] = slots
    elif re.findall(r'ringo|star*s*', ctx.last_request, re.IGNORECASE) != []:
        slots["beatles_member"] = "Ringo Starr"
        ctx.misc["slots"] = slots
    elif re.findall(r'george|har*ison', ctx.last_request, re.IGNORECASE) != []:
        slots["beatles_member"] = "George Harrison"
        ctx.misc["slots"] = slots

    return node_label, node


def extract_inst(node_label: str, node: Node, ctx: Context, actor: Actor, *args, **kwargs):
    slots = ctx.misc.get("slots", {})
    insts = ["trumpet", "drums", "guitar"]
    insts_re = "|".join(insts)
    extracted_inst = re.findall(insts_re, ctx.last_request, re.IGNORECASE)
    if "guitar" in extracted_inst:
        slots["instrument_intro"] = "Cool! We have a lot of guitars here. Let's begin with a story about Paul McCartney's first guitar. "
        ctx.misc["slots"] = slots
    elif "trumpet" in extracted_inst:
        slots["instrument_intro"] = "Then I have a funny story about trumpets for you! "
        ctx.misc["slots"] = slots
    elif "drums" in extracted_inst:
        slots["instrument_intro"] = "If you like drums, you must like Ringo Starr! Let's save his his drumkit for last and begin with the guitars. "
        ctx.misc["slots"] = slots
    else:
        slots["instrument_intro"] = "Well, let me show you the collection of instruments that we have here. "
        ctx.misc["slots"] = slots
    return node_label, node


def extract_albums(node_label: str, node: Node, ctx: Context, actor: Actor, *args, **kwargs):
    slots = ctx.misc.get("slots", {})
    albums = [
        "Please Please Me",
        "With the Beatles",
        "Introducing... The Beatles",
        "Meet the Beatles!",
        "Twist and Shout",
        "The Beatles' Second Album",
        "The Beatles' Long Tall Sally",
        "A Hard Day's Night",
        "Something New",
        "Help!",
        "Sgt. Pepper's Lonely Hearts Club Band",
        "White Album",
        "The Beatles Beat",
        "Another Beatles Christmas Record",
        "Beatles '65",
        "Beatles VI",
        "Five Nights In A Judo Arena",
        "The Beatles at the Hollywood Bowl",
        "Live! at the Star-Club in Hamburg, German; 1962",
        "The Black Album",
        "20 Exitos De Oro",
        "A Doll's House",
        "The Complete Silver Beatles",
        "Rock 'n' Roll Music Vol. 1",
        "Yellow Submarine",
        "Let It Be",
        "Beatles for Sale",
        "Revolver",
        "Abbey Road",
        "Rubber Soul",
    ]

    albums_re = "|".join(albums)
    extracted_album = re.findall(albums_re, ctx.last_request, re.IGNORECASE)
    if extracted_album:
        slots["album_name"] = extracted_album[0]
        ctx.misc["slots"] = slots

    return node_label, node


def slot_filling_albums(node_label: str, node: Node, ctx: Context, actor: Actor, *args, **kwargs):
    slots = ctx.misc.get("slots", {})
    slots["first_album"] = "Let's begin our trip here. I will show you some albums first. If you get tired, just say 'MOVE ON'. "
    slots["sgt_peppers"] = "George Martin played a significant role in recording most of the band’s albums, including their arguably greatest success — Sgt Pepper’s Lonely Hearts Club."
    slots["a_hard_days_night_corr"] = "And you're right, A Hard Day's Night it was! "
    slots["a_hard_days_night_wrong"] = "It was A Hard Day's Night! "
    slots["rubber_soul"] = "However, it was after this cry for 'Help' that the Beatles became the Beatles. "
    slots["yellow_submarine"] = "Then let's take a look at the album. "
    slots["abbey_road"] = (
        "By the way, The White Album' recording sessions lasted 137 days! Abbey Road, on the opposite, "
        "was recorded in one 12-hour session -- even faster than Please Please Me! "
    )
    slots["let_it_be"] = (
        "Did you know that Abbey Road was created and issued after the recording of the Beatles' "
        "last released album took place? "
    )

    for slot_name, slot_value in slots.items():
        if ctx.misc.get("first_album") is None and slot_name == "first_album":
            ctx.misc["first_album"] = True
        elif ctx.misc["first_album"] == True and slot_name == "first_album":
            slot_value = ""
        node.response = node.response.replace("{" f"{slot_name}" "}", slot_value)

    return node_label, node


def extract_song_id(node_label: str, node: Node, ctx: Context, actor: Actor, *args, **kwargs):
    songs = [
        "Hey Jude",
        "Don't Let Me Down",
        "We Can Work it Out",
        "Come Together",
        "Yellow Submarine",
        "Revolution",
        "Imagine",
        "Something",
        "Hello, Goodbye",
        "A Day In The Life",
        "Help!",
        "Penny Lane",
    ]

    songs_ids = {
        "Hey Jude": "826kt29479qp27",
        "Don't Let Me Down": "hvnck9pvgnpft4",
        "We Can Work it Out": "s1mfzw528vt05m",
        "Come Together": "qrg1tn7dpx2066",
        "Yellow Submarine": "bsqcc0bkbkxb75",
        "Revolution": "grmx7c4g9rb412",
        "Imagine": "rh8bfh6m7fr13g",
        "Something": "74v09tbmqmbf9z",
        "Hello, Goodbye": "87krd594czgd2d",
        "A Day In The Life": "b8ptdvbm1rzccs",
        "Help!": "zk3dvf2qt7sr0p",
        "Penny Lane": "zhw7593t9mb9gn",
    }

    songs_re = "|".join(songs)
    extracted_song = re.findall(songs_re, ctx.last_request, re.IGNORECASE)
    if extracted_song:
        for k in songs_ids.keys():
            if extracted_song[0].lower() == k.lower():
                id = songs_ids[k]

    node.misc = {"command": "goto", "objectId": id}

    return node_label, node


def fill_slots(node_label: str, node: Node, ctx: Context, actor: Actor, *args, **kwargs):
    for slot_name, slot_value in ctx.misc.get("slots", {}).items():
        node.response = node.response.replace("{" f"{slot_name}" "}", slot_value)
    return node_label, node


def increment_album_counter(node_label: str, node: Node, ctx: Context, actor: Actor, *args, **kwargs):
    ctx.misc["album_counter"] = ctx.misc.get("album_counter", 0) + 1
    return node_label, node


def add_misc_to_response(node_label: str, node: Node, ctx: Context, actor: Actor, *args, **kwargs):
    node.response = f"{node.response} {json.dumps(node.misc)}"
    return node_label, node