"""
Module for store info imports from another systems, e.g cigam, shoplive, e-commerce...
"""
import re
from django.core.cache import cache
from core.services.cigam_client import CigamClient
from store import models
from core.model.ecomm_models import OurStores


def detect_franchise_alias(store_name: str) -> str:
    """
    Detect franchise alias from store name.
    Returns one of: STD, FRQ, LPF, OUT (default OUT if nothing matches).
    """
    if not store_name:
        return None

    name_upper = store_name.upper()

    if "LPF" in name_upper:
        return "LPF"
    elif "FRQ" in name_upper:
        return "FRQ"
    elif "STD" in name_upper:
        return "STD"
    else:
        return "OUT"


class CigamStores:
    """Simplified client for fetching and processing Cigam API data."""

    def __init__(self):
        self.client = CigamClient()

    def run_cigam_stores(self):
        try:
            results_raw = self.client.get_data("CIGAM_LOJAS", {"credencial": "53587920250704"}) or []

            results = []
            cnpj_list = []

            # preload franchises {alias -> Franchise instance}
            franchises = {f.alias: f for f in models.Franchises.objects.all()}

            for store in results_raw:
                store_cnpj = re.sub(r'[^0-9]', '', str(store.get('numcnpj', ''))) if store.get('numcnpj') else ''
                if len(store_cnpj) != 14:
                    continue

                cnpj_list.append(store_cnpj)

                # detect alias from store name
                alias = detect_franchise_alias(store.get('nomfantasia'))

                # get the Franchise from DB (may be None if alias missing)
                franchise_id = franchises.get(alias)

                results.append(models.Stores(
                    cigam_id=store.get('codempresa'),
                    cnpj=store_cnpj,
                    name=store.get('nomfantasia'),
                    franchise_id=franchise_id.id if franchise_id else None
                ))

            if cnpj_list:
                cache.set('active_stores', "','".join(f"{cnpj}" for cnpj in cnpj_list))

            response = models.Stores.objects.bulk_create(
                results,
                update_conflicts=True,
                update_fields=["cigam_id", "name", "franchise_id"],
                unique_fields=["cigam_id"]
            )

            return response

        except Exception as e:
            raise e


class EcommStores:
		"""Simplified client for fetching and processing E-commerce store data."""
		def __init__(self, db_alias="live_ecomm"):
				self.db_alias = db_alias

		def get(self, *fields, **filters):
				"""Return dicts with only the specified fields, optional filters"""
				qs = OurStores.objects.using(self.db_alias).values(*fields)
				if filters:
						qs = qs.filter(**filters)
				return qs

		def run_ecomm_stores(self):
				try:
						stores = self.get("cnpj", "status", cnpj__isnull=False)

						results = []

						for store in stores:
								cnpj_raw = str(store.get("cnpj", ""))
								cnpj = re.sub(r"[^0-9]", "", cnpj_raw)
								if len(cnpj) != 14:
										continue

								status = store.get("status")

								results.append(models.Stores(
										cnpj=cnpj,
										status=status,
								))
						seen = set()
						unique_results = []

						for store in stores:
								cnpj_raw = str(store.get("cnpj", ""))
								cnpj = re.sub(r"[^0-9]", "", cnpj_raw)
								if len(cnpj) != 14 or cnpj in seen:
										continue

								seen.add(cnpj)
								status = store.get("status")

								unique_results.append(models.Stores(
										cnpj=cnpj,
										status=status,
								))

						response = models.Stores.objects.bulk_create(
								unique_results,
								update_conflicts=True,
								update_fields=["cnpj", "status"],
								unique_fields=["cnpj"]
						)

						return response

				except Exception as e:
						raise e
