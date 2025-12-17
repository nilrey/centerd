from django import forms


class MailConnectionForm(forms.Form):
    host = forms.CharField(
        label='IMAP сервер',
        max_length=255,
        help_text='Например: 192.168.56.101 или imap.example.com',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    port = forms.IntegerField(
        label='Порт',
        min_value=1,
        max_value=65535,
        help_text='Обычно 143 (IMAP) или 993 (IMAP SSL)',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    use_ssl = forms.BooleanField(
        label='Использовать SSL',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    username = forms.CharField(
        label='Пользователь',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
    )
    folder = forms.CharField(
        label='Папка',
        max_length=64,
        initial='INBOX',
        help_text='Например: INBOX, Sent, Spam',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )


class MultipleFileInput(forms.ClearableFileInput):
    """Allow selecting multiple files in Django 3.x."""
    allow_multiple_selected = True


class ComposeEmailForm(forms.Form):
    to = forms.EmailField(
        label='Кому',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@example.com'}),
    )
    subject = forms.CharField(
        label='Тема',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема письма'}),
    )
    body = forms.CharField(
        label='Сообщение',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Текст письма'}),
    )
    attachments = forms.FileField(
        label='Вложения',
        required=False,
        widget=MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}),
        help_text='Можно выбрать несколько файлов',
    )