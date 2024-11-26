import pytest
import json
from urllib.request import urlopen
import csv


@pytest.fixture
def family_metadata():
    data = json.loads(
        urlopen("https://fonts.google.com/metadata/fonts").read().decode("utf-8")
    )
    return data["familyMetadataList"]


@pytest.fixture
def family_tags():
    csv_data = (
        urlopen(
            "https://raw.githubusercontent.com/google/fonts/main/tags/all/families.csv"
        )
        .read()
        .decode("utf-8")
    )
    reader = csv.reader(csv_data.splitlines())
    res = []
    for row in reader:
        res.append([row[0], row[1], float(row[2])])
    return res


def test_families_missing_tags(family_tags, family_metadata):
    tagged_families = set(f[0] for f in family_tags)
    families_in_gf = set(f["family"] for f in family_metadata)
    families_missing_tags = sorted(families_in_gf - tagged_families)
    missing_list = "\n".join(families_missing_tags)

    assert len(families_missing_tags) == 0, (
        f"The following {len(families_missing_tags)} families are missing tags:\n\n"
        f"{missing_list}\n\n"
        "Please add tags for these families using the following webapp: "
        "https://google.github.io/fonts/tags.html"
    )


def test_no_duplicate_families(family_tags):
    import pdb; pdb.set_trace()
    seen = set()
    dups = []
    for family, cat, _ in family_tags:
        key = (family, cat)
        if key in seen:
            dups.append(",".join(key))
        seen.add(key)
    assert not dups, f"Duplicate tags found: {dups}"