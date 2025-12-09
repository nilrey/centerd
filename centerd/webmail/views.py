import imaplib

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

from .forms import MailConnectionForm
from .utils import fetch_recent_messages, MailConnectionError


def mail_connect_view(request):
    """Страница проверки подключения к IMAP-серверу с заданными параметрами."""
    initial = {
        'host': getattr(settings, 'WEBMAIL_IMAP_HOST', '192.168.56.101'),
        'port': getattr(settings, 'WEBMAIL_IMAP_PORT', 143),
        'use_ssl': getattr(settings, 'WEBMAIL_IMAP_USE_SSL', False),
        'username': getattr(settings, 'WEBMAIL_IMAP_USERNAME', 'test'),
        'password': getattr(settings, 'WEBMAIL_IMAP_PASSWORD', '12345678'),
        'folder': getattr(settings, 'WEBMAIL_INBOX_FOLDER', 'INBOX'),
    }

    form = MailConnectionForm(request.POST or None, initial=initial)
    result = None

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        host, port = data['host'], data['port']
        username, password = data['username'], data['password']
        folder = data['folder']
        use_ssl = data['use_ssl']
        client = None

        try:
            client = imaplib.IMAP4_SSL(host, port) if use_ssl else imaplib.IMAP4(host, port)
            status, _ = client.login(username, password)
            if status != 'OK':
                raise MailConnectionError("Ошибка аутентификации на почтовом сервере")

            status, mailbox_info = client.select(folder, readonly=True)
            if status != 'OK':
                raise MailConnectionError(f"Не удалось открыть папку {folder}")

            # mailbox_info: [b'10'] -> количество писем в папке
            try:
                messages_count = int(mailbox_info[0])
            except Exception:
                messages_count = None

            result = {
                'host': host,
                'port': port,
                'folder': folder,
                'messages_count': messages_count,
                'use_ssl': use_ssl,
            }
            messages.success(request, "Подключение успешно выполнено.")
        except MailConnectionError as exc:
            messages.error(request, str(exc))
        except imaplib.IMAP4.error as exc:
            messages.error(request, f"Ошибка IMAP: {exc}")
        except OSError:
            messages.error(request, f"Не удалось подключиться к {host}:{port}")
        except Exception:
            messages.error(request, "Произошла ошибка при попытке подключения")
        finally:
            if client is not None:
                try:
                    client.logout()
                except Exception:
                    pass

    context = {
        'form': form,
        'result': result,
    }
    return render(request, 'webmail/connect.html', context)


def inbox_view(request):
    """Отображение последних писем из почтового ящика, указанного в конфиге."""
    messages_list = []
    error = None

    try:
        messages_list = fetch_recent_messages()
    except MailConnectionError as exc:
        error = str(exc)
    except Exception:
        error = 'Произошла ошибка при получении писем'

    if error:
        messages.error(request, error)

    context = {
        'messages_list': messages_list,
        'error': error,
        'folder': getattr(settings, 'WEBMAIL_INBOX_FOLDER', 'INBOX'),
    }
    return render(request, 'webmail/inbox.html', context)
