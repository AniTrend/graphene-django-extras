# -*- coding: utf-8 -*-
from __future__ import absolute_import

import binascii

import graphene
from graphene.types.datetime import Date, Time, DateTime
from graphene.utils.str_converters import to_camel_case
from graphql.language import ast

try:
    import iso8601
except:
    raise ImportError(
        "iso8601 package is required for DateTime Scalar.\n"
        "You can install it using: pip install iso8601."
    )


def object_type_factory(_type, new_model, new_name=None, new_only_fields=(), new_exclude_fields=(),
                        new_filter_fields=None, new_registry=None, new_skip_registry=False):

    class GenericType(_type):
        class Meta:
            model = new_model
            name = new_name or to_camel_case('{}_Generic_Type'.format(new_model.__name__))
            only_fields = new_only_fields
            exclude_fields = new_exclude_fields
            filter_fields = new_filter_fields
            registry = new_registry
            skip_registry = new_skip_registry
            description = 'Auto generated Type for {} model'.format(new_model._meta.verbose_name)

    return GenericType


def object_list_type_factory(_type, new_model, new_only_fields=(), new_exclude_fields=(), new_results_field_name=None,
                             new_filter_fields=None, new_name=None, new_pagination=None, new_queryset=None):

    class GenericListType(_type):
        class Meta:
            model = new_model
            name = new_name or to_camel_case('{}_List_Type'.format(new_model.__name__))
            only_fields = new_only_fields
            exclude_fields = new_exclude_fields
            filter_fields = new_filter_fields
            results_field_name = new_results_field_name
            pagination = new_pagination
            queryset = new_queryset
            description = 'Auto generated list Type for {} model'.format(new_model._meta.verbose_name)

    return GenericListType


def input_object_type_factory(input_type, new_model, new_input_for, new_name=None, new_only_fields=(),
                              new_exclude_fields=(), new_filter_fields=None,new_nested_fields=False,
                              new_registry=None, new_skip_registry=False):

    class GenericInputType(input_type):
        class Meta:
            model = new_model
            name = new_name or to_camel_case('{}_{}_Generic_Type'.format(new_model.__name__, new_input_for))
            only_fields = new_only_fields
            exclude_fields = new_exclude_fields
            filter_fields = new_filter_fields
            nested_fields = new_nested_fields
            registry = new_registry
            skip_registry = new_skip_registry
            input_for = new_input_for
            description = ' Auto generated InputType for {} model'.format(new_model._meta.verbose_name)

    return GenericInputType


class DjangoListObjectBase(object):
    def __init__(self, results, count, results_field_name='results'):
        self.results = results
        self.count = count
        self.results_field_name = results_field_name

    def to_dict(self):
        return {
            self.results_field_name: [e.to_dict() for e in self.results],
            'count': self.count,
        }


def resolver(attr_name, root, instance, info):
    if attr_name == 'app_label':
        return instance._meta.app_label
    elif attr_name == 'id':
        return instance.id
    elif attr_name == 'model_name':
        return instance._meta.model.__name__


class GenericForeignKeyType(graphene.ObjectType):
    app_label = graphene.String()
    id = graphene.ID()
    model_name = graphene.String()

    class Meta:
        description = ' Auto generated Type for a model\'s GenericForeignKey field '
        default_resolver = resolver


class GenericForeignKeyInputType(graphene.InputObjectType):
    app_label = graphene.Argument(graphene.String, required=True)
    id = graphene.Argument(graphene.ID, required=True)
    model_name = graphene.Argument(graphene.String, required=True)

    class Meta:
        description = ' Auto generated InputType for a model\'s GenericForeignKey field '


# ************************************************ #
# ************** CUSTOM BASE TYPES *************** #
# ************************************************ #
class Binary(graphene.Scalar):
    """
    BinaryArray is used to convert a Django BinaryField to the string form
    """
    @staticmethod
    def binary_to_string(value):
        return binascii.hexlify(value).decode("utf-8")

    serialize = binary_to_string
    parse_value = binary_to_string

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            return cls.binary_to_string(node.value)


class CustomDateFormat(object):

    def __init__(self, date):
        self.date_str = date


class CustomTime(Time):

    @staticmethod
    def serialize(time):
        if isinstance(time, CustomDateFormat):
            return time.date_str

        return super(Date).serialize(time)

class CustomDate(Date):

    @staticmethod
    def serialize(date):
        if isinstance(date, CustomDateFormat):
            return date.date_str

        return super(Date).serialize(date)


class CustomDateTime(DateTime):

    @staticmethod
    def serialize(dt):
        if isinstance(dt, CustomDateFormat):
            return dt.date_str

        return super(DateTime).serialize(dt)
