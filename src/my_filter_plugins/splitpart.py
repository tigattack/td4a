from ansible.errors import AnsibleFilterError, AnsibleUndefinedVariable
from ansible.module_utils._text import to_native, to_text
from jinja2.exceptions import UndefinedError


# https://stackoverflow.com/a/30515659
def splitpart(_input_string, split_string=' ', index=0, alias='splitpart'):
    try:
        value = _input_string.split(split_string)[index]
    except UndefinedError as error:
        raise AnsibleUndefinedVariable(
            f"{alias}: Something happened, this was the original exception: " +
            {to_native(error)}
        ) from error
    except Exception as error:
        raise AnsibleFilterError(
            f"{alias}: Something happened, this was the original exception: " +
            {to_native(error)}
        ) from error

    return to_text(value)


class FilterModule():  # pylint: disable=too-few-public-methods
    def filters(self):
        return {
            'splitpart': splitpart
        }
