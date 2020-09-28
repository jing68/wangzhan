from django import forms

class calculatorForm(forms.Form):
	x= forms.IntegerField()
	y= forms.IntegerField()

	def clean_y(self):
		y=self.cleaned_data['y']
		if y == 0:
			raise forms.ValidationError("Cannot divide by zero")
		return y