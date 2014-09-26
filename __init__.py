# This file is part of the account_invoice_party_without_vat module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .configuration import *
from .invoice import *

def register():
    Pool.register(
        AccountConfiguration,
        Invoice,
        module='account_invoice_party_without_vat', type_='model')
