# orders/migrations/0002_hypertable.py
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        # Ensure the TimescaleDB extension is available.
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS timescaledb;",
            reverse_sql="DROP EXTENSION IF EXISTS timescaledb;",
        ),
        # Convert the orders table into a hypertable with daily chunks.
        migrations.RunSQL(
            sql="""
                SELECT create_hypertable(
                    'order_order',           -- table name
                    by_range('created_at', INTERVAL '1 day')
                );
            """,
            reverse_sql="SELECT 1;",
        ),
        # Enable compression policy
        # Add a compression policy: compress chunks older than 30 days.
        migrations.RunSQL(
            sql="""
                ALTER TABLE order_order SET (timescaledb.compress);
                SELECT add_compression_policy(
                    'order_order',           -- table name
                    INTERVAL '30 days'
                );
            """,
            reverse_sql="SELECT remove_compression_policy('order_order');",
        ),
    ]
