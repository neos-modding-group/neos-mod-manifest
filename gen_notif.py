#!/bin/python

"""
Does rudimentary JSON diffing between two git versions of the manifest.json file,
and on new mod versions prints a GHA output for a discord webhook message's JSON.
"""

# pylint: disable=redefined-outer-name,broad-except

import json
import datetime
from os import environ
from copy import deepcopy
from typing import Any

import util

REF_BASE = util.exec_shell(f"git rev-parse {environ.get('REF_BASE') or 'HEAD^1'}")
REF_NEW = util.exec_shell(f"git rev-parse {environ.get('REF_NEW') or 'HEAD'}")

# The JSON manifests.
OLD_MANIFEST: dict[str, Any] = json.loads(util.exec_shell(f"git show {REF_BASE}:manifest.json"))
NEW_MANIFEST: dict[str, Any] = json.loads(util.exec_shell(f"git show {REF_NEW}:manifest.json"))

EMBEDS = []

BASE_EMBED: dict[str, Any] = {
    "footer": {
        "icon_url": "https://avatars.githubusercontent.com/u/101987083?s=200&v=4"
    },
    "timestamp": datetime.datetime.utcnow().isoformat(),
    "color": "000000",
    "fields": []
}

def mod_to_embed(mod: dict[str, Any]) -> dict[str, Any]:
    """
    Create discord embed JSON from a mod and it's first release
    """
    embed: dict[str, Any] = deepcopy(BASE_EMBED)

    embed['title'] = "[" + mod['name'] + "/" + str(mod["versions"][0]["id"]) + "]"
    embed['description'] = mod['description']
    embed['footer']['text'] = f"{mod['guid']}"
    if 'color' in mod:
        embed['color'] = int(mod['color'], 16)

    if 'releaseUrl' in mod['versions'][0]:
        embed['url'] = mod['versions'][0]['releaseUrl']

    embed['fields'].append({
        "name": "Category",
        "value": mod['category'],
        "inline": True
    })

    if len(mod['authors']) > 0:
        author_names = iter(mod['authors'])
        first_author_name = next(author_names)
        embed['author'] = {
            "name": first_author_name
        }
        if 'url' in mod['authors'][first_author_name]:
            embed['author']['url'] = mod['authors'][first_author_name]['url']
        if 'iconUrl' in mod['authors'][first_author_name]:
            embed['author']['icon_url'] = mod['authors'][first_author_name]['iconUrl']

        additional_authors: list[str] = []
        for author_name in author_names:
            if 'url' in mod['authors'][author_name]:
                author_link = f"[{author_name}]({mod['authors'][author_name]['url']})"
                additional_authors.append(author_link)
            else:
                additional_authors.append(author_name)
        if len(additional_authors)  > 0:
            embed['fields'].append({
                "name": "Additional authors",
                "value": ", ".join(additional_authors),
                "inline": True
                })

    flags: list[str] = []
    if 'flags' in mod:
        flags.extend(mod['flags'])
    if 'flags' in mod['versions'][0]:
        flags.extend(mod['versions'][0]['flags'])
    if len(flags) > 0:
        embed['fields'].append({
            "name": "Flags",
            "value": "`" + "`, `".join(flags) + "`",
            "inline": True
            })

    if 'tags' in mod:
        embed['fields'].append({
            "name": "Tags",
            "value": ", ".join(mod['tags']),
            "inline": True
        })



    links: list[str] = []
    if 'website' in mod:
        links.append("[Website](" + mod['website'] + ")")
    if 'sourceLocation' in mod:
        links.append("[Source](" + mod['sourceLocation'] + ")")
    if len(links) > 0:
        embed['fields'].append({
          "name": "URL(s)",
          "value": ", ".join(links),
          "inline": True
        })

    if 'conflicts' in mod['versions'][0]:
        conflicts: [str] = []
        for conflict_guid in mod['versions'][0]['conflicts']:
            conflict_version = mod['versions'][0]['conflicts'][conflict_guid]['version']
            conflicts.append(f"`{conflict_guid}`: {conflict_version}")

        if len(conflicts) > 0:
            embed['fields'].append({
                "name": "Conflicts",
                "value": "- " + "\n- ".join(conflicts),
            })

    if 'dependencies' in mod['versions'][0]:
        dependencies: [str] = []
        for dep_guid in mod['versions'][0]['dependencies']:
            dep_version = mod['versions'][0]['dependencies'][dep_guid]['version']
            dependencies.append(f"`{dep_guid}`: {dep_version}")

        if len(dependencies) > 0:
            embed['fields'].append({
                "name": "Dependencies",
                "value": "- " + "\n- ".join(dependencies),
            })

    if 'changelog' in mod['versions'][0]:
        embed['fields'].append({
            "name": "Changelog",
            "value": mod['versions'][0]['changelog'],
        })


    #escape strings
    for Sstr in embed:
        Sstr.replace("\\", "\\\\")
        Sstr.replace("'", "\\'")

    return embed


# Iterate over all the (new) mods
for mod_guid in NEW_MANIFEST["mods"]:
    mod: dict[str, Any] = NEW_MANIFEST["mods"][mod_guid]


    # Maps the versions into filtered & validated ones
    mod["versions"] = util.map_mod_versions(mod["versions"], mod_guid)

    # Transfer only mods that should be shown to grouped_mods
    if util.should_show_mod(mod):
        # Sort the mod's versions
        mod["versions"].sort(reverse=True, key=lambda version: version["id"])
        IS_NEW_MOD = True
        if mod_guid in OLD_MANIFEST["mods"]:
            old_versions = OLD_MANIFEST["mods"][mod_guid]['versions']
            old_versions = util.map_mod_versions(old_versions, mod_guid)
            for version in old_versions:
                if version['id'] == mod["versions"][0]['id']:
                    IS_NEW_MOD = False
                    break

        if IS_NEW_MOD:
            mod["guid"] = mod_guid
            EMBEDS.append(mod_to_embed(mod))


if len(EMBEDS) > 0:
    DISCORD_JSON = {
        "content": None,
        "embeds": EMBEDS,
        "allowed_mentions": { "parse": [] },
        "username": "NMG mod verifications",
        "avatar_url": "https://avatars.githubusercontent.com/u/101987083",
        "attachments": []
    }
    print("::set-output name=JSON::" + json.dumps(DISCORD_JSON))
