FROM jjanzic/docker-python3-opencv:latest
MAINTAINER Lei Han <l.han@alumnos.urjc.es>
COPY /people_detector .
RUN pip install opencv-contrib-python
ENTRYPOINT ["python3", "docker_people_detector.py"]
