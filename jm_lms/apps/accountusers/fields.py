# from django.db import models
# from django.core.exceptions import ObjectDoesNotExist
# import collections

# PhoneNumber = collections.namedtuple('PhoneNumber', ['country','country_code'])


# class EastAfricaPhoneNumber:
# 	countries = ['Kenya','Uganda','Tanzania']
# 	country_codes = '+254 +256 +255'.split()

# 	def __init__(self):
# 		self._phoneNumbers = [PhoneNumber(country, country_code) for country_code in self.country_codes
# 		                                                          for country in self.countries]
# 		self.defaultNumber = '000000000'


#     def __repr__(self):
#     	return self.country_code + self.defaultNumber

	

# class EastAfricaPhoneNumberField(models.Field):
# 	description = "East Africa telephone number fields with respective country prefixes"
# 	__metaclass__ = models.SubfieldBase


# 	def __init__(self, help_text=("East Africa telephone number fields with respective country prefixes"), 
# 		verbose_name='eastafricaphonenumberfield', *args, **kwargs):
# 	    self.name = 'EastAfricaPhoneNumberField'
# 	    self.through = None
# 	    self.help_text = help_text
# 	    self.blank = True
# 	    self.editable = True
# 	    self.creates_tables = False
# 	    self.db_column = None
# 	    self.serialize = False
# 	    self.null = True
# 	    self.creation_counter = models.Field.creation_counter
# 	    models.Field.creation_counter += 1
# 	    super(EastAfricaPhoneNumberField, self).__init__(*args, **kwargs)
        
#         def db_type(self, connection):
#         	return 'varchar(13)'

#         def to_python(self, value):
#         	if value in (None, ''):
#         		return EastAfricaPhoneNumber()
#         	else:
#         		if isinstance(value, EastAfricaPhoneNumber):
#         			return value
#         		else:
#         			args = value.split(',')[3],value.split(',')[3]
#         			if len(args) != 13 and value is not None:
#         				raise ValidationError("Invalid input for an East African Phone number")
#         		    return EastAfricaPhoneNumber(*args)


#         def get_prep_value(self, value):
#         	return ','.join(value.country_code),(value.defaultNumber)


#         def get_internal_type(self):
#         	return 'CharField'


#         def value_to_string(self, obj):
#         	value = self._get_val_from_obj(obj)
#         	return self.get_prep_value(value)
