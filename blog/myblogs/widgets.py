from django import forms


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'myblogs/widgets/custom_checkbox.html'
    option_template_name = "myblogs/widgets/custom_checkbox_option.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs["class"] += "custom-checkbox hidden text-white"
        else:
            self.attrs["class"] = "custom-checkbox hidden text-white"
