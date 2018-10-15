from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=15, blank=True)
	profile_image = models.ImageField(upload_to='Profile', blank=True, null=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=15, blank=True)
	profile_image = models.ImageField(upload_to='Profile', blank=True, null=True)

	# card_holder_name = models.CharField(max_length=100,blank=True)
	# cc_number = models.CharField(max_length=16,blank=True)
	# expiray_month = models.CharField(max_length=3,blank=True)
	# expiray_year = models.CharField(max_length=4,blank=True)
	# cvv_number = models.CharField(max_length=4,blank=True)
	# email = models.CharField(max_length=50,blank=True)
	# phone = models.CharField(max_length=20,blank=True)


class Checkout(models.Model):
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)
	address1 = models.TextField(max_length=500, blank=True)
	address2 = models.TextField(max_length=500, blank=True)
	city = models.CharField(max_length=50, blank=True)
	state = models.CharField(max_length=50, blank=True)
	zipcode = models.CharField(max_length=20, blank=True)
	email = models.CharField(max_length=50, blank=True)
	phone = models.CharField(max_length=50, blank=True)
	card_num = models.CharField(max_length=16, blank=True)
	card_cvv = models.CharField(max_length=16, blank=True)
	# card_expired_month = models.CharField(max_length=4,blank=True)
	card_expired_date = models.CharField(max_length=200, blank=True)
	# paypal_use = models.CharField(max_length=2,blank=True)
	paypal_use = models.CharField(max_length=5, blank=True)
	paypal_email = models.CharField(max_length=50, blank=True)
	paypal_pw = models.CharField(max_length=50, blank=True)


class BotTaskType:
    PINVERIFY = 'pinverify'
    SEARCH = 'search'

    task_types = (
        (PINVERIFY, PINVERIFY),
        (SEARCH, SEARCH),
    )


class BotTaskStatus:
	QUEUED = 'Queued'
	RUNNING = 'Running'
	NOSEARCHRESULT = 'NotResult'
	RESEARCH = 'ReSearching'
	NOTAVAILABLE = 'Not Available'
	CHECKOUTING = 'Checkouting'
	PIN_REQUIRED = 'Pin Required'
	PIN_CHECKING = 'Pin Checking'
	PIN_INVALID = 'Pin Invalid'
	ERROR = 'Error'
	DONE = 'Done'
	CAPTCHA_SOLVING = 'Captcha solving'
	statuses = (
	    (QUEUED, QUEUED),
		(RUNNING, RUNNING),
        (RESEARCH, RESEARCH),
		(NOSEARCHRESULT, NOSEARCHRESULT),
		(NOTAVAILABLE, NOTAVAILABLE),
		(CHECKOUTING, CHECKOUTING),
        (PIN_REQUIRED, PIN_REQUIRED),
        (PIN_CHECKING, PIN_CHECKING),
		(PIN_INVALID, PIN_INVALID),
        (CAPTCHA_SOLVING, CAPTCHA_SOLVING),
        (ERROR, ERROR),
        (DONE, DONE)
    )


class ShopifyUrl(models.Model):
	url = models.CharField(max_length=500, blank=True)


class Proxies(models.Model):
	ip = models.CharField(max_length=50, blank=True)
	port = models.CharField(max_length=50, blank=True)


class Task(models.Model):
	site = models.ForeignKey(ShopifyUrl, related_name='site', on_delete=models.CASCADE, default=2)
	size = models.TextField(max_length=500, blank=True)
	product = models.TextField(max_length=500, blank=True)
	start_time = models.CharField(max_length=50, blank=True)
	checkout = models.ForeignKey(Checkout, related_name='checkout',	on_delete=models.CASCADE, default=2)
	proxy = models.ForeignKey(Proxies, related_name='proxy', on_delete=models.CASCADE, default=2)
	quantity = models.CharField(max_length=50, blank=True)
	completed_date = models.CharField(max_length=50, blank=True)
	keyword = models.CharField(max_length=50, blank=True)
	checkout_type = models.CharField(max_length=50, blank=True)
	status = models.CharField(max_length=20, choices=BotTaskStatus.statuses, default=BotTaskStatus.QUEUED)
	action = models.CharField(max_length=20, blank=True)


class GmailAccount(models.Model):
	email = models.CharField(max_length=50, blank=True)
	password= models.CharField(max_length=50, blank=True)






