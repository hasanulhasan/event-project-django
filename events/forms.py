# forms.py
from django import forms
from events.models import Event

# forms.py

class StyledFormMixin:
    """
    Add Tailwind CSS classes to form fields for consistent styling.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = field.widget

            base_classes = "w-full block rounded-md shadow-sm border-gray-300 focus:ring focus:ring-indigo-200 text-sm"
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = "rounded border-gray-300 text-indigo-600 shadow-sm focus:ring-indigo-500"
            elif isinstance(widget, forms.RadioSelect):
                widget.attrs['class'] = "text-indigo-600 focus:ring-indigo-500"
            elif isinstance(widget, (forms.CheckboxSelectMultiple, forms.SelectMultiple)):
                widget.attrs['class'] = "w-full rounded border-gray-300 text-sm shadow-sm focus:ring focus:ring-indigo-200"
            else:
                widget.attrs['class'] = widget.attrs.get('class', '') + f" {base_classes}"


class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'location', 'category', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'participants': forms.CheckboxSelectMultiple(),
        }
