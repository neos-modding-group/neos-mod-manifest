#!/bin/python

"""
Does rudimentary JSON diffing between two git versions of the manifest.json file,
and on new mod versions updates the mods.xml RSS feed in the github pages repo.
"""

# pylint: disable=redefined-outer-name,broad-except

import json
import datetime
from os import environ
from typing import Any
from xml.dom import minidom

import util

REF_BASE = util.exec_shell(f"git rev-parse {environ.get('REF_BASE') or 'HEAD^1'}")
REF_NEW = util.exec_shell(f"git rev-parse {environ.get('REF_NEW') or 'HEAD'}")

# The JSON manifests.
OLD_MANIFEST: dict[str, Any] = json.loads(util.exec_shell(f"git show {REF_BASE}:manifest.json"))
NEW_MANIFEST: dict[str, Any] = json.loads(util.exec_shell(f"git show {REF_NEW}:manifest.json"))

MODS = []

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
            MODS.append(mod_to_embed(mod))


if len(MODS) > 0:
    # This is currently dependent on the machine's locale and timezone but that shouldn't matter as this will run in Github actions which are set to English/UTC.
    rssNow = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    with minidom.parse("gh-pages/feed.xml") as rssFeed:
        rssFeed.getElementsByTagName("pubDate").item(0).firstChild.data = rssNow
        rssFeed.getElementsByTagName("lastBuildDate").item(0).firstChild.data = rssNow
        for mod in MODS:
            item = rssFeed.createElement("item")
            title = rssFeed.createElement("title")
            title.appendChild(rssFeed.createTextNode("Released Version " + mod["versions"][0]["id"] + " for '" + mod["name"] + "'"))
            description = rssFeed.createElement("description")
            description.appendChild(rssFeed.createTextNode(mod["description"]))
            category = rssFeed.createElement("category")
            category.appendChild(rssFeed.createTextNode("Games/NeosVR/Mods/" + mod["category"]))
            pubDate = rssFeed.createElement("pubDate")
            pubDate.appendChild(rssFeed.createTextNode(rssNow))
            link = rssFeed.createElement("link")
            link.appendChild(rssFeed.createTextNode(mod["versions"][0]["releaseUrl"]))
            source = rssFeed.createElement("source")
            source.setAttribute("url", "https://www.neosmodloader.com/mods.xml")
            source.appendChild(rssFeed.createTextNode("Neos Mod Releases"))

            item.appendChild(title)
            item.appendChild(description)
            item.appendChild(category)
            item.appendChild(pubDate)
            item.appendChild(source)
            item.appendChild(link)

            rssFeed.getElementsByTagName("channel").item(0).appendChild(item)

        rssWriter = open("gh-pages/feed.xml", "w")
        xmlString = rssFeed.toprettyxml(encoding="utf-8", standalone=True).decode("utf-8")
        xmlString = "\n".join([line for line in xmlString.splitlines() if line.strip()])
        rssWriter.write(xmlString)
        rssWriter.close()
