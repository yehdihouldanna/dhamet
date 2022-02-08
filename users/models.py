from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.utils.translation import ugettext as _

from django.db.models.signals import pre_save
from django.dispatch import receiver


# http://xml.coverpages.org/country3166.html
#region
COUNTRIES = (
    ('AD', _('Andorra')),
    ('AE', _('United Arab Emirates')),
    ('AF', _('Afghanistan')),
    ('AG', _('Antigua & Barbuda')),
    ('AI', _('Anguilla')),
    ('AL', _('Albania')),
    ('AM', _('Armenia')),
    ('AN', _('Netherlands Antilles')),
    ('AO', _('Angola')),
    ('AQ', _('Antarctica')),
    ('AR', _('Argentina')),
    ('AS', _('American Samoa')),
    ('AT', _('Austria')),
    ('AU', _('Australia')),
    ('AW', _('Aruba')),
    ('AZ', _('Azerbaijan')),
    ('BA', _('Bosnia and Herzegovina')),
    ('BB', _('Barbados')),
    ('BD', _('Bangladesh')),
    ('BE', _('Belgium')),
    ('BF', _('Burkina Faso')),
    ('BG', _('Bulgaria')),
    ('BH', _('Bahrain')),
    ('BI', _('Burundi')),
    ('BJ', _('Benin')),
    ('BM', _('Bermuda')),
    ('BN', _('Brunei Darussalam')),
    ('BO', _('Bolivia')),
    ('BR', _('Brazil')),
    ('BS', _('Bahama')),
    ('BT', _('Bhutan')),
    ('BV', _('Bouvet Island')),
    ('BW', _('Botswana')),
    ('BY', _('Belarus')),
    ('BZ', _('Belize')),
    ('CA', _('Canada')),
    ('CC', _('Cocos (Keeling) Islands')),
    ('CF', _('Central African Republic')),
    ('CG', _('Congo')),
    ('CH', _('Switzerland')),
    ('CI', _('Ivory Coast')),
    ('CK', _('Cook Iislands')),
    ('CL', _('Chile')),
    ('CM', _('Cameroon')),
    ('CN', _('China')),
    ('CO', _('Colombia')),
    ('CR', _('Costa Rica')),
    ('CU', _('Cuba')),
    ('CV', _('Cape Verde')),
    ('CX', _('Christmas Island')),
    ('CY', _('Cyprus')),
    ('CZ', _('Czech Republic')),
    ('DE', _('Germany')),
    ('DJ', _('Djibouti')),
    ('DK', _('Denmark')),
    ('DM', _('Dominica')),
    ('DO', _('Dominican Republic')),
    ('DZ', _('Algeria')),
    ('EC', _('Ecuador')),
    ('EE', _('Estonia')),
    ('EG', _('Egypt')),
    ('EH', _('Western Sahara')),
    ('ER', _('Eritrea')),
    ('ES', _('Spain')),
    ('ET', _('Ethiopia')),
    ('FI', _('Finland')),
    ('FJ', _('Fiji')),
    ('FK', _('Falkland Islands (Malvinas)')),
    ('FM', _('Micronesia')),
    ('FO', _('Faroe Islands')),
    ('FR', _('France')),
    ('FX', _('France, Metropolitan')),
    ('GA', _('Gabon')),
    ('GB', _('United Kingdom (Great Britain)')),
    ('GD', _('Grenada')),
    ('GE', _('Georgia')),
    ('GF', _('French Guiana')),
    ('GH', _('Ghana')),
    ('GI', _('Gibraltar')),
    ('GL', _('Greenland')),
    ('GM', _('Gambia')),
    ('GN', _('Guinea')),
    ('GP', _('Guadeloupe')),
    ('GQ', _('Equatorial Guinea')),
    ('GR', _('Greece')),
    ('GS', _('South Georgia and the South Sandwich Islands')),
    ('GT', _('Guatemala')),
    ('GU', _('Guam')),
    ('GW', _('Guinea-Bissau')),
    ('GY', _('Guyana')),
    ('HK', _('Hong Kong')),
    ('HM', _('Heard & McDonald Islands')),
    ('HN', _('Honduras')),
    ('HR', _('Croatia')),
    ('HT', _('Haiti')),
    ('HU', _('Hungary')),
    ('ID', _('Indonesia')),
    ('IE', _('Ireland')),
    ('IL', _('Israel')),
    ('IN', _('India')),
    ('IO', _('British Indian Ocean Territory')),
    ('IQ', _('Iraq')),
    ('IR', _('Islamic Republic of Iran')),
    ('IS', _('Iceland')),
    ('IT', _('Italy')),
    ('JM', _('Jamaica')),
    ('JO', _('Jordan')),
    ('JP', _('Japan')),
    ('KE', _('Kenya')),
    ('KG', _('Kyrgyzstan')),
    ('KH', _('Cambodia')),
    ('KI', _('Kiribati')),
    ('KM', _('Comoros')),
    ('KN', _('St. Kitts and Nevis')),
    ('KP', _('Korea, Democratic People\'s Republic of')),
    ('KR', _('Korea, Republic of')),
    ('KW', _('Kuwait')),
    ('KY', _('Cayman Islands')),
    ('KZ', _('Kazakhstan')),
    ('LA', _('Lao People\'s Democratic Republic')),
    ('LB', _('Lebanon')),
    ('LC', _('Saint Lucia')),
    ('LI', _('Liechtenstein')),
    ('LK', _('Sri Lanka')),
    ('LR', _('Liberia')),
    ('LS', _('Lesotho')),
    ('LT', _('Lithuania')),
    ('LU', _('Luxembourg')),
    ('LV', _('Latvia')),
    ('LY', _('Libyan Arab Jamahiriya')),
    ('MA', _('Morocco')),
    ('MC', _('Monaco')),
    ('MD', _('Moldova, Republic of')),
    ('MG', _('Madagascar')),
    ('MH', _('Marshall Islands')),
    ('ML', _('Mali')),
    ('MN', _('Mongolia')),
    ('MM', _('Myanmar')),
    ('MO', _('Macau')),
    ('MP', _('Northern Mariana Islands')),
    ('MQ', _('Martinique')),
    ('MR', _('Mauritania')),
    ('MS', _('Monserrat')),
    ('MT', _('Malta')),
    ('MU', _('Mauritius')),
    ('MV', _('Maldives')),
    ('MW', _('Malawi')),
    ('MX', _('Mexico')),
    ('MY', _('Malaysia')),
    ('MZ', _('Mozambique')),
    ('NA', _('Namibia')),
    ('NC', _('New Caledonia')),
    ('NE', _('Niger')),
    ('NF', _('Norfolk Island')),
    ('NG', _('Nigeria')),
    ('NI', _('Nicaragua')),
    ('NL', _('Netherlands')),
    ('NO', _('Norway')),
    ('NP', _('Nepal')),
    ('NR', _('Nauru')),
    ('NU', _('Niue')),
    ('NZ', _('New Zealand')),
    ('OM', _('Oman')),
    ('PA', _('Panama')),
    ('PE', _('Peru')),
    ('PF', _('French Polynesia')),
    ('PG', _('Papua New Guinea')),
    ('PH', _('Philippines')),
    ('PK', _('Pakistan')),
    ('PL', _('Poland')),
    ('PM', _('St. Pierre & Miquelon')),
    ('PN', _('Pitcairn')),
    ('PR', _('Puerto Rico')),
    ('PT', _('Portugal')),
    ('PW', _('Palau')),
    ('PY', _('Paraguay')),
    ('QA', _('Qatar')),
    ('RE', _('Reunion')),
    ('RO', _('Romania')),
    ('RU', _('Russian Federation')),
    ('RW', _('Rwanda')),
    ('SA', _('Saudi Arabia')),
    ('SB', _('Solomon Islands')),
    ('SC', _('Seychelles')),
    ('SD', _('Sudan')),
    ('SE', _('Sweden')),
    ('SG', _('Singapore')),
    ('SH', _('St. Helena')),
    ('SI', _('Slovenia')),
    ('SJ', _('Svalbard & Jan Mayen Islands')),
    ('SK', _('Slovakia')),
    ('SL', _('Sierra Leone')),
    ('SM', _('San Marino')),
    ('SN', _('Senegal')),
    ('SO', _('Somalia')),
    ('SR', _('Suriname')),
    ('ST', _('Sao Tome & Principe')),
    ('SV', _('El Salvador')),
    ('SY', _('Syrian Arab Republic')),
    ('SZ', _('Swaziland')),
    ('TC', _('Turks & Caicos Islands')),
    ('TD', _('Chad')),
    ('TF', _('French Southern Territories')),
    ('TG', _('Togo')),
    ('TH', _('Thailand')),
    ('TJ', _('Tajikistan')),
    ('TK', _('Tokelau')),
    ('TM', _('Turkmenistan')),
    ('TN', _('Tunisia')),
    ('TO', _('Tonga')),
    ('TP', _('East Timor')),
    ('TR', _('Turkey')),
    ('TT', _('Trinidad & Tobago')),
    ('TV', _('Tuvalu')),
    ('TW', _('Taiwan, Province of China')),
    ('TZ', _('Tanzania, United Republic of')),
    ('UA', _('Ukraine')),
    ('UG', _('Uganda')),
    ('UM', _('United States Minor Outlying Islands')),
    ('US', _('United States of America')),
    ('UY', _('Uruguay')),
    ('UZ', _('Uzbekistan')),
    ('VA', _('Vatican City State (Holy See)')),
    ('VC', _('St. Vincent & the Grenadines')),
    ('VE', _('Venezuela')),
    ('VG', _('British Virgin Islands')),
    ('VI', _('United States Virgin Islands')),
    ('VN', _('Viet Nam')),
    ('VU', _('Vanuatu')),
    ('WF', _('Wallis & Futuna Islands')),
    ('WS', _('Samoa')),
    ('YE', _('Yemen')),
    ('YT', _('Mayotte')),
    ('YU', _('Yugoslavia')),
    ('ZA', _('South Africa')),
    ('ZM', _('Zambia')),
    ('ZR', _('Zaire')),
    ('ZW', _('Zimbabwe')),
    ('ZZ', _('Unknown or unspecified country')),
)
#region

