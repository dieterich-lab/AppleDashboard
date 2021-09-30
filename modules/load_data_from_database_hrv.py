import pandas as pd
def table_hrv(rdb):

    sql = """ select "Patient","Day","Date"::time as Time, "hrvOwn", "SDNN", "SENN", "SDSD", "pNN20", "pNN50", "lf", "hf", "lf_hf_ratio",
            "total_power", "vlf", "Classification" from ecg  order by "Patient","Day" """

    try:
        df = pd.read_sql(sql, rdb)
    except:
        df = []
    return df

