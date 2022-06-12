import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ToImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            service, image = data.split(';base64,')
            extention = service.split('/')[-1]
            id_ = uuid.uuid4()
            data = ContentFile(
                base64.b64decode(image), name=id_.urn[9:] + '.' + extention
            )
        return super().to_internal_value(data)
