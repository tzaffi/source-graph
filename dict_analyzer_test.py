import json
from pathlib import Path

from dict_analyzer import analyze_dict, data


def test_analyze_dict():
    with open(Path.cwd() / "fixtures" / "boxes.json") as f:
        d = json.loads(f.read())

    assert data(
        dCount=312, lCount=59, oCount=803, maxLen=45, maxDepth=11
    ) == analyze_dict(d)
