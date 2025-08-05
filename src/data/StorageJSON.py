import json


class StorageJSON:
    @staticmethod
    def save_data(path, disciplines):
        data = []
        for discipline in disciplines:
            data.append({
                "name": discipline.name,
                "assessments": discipline.points,
                "max_points": discipline.max_points
            })

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_data(path):
        try:
            with open(path, "r") as f:
                disciplines = json.load(f)
            return disciplines
        except FileNotFoundError:
            return []
