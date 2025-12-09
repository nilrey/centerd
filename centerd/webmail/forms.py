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
