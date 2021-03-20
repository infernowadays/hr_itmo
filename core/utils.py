def handle_serializer_errors(model, errors):
    error_message = "Поля, обязательные для заполенения: "
    empty = True
    for error in errors:
        for field in model._meta.fields:
            if error == field.attname:
                if empty is False:
                    error_message += ", "
                error_message += errors.get(field.attname)[0]
                empty = False
    return error_message
