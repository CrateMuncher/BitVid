from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError


from main.exceptions import ModelSaveException, ValidationException
from main.models import Channel

def create(name,owner):
    """
    Tries to create a channel and returns it, throws ModelSaveException on failure
    """

    channel = Channel(name=name)
    try:
        channel.save()
        channel.members.add(owner) # Channel needs to be saved before we can add a relationshp
        channel.full_clean() # validate
        channel.save()

    except IntegrityError: #
        raise ModelSaveException("Channel with this name already exists")

    except ValidationError, e:
        non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        raise ModelSaveException(non_field_errors)
    