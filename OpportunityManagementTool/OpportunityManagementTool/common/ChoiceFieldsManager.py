from django.forms import ModelChoiceField



class NameChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return obj


class EmailChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return obj

