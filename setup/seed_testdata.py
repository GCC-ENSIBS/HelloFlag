# -*- coding: utf-8 -*-
"""
    Copyright 2026 Root the Box

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
------------------------------------------------------------------------------

Seeds a playable demo game: game levels, boxes with flags, teams with members,
and a spread of captures so the scoreboard, the box pages and the team pages all
have something to show. Re-running it is a no-op.
"""

import logging

from libs.ConsoleColors import INFO
from models import dbsession
from models.Box import Box
from models.Category import Category
from models.Corporation import Corporation
from models.Flag import Flag
from models.GameLevel import GameLevel
from models.Team import Team
from models.User import User

SEED_PASSWORD = "rootthebox"

# number, name, buyout, reward
LEVELS = [
    (0, "Warm Up", 0, 0),
    (1, "Getting Serious", 500, 250),
    (2, "End Game", 1500, 500),
]

CATEGORIES = ["Web", "Crypto", "Pwn", "Forensics", "OSINT"]

CORPORATIONS = ["Initech", "Umbrella Corp"]

# name, os, corporation, level, category, box value, description, flags
BOXES = [
    (
        "Gibson",
        "linux",
        "Initech",
        0,
        "Web",
        100,
        "An ageing intranet portal nobody has patched since the merger.",
        [
            ("Login Bypass", "rtb{s1mpl3_sql1}", 50),
            ("Hidden Admin Page", "rtb{r0b0ts_txt_le4ks}", 75),
            ("Session Forgery", "rtb{c00k13_m0nst3r}", 125),
        ],
    ),
    (
        "Nebuchadnezzar",
        "linux",
        "Initech",
        0,
        "Crypto",
        100,
        "The build server still signs releases with a key from 2009.",
        [
            ("Weak Key", "rtb{512_b1ts_1s_n0t_en0ugh}", 75),
            ("Padding Oracle", "rtb{cbc_b1t_fl1pp1ng}", 150),
        ],
    ),
    (
        "Wintermute",
        "windows",
        "Initech",
        0,
        "Forensics",
        75,
        "A workstation image pulled after a phishing report.",
        [
            ("Macro Payload", "rtb{vb4_n3v3r_d13s}", 50),
            ("Deleted Journal", "rtb{usn_j0urn4l}", 100),
        ],
    ),
    (
        "Zion Mainframe",
        "linux",
        "Umbrella Corp",
        1,
        "Pwn",
        200,
        "The payroll daemon, written in C, in 1998, by an intern.",
        [
            ("Stack Smash", "rtb{cl4ss1c_0verfl0w}", 150),
            ("ROP Chain", "rtb{r0p_r0p_r0p}", 250),
            ("Kernel Escape", "rtb{r1ng0_st4rr}", 400),
        ],
    ),
    (
        "Ozymandias",
        "linux",
        "Umbrella Corp",
        1,
        "OSINT",
        150,
        "The CTO posts a lot. Probably too much.",
        [
            ("Leaked Commit", "rtb{g1t_h1st0ry_1s_f0r3v3r}", 100),
            ("Exif Trail", "rtb{sm1l3_f0r_th3_g30t4g}", 175),
        ],
    ),
    (
        "Black Mesa",
        "freebsd",
        "Umbrella Corp",
        2,
        "Pwn",
        300,
        "Air-gapped, allegedly. The VPN concentrator disagrees.",
        [
            ("Firmware Backdoor", "rtb{h4rdc0d3d_cr3ds}", 300),
            ("Full Domain Takeover", "rtb{g0ld3n_t1ck3t}", 500),
        ],
    ),
]

# team name, motto, members (handle, display name), flags captured
TEAMS = [
    ("Segfault Sages", "Core dumped, ego intact", ["neo", "trinity", "morpheus"], 10),
    ("Null Pointers", "We go nowhere, fast", ["acid_burn", "zero_cool"], 7),
    (
        "Rubber Ducks",
        "Explain it to me again",
        ["bishop", "ripley", "hicks", "vasquez"],
        5,
    ),
    ("Kernel Panic", "It worked on the staging box", ["cereal", "phantom_phreak"], 3),
    ("Late Joiners", "We read the rules first", ["lord_nikon", "joey"], 1),
]


def seed():
    """Create the demo game, teams and captures, skipping anything that exists"""
    if Team.by_name(TEAMS[0][0]) is not None:
        logging.info("Test data is already present, nothing to seed")
        return
    levels = _seed_levels()
    _seed_categories()
    corporations = _seed_corporations()
    boxes = _seed_boxes(levels, corporations)
    teams = _seed_teams()
    _seed_captures(teams, boxes)
    print(
        INFO
        + "Seeded %d teams, %d boxes and %d flags"
        % (len(teams), len(boxes), sum(len(box.flags) for box in boxes))
    )


