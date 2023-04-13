from django.core.exceptions import ValidationError

def file_size_validator(file):
    max_size_kb=50
    if file.size>max_size_kb*1024:
        raise ValidationError('file cannot be larger then 50 kb')
    