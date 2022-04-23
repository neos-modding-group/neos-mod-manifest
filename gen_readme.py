#!/bin/python
import json
import datetime

grouped_mods = {}

with open("manifest.json", "r", encoding = "UTF-8") as f:
    MANIFEST = json.load(f)
    for mod_guid in MANIFEST["mods"]:
        mod = MANIFEST["mods"][mod_guid]
        mod["guid"] = mod_guid

        if "flags" not in mod or (
            "plugin" not in mod["flags"] and
            "file" not in mod["flags"]
        ):
            mods = grouped_mods.get(mod["category"])
            if mods is None:
                mods = []

            mods.append(mod)
            grouped_mods[mod["category"]] = mods

README = None
with open("gh-pages/.templates/mod-list-template.md", "r", encoding = "UTF-8") as f:
    README = f.read()

now = datetime.datetime.now(tz=datetime.timezone.utc)
README += "Last updated at "
README += f"<time datetime='{now.isoformat()}'>{now.strftime('%d %B %Y, %I:%S')} UTC</time>\n\n"

for group, mods in grouped_mods.items():
    mods = mods.sort(key=lambda mod: mod["name"])


def should_show_mod(mod):
    """
    Checks if mod should be shown.

    Parameters:
    mod: The mod in question
    """

    # Only show mods with versions
    if mod["versions"] is None or len(mod["versions"]) == 0:
        return False

    # Don't show mods with only vulnerable versions
    for version in mod["versions"].values():
        if "flags" in version:
            for flag in version["flags"]:
                if flag.startswith("vulnerability:"):
                    return False

    # Show all mods by default
    return True

for group, mods in sorted(grouped_mods.items()):
    README += f"\n## {group}\n"
    for mod in mods:
        if not should_show_mod(mod):
            continue
        README += "\n<!--" + mod["guid"] + "-->\n"
        README += "#### "
        README += f"[{mod['name']}]({mod['sourceLocation']})"


        if len(mod["authors"]) > 0:
            README += " by "
            for author_name, author_data in mod["authors"].items():
                README += f"[{author_name}]({author_data['url']}), "
            # Remove the ", "
            README = README[:-2]

        README += "\n\n"

        README += mod['description'] + "\n"


with open("gh-pages/mods.md", "w", encoding = "UTF-8") as f:
    f.write(README)
