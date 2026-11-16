from typing import Any, Type

from utils.exceptions import ArgumentException


def get_yaml_parameter(yaml: dict[str, Any], parameter_name: str, parameter_type: Type | set[Type]):
    parameter = yaml.get(parameter_name, None)
    if parameter is None:
        raise ArgumentException(f'missing required parameter: {parameter_name}')

    if isinstance(parameter_type, set):
        valid = False
        for p_type in parameter_type:
            if isinstance(parameter, p_type):
                valid = True
                break

        if not valid:
            valid_types: str = ", ".join([x.__name__ for x in parameter_type])
            raise ArgumentException(f'parameter {parameter_name} has invalid type {parameter_type}\n'
                                    f'Must be of type {valid_types}')

        return parameter

    if not isinstance(parameter, parameter_type):
        raise ArgumentException(f'parameter {parameter_name} has invalid value {parameter}. Must be of type {parameter_type.__name__}')

    return parameter
