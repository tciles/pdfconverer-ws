import os
import subprocess
from zipfile import ZipFile
from os.path import basename

from flask import Flask, request, render_template, abort, jsonify, send_file
from flask_cors import CORS
from flasgger import Swagger
from redis import Redis
from rq import Queue
from rq.job import Job

import utils
import worker

DEVELOPMENT = os.environ.get('environment', 'production').lower() == 'development'

conn = Redis(host=os.environ.get("REDIS_HOST", "localhost"))
q = Queue(connection=conn, default_timeout=3600)

application = Flask(__name__)


# Zip the files from given directory that matches the filter
def zipFilesInDir(dirName, zipFileName, filter):
   # create a ZipFile object
   with ZipFile(zipFileName, 'w') as zipObj:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk(dirName):
           for filename in filenames:
               if filter(filename):
                   # create complete filepath of file in directory
                   filePath = os.path.join(folderName, filename)
                   # Add file to zip
                   zipObj.write(filePath, basename(filePath))


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.route('/', methods=['GET'])
def get_main():
    return render_template('index.html')

@application.route('/convert', methods=['POST'])
def post_convert():
    file = request.files["pdf"]

    job_id = utils.generate_id()
    dirId = utils.storage_dir_for_id(job_id)
    os.makedirs(dirId)
    fileName = os.path.join(dirId, job_id + ".pdf")
    file.save(fileName)

    job = q.enqueue(worker.process, args=(job_id,), job_id = job_id, result_ttl=86400)

    return jsonify({"job_id": job.get_id()})

@application.route('/result/<job_id>', methods=['GET'])
def get_result(job_id):
    job = Job.fetch(job_id, connection = conn)

    if job.is_finished:
        dirId = utils.storage_dir_for_id(job_id)
        fileName = os.path.join(dirId, job_id+'.zip')
        zipFilesInDir(dirId, fileName, lambda name : 'png' in name)

        try:
            return send_file(fileName)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": job.get_status(), "data": ""}), 202
