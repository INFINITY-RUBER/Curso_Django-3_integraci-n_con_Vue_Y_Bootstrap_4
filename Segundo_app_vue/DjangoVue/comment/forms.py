from  django.forms import ModelForm, Textarea

from .models import Comment, TypeContact


class CommentForm(ModelForm):
    
    class Meta:        
        model = Comment
        fields = ('text',)
        widgets = {
            'text' : Textarea(attrs={'class':'form-input'})
        }
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class':'form-input'})
        '''

    def save(self, commit=True, text=""):
        instance = super(CommentForm, self).save(commit=commit)

        if (text == ""):
            instance.text= text #"No podras modificar"

        if (commit):
            instance.save()
            
        return instance


from django import forms
from django.core.validators import MinLengthValidator,EmailValidator


class ContactForm(forms.Form):
    SEX = (
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
        ('O', 'OTRO')
    )
    # name = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}) ,label='Nombre', max_length=10, min_length=2)
    # name = forms.CharField(label='Nombre', validators=[MinLengthValidator(2, message='Muy corto')])
    # email = forms.CharField(label='Correo', validators=[EmailValidator(message='Correo no valido', whitelist=['gmail'])])
    # document = forms.ImageField(label='Documento')
    name = forms.CharField(label='Nombre', initial='Ruber', required=True, disabled=False, max_length=10, min_length=2)
    surname = forms.CharField(label='Apellido',required=False, max_length=10, min_length=3)
    phone = forms.RegexField(label='Telefono',initial='(310)322-1028',regex= '\(\w{3}\)\w{3}-\w{4}', max_length=13, min_length=13)
    date_birth = forms.DateField(label='Fecha de Nacimiento', initial='2020-11-11')
    email = forms.EmailField(label='Correo', initial='Ruber@gmail.com')
    # type_contact = forms.ChoiceField(label='Documento', choices=CHOICE, initial=2)
    type_contact = forms.ModelChoiceField(label='Tipo de Contacto', queryset=TypeContact.objects.all(), initial=3)
    sex = forms.ChoiceField(label='Sexo', choices=SEX)
    document = forms.FileField(label='Documento', required=False)
    tems = forms.BooleanField(label='Condiciones de servicio')

 
        
