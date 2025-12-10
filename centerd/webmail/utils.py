import email
import imaplib
from email.header import decode_header
from email.utils import collapse_rfc2231_value
from typing import Dict, List

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


def _decode_filename(part, fallback: str) -> str:
    """Decode filename from attachment part, handling RFC2231 and encoded-words."""
    filename = part.get_filename()
    if filename:
        decoded = _decode_header_value(filename)
        if decoded:
            return decoded

    # Try RFC2231 encoded filename parameters
    cd_param = part.get_param('filename', header='content-disposition')
    if cd_param:
        decoded = collapse_rfc2231_value(cd_param)
        if decoded:
            return decoded

    name_param = part.get_param('name')
    if name_param:
        decoded = _decode_header_value(name_param)
        if decoded:
            return decoded

    return fallback


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
    Fetch messages from configured inbox.
    If limit is None, falls back to WEBMAIL_MAX_MESSAGES.
    If limit is 0 or negative, returns all messages.
    Returns list of dicts with uid, subject, from, date.
    """
    if limit is None:
        limit = settings.WEBMAIL_MAX_MESSAGES
    client = get_imap_client()
    try:
        status, _ = client.select(settings.WEBMAIL_INBOX_FOLDER, readonly=True)
        if status != 'OK':
            raise MailConnectionError("Не удалось открыть папку входящих")

        status, data = client.search(None, 'ALL')
        if status != 'OK':
            raise MailConnectionError("Не удалось получить список писем")

        message_ids = data[0].split()
        recent_ids = message_ids if limit <= 0 else message_ids[-limit:]
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
                'uid': msg_id.decode(),
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


def fetch_message(uid: str) -> Dict[str, str]:
    """Fetch single message by UID/sequence id."""
    client = get_imap_client()
    try:
        status, _ = client.select(settings.WEBMAIL_INBOX_FOLDER, readonly=True)
        if status != 'OK':
            raise MailConnectionError("Не удалось открыть папку входящих")

        status, msg_data = client.fetch(uid, '(RFC822)')
        if status != 'OK' or not msg_data:
            raise MailConnectionError("Не удалось получить письмо")

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = _decode_header_value(msg.get('Subject', 'Без темы'))
        sender = _decode_header_value(msg.get('From', 'Неизвестно'))
        date = msg.get('Date', '')

        body = ""
        attachments = []
        if msg.is_multipart():
            for idx, part in enumerate(msg.walk()):
                content_type = part.get_content_type()
                disposition = part.get_content_disposition()
                filename_candidate = _decode_filename(part, f'attachment-{idx}')
                has_filename = bool(part.get_filename() or part.get_param('filename', header='content-disposition') or part.get_param('name'))

                if disposition == 'attachment' or has_filename:
                    payload = part.get_payload(decode=True) or b""
                    attachments.append({
                        'id': str(idx),
                        'filename': filename_candidate,
                        'content_type': content_type,
                        'size': len(payload),
                    })
                    continue

                if content_type == 'text/plain' and not body:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        body = part.get_payload(decode=True).decode(charset, errors='replace')
                    except Exception:
                        body = part.get_payload(decode=True).decode(errors='replace')
        else:
            charset = msg.get_content_charset() or 'utf-8'
            try:
                body = msg.get_payload(decode=True).decode(charset, errors='replace')
            except Exception:
                body = msg.get_payload(decode=True).decode(errors='replace')

        return {
            'uid': uid,
            'subject': subject,
            'from': sender,
            'date': date,
            'body': body,
            'attachments': attachments,
        }
    finally:
        try:
            client.logout()
        except Exception:
            pass


def fetch_attachment(uid: str, part_id: str) -> Dict[str, bytes]:
    """Fetch attachment payload by UID and part index."""
    client = get_imap_client()
    try:
        status, _ = client.select(settings.WEBMAIL_INBOX_FOLDER, readonly=True)
        if status != 'OK':
            raise MailConnectionError("Не удалось открыть папку входящих")

        status, msg_data = client.fetch(uid, '(RFC822)')
        if status != 'OK' or not msg_data:
            raise MailConnectionError("Не удалось получить письмо")

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        for idx, part in enumerate(msg.walk()):
            if str(idx) != str(part_id):
                continue
            disposition = part.get_content_disposition()
            has_filename = bool(part.get_filename() or part.get_param('filename', header='content-disposition') or part.get_param('name'))
            if disposition != 'attachment' and not has_filename:
                continue
            filename = _decode_filename(part, f'attachment-{idx}')
            payload = part.get_payload(decode=True) or b""
            content_type = part.get_content_type()
            return {
                'filename': filename,
                'content_type': content_type,
                'content': payload,
            }

        raise MailConnectionError("Вложение не найдено")
    finally:
        try:
            client.logout()
        except Exception:
            pass
