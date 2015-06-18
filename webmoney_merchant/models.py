from datetime import datetime, timedelta
from time import sleep
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models, transaction


class Purse(models.Model):
    purse = models.CharField(_('Purse'), max_length=13, unique=True)
    secret_key = models.CharField(_('Secret key'), max_length=50)

    class Meta:
        verbose_name = _("purse")
        verbose_name_plural = _("purses")

    def __unicode__(self):
        return self.purse


class Invoice(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_("User"))
    created_on = models.DateTimeField(_("Created on"), unique=True, editable=False)
    payment_no = models.PositiveIntegerField(_("Payment on"), unique=True, editable=False)
    payment_info = models.CharField(_("Payment Info"), editable=False, max_length=128)

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    def _is_payed_admin(self):
        try:
            self.payment
        except ObjectDoesNotExist:
            return False
        else:
            return True

    _is_payed_admin.boolean = True
    _is_payed_admin.short_description = _('is payed')
    _is_payed_admin.admin_order_field = _('payment')

    is_payed = property(_is_payed_admin)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        sid = transaction.savepoint()
        if self.pk is None:
            i = 1
            while self.pk is None:

                if i > 10:
                    sleep(0.001)

                if i > 20:
                    # Protection from infinite loop
                    raise IntegrityError('Too many iterations while generating unique Invoice number.')

                try:
                    self.created_on = datetime.utcnow()
                    self.created_on = self.created_on - timedelta(microseconds=self.created_on.microsecond % 100)

                    self.payment_no = (self.created_on.hour * 3600 +
                                       self.created_on.minute * 60 +
                                       self.created_on.second) * 10000 + (self.created_on.microsecond // 100)
                    super(Invoice, self).save(force_insert, force_update)

                except IntegrityError:
                    transaction.savepoint_rollback(sid)

                i += 1
        else:
            super(Invoice, self).save(force_insert, force_update)

        transaction.savepoint_commit(sid)
        transaction.commit()

    def __unicode__(self):
        return _('%(payment_no)s/%(created_on)s (for: %(user)s)') % {'payment_no': self.payment_no,
                                                                     'created_on': self.created_on.date(),
                                                                     'user': self.user}


class Payment(models.Model):
    PAYMENT_MODE_CHOICES = ((0, 'REAL'), (1, 'TEST'))

    created_on = models.DateTimeField(_('Created on'), auto_now_add=True, editable=False)
    invoice = models.OneToOneField(Invoice, blank=True, null=True, related_name='payment', verbose_name=_('Invoice'))
    payee_purse = models.ForeignKey(Purse, related_name='payments', verbose_name=_('Payee purse'))
    amount = models.DecimalField(_('Amount'), decimal_places=2, max_digits=9)
    payment_no = models.PositiveIntegerField(_('Payment no'), unique=True)
    mode = models.PositiveSmallIntegerField(_('Mode'), choices=PAYMENT_MODE_CHOICES)
    sys_invs_no = models.PositiveIntegerField(_('LMI_SYS_INVS_NO'))
    sys_trans_no = models.PositiveIntegerField(_('LMI_SYS_TRANS_NO'))
    sys_trans_date = models.DateTimeField(_('LMI_SYS_TRANS_DATE'))
    payer_purse = models.CharField(_('Payer purse'), max_length=13)
    payer_wm = models.CharField(_('Payer WM'), max_length=12)
    paymer_number = models.CharField(_('Paymer number'), max_length=30, blank=True)
    paymer_email = models.EmailField(_('Paymer email'), blank=True)
    telepat_phonenumber = models.CharField(_('Phone number'), max_length=30, blank=True)
    telepat_orderid = models.CharField(_('Order id'), max_length=30, blank=True)
    payment_creditdays = models.PositiveIntegerField(_('Credit days'), blank=True, null=True)

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")

    def __unicode__(self):
        return _("%(payment_no)s - %(amount)s WM%(payee_purse)s") % {'payment_no': self.payment_no,
                                                                     'amount': self.amount,
                                                                     'payee_purse': self.payee_purse[0]}
