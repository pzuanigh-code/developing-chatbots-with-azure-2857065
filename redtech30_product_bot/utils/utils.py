
class IntentHandler:
    def __init__(self):
        self.recognizer_result = None

    def handle(self, recognizer_result):
        self.recognizer_result = recognizer_result
        intent = self.get_top_intent()
        return getattr(self, intent, self.default_intent)()

    def default_intent(self):
        return "Intent not supported"

    def get_top_intent(self):
        top_intent = self.recognizer_result.get_top_scoring_intent()
        return top_intent.intent

    def get_entities(self):
        """Converts LUIS type entities to consumable mapping

        Input: {'$instance': {'product_categories': [{'startIndex': 17, 'endIndex': 24, 'text': 'android', 'type': 'product_categories'}]}, 'product_categories': [['Mobile']]}
        Output: {'product_categories': ["ssn", "kubernetes"]}
        """
        entities = self.recognizer_result.entities
        entities.pop("$instance", {})
        for key, values in entities.items():
            if isinstance(values, list) and isinstance(values[0], list):
                entities[key] = [v for value in values for v in value]
        return entities