from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    """
    Helps to specify order for various models by providing additional behaviour

        *** Automatically assigns an order value when no specific order is provided
            i.e ****if their are two objects with order 1 and 2 respectively, when saving
                    the third object, it assigns the order 3
                **** Order objects in respect to other fields. modules will be ordered
                    with respect to the course they belong and lessons in respect to the module
                     they belong
    """
    pass
