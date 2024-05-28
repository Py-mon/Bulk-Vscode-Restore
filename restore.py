import argparse
import datetime
import json
import pathlib

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
parser.add_argument(
    "--no-entries",
    action="store_true",
    help=r"Doesn't show the amount of entries in files.",
)

parser.add_argument(
    "--no-date",
    action="store_true",
    help=r"Doesn't show the date of the last save.",
)

args = parser.parse_args()

history = pathlib.Path(args.history)
restore_from = pathlib.Path(args.restore_from)
restore_to = pathlib.Path(args.restore_to)


def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp) / 1000)


max_entries = 0
all_history_data = []
for file_history_folder in history.glob("*"):
    json_file = file_history_folder / "entries.json"

    if not json_file.exists():
        continue

    data = json.load(open(json_file))
    entries = len(data["entries"])
    if entries > max_entries:
        max_entries = entries

    all_history_data.append((file_history_folder, data))

for file_history_folder, data in all_history_data:
    path = pathlib.Path("C:\\") / pathlib.Path(
        *pathlib.Path(data["resource"]).parts[2:]
    )

    put_in = restore_to.joinpath(*path.parts[1:])

    entries = len(data["entries"])
    if entries / max_entries == 1:
        status = "Modified A Lot"
    elif entries / max_entries >= 0.4:
        status = "Modified Often"
    elif entries / max_entries < 0.4:
        status = "Not Modified Often"
    elif entries / max_entries == 1 / max_entries:
        status = "Copied"

    for parent in path.parents:
        if parent == restore_from:
            break
    else:
        # Not apart of restore_from
        continue

    # Create Parent Folders
    put_in.parent.mkdir(exist_ok=True, parents=True)

    date = datetime.datetime.strftime(
        convert_timestamp(data["entries"][-1]["timestamp"]),
        "%Y-%m-%d %I:%M %p  %B, %d, %A",
    )

    code_path = file_history_folder / data["entries"][-1]["id"]
    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read()

    with put_in.open("w", encoding="utf-8") as f:
        text = code
        if put_in.suffix not in [".json", ".toml"]:
            if not args.no_date:
                text = f"'{date}'\n" + code
            if not args.no_entries:
                text = f"'Entries: {entries}/{max_entries} ({status})'\n\n" + code
        f.write(text)

    print("RESTORED:", path)
