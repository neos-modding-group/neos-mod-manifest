#!/bin/python

"""
Generates a markdown file to stdout from the JSON manifest passed in with stdin
"""

# pylint: disable=redefined-outer-name,broad-except

import json
import datetime
import sys
from typing import Any

import util

# A dict of category names -> list of mods in that category.
grouped_mods: dict[str, list[dict[str, Any]]] = {}

# The JSON manifest.
MANIFEST: dict[str, Any] = json.load(sys.stdin)

# Iterate over all the mods
for mod_guid in MANIFEST["mods"]:
    mod: dict[str, Any] = MANIFEST["mods"][mod_guid]

    # Add the GUID to the mod
    mod["guid"] = mod_guid

    # Maps the versions into filtered & validated ones
    mod["versions"] = util.map_mod_versions(mod["versions"], mod_guid)

    # Transfer only mods that should be shown to grouped_mods
    if util.should_show_mod(mod):
        # Sort the mod's versions
        mod["versions"].sort(reverse=True, key=lambda version: version["id"])

        # Get the group for the mods,
        # or create it if it doesn't exist.
        mods_group = grouped_mods.get(mod["category"])
        if mods_group is None:
            mods_group = []

        # Add the mod to the group
        mods_group.append(mod)
        grouped_mods[mod["category"]] = mods_group


# Sort the groups' mods
for group, mods in grouped_mods.items():
    mods.sort(key=lambda mod: mod["name"])

# The markdown output
README = ""

# Add update time to the start of the markdown
now = datetime.datetime.now(tz=datetime.timezone.utc)
README += "Last updated at "
README += f"<time datetime='{now.isoformat()}'>{now.strftime('%d %B %Y, %I:%S')} UTC</time>\n"

# Iterate over the groups in an alphabetical fashion.
for group, mods in sorted(grouped_mods.items()):
    # Add header for the mods group
    README += f"\n## {group}\n"
    for mod in mods:
        # Add header for the mod in question
        README += "\n<!--" + mod["guid"] + "-->\n"
        README += "### "
        README += f"[{mod['name']}]({mod['sourceLocation']})"

        # Append authors to mod header
        if "authors" in mod and len(mod["authors"]) > 0:
            README += " by "
            for author_name, author_data in mod["authors"].items():
                README += f"[{author_name}]({author_data['url']}), "
            # Remove the ", "
            README = README[:-2]

        # Add newline and empty line after each mod header
        README += "\n\n"

        # Add mod description
        README += mod["description"] + "\n\n"

        # Add latest version number
        latest_version = mod["versions"][0]
        if "releaseUrl" in latest_version:
            README += "The latest version is ["
            README += str(latest_version['id'])
            README += "]("
            README += latest_version["releaseUrl"]
            README += ")"
        else:
            README += f"The latest version is {str(latest_version['id'])}"
        if "changelog" in latest_version:
            README += ":\n"
            if latest_version["changelog"].strip().startswith("- "):
                README += "\n"
            README += latest_version["changelog"].strip()
        README += "\n"

# Output markdown to stdout
print(README)
