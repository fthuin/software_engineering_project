class ClassName (models.Model) :
    #Variables
    
    #Methodes
    def __str__(self):

    def __unicode__(self):

class infoTournoi(models.Model):
    prix = models.DecimalField(max_digits=11, decimal_places=2, 
        verbose_name="Prix de l'inscription")
    date = models.DateTimeField(verbose_name="Date du tournoi")
    edition = models.IntegerField(primary_key=True)
    addr = models.TextField(verbose_name="Adresse du QG")
    latitude = models.DecimalField(
        max_digits=19, decimal_places=10, default="50.8539751", 
        blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(
        max_digits=19, decimal_places=10, default="4.398054", 
        blank=True, verbose_name="Longitude")
    resultats = models.ManyToManyField(Resultat)

    def __str__(self):
        return "Edition " + str(self.edition)

    def __unicode__(self):
        return u'' + "Edition " + repr(self.edition)