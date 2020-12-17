# Create your models here
from django.db import models 
from django.contrib.postgres.fields import ArrayField
 

class AllRecipes(models.Model):
    '''
    This model holds hyperlinks (hrefs with anchor text)
    ''' 
    anchortext = models.TextField(max_length=500, null=True, blank=True)
    hyperlink = models.TextField(max_length=500, null=True, blank=True)
    extra = models.TextField(default=0)
    user_search_terms = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    
    class Meta: # this eliminates the extra "s" added to the model name
        verbose_name_plural = "AllRecipes"
        ordering = ['anchortext']    # alphabetical order    
     
    def __str__(self):
        return self.hyperlink

 
class SearchTerms(models.Model):
    '''
    In the search view, the user is inputting a search term or search terms. The search term(s) will be permanently stored
    here in this model, after weeding out dupes
    ''' 
    searchterm= models.TextField(max_length=150, null=True, blank=True)

    class Meta:  # this eliminates the extra "s" added to the model name
        verbose_name_plural = "SearchTerms"
    def _str_(self):
        return self.searchterm
