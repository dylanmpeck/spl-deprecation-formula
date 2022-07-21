from query_lab_records import query_lab_records, save_dataframe, load_dataframe
from brute_force import get_usage_and_rating, Lab_Record, add_to_lab_record
import globals
import csv

def read_buganizer_data():
    buganizer_ticket_number = {}
    with open("buganizer.csv", "r") as filestream:
        for line in filestream:
            columns = line.split(",")
            buganizer_ticket_number[columns[0]] = columns[2]
    return buganizer_ticket_number

def normalize_and_write_to_csv(lab_metrics, buganizer_metrics):
    with open('example.csv', 'w') as file:
        writer = csv.writer(file)
        header = ["Title", "Slug", "Score", "Usage", "Normalized_Usage", "Average_Rating", "Normalized_Rating", "Bug_Count", "Normalized_Bug_Count_Reverse_Scale", "Consumption_Link"]
        writer.writerow(header)
        for lab_title, lab_record in lab_metrics.items():
            if lab_title in buganizer_metrics:
                normalized_usage = float(lab_record.usage / globals.MAX_USAGE)
                normalized_ratings = float(lab_record.average_rating / 5.0)
                normalized_bugs = float(1 - (float(buganizer_metrics[lab_title]) + 1) / 8.0) #reverse_scale (add one to avoid divide by 0)
                score = normalized_bugs + normalized_ratings + normalized_usage
                data = [lab_title, lab_record.slug, str(score), str(lab_record.usage), str(normalized_usage), str(lab_record.average_rating), str(normalized_ratings), str(buganizer_metrics[lab_title]), str(normalized_bugs), lab_record.consumption_link]
                writer.writerow(data)



def main():
    globals.initialize()
    # lab_records_df = query_lab_records()
    # lab_records_df.drop([is_gwg_content,course_enrollment_id,course_enrolled_at,course_completed_at,course_session_start_date,course_session_end_date,course_session_country,course_session_owner,course_session_training_body,course_session_type,course_session_id,course_title,course_library,course_slug,course_version,course_revision,spl_reseller,during_free_trial], axis=1, inplace=True)
    # save_dataframe(lab_records_df)
    print("Loading Dataframe...")
    lab_records_df = load_dataframe("lab_records_df.csv")
    # Drop "A Tour of Google Cloud Hands-On Labs" - it dwarves the usage normalization and will never be retired anyway
    lab_records_df = lab_records_df[lab_records_df["lab_title"].str.contains("A Tour of Google Cloud Hands-on Labs") == False]
    # print(lab_records_df.head())
    print("Collecting Usage and Rating Data over Last Year...")
    lab_metrics = get_usage_and_rating(lab_records_df)
    print("Reading Buganizer Data...")
    buganizer_metrics = read_buganizer_data()
    print("Normalizing data and writing to file...")
    normalize_and_write_to_csv(lab_metrics, buganizer_metrics)



if __name__ == "__main__":
    main()