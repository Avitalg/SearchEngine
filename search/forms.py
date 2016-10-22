from django.forms import ModelForm
from .models import Article

# Create the form class.
class ArticleForm(ModelForm):
     class Meta:
         model = Article
         fields = ['file']

# Creating a form to add an article.
form = ArticleForm()

# Creating a form to change an existing article.
article = Article.objects.get(pk=1)
form = ArticleForm(instance=article)