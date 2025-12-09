import imaplib
import email
from email.header import decode_header
from typing import List, Dict

from django.conf import settings


class MailConnectionError(Exception):
    """Raised when connection to mail server fails."""


def _decode_header_value(raw_value: str) -> str:
    """Decode MIME encoded header parts to readable string."""
    if not raw_value:
        return ''
    decoded_parts = decode_header(raw_value)
    decoded_strings = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            decoded_strings.append(part.decode(charset or 'utf-8', errors='replace'))
        else:
            decoded_strings.append(part)
    return ''.join(decoded_strings)


def get_imap_client() -> imaplib.IMAP4:
    """
    Create an IMAP client using configuration from settings.
    Returns an authenticated IMAP4/IMAP4_SSL instance.
    """
    host = settings.WEBMAIL_IMAP_HOST
    port = settings.WEBMAIL_IMAP_PORT

    try:
        if settings.WEBMAIL_IMAP_USE_SSL:
            client = imaplib.IMAP4_SSL(host, port)
        else:
            client = imaplib.IMAP4(host, port)
    except OSError as exc:
        raise MailConnectionError(f"Не удалось подключиться к {host}:{port}") from exc

    try:
        client.login(settings.WEBMAIL_IMAP_USERNAME, settings.WEBMAIL_IMAP_PASSWORD)
    except imaplib.IMAP4.error as exc:
        client.logout()
        raise MailConnectionError("Ошибка аутентификации на почтовом сервере") from exc

    return client


def fetch_recent_messages(limit: int = None) -> List[Dict[str, str]]:
    """
    Fetch recent messages from configured inbox.
    Returns list of dicts with subject, from, date.
    """
    limit = limit or settings.WEBMAIL_MAX_MESSAGES
    client = get_imap_client()
    try:
        status, _ = client.select(settings.WEBMAIL_INBOX_FOLDER, readonly=True)
        if status != 'OK':
            raise MailConnectionError("Не удалось открыть папку входящих")

        status, data = client.search(None, 'ALL')
        if status != 'OK':
            raise MailConnectionError("Не удалось получить список писем")

        message_ids = data[0].split()
        recent_ids = message_ids[-limit:]
        messages = []

        for msg_id in reversed(recent_ids):
            status, msg_data = client.fetch(msg_id, '(RFC822)')
            if status != 'OK' or not msg_data:
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = _decode_header_value(msg.get('Subject', 'Без темы'))
            sender = _decode_header_value(msg.get('From', 'Неизвестно'))
            date = msg.get('Date', '')

            messages.append({
                'subject': subject,
                'from': sender,
                'date': date,
            })

        return messages
    finally:
        try:
            client.logout()
        except Exception:
            pass
