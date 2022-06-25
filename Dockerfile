FROM promethee/pimoroni.breakout-garden:latest
RUN apt install -y git fontconfig-config build-essential libfreetype6-dev libjpeg-dev libopenjp2-7 libportmidi-dev libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev python3-dev python3-pip
RUN dpkg-reconfigure fontconfig-config
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
WORKDIR /usr/src/app
RUN git clone https://github.com/rm-hull/luma.examples.git
WORKDIR /usr/src/app/luma.examples/examples
CMD python3 welcome.py --display sh1106 --height 128 --rotate 2 --interface i2c
