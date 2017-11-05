class Contexts(object):

    def __init__(self):
        self.contexts = {}

    def get_context(self, user_id: str):
        return self.contexts.get(user_id, {})

    def set_context(self, user_id: str, context: dict):
        self.contexts[user_id] = context
