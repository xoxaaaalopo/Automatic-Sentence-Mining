import pysrt

def get_timestamps(sub_file, target_sentence):
    subs = pysrt.open(sub_file)

    for sub in subs:
        if target_sentence in sub.text:
            start_time = sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds + sub.start.milliseconds / 1000.0
            end_time = sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds + sub.end.milliseconds / 1000.0
            return start_time, end_time
            
    raise ValueError(f'Sentence not found in subtitles: {target_sentence}')