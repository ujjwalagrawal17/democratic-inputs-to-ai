from rest_framework import serializers

import keys


class BaseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop(keys.FIELDS, None)
        exclude = kwargs.pop(keys.EXCLUDE, None)
        if fields is not None and exclude is not None:
            serializers.ValidationError(
                "fields and serializers simultaneously not allowed")
        super().__init__(*args, **kwargs)
        if fields:
            for field in set(self.fields.keys()) - set(fields):
                self.fields.pop(field, None)
        if exclude:
            for field in set(exclude):
                self.fields.pop(field, None)

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exc:
            if type(data) == dict:
                custom_error_message = data.pop('error_message', None)
            else:
                custom_error_message = ""
            error_messages = {}
            for field, errors in exc.detail.items():
                field_errors = []
                for error in errors:
                    field_errors.append(str(error))
                error_messages[field] = field_errors
            error_messages['message'] = custom_error_message if custom_error_message else ['Something went wrong']
            raise serializers.ValidationError(error_messages)