countries = ['afghanistan', 'aland-islands', 'albania', 'algeria', 'american-samoa', 'andorra', 'angola',
'anguilla', 'antigua-and-barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan',
'azores-islands', 'bahamas', 'bahrain', 'balearic-islands', 'bangladesh', 'barbados', 'basque-country',
'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bonaire', 'bosnia-and-herzegovina',
'botswana', 'brazil', 'british-columbia', 'british-indian-ocean-territory', 'british-virgin-islands',
'brunei', 'bulgaria', 'burkina-faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'canary-islands',
'cape-verde', 'cayman-islands', 'central-african-republic', 'ceuta', 'chad', 'chile', 'china', 'christm',
'cuba', 'curacao', 'czech-republic', 'democratic-republic-of-congo', 'denmark', 'djibouti', 'dominica',
'dominican-republic', 'east-timor', 'ecuador', 'egypt', 'el-salvador', 'england', 'equatorial-guinea',
'eritrea', 'estonia', 'ethiopia', 'european-union', 'falkland-islands', 'fiji', 'finland', 'flag',
'france', 'french-polynesia', 'gabon', 'galapagos-islands', 'gambia', 'georgia', 'germany', 'ghana',
'gibraltar', 'greece', 'greenland', 'grenada', 'guam', 'guatemala', 'guernsey', 'guinea-bissau', 'guinea',
'haiti', 'hawaii', 'honduras', 'hong-kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq',
'ireland', 'isle-of-man', 'israel', 'italy', 'ivory-coast', 'jamaica', 'japan', 'jersey', 'jordan',
'kazakhstan', 'kenya', 'kiribati', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon',
'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'madagascar',
'madeira', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall-island', 'martinique',
'mauritania', 'mauritius', 'melilla', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia',
'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nato', 'nauru',
'nepal', 'netherlands', 'new-zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk-island',
'north-korea', 'northern-cyprus', 'northern-mariana-islands', 'norway', 'oman', 'ossetia', 'pakistan',
'palau', 'palestine', 'panama', 'papua-new-guinea', 'paraguay', 'peru', 'philippines', 'pitcairn-islands',
'poland', 'portugal', 'puerto-rico', 'qatar', 'rapa-nui', 'republic-of-macedonia', 'republic-of-the-congo',
'romania', 'russia', 'rwanda', 'saba-island', 'sahrawi-arab-democratic-republic', 'saint-kitts-and-nevis',
'samoa', 'san-marino', 'sao-tome-and-prince', 'sardinia', 'saudi-arabia', 'scotland', 'senegal', 'serbia',
'seychelles', 'sicily', 'sierra-leone', 'singapore', 'sint-eustatius', 'sint-maarten', 'slovakia',
'slovenia', 'solomon-islands', 'somalia', 'somaliland', 'south-africa', 'south-korea', 'south-sudan',
'spain', 'sri-lanka', 'st-barts', 'st-lucia', 'st-vincent-and-the-grenadines', 'sudan', 'suriname',
'swaziland', 'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'tibet',
'togo', 'tokelau', 'tonga', 'transnistria', 'trinidad-and-tobago', 'tunisia', 'turkey', 'turkmenistan',
'turks-and-caicos', 'tuvalu-1', 'tuvalu', 'uganda', 'uk', 'ukraine', 'united-arab-emirates',
'united-kingdom', 'united-nations', 'united-states', 'uruguay', 'uzbekistan', 'vanuatu', 'vatican-city',
'venezuela', 'vietnam', 'virgin-islands', 'wales', 'yemen', 'zambia', 'zimbabwe']