def _seed_levels():
    """Create the game levels and chain them together"""
    levels = {}
    for number, name, buyout, reward in LEVELS:
        level = GameLevel.by_number(number)
        if level is None:
            level = GameLevel(number=number, buyout=buyout)
            dbsession.add(level)
        level.name = name
        level.reward = reward
        levels[number] = level
    dbsession.flush()
    ordered = sorted(levels.values(), key=lambda lvl: lvl.number)
    for index, level in enumerate(ordered[:-1]):
        level.next_level_id = ordered[index + 1].id
    dbsession.commit()
    return levels


def _seed_categories():
    """Create the flag categories"""
    existing = Category.list()
    for name in CATEGORIES:
        if name not in existing:
            dbsession.add(Category(_category=name))
    dbsession.commit()


def _seed_corporations():
    """Create the corporations the boxes belong to"""
    corporations = {}
    for name in CORPORATIONS:
        corporation = Corporation.by_name(name)
        if corporation is None:
            corporation = Corporation()
            corporation.name = name
            dbsession.add(corporation)
        corporations[name] = corporation
    dbsession.commit()
    return corporations


def _seed_boxes(levels, corporations):
    """Create the boxes and their flags"""
    boxes = []
    for name, os_name, corp, level, category, value, description, flags in BOXES:
        box = Box.by_name(name)
        if box is None:
            box = Box(
                name=name,
                operating_system=os_name,
                description=description,
                game_level_id=levels[level].id,
                value=value,
                corporation_id=corporations[corp].id,
            )
            box.categories.append(Category.by_category(category))
            dbsession.add(box)
            dbsession.flush()
        _seed_flags(box, flags)
        boxes.append(box)
    dbsession.commit()
    return boxes


def _seed_flags(box, flags):
    """Create the static flags of a single box"""
    for flag_name, token, value in flags:
        if Flag.by_name(flag_name) is not None:
            continue
        flag = Flag.create_flag(
            "static", box, flag_name, token, "Find it and submit it.", value
        )
        dbsession.add(flag)
    dbsession.flush()


def _seed_teams():
    """Create the teams and their members"""
    teams = []
    for name, motto, handles, _ in TEAMS:
        team = Team.by_name(name)
        if team is None:
            team = Team()
            team.name = name
            team.motto = motto
            team.set_score("start", 0)
            team.game_levels.append(GameLevel.by_number(0))
            dbsession.add(team)
        for handle in handles:
            team.members.append(_seed_user(handle))
        teams.append(team)
    dbsession.commit()
    return teams


def _seed_user(handle):
    """Create a single player account"""
    user = User.by_handle(handle)
    if user is None:
        user = User(handle=handle, name=handle, email="%s@rootthebox.com" % handle)
        user.password = SEED_PASSWORD
        dbsession.add(user)
        dbsession.flush()
    return user


def _seed_captures(teams, boxes):
    """Give each team its share of the flags, spread across its members"""
    flags = [flag for box in boxes for flag in box.flags]
    for team, spec in zip(teams, TEAMS):
        members = team.members
        for index, flag in enumerate(flags[: spec[3]]):
            _capture(team, members[index % len(members)], flag)
        dbsession.commit()
    _award_completions(teams, boxes)


def _capture(team, user, flag):
    """Record one capture the same way MissionsHandler.attempt_capture does"""
    if flag in team.flags:
        return
    value = flag.dynamic_value(team)
    team.set_score("flag", value + team.money)
    team.add_flag(flag)
    user.money += value
    user.flags.append(flag)
    dbsession.add(user)
    dbsession.add(team)


def _award_completions(teams, boxes):
    """Pay out the box and level bonuses the captures have earned"""
    for team in teams:
        for box in boxes:
            if box.value > 0 and _is_complete(team, box.flags):
                team.set_score("box", box.value + team.money)
        _unlock_levels(team)
        dbsession.add(team)
    dbsession.commit()


def _unlock_levels(team):
    """Reward every completed level and unlock the one after it"""
    for level in GameLevel.all():
        if not level.flags or not _is_complete(team, level.flags):
            continue
        if level.reward > 0:
            team.set_score("level", level.reward + team.money)
        next_level = GameLevel.by_id(level.next_level_id)
        if next_level and next_level not in team.game_levels:
            team.game_levels.append(next_level)


def _is_complete(team, flags):
    """True when the team holds every flag in the list"""
    return all(flag in team.flags for flag in flags)
