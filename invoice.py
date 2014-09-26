# This file is part of the account_invoice_party_without_vat module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['Invoice']
__metaclass__ = PoolMeta


class Invoice:
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        cls._error_messages.update({
                'party_has_not_vat': ('The party with ID %s has not any VAT'),
                'not_default_invoicing_party_configured': ('And the default '
                    'invoicing party is not configured.'),
                'default_invoicing_party_has_not_address': ('And the default '
                    'invoicing party has not any address.'),
                })

    @classmethod
    def create(cls, vlist):
        Party = Pool().get('party.party')
        for values in vlist:
            if values['type'] in ('out_invoice', 'out_credit_note'):
                party, = Party.search([('id', '=', values['party'])])
                if not party.vat_number:
                    cls.assign_default_customer(values)
        return super(Invoice, cls).create(vlist)

    @classmethod
    def assign_default_customer(cls, values):
        AccountConfiguration = Pool().get('account.configuration')
        account_configuration, = AccountConfiguration.search([])
        party = account_configuration.default_invoicing_party
        if not party:
            cls.raise_user_error('party_has_not_vat',
                error_args=(values['party'],),
                error_description='not_default_invoicing_party_configured',)
        invoice_address = party.address_get(type='invoice')
        if not invoice_address:
            cls.raise_user_error('party_has_not_vat',
                error_args=(values['party'],),
                error_description='default_invoicing_party_has_not_address')
        journal = account_configuration.default_invoicing_journal
        values['party'] = party
        values['invoice_address'] = invoice_address
        values['journal'] = journal