DEFAULT_AVATAR = "uploads\images\Profile_default.jpg"

class CountryField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', COUNTRIES)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"
class User(AbstractUser):
    """Default user for Project."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    phone = models.CharField(verbose_name=_("Phone"), max_length=20, blank=False)

    id = models.AutoField(primary_key=True)
    score = models.IntegerField("Score",default = 1000 , blank=False,null=False)
    avatar_url = models.CharField(default = DEFAULT_AVATAR , blank=True,max_length=255)
    # avatar = models.ImageField(upload_to='uploads/')
    is_fake = models.BooleanField(default=False,null=False,blank=False)
    tier = models.IntegerField(default =0,null=False,blank=False)
    country = CountryField(default = "ZZ", blank = False)

    @receiver(pre_save)
    def my_callback(sender, instance, *args, **kwargs):
        try :
            instance.name = instance.username
        except :
            pass

    def set_user_score(self,new_score):
        self.score = new_score
        self.save()

    def set_user_country(self,new_country):
        self.country = new_country
        self.save()

    def get_user_country(self):
        return self.country

    def update_user_score(self,score_change):
        self.score = max(0,self.score+score_change)
        self.save()

    def get_user_flag_url(self):
        return 'assets/media/flags/'+self.country+'.svg'

    def __str__(self):
        if self.name: return f"{self.name}"
        return f"{self.username}: {self.phone}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_permissions = []
        permissions = [
            ("add_user", _("Can add user")),
            ("view_user", _("Can view user")),
            ("change_user", _("Can change user")),
            ("delete_user", _("Can delete user")),
            ("list_user", _("Can list users")),
        ]

    def get_update_url(self):
        return reverse("users:update", kwargs={"pk": self.pk})


