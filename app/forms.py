from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Student

class StudentForm(forms.ModelForm):
    password = forms.CharField(required=True, label="Password")         # Add extra field
    con_password = forms.CharField(required=True, label="CPassword")    # Add extra field

    class Meta:
        model = Student
        fields = '__all__'
        error_messages = {
                        'name': {
                            'required': "Please enter the student's name.",
                            'max_length': "Name is too long."
                        },
                        'email': {
                            'required': "Email is mandatory.",
                            'invalid': "Enter a valid email address."
                        },
                        'contact': {
                            'required': "Please enter the contact detail",
                            'invalid': "Not more then 10 digits"
                        },
                        'image': {
                            'required': "Please upload your recent photo",
                            'invalid': "Not more then 2MB"
                        },
                        'file': {
                            'required': "Please upload your resume",
                            'invalid': "Not more then 2MB"
                        }
                    }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'contact': 'Phone Number',
            'image': 'Profile Picture',
            'file': 'Resume'
        }
        help_texts = {
            'name': 'Enter your full name',
            'email': 'Enter a valid email address',
            'contact': 'Enter 10 digit mobile number',
            'image': 'Upload JPG/PNG (max 2MB)',
            'file': 'Upload PDF/DOC/DOCX (max 20MB)'
        }
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        #     'contact': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'})
        # }

    def clean(self):
        print(super().clean())
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        contact = cleaned_data.get('contact')
        image = cleaned_data.get('image')
        file = cleaned_data.get('file')
  
        if name and not name.replace(" ", "").isalpha():
            self.add_error('name', "Name should only contain letters and spaces.")

        if email and not email.lower().endswith(('@gmail.com', '@yahoo.com')):
            self.add_error('email', "Only gmail and yahoo addresses are allowed.")
        
        if contact and not re.match(r'^\d{10}$', str(contact)):
            self.add_error('contact', "Contact must be a 10-digit number.")
        
        if image:
            if image.size > 2 * 1024 * 1024:
                self.add_error('image', "Image size should not exceed 2MB.")

            elif not image.name.lower().endswith(('.jpeg','.jpg', '.png')):
                self.add_error('image', "Image must be either .jpeg or .png.")

        if file:
            if file.size > 20 * 1024 * 1024:
                self.add_error('image', "Image size should not exceed 20MB.")
                
            elif file and not file.name.lower().endswith(('.pdf', '.doc', '.docx')):
                self.add_error('file', "Only PDF, DOC, and DOCX files are allowed.") 
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance
