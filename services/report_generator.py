from datetime import timedelta
import pytz
from sqlalchemy import text
import pandas as pd
from models.data_model import engine
from .report_cache import report_cache 


def fetch_table(table_name: str) -> pd.DataFrame:
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table_name}"))
        data = result.fetchall()

    df = pd.DataFrame(data, columns=result.keys())
    return df

def convert_to_utc(timestamp_str, timezone_str='America/Chicago'):
    try:
        tz_local = pytz.timezone(timezone_str)
        dt_local = pd.to_datetime(timestamp_str)  # Convert timestamp to datetime object
        dt_local = tz_local.localize(dt_local)
        dt_utc = dt_local.astimezone(pytz.utc)
        return dt_utc
    except Exception as e:
        print(f"Error converting local time to UTC: {e}")
        return None

def calculate_uptime_downtime():
    df_status = fetch_table('store_status')
    df_business_hours = fetch_table('store_hours')
    df_timezones = fetch_table('store_timezones')

    # Convert timestamp_utc to datetime
    df_status['timestamp_utc'] = pd.to_datetime(df_status['timestamp_utc'])

    results = []

    for store_id in df_status['store_id'].unique():
        print(f"\nProcessing store_id: {store_id}")

        store_status = df_status[df_status['store_id'] == store_id]
        business_hours = df_business_hours[df_business_hours['store_id'] == store_id]

        if business_hours.empty:
            print("No business hours data found for this store.")
            # Assume the store is open 24/7
            results.append({
                'store_id': store_id,
                'uptime_last_hour': 60 if len(store_status) > 0 else 0,
                'uptime_last_day': 24 if len(store_status) > 0 else 0,
                'uptime_last_week': 24 * 7 if len(store_status) > 0 else 0,
                'downtime_last_hour': 0 if len(store_status) > 0 else 60,
                'downtime_last_day': 0 if len(store_status) > 0 else 24,
                'downtime_last_week': 0 if len(store_status) > 0 else 24 * 7
            })
            continue

        timezone_str = df_timezones[df_timezones['store_id'] == store_id]['timezone_str'].iloc[0] if not df_timezones[df_timezones['store_id'] == store_id].empty else 'America/Chicago'

        uptime_last_hour = 0
        downtime_last_hour = 0
        uptime_last_day = 0
        downtime_last_day = 0
        uptime_last_week = 0
        downtime_last_week = 0

        for _, row in business_hours.iterrows():
            start_time_utc = convert_to_utc(row['start_time_local'], timezone_str)
            end_time_utc = convert_to_utc(row['end_time_local'], timezone_str)

            if pd.isnull(start_time_utc) or pd.isnull(end_time_utc):
                print("Invalid start or end time detected, skipping.")
                continue

            status_within_hours = store_status[(store_status['timestamp_utc'].dt.time >= start_time_utc.time()) &
                                               (store_status['timestamp_utc'].dt.time <= end_time_utc.time())]

            for _, status_row in status_within_hours.iterrows():
                timestamp_utc = status_row['timestamp_utc']

                day_of_week = timestamp_utc.weekday()
                day_start = timestamp_utc.replace(hour=0, minute=0, second=0, microsecond=0)
                week_start = day_start - timedelta(days=day_of_week)

                last_hour_start = timestamp_utc - timedelta(hours=1)
                last_day_start = day_start
                last_week_start = week_start

                if status_row['status'] == 'active':
                    # Calculate uptime for the last hour, day, and week
                    uptime_last_hour = min(uptime_last_hour + (timestamp_utc - last_hour_start).total_seconds() / 60, 60)
                    uptime_last_day = min(uptime_last_day + (timestamp_utc - last_day_start).total_seconds() / 3600, 24)
                    uptime_last_week = min(uptime_last_week + (timestamp_utc - last_week_start).total_seconds() / (3600 * 24 * 7), 168)
                else:
                    # Calculate downtime for the last hour, day, and week
                    downtime_last_hour = min(downtime_last_hour + (timestamp_utc - last_hour_start).total_seconds() / 60, 60)
                    downtime_last_day = min(downtime_last_day + (timestamp_utc - last_day_start).total_seconds() / 3600, 24)
                    downtime_last_week = min(downtime_last_week + (timestamp_utc - last_week_start).total_seconds() / (3600 * 24 * 7), 168)

        uptime_last_day = min(uptime_last_day, uptime_last_week)
        downtime_last_day = min(downtime_last_day, downtime_last_week)

        results.append({
            'store_id': store_id,
            'uptime_last_hour': uptime_last_hour,
            'uptime_last_day': uptime_last_day,
            'uptime_last_week': uptime_last_week,
            'downtime_last_hour': 60 - uptime_last_hour,
            'downtime_last_day': 24 - uptime_last_day,
            'downtime_last_week': 168 - uptime_last_week
        })

    return pd.DataFrame(results)


def generate_report(report_id: str):
    try:
        report_cache[report_id] = {'status': 'Running'}  # Mark the report as running in the cache
        report_df = calculate_uptime_downtime()

        # report_file_path = f"report_data/report_{report_id}.csv"
        # report_df.to_csv(report_file_path, index=False)

        report_cache[report_id]['report'] = report_df
        
        report_cache[report_id]['status'] = 'Complete'  # Mark the report as complete in the cache

        print(f"Report generated successfully for report_id: {report_id}")
    except Exception as e:
        print(f"Error generating report: {e}")
        report_cache[report_id]['status'] = 'Failed'  # Mark the report as failed in the cache
