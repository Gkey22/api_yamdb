from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from reviews.models import Title, CustomUser


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


def generate_and_send_confirmation_code_to_email(username):
    user = get_object_or_404(CustomUser, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтвержения для регистрации',
        f'Ваш код для получения токена {confirmation_code}',
        settings.EMAIL_ADMIN,
        [user.email],
        fail_silently=False,
    )
    user.save()
