# Submission Tutorial
## Adding a new mod

Create a [new pull request] adding a new mod definition to the [manifest]. An example mod definition is provided below. Note that comments are not allowed in JSON and are only provided here for your reference.

```json
"dev.zkxs.examplemod": { // GUID for your mod. This MUST be unique.
    "name": "Example Mod", // Your mod's name
    "description": "Doesn't do anything", // Short description of your mod's functionality
    "category": "For Mod Developers", // The category that best fits your mod.
    "website": "https://github.com/zkxs/ExampleMod", // your mod's homepage
    "sourceLocation": "https://github.com/zkxs/ExampleMod", // where your source code is hosted
    "authors": { // note that you can have more than one author!
        "runtime": { // author name
            "url": "https://github.com/zkxs" // author's website
        }
    },
    "versions": { // all of your versions go here
        "1.1.0": { // version number
            "releaseUrl": "https://github.com/zkxs/ExampleMod/releases/tag/1.1.0.0", // home page for this version
            "artifacts": [ // note that you can have more than one artifact!
                {
                    "url": "https://github.com/zkxs/ExampleMod/releases/download/1.1.0.0/ExampleMod.dll", // download URL
                    "sha256": "4d7aee0c357c6683bc6d046b1961ed1ce21bbbd23f120b8dc7b1553db01d7174" // sha256 hash of ExampleMod.dll. It is very important that this is correct.
                }
            ]
        }
    }
}
```

Some of these fields are optional, and some rarely-used fields are omitted from this example. Consult the [schema] for more details.

## Choosing a Category

Take a look at the [category list][categories] and check how [other mods][mod list] are categoriezed.

<!-- Links -->
[categories]: categories.md
[manifest]: ../manifest.json
[mod list]: ../README.md#mods
[mod submission guidelines]: mod-guidelines.md
[new pull request]: https://github.com/neos-modding-group/neos-mod-manifest/compare
[schema]: schema.md
