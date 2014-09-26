# This file is part of account_invoice_party_without_vat module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Bool, Eval

__all__ = ['AccountConfiguration']
__metaclass__ = PoolMeta


class AccountConfiguration:
    __name__ = 'account.configuration'
    default_invoicing_party = fields.Property(fields.Many2One(
            'party.party', 'Default Invoicing Party',
            help='The default party to set in invoices when the selected one '
                'has not any VAT.'))
    default_invoicing_journal = fields.Property(fields.Many2One(
            'account.journal', 'Default Invoicing Journal',
            help='The default journal to set in invoices when the party '
                'selected one has not any VAT.',
            states={
                'required': Bool(Eval('default_invoicing_party', False)),
                }))
