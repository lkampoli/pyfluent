#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class ir_st_absorbtivity(Group):
    """'ir_st_absorbtivity' child."""

    fluent_name = "ir-st-absorbtivity"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of ir_st_absorbtivity
    """
    constant: constant = constant
    """
    constant child of ir_st_absorbtivity
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ir_st_absorbtivity
    """
    field_name: field_name = field_name
    """
    field_name child of ir_st_absorbtivity
    """
    udf: udf = udf
    """
    udf child of ir_st_absorbtivity
    """