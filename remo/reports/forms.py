from happyforms import forms

from models import Report, ReportComment, ReportEvent, ReportLink

ReportEventFormset = forms.models.inlineformset_factory(Report,
                                                        ReportEvent)
ReportLinkFormset = forms.models.inlineformset_factory(Report,
                                                       ReportLink)

class ReportForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ReportForm, self).clean()
        if cleaned_data['empty'] == True:
            for text_field in ['recruits_comments', 'past_items',
                          'next_items', 'flags']:
                cleaned_data[text_field] = ''
            cleaned_data['recruits'] = 0
        return cleaned_data

    class Meta:
        model = Report
        exclude = ['user', 'month', 'mentor']
        include = ['empty', 'recruits', 'recruits_comments', 'past_items',
                   'next_items', 'flags']

class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        exclude = ['report', 'user']
        include = ['comment']


class ReportEventForm(forms.ModelForm):
    class Meta:
        model = ReportEvent
        exclude = ['report']
        include = ['name', 'description', 'link', 'participation_type']


class ReportLinkForm(forms.ModelForm):
    class Meta:
        model = ReportLink
        export = ['report']
        include = ['description', 'link']
