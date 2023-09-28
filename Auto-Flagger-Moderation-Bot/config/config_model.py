class SubredditConfig:
    def __init__(self, name, rules=None, keywords=None):
        self.name = name
        self.rules = rules if rules is not None else []
        self.keywords = keywords if keywords is not None else []

    @classmethod
    def from_json(cls, json_data):
        return cls(
            name=json_data.get('name', ''),
            rules=json_data.get('rules', []),
            keywords=json_data.get('keywords', [])
        )

    def to_json(self):
        return {
            'name': self.name,
            'rules': self.rules,
            'keywords': self.keywords
        }