from django.apps import apps

class DeliberatingAppConfig(AppConfig):
    def ready(self):
        vote_model = apps.get_model("app", "VoteOption")
        secretballot.enable_voting_on(vote_model)