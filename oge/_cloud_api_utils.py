import six


def encode_number_as_cloud_value(number):
    # Numeric values in constantValue-style nodes end up stored in doubles. If the
    # input is an integer that loses precision as a double, use the int64 slot
    # ("integerValue") in ValueNode.
    if (isinstance(number, six.integer_types) and float(number) != number):
        return {'integerValue': str(number)}
    else:
        return {'constantValue': number}
