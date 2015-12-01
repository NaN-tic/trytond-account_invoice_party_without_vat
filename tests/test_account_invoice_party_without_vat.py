# This file is part of the account_invoice_party_without_vat module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoicePartyWithoutVatTestCase(ModuleTestCase):
    'Test Account Invoice Party Without Vat module'
    module = 'account_invoice_party_without_vat'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoicePartyWithoutVatTestCase))
    return suite