from django.db import models

# Create your models here.
class Topic(models.Model):
    # A TOPIC THE USER IS LEARNING ABOUT
    text = models.CharField(max_length=200)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ RETURN A STRING REPRESENTATION OF A MODEL """
        return self.text
    
class Entry(models.Model):
    """ SOMETHING SPECIFIC LEARNED ABOUT A TOPIC """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'entries'

    def __str__(self):
        """ RETURN A SIMPLE STRING REPRESENTING THE ENTRY """
        return f"{self.text[:50]}..."