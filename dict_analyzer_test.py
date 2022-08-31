import json
from pathlib import Path
import yaml

from dict_analyzer import analyze_dict, data, export


def test_analyze_dict():
    with open(Path.cwd() / "fixtures" / "boxes.json") as f:
        d = json.loads(f.read())

    assert data(
        dCount=312, lCount=59, oCount=803, maxLen=45, maxDepth=11
    ) == analyze_dict(d)


def test_export():
    boxes = Path.cwd() / "fixtures" / "boxes.json"
    summary = boxes.parent / f"_{boxes.stem}.yml"
    export(boxes, summary)

    expected_summary = Path.cwd() / "fixtures" / "boxes.yml"
    summary
    with open(expected_summary) as f:
        e_summary = yaml.safe_load(f.read())

    with open(summary) as f:
        a_summary = yaml.safe_load(f.read())

    assert e_summary == a_summary
