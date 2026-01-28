from django import forms

from .models import WebFtpFile


class WebFtpFileForm(forms.ModelForm):
    class Meta:
        model = WebFtpFile
        fields = ['file', 'alias', 'description', 'allowed_usernames']
        labels = {
            'file': 'Добавить файл',
            'alias': 'Псевдоним файла',
            'description': 'Описание файла',
            'allowed_usernames': 'Пользователи с доступом (логины через запятую)',
        }

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if not f:
            raise forms.ValidationError('Не выбран файл для загрузки.')
        return f


