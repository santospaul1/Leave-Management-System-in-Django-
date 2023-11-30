from django import forms
from myadmin.models import LeaveType, Employee


class LeaveForm(forms.Form):
    fromdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    todate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    leavetype = forms.ChoiceField(choices=[('', 'Select Leave Type')], required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        leave_types = LeaveType.objects.all().values_list('leavetype', 'leavetype')
        self.fields['leavetype'] = forms.ChoiceField(choices=[('', 'Select Leave Type')] + list(leave_types), required=True)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['firstName', 'lastName','gender', 'address', 'city', 'country', 'mobileno']