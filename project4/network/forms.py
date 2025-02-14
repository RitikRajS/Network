from .models import Post
from django.forms import ModelForm
from django import forms

class PostForm(ModelForm):

    class Meta:
        
        model = Post
        fields=["post_content"]
        widgets = {
            "post_content":forms.Textarea(attrs={"placeholder":"Post", "class":"form-control post-field"}),
        }
        labels = {
            "post_content":""
        }

    # Validate the form is not empty

    def clean_content(self):

        posted_content = self.cleaned_data.get("post_content")

        if posted_content is None or posted_content == "":
            raise forms.ValidationError("An empty post cannot be added")
        return posted_content
