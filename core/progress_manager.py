import json
from pathlib import Path


class ProgressManager:

    def __init__(self):

        self.file = Path(
            "data/progress.json"
        )

        self.file.parent.mkdir(
            exist_ok=True
        )

        if not self.file.exists():

            self.file.write_text(
                "{}",
                encoding="utf-8"
            )

    def load(self):

        return json.loads(
            self.file.read_text(
                encoding="utf-8"
            )
        )

    def save(self, data):

        self.file.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def get_progress(
        self,
        account_id
    ):

        data = self.load()

        return data.get(
            account_id,
            {
                "round": 1,
                "last_note_id": None
            }
        )

    def update_note(
        self,
        account_id,
        note_id
    ):

        data = self.load()

        if account_id not in data:

            data[account_id] = {
                "round": 1,
                "last_note_id": None
            }

        data[account_id][
            "last_note_id"
        ] = note_id

        self.save(data)

    def restart_round(
        self,
        account_id
    ):

        data = self.load()

        current = data.get(
            account_id,
            {
                "round": 1,
                "last_note_id": None
            }
        )

        current["round"] += 1

        current["last_note_id"] = None

        data[account_id] = current

        self.save(data)