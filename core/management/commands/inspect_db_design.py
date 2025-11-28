from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection
from django.conf import settings
import re

class Command(BaseCommand):
    help = 'Inspect DB design: list apps/models, model fields, DB tables and sample schemas (SQLite)'

    def handle(self, *args, **options):
        self.stdout.write("Models by app:")
        for app_config in apps.get_app_configs():
            self.stdout.write(f"- {app_config.label} ({app_config.name})")
            for model in app_config.get_models():
                self.stdout.write(f"  - Model: {model.__name__} -> table: {model._meta.db_table}")
                field_lines = []
                for f in model._meta.get_fields():
                    # show simple field summary for concrete fields
                    try:
                        field_cls = f.__class__.__name__
                        if hasattr(f, 'max_length'):
                            extra = f"(max_length={getattr(f, 'max_length', None)})"
                        elif hasattr(f, 'decimal_places'):
                            extra = f"(max_digits={getattr(f, 'max_digits', None)}, decimal_places={getattr(f, 'decimal_places', None)})"
                        else:
                            extra = ""
                        field_lines.append(f"{f.name}:{field_cls}{extra}")
                    except Exception:
                        field_lines.append(str(f))
                self.stdout.write("    Fields: " + ", ".join(field_lines))

        # list DB tables
        with connection.cursor() as cursor:
            try:
                tables = connection.introspection.table_names()
            except Exception:
                tables = []
            self.stdout.write(f"\nDatabase tables ({len(tables)}):")
            for t in tables:
                self.stdout.write(f" - {t}")

            # If SQLite, show schema for likely tables
            engine = settings.DATABASES['default']['ENGINE']
            if 'sqlite' in engine:
                interesting = [t for t in tables if re.search(r'order|order_item|orderitem|product|cart|item', t, re.I)]
                if interesting:
                    self.stdout.write("\nSchemas for matching tables:")
                    for t in interesting:
                        self.stdout.write(f"\nSchema for {t}:")
                        try:
                            cursor.execute(f"PRAGMA table_info('{t}')")
                            rows = cursor.fetchall()
                            for r in rows:
                                cid, name, col_type, notnull, default_val, pk = r
                                self.stdout.write(f"  {name} {col_type} notnull={notnull} pk={pk} default={default_val}")
                        except Exception as e:
                            self.stdout.write(f"  (error reading schema: {e})")
                else:
                    self.stdout.write("\nNo obvious order/product tables matched; inspect table list above.")
            else:
                # Generic introspection for other DBs (sample)
                self.stdout.write("\nColumn descriptions (first 5 tables):")
                for t in tables[:5]:
                    self.stdout.write(f"\nDescription for {t}:")
                    try:
                        desc = connection.introspection.get_table_description(cursor, t)
                        for col in desc:
                            # attempt attribute access for name/type
                            name = getattr(col, 'name', str(col))
                            type_code = getattr(col, 'type_code', '')
                            self.stdout.write(f"  {name} type_code={type_code}")
                    except Exception as e:
                        self.stdout.write(f"  (unable to introspect: {e})")

        # quick search hints
        self.stdout.write("\nHints:")
        self.stdout.write(" - Look for models/tables named Order, OrderItem, order_item, product, cart, item.")
        self.stdout.write(" - For each OrderItem you should see fields like: id, order_id (FK), product_id (FK), quantity, price (Decimal).")
        self.stdout.write(" - If you can't find OrderItem, search models for fields on Order that store items as JSON or m2m.")
