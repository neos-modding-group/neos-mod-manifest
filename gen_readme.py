#!/bin/python

"""
Generates a markdown file to stdout from the JSON manifest passed in with stdin
"""

# pylint: disable=redefined-outer-name,broad-except

import json
import datetime
import sys
from typing import Any
import packaging.version

def should_show_mod(mod: dict[str, Any]) -> bool:
    """
    Checks if mod should be shown.

    Parameters:
    mod: The mod in question
    """

    # Exclude plugins and libraries from being shown
    if "flags" in mod and (
        "plugin" in mod["flags"] or
        "file" in mod["flags"]
    ):
        return False

    # Don't add listings for NSFW mods on the website.
    # NSFW needs to be opt-in to be shown,
    # mod managers can implement that.
    if mod["category"] == "NSFW":
        return False

    # Only show mods with versions
    if mod["versions"] is None or len(mod["versions"]) == 0:
        return False

    # Don't show mods with only vulnerable versions
    only_vulnerable_versions = True
    for version in mod["versions"]:
        if "flags" not in version:
            only_vulnerable_versions = False
        else:
            if not any(flag.startswith("vulnerability:") for flag in version["flags"]):
                only_vulnerable_versions = False

    if only_vulnerable_versions:
        return False

    # Show all mods by default
    return True

# A dict of category names -> list of mods in that category.
grouped_mods: dict[str, list[dict[str, Any]]] = {}

# The JSON manifest.
MANIFEST: dict[str, Any] = json.load(sys.stdin)

# Iterate over all the mods
for mod_guid in MANIFEST["mods"]:
    mod: dict[str, Any] = MANIFEST["mods"][mod_guid]

    # Add the GUID to the mod
    mod["guid"] = mod_guid

    # Turn versions into a list of validated IDs
    versions_list: list[dict[str, Any]] = []
    for version_id in mod["versions"]:
        try:
            mod_version = mod["versions"][version_id]
            mod_version["id"] = packaging.version.parse(version_id)
            versions_list.append(mod_version)
        except Exception as e:
            print(
                f"Failed to process [{mod_guid}/{version_id}], reason: {e}",
                file=sys.stderr
            )
    mod["versions"] = versions_list

    # Transfer only mods that should be shown to grouped_mods
    if should_show_mod(mod):
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
    mods = mods.sort(key=lambda mod: mod["name"])

# The markdown output
README = ""

# Add update time to the start of the markdown
now = datetime.datetime.now(tz=datetime.timezone.utc)
README += "Last updated at "
README += f"<time datetime='{now.isoformat()}'>{now.strftime('%d %B %Y, %I:%S')} UTC</time>\n\n"

# Iterate over the groups in an alphabetical fashion.
for group, mods in sorted(grouped_mods.items()):
    # Add header for the mods group
    README += f"\n## {group}\n"
    for mod in mods:
        # Add header for the mod in question
        README += "\n<!--" + mod["guid"] + "-->\n"
        README += "#### "
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
        README += mod['description'] + "\n"

# Output markdown to stdout
print(README)
