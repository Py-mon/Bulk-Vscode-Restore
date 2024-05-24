import pathlib
import json
import argparse

parser = argparse.ArgumentParser(description="Easily bulk restore files in vscode.")

parser.add_argument(
    "restore_from",
    type=str,
    help=r"The folder that gets restored.",
)
parser.add_argument(
    "history",
    type=str,
    help=r"The vscode folder where local history is stored. Changes depending on OS but for windows usually C:\Users\{USER_NAME}\AppData\Roaming\Code\User\History",
)
parser.add_argument(
    "restore_to",
    type=str,
    help=r"Where folder gets restored.",
)
args = parser.parse_args()

history = pathlib.Path(args.history)
restore_from = pathlib.Path(args.restore_from)
restore_to = pathlib.Path(args.restore_to)

for file_saves in history.glob("*"):
    json_file = file_saves / "entries.json"

    if not json_file.exists():
        continue

    data = json.load(open(json_file))
    path = pathlib.Path("C:\\") / pathlib.Path(
        *pathlib.Path(data["resource"]).parts[2:]
    )

    for parent in path.parents:
        if parent != restore_from:
            continue

        put_in = restore_to.joinpath(*path.parts[1:])

        put_in.parent.mkdir(exist_ok=True, parents=True)

        code_path = file_saves / data["entries"][-1]["id"]
        with open(code_path, "r", encoding="utf-8") as f:
            print(path)
            code = f.read()

        with put_in.open("w", encoding="utf-8") as f:
            f.write(code)
