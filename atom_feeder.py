#!/bin/python

"""
Does rudimentary JSON diffing between two git versions of the manifest.json file,
and on new mod versions updates the feed.xml Atom feed in the github pages repo.
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
    atomNow = datetime.datetime.now(datetime.timezone.utc).isoformat()

    with minidom.parse("gh-pages/feed.xml") as atomFeed:
        atomFeed.getElementsByTagName("updated").item(0).firstChild.data = atomNow
        for mod in MODS:
            entry = atomFeed.createElement("entry")

            title = atomFeed.createElement("title")
            title.appendChild(atomFeed.createTextNode("Released Version " + mod["versions"][0]["id"] + " for '" + mod["name"] + "'"))
            entry.appendChild(title)

            content = atomFeed.createElement("content")
            content.appendChild(atomFeed.createTextNode(mod["description"]))
            entry.appendChild(content)

            for modAuthor in mod["authors"]:
                author = atomFeed.createElement("author")
                authorName = atomFeed.createElement("name")
                authorName.appendChild(atomFeed.createTextNode(modAuthor))
                author.appendChild(authorName)
                authorUri = atomFeed.createElement("uri")
                authorUri.appendChild(atomFeed.createTextNode(mod["authors"][modAuthor]["url"]))
                author.appendChild(authorUri)
                entry.appendChild(author)

            contributor = atomFeed.createElement("contributor")
            contributorName = atomFeed.createElement("name")
            contributorName.appendChild(atomFeed.createTextNode(environ.get("GITHUB_ACTOR")))
            contributor.appendChild(contributorName)
            entry.appendChild(contributor)

            category = atomFeed.createElement("category")
            category.setAttribute("term", "Games/NeosVR/Mods/" + mod["category"])
            category.setAttribute("label", "NeosVR Mods")
            entry.appendChild(category)

            published = atomFeed.createElement("published")
            published.appendChild(atomFeed.createTextNode(atomNow))
            entry.appendChild(published)

            updated = atomFeed.createElement("updated")
            updated.appendChild(atomFeed.createTextNode(atomNow))
            entry.appendChild(updated)

            atomFeed.getElementsByTagName("channel").item(0).appendChild(item)

        atomWriter = open("gh-pages/feed.xml", "w")
        xmlString = atomFeed.toprettyxml(encoding="utf-8", standalone=True).decode("utf-8")
        xmlString = "\n".join([line for line in xmlString.splitlines() if line.strip()])
        atomWriter.write(xmlString)
        atomWriter.close()