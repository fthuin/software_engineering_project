from django.core.management.base import BaseCommand
from tennis.models import Participant, Ranking
from django.contrib.auth.models import User
import datetime
import random
from django.db.utils import IntegrityError

RES_FILE = "res.csv"

list_rankings = ["NC"] * 10 # On improve le nombre de non rank
list_rankings += ["C30.5", "C30.4", "C30.3", "C30.2", "C30.1", "C30", "C15.5", "C15.4", "C15.3", "C15.2", "C15.1", "C15", "B+4/6", "B+2/6", "B0"]

class Command(BaseCommand):
    help = 'this method will populate the db with the participants of res.csv'

    def _create_participants(self):
        with open(RES_FILE, "r") as file:
            data_read = file.read()
            data_read = data_read.split("\n")
            data_read.pop()
            for data in data_read:
                items = data.split(",")
                titre = ""
                if items[0] == "Mr":
                    titre = items[0]
                elif items[0] == "Ms":
                    titre = "Mme"
                prenom = items[1]
                nom = items[2]
                telephone = items[3]
                numero = items[4]
                rue = items[5]
                code = items[6]
                ville = items[7]
                datenaissance = datetime.datetime(day=int(items[8]),month=int(items[9]),year=int(items[10]))
                username = items[11]
                mdp = items[12]
                email = items[13]
                latitude = float(items[14])
                longitude = float(items[15])
                classement = Ranking.objects.get(nom=random.choice(list_rankings))
                try:
                    user = User.objects.create_user(username, email, mdp)
                    user.save()
                    participant = Participant(user=user, titre=titre, nom=nom, prenom=prenom, rue=rue, numero=numero, boite="", codepostal=code, localite=ville, telephone="", fax="", gsm=telephone, classement=classement, oldparticipant=random.choice([False, True]), datenaissance=datenaissance, latitude=latitude, isClassementVerified=random.choice([True, False]), longitude=longitude).save()
                except IntegrityError:
                    print("IntegrityError: " +username+ " is already used")

    def handle(self, *args, **options):
        self._create_participants()
