from django import forms

from .models import Site, SiteHistory

from utils.tools import MixinForm


class SiteForm(forms.ModelForm, MixinForm):
    class Meta:
        model = Site
        exclude = ['add_time', 'need_verification']
        error_messages = {
            'name': {
                'required': '请输入站点名称',
            },
            'href': {
                'required': '请输入网址',
            }
        }