import datetime

from cerberus import Validator
from cerberus.schema import SchemaRegistry


class MalisValidator(Validator):
    def _validate_isvaliddate(self, isvaliddate, field, value):
        """Test if a string is a valid date string of YYYY-MM-DD
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        try:
            if isvaliddate and (value is not None and value != ""):
                datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            if isvaliddate:
                self._error(field, "Must be a valid YYYY-MM-DD date string")


pc_build_schema_registry = SchemaRegistry()

# Trim all white space from string
def trim_white_space(str_item):
    if len(str_item.strip()) > 0 or str_item is not None:
        return str_item.strip()
    return None


strip_str = lambda v: trim_white_space(v)

# importing the other schemas
