import random
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models, transaction


class Purse(models.Model):

    # https://wiki.webmoney_merchant.ru/projects/webmoney_merchant/wiki/titulnye_znaki
    PURSE_TYPE_CHOICES = [(i, 'WM%s' % i) for i in ('B', 'C', 'D', 'E', 'G', 'K', 'R', 'U', 'X', 'Y', 'Z')]

    purse = models.CharField(_('Purse'), max_length=13, unique=True)
    purse_type = models.CharField(_('Purse type'), max_length=1, unique=True, default=PURSE_TYPE_CHOICES[0][0],
                                  choices=PURSE_TYPE_CHOICES)
    secret_key = models.CharField(_('Secret key'), max_length=50)

    class Meta:
        verbose_name = _("purse")
        verbose_name_plural = _("purses")

    @classmethod
    def get_purse_type_for_type(cls, purse):
        try:
            return cls.objects.filter(purse_type=purse.upper()).get().purse
        except ObjectDoesNotExist:
            return None

    def __unicode__(self):
        return self.purse


class Invoice(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_("User"), editable=False)
    created_on = models.DateTimeField(_("Created on"), unique=True, editable=False, auto_now_add=True)
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

    @classmethod
    def remove_old(cls, days):
        cls.objects.filter(created_on__lt=timezone.now()-timedelta(days=days), payment__isnull=True).delete()

    def save(self, *args, **kwargs):
        sid = transaction.savepoint()
        if self.pk is None:
            i = 1
            while self.pk is None:

                # Protection from infinite loop
                if i > 20:
                    raise IntegrityError('Too many iterations while generating unique Invoice number.')

                self.payment_no = random.getrandbits(32)

                try:
                    super(Invoice, self).save(*args, **kwargs)
                except IntegrityError:
                    transaction.savepoint_rollback(sid)

                i += 1
        else:
            super(Invoice, self).save(*args, **kwargs)

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
    sys_invs_no = models.PositiveIntegerField('LMI_SYS_INVS_NO')
    sys_trans_no = models.PositiveIntegerField('LMI_SYS_TRANS_NO')
    sys_trans_date = models.DateTimeField('LMI_SYS_TRANS_DATE')
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
                                                                     'payee_purse': self.payee_purse.purse}
