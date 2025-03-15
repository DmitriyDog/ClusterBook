from django import forms


class ReadArticleForm(forms.Form):
    article_state = forms.BooleanField(label="Статья прочитана:",
                                       initial=False,
                                       required=False,
                                       widget=forms.CheckboxInput(attrs={"class": "big-checkbox"}))
    required_css_class = "boolean-style"
