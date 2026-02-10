import os
from typing import Dict

from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.db import models
from django.utils.encoding import force_str

from .forms import WebFtpFileForm
from .models import WebFtpFile


def _transliterate_ru_to_en(text: str) -> str:
    """
    Простейшая транслитерация русских букв в английские.
    Достаточно для формирования псевдонима по требованиям.
    """
    mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    result = []
    for ch in force_str(text):
        lower = ch.lower()
        if lower in mapping:
            repl = mapping[lower]
            if ch.isupper():
                repl = repl.capitalize()
            result.append(repl)
        else:
            result.append(ch)
    return ''.join(result)


def _build_alias_from_filename(filename: str) -> str:
    # Убираем путь и расширение
    base = os.path.basename(filename)
    name_without_ext, _ext = os.path.splitext(base)
    return _transliterate_ru_to_en(name_without_ext)


def webftp_upload_view(request: HttpRequest) -> HttpResponse:
    """
    Форма загрузки файла на сервер с сохранением метаданных.
    Обязательное поле: файл.
    """
    form = WebFtpFileForm(request.POST or None, request.FILES or None)
    success_message = None
    error_message = None

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)

            f = form.cleaned_data['file']
            instance.original_name = os.path.basename(f.name)
            instance.size = getattr(f, 'size', None)
            instance.content_type = getattr(f, 'content_type', '') or ''
            _name, ext = os.path.splitext(instance.original_name)
            instance.extension = ext.lstrip('.')

            # Правило по псевдониму:
            # если псевдоним пустой, берём имя файла без расширения,
            # при этом русские буквы транслитерируем в английские.
            alias = form.cleaned_data.get('alias') or ''
            if not alias.strip():
                alias = _build_alias_from_filename(instance.original_name)
            else:
                alias = _transliterate_ru_to_en(alias)
            instance.alias = alias

            instance.save()
            success_message = 'Файл успешно загружен.'
            form = WebFtpFileForm()  # Очистить форму
        else:
            error_message = f'Ошибки формы: {form.errors}'

    context: Dict[str, object] = {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
    }
    return render(request, 'webftp/upload.html', context)


def webftp_file_list_view(request: HttpRequest) -> HttpResponse:
    """
    Страница со списком файлов пользователя.
    Файлом считается "мой", если:
      - поле allowed_usernames пустое (доступ для всех), либо
      - в списке логинов (через запятую) присутствует логин текущего пользователя.
    """
    qs = WebFtpFile.objects.all()
    username = None
    if getattr(request, 'user', None) and request.user.is_authenticated:
        username = request.user.username.strip()

    if username:
        # Простая фильтрация по подстроке; при необходимости можно доработать.
        qs = qs.filter(
            models.Q(allowed_usernames__isnull=True) |
            models.Q(allowed_usernames='') |
            models.Q(allowed_usernames__icontains=username)
        )

    files = qs.order_by('-created_at')

    context: Dict[str, object] = {
        'files': files,
    }
    return render(request, 'webftp/file_list.html', context)


def _user_has_access(request: HttpRequest, obj: WebFtpFile) -> bool:
    """
    Простая проверка доступа к файлу на основе allowed_usernames.
    Пустое поле - доступ для всех.
    """
    allowed = (obj.allowed_usernames or '').strip()
    if not allowed:
        return True

    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return False

    username = request.user.username.strip().lower()
    # Разбиваем логины по запятой и сравниваем без пробелов, в нижнем регистре
    allowed_list = [x.strip().lower() for x in allowed.split(',') if x.strip()]
    return username in allowed_list


def webftp_download_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Скачивание файла:
      - по отдельному URL;
      - также используется для ссылок на псевдоним и оригинальное имя.
    """
    obj = get_object_or_404(WebFtpFile, pk=pk)

    if not _user_has_access(request, obj):
        raise Http404("Файл не найден")

    if not obj.file:
        raise Http404("Файл отсутствует на сервере")

    response = FileResponse(obj.file.open('rb'), as_attachment=True)
    # Используем оригинальное имя файла при скачивании
    response['Content-Disposition'] = f'attachment; filename="{obj.original_name}"'
    return response


def webftp_file_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Детальный просмотр информации о файле с возможностью скачать его.
    """
    obj = get_object_or_404(WebFtpFile, pk=pk)
    if not _user_has_access(request, obj):
        raise Http404("Файл не найден")

    context: Dict[str, object] = {
        'file_obj': obj,
    }
    return render(request, 'webftp/file_detail.html', context)


def webftp_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Удаление файла: запись в БД и физический файл на диске.
    Доступно только по POST и только для пользователей, имеющих доступ к файлу.
    """
    obj = get_object_or_404(WebFtpFile, pk=pk)
    if not _user_has_access(request, obj):
        raise Http404("Файл не найден")

    if request.method != 'POST':
        return redirect('webftp:file_list')

    # Сначала удаляем физический файл, затем запись
    if obj.file:
        # Удаление через storage
        storage = obj.file.storage
        name = obj.file.name
        if name and storage.exists(name):
            storage.delete(name)
        # Дополнительная попытка удалить файл по физическому пути, если он существует
        try:
            file_path = obj.file.path
        except (ValueError, AttributeError):
            file_path = None
        if file_path:
            import os
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    # Если не удалось удалить, просто продолжаем удаление записи
                    pass
    obj.delete()
    messages.success(request, 'Файл успешно удалён.')
    return redirect('webftp:file_list')
