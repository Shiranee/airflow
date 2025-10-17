'''
Stores models.
'''
from django.db import models
from django.db.models.functions import Now


class Stores(models.Model):
		class Meta:
				verbose_name = 'Store'
				verbose_name_plural = 'Stores'
				db_table = 'stores'
				db_table_comment = "Stores information including personal details and contacts information"
				managed = False

		id = models.AutoField(primary_key=True, db_comment='Auto-incrementing unique identifier for each database record')
		cnpj = models.CharField(unique=True, max_length=20, db_comment='CNPJ (Brazilian business identifier) of the store; primary key')
		cigam_id = models.CharField(max_length=20, blank=True, null=True, db_comment='Internal unique identifier for the store')
		franchise_id = models.BigIntegerField(blank=True, null=True, db_comment='Franchising id')
		status = models.BooleanField(blank=True, null=True, default=False, db_default=models.Value(False), db_comment='Current status of the employee (e.g., active, inactive)')
		name = models.CharField(max_length=255, blank=True, null=True, db_comment='Commercial name of the store')
		name_legal = models.CharField(max_length=255, blank=True, null=True, db_comment='Registered legal name of the store')
		inaugurated_at = models.DateField(blank=True, null=True, db_comment='Date this store was opened')
		created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, db_default=Now(), db_comment='Timestamp when this record was created')
		updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, db_default=Now(), db_comment='Timestamp when this record was last updated')
		deleted_at = models.DateTimeField(blank=True, null=True, db_comment='Timestamp when this record was soft-deleted (NULL if active)')

		def __str__(self):
				return f"{self.id} - {self.name}"


class StoreSocial(models.Model):
    class Meta:
        verbose_name = 'Store Social'
        verbose_name_plural = 'Stores Social'
        db_table = 'store_social'
        db_table_comment = "Stores information including personal details and contacts information"
        managed = False

    id = models.AutoField(primary_key=True, db_comment='Auto-incrementing unique identifier for each database record')
    store = models.ForeignKey(Stores, on_delete=models.CASCADE, db_comment='id that relates to main stores table')
    store_cnpj = models.CharField(unique=True, max_length=20, db_comment='CNPJ (Brazilian business identifier) of the store; primary key')
    status = models.BooleanField(blank=True, null=True, default=False, db_default=models.Value(False), db_comment='Current status of the employee (e.g., active, inactive)')
    name = models.CharField(max_length=255, blank=True, null=True, db_comment='Display name of the store')
    coupon_id = models.BigIntegerField(blank=True, null=True, db_comment='Associated coupon or promotion ID')
    email = models.CharField(max_length=255, blank=True, null=True, db_comment='Email adress of the store')
    phone = models.CharField(max_length=50, blank=True, null=True, db_comment="Store's primary contact phone number")
    whatsapp = models.CharField(max_length=50, blank=True, null=True, db_comment="Store's WhatsApp number for customer contact")
    url = models.CharField(max_length=50, blank=True, null=True, db_comment='Website or landing page URL of the store')
    instagram = models.CharField(max_length=255, blank=True, null=True, db_comment='URL of the store Instagram')
    facebook = models.CharField(max_length=255, blank=True, null=True, db_comment='URL of the store Instagram')
    cover_photo = models.CharField(max_length=255, blank=True, null=True, db_comment="URL or path to the store's cover photo")
    store_photo = models.CharField(max_length=255, blank=True, null=True, db_comment="URL or path to the store's profile photo")
    working_days = models.JSONField(blank=True, null=True, db_comment='Days of the week the store is open')
    working_hours = models.JSONField(blank=True, null=True, db_comment='Operating hours of the store')
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, db_default=Now(), db_comment='Timestamp when this record was created')
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, db_default=Now(), db_comment='Timestamp when this record was last updated')
    deleted_at = models.DateTimeField(blank=True, null=True, db_comment='Timestamp when this record was soft-deleted (NULL if active)')

    def __str__(self):
        return f"{self.id}"


class StoreAdresses(models.Model):
    class Meta:
        verbose_name = 'Store Adresses'
        verbose_name_plural = 'Stores Adresses'
        db_table = 'store_adresses'
        db_table_comment = "Stores information including personal details and contacts information"
        managed = False

    id = models.AutoField(primary_key=True, db_comment='Auto-incrementing unique identifier for each database record')
    store = models.ForeignKey(Stores, on_delete=models.CASCADE, db_comment='id that relates to main stores table')
    store_cnpj = models.CharField(max_length=20, null=True, db_comment='CNPJ (Brazilian business identifier) of the store; primary key')
    status = models.BooleanField(blank=True, null=True, default=False, db_default=models.Value(False), db_comment='Current status of the employee (e.g., active, inactive)')
    zip_code = models.CharField(max_length=9, blank=True, null=True, db_comment="Postal code of the store's location")
    state = models.CharField(max_length=5, blank=True, null=True, db_comment='State where the store is located')
    city = models.CharField(max_length=255, blank=True, null=True, db_comment='City where the store is located')
    neighborhood = models.CharField(max_length=255, blank=True, null=True, db_comment='Neighborhood of the store')
    street = models.CharField(max_length=255, blank=True, null=True, db_comment='Street name of the store address')
    number = models.CharField(max_length=10, blank=True, null=True, db_comment='Street number of the store')
    complement = models.CharField(max_length=255, blank=True, null=True, db_comment='Additional address information (e.g., suite or floor)')
    lat = models.CharField(max_length=50, blank=True, null=True, db_comment='Latitude coordinate of the store')
    lng = models.CharField(max_length=50, blank=True, null=True, db_comment='Longitude coordinate of the store')
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, db_default=Now(), db_comment='Timestamp when this record was created')
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, db_default=Now(), db_comment='Timestamp when this record was last updated')
    deleted_at = models.DateTimeField(blank=True, null=True, db_comment='Timestamp when this record was soft-deleted (NULL if active)')

    def __str__(self):
        return f"{self.id}"


class Franchises(models.Model):
    class Meta:
        verbose_name = 'Store Franchises'
        verbose_name_plural = 'Stores Franchises'
        db_table = 'franchises'
        db_table_comment = "Stores information including personal details and contacts information"

    id = models.AutoField(
        primary_key=True,
        help_text="Auto-incrementing unique identifier for each database record"
    )

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Short descriptive name of the franchise type"
    )

    status = models.BooleanField(
        default=False,
        null=True,
        help_text="Current status (e.g., active, inactive)"
    )

    alias = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Simplified version of the franchise name"
    )

    owner_type = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Organization that owns this franchise type"
    )

    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the franchise type"
    )
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, db_default=Now(), db_comment='Timestamp when this record was created')
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, db_default=Now(), db_comment='Timestamp when this record was last updated')
    deleted_at = models.DateTimeField(blank=True, null=True, db_comment='Timestamp when this record was soft-deleted (NULL if active)')

    def __str__(self):
        return f"{self.id} - {self.name}"
