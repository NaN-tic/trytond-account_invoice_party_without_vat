# This file is part of the account_invoice_party_without_vat module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields

__all__ = ['Invoice']


class Invoice:
    __metaclass__ = PoolMeta
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        cls._error_messages.update({
                'party_has_not_vat': ('The party with ID %s has not any VAT'),
                'default_invoicing_party_has_not_address': ('And the default '
                    'invoicing party has not an address.'),
                })

    @fields.depends('party')
    def on_change_party(self):
        AccountConfiguration = Pool().get('account.configuration')

        super(Invoice, self).on_change_party()

        if self.party and not self.party.vat_code:
            # change journal if party has not VAT; not change party
            configuration = AccountConfiguration(1)
            if configuration.default_invoicing_journal:
                self.journal = configuration.default_invoicing_journal

    @classmethod
    def create(cls, vlist):
        Party = Pool().get('party.party')
        for values in vlist:
            if values['type'] == 'out':
                parties = Party.search([('id', '=', values['party'])])
                if not parties:
                    cls.assign_without_vat(values)
                party, = parties
                if not party.vat_code:
                    cls.assign_without_vat(values)
        return super(Invoice, cls).create(vlist)

    @classmethod
    def assign_without_vat(cls, values):
        AccountConfiguration = Pool().get('account.configuration')
        account_configuration = AccountConfiguration(1)
        
        party = account_configuration.default_invoicing_party
        if party:
            values['party'] = party

            invoice_address = party.address_get(type='invoice')
            if not invoice_address:
                cls.raise_user_error('party_has_not_vat',
                    error_args=(values['party'],),
                    error_description='default_invoicing_party_has_not_address')
            values['invoice_address'] = invoice_address

        journal = account_configuration.default_invoicing_journal
        if journal:
            values['journal'] = journal
