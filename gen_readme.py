#!/bin/python
import json

grouped_mods = {}

with open("master/manifest.json", "r", encoding = "UTF-8") as f:
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

for group, mods in grouped_mods.items():
    mods = mods.sort(key=lambda mod: mod["name"])

for group, mods in sorted(grouped_mods.items()):
    README += f"\n## {group}\n"
    for mod in mods:
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


with open("gh-pages/index.md", "w", encoding = "UTF-8") as f:
    f.write(README)
