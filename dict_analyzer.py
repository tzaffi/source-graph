from dataclasses import dataclass
import json
from pathlib import Path
import yaml


@dataclass
class data:
    dCount: int = 0
    lCount: int = 0
    oCount: int = 0
    maxLen: int = 0
    maxDepth: int = 0

    def __iadd__(self, o: "data") -> None:
        self.dCount += o.dCount
        self.lCount += o.lCount
        self.oCount += o.oCount
        self.maxLen = max(self.maxLen, o.maxLen)
        self.maxDepth = max(self.maxDepth, o.maxDepth)
        return self


def analyze_dict(d: dict, depth: int = 0) -> data:
    stats = data(dCount=1, maxLen=len(d), maxDepth=depth)
    for k, v in d.items():
        match v:
            case dict():
                stats += analyze_dict(v, depth=depth + 1)
            case list():
                stats += analyze_list(v, depth=depth + 1)
            case _:
                stats += analyze_other(v, depth=depth + 1)
    return stats


def analyze_list(a: list, depth: int = 0) -> data:
    stats = data(lCount=1, maxLen=len(a), maxDepth=depth)
    for elt in a:
        match elt:
            case dict():
                stats += analyze_dict(elt, depth=depth + 1)
            case list():
                stats += analyze_list(elt, depth=depth + 1)
            case _:
                stats += analyze_other(elt, depth=depth + 1)
    return stats


def analyze_other(o: object, depth: int = 0) -> data:
    return data(oCount=1, maxDepth=depth)


def export(import_path: Path, export_path: Path = None):
    stem = import_path.stem
    with open(import_path) as f:
        d = json.loads(f.read())

    summary = analyze_dict(d)
    ysummary = {
        stem: {
            "source": import_path.name,
            "dicts": summary.dCount,
            "lists": summary.lCount,
            "objects": summary.oCount,
            "maxLength": summary.maxLen,
            "depth": summary.maxDepth,
        }
    }

    if not export_path:
        export_path = import_path.parent / stem / "yml"

    with open(export_path, "w") as f:
        yaml.dump(ysummary, f, sort_keys=False)
