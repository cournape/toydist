from attr import attr, attributes
from yaml import safe_load


@attributes
class PackageDescription(object):
    name = attr()
    version = attr()
    summary = attr()
    description = attr()

    classifiers = attr()

    packages = attr()

    @classmethod
    def from_yaml(cls, filename):
        with open(filename, "rt") as fp:
            data = safe_load(fp)

        name = data["Name"]
        version = data["Version"]

        summary = data.get("Summary", u"")
        description = data.get("Description", u"")

        classifiers = data.get("Classifiers", [])

        packages = data.get("Packages", [])

        return cls(name, version, summary, description, classifiers, packages)
