FROM promethee/pimoroni.breakout-garden:latest
RUN apt install -y git libfreetype6-dev libjpeg-dev libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
WORKDIR /usr/src/app
RUN git clone https://github.com/rm-hull/luma.examples.git
WORKDIR /usr/src/app/luma.examples/examples
CMD python3 welcome.py --display sh1106 --height 128 --rotate 2 --interface i2c
