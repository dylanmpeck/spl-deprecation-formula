import math
import globals
from alive_progress import alive_bar

class Lab_Record:
  def __init__(self, title, slug):
    self.title = title
    self.slug = slug
    self.consumption_link = ""
    self.usage = 0
    self.total_rating = 0
    self.total_times_rated = 0
    self.average_rating = 0.0

def add_to_lab_record(lab_dict, lab_title, df_row):
    lab_dict[lab_title].usage += 1
    if lab_dict[lab_title].usage > globals.MAX_USAGE:
        globals.MAX_USAGE = lab_dict[lab_title].usage 
    if type(df_row['rating']) == int or float and math.isnan(df_row['rating']) == False:
        lab_dict[lab_title].total_rating += df_row['rating']
        lab_dict[lab_title].total_times_rated += 1
        lab_dict[lab_title].average_rating = float(lab_dict[lab_title].total_rating / lab_dict[lab_title].total_times_rated)

def get_usage_and_rating(lab_records_df):
    lab_usage_and_ratings_dict = {}
    with alive_bar(lab_records_df.shape[0]) as bar:
        for _, row in lab_records_df.iterrows():
            lab_title = row['lab_title']
            if lab_title in lab_usage_and_ratings_dict:
                add_to_lab_record(lab_usage_and_ratings_dict, lab_title, row)
            else:
                lab_usage_and_ratings_dict[lab_title] = Lab_Record(lab_title, row['lab_slug'])
                gsp_num = row['lab_slug'].split("-")[0][3:]
                lab_usage_and_ratings_dict[lab_title].consumption_link = "https://qwiklabs.looker.com/dashboards/1227?Slug+Tag=GSP" + gsp_num + "&Created+Date=this+year+to+second"
                add_to_lab_record(lab_usage_and_ratings_dict, lab_title, row)
            bar()
    return lab_usage_and_ratings_dict