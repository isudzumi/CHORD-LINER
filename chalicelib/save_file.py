import os
import logging
import boto3
from botocore.exceptions import ClientError
from scipy.io import wavfile

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

def save_wavefile(chord_info):
    wave_signals = 0.1*(chord_info.signals)
    wave = (wave_signals * float(2 ** 15 - 1)).astype(np.int16)
    wavfile.write(chord_info.file_name, chord_info.sampling_rate, wave)

def uploadToS3(file_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(
            file_name,
            S3_BUCKET_NAME,
            file_name,
            ExtraArgs={'ACL': 'public-read'}
        )
    except ClientError as e:
        logging.error(e)

def save_file(chord_info):
    save_wavefile(chord_info)
    uploadToS3(chord_info.file_name)
    return {
        'url': 'https://{0}.s3-{1}.amazonaws.com/{2}'.format(
            S3_BUCKET_NAME,
            os.environ['AWS_REGION'],
            chord_info.file_name
        )
    }

if __name__ == "__main__":
    pass