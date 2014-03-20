from django import forms
from django.forms.util import ErrorList

class BlogPostForm(forms.Form):

    # Lets support a passed in instance!
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        if instance is not None:
            # Disgusting hijack of the inital values variable to populate
            # the fields for an editing form. This is a bit ugly, and I
            # should feel bad. But this makes our Form behave like a
            # ModelForm. Quack quack.
            initial = instance.__dict__['_entity']
        super(forms.Form, self).__init__(data, files, auto_id, prefix, initial,
                                   error_class, label_suffix, empty_permitted)


    title = forms.CharField(max_length = 100, required = True)
    content = forms.CharField(widget = forms.Textarea, required = True)
    
