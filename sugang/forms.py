from django import forms
from sugang.models import accessURL, resultInfo


class URLForm(forms.ModelForm):
    class Meta:
        model = accessURL
        fields = ['testURL'] #accessURL의 testURL 속성을 사용할 예정임.
        