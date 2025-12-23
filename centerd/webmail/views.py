import imaplib
import logging
import smtplib
from email.message import EmailMessage
from typing import Iterable
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ComposeEmailForm, MailConnectionForm
from .utils import (
    MailConnectionError,
    fetch_attachment,
    fetch_message,
    fetch_recent_messages,
    mark_message_seen,
)

logger = logging.getLogger(__name__)


def _smtp_send_message(to_email: str, subject: str, body: str, attachments: Iterable) -> None:
    """
    Отправка письма через прямое подключение SMTP (без TLS/SSL),
    по аналогии с client_smtp.py.
    """
    host = getattr(settings, 'EMAIL_HOST', '192.168.56.101')
    port = getattr(settings, 'EMAIL_PORT', 25)
    username = getattr(settings, 'EMAIL_HOST_USER', '')
    password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')

    from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    if not from_addr:
        if '@' in username:
            from_addr = username
        else:
            fallback_host = (getattr(settings, 'ALLOWED_HOSTS', ['192.168.56.101']) or ['192.168.56.101'])[0]
            from_addr = f"{username}@{fallback_host}"

    msg = EmailMessage()
    msg['Subject'] = subject or ''
    msg['From'] = from_addr
    msg['To'] = to_email
    msg.set_content(body or '')

    for f in attachments or []:
        content_type = f.content_type or 'application/octet-stream'
        if '/' in content_type:
            maintype, subtype = content_type.split('/', 1)
        else:
            maintype, subtype = 'application', 'octet-stream'
        msg.add_attachment(
            f.read(),
            maintype=maintype,
            subtype=subtype,
            filename=f.name,
        )

    with smtplib.SMTP(host, port, timeout=15) as smtp:
        smtp.ehlo()
        if username:
            smtp.login(username, password)
        smtp.send_message(msg)


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
        messages_list = fetch_recent_messages(limit=0)
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


def message_detail_view(request, uid: str):
    """Детальный просмотр одного письма."""
    mail = None
    error = None

    try:
        mail = fetch_message(uid)
        mark_message_seen(uid)
        if mail:
            mail['seen'] = True
    except MailConnectionError as exc:
        error = str(exc)
    except Exception:
        error = 'Произошла ошибка при получении письма'

    if error:
        messages.error(request, error)

    context = {
        'mail': mail,
        'error': error,
        'folder': getattr(settings, 'WEBMAIL_INBOX_FOLDER', 'INBOX'),
    }
    return render(request, 'webmail/message_detail.html', context)


def message_attachment_view(request, uid: str, part_id: str):
    """Скачивание вложения письма."""
    try:
        attachment = fetch_attachment(uid, part_id)
    except MailConnectionError as exc:
        messages.error(request, str(exc))
        return render(request, 'webmail/message_detail.html', {'mail': None, 'error': str(exc)})
    except Exception:
        error = 'Произошла ошибка при получении вложения'
        messages.error(request, error)
        return render(request, 'webmail/message_detail.html', {'mail': None, 'error': error})

    response = HttpResponse(attachment['content'], content_type=attachment['content_type'])
    filename = attachment.get('filename') or 'attachment'
    quoted = quote(filename)
    ascii_fallback = filename.encode('ascii', errors='ignore').decode() or 'attachment'
    response['Content-Disposition'] = f"attachment; filename=\"{ascii_fallback}\"; filename*=UTF-8''{quoted}"
    return response


def compose_view(request):
    """Создание и отправка нового письма с несколькими вложениями."""
    form = ComposeEmailForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        print("request.FILES:", request.FILES)
        print("form.errors:", form.errors)
        if not form.is_valid():
            messages.error(request, f'Ошибки формы: {form.errors}')
        else:
            data = form.cleaned_data
            attachments = request.FILES.getlist('attachments')
            try:
                _smtp_send_message(
                    to_email=data['to'],
                    subject=data.get('subject') or '',
                    body=data.get('body') or '',
                    attachments=attachments,
                )
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect('webmail:inbox')
            except Exception as exc:
                logger.exception("Не удалось отправить письмо")
                messages.error(request, f'Не удалось отправить письмо: {exc}')

    return render(request, 'webmail/compose.html', {'form': form})
