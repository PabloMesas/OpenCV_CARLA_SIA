#!/usr/bin/env python3 

# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma
# de Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
#
# Custom CARLA client from SIA

from __future__ import print_function

import argparse
import logging
import time
import detection_car_driving as eyes
import fuzzyLogic as fl

from cv2 import cv2
from carla.client import make_carla_client
from carla.sensor import Camera
from carla.settings import CarlaSettings
from carla.tcp import TCPConnectionError
from carla.util import print_over_same_line

def run_carla_client(args):
    # Here we will run 2 episodes with 1200 frames each.
    # One episode for each corner of the map
    number_of_episodes = 2

    # We assume the CARLA server is already waiting for a client to connect at
    # host:port.
    with make_carla_client(args.host, args.port) as client:
        print('CarlaClient connected')
           
        # Create a CarlaSettings object. This object is a wrapper around
        # the CarlaSettings.ini file.
        settings = CarlaSettings()
        settings.set(
            SynchronousMode=True,
            SendNonPlayerAgentsInfo=True,
            NumberOfVehicles=0,
            NumberOfPedestrians=0,
            WeatherId=1,
            QualityLevel=args.quality_level)
        settings.randomize_seeds()

        # Now we want to add a camera to the player vehicle. We
        # will collect the images produced by these cameras every
        # frame.

        # The default camera captures RGB images of the scene.
        camera0 = Camera('CameraRGB')
        # Fish eye
        camera0.set(FOV=140.0)
        # Set image resolution in pixels.
        camera0.set_image_size(1280, 720)
        # Set its position relative to the car in meters
        # (At the end of the car's hood).
        camera0.set_position(2.10, 0, 1.10)
        settings.add_sensor(camera0)
        
        # Now we load these settings into the server. The server replies
        # with a scene description containing the available start spots for
        # the player. Here we can provide a CarlaSettings object or a
        # CarlaSettings.ini file as string.
        client.load_settings(settings)
        
        # Setting the corners fo the map as starting positions. 
        start_positions = [97, 46]
        
        # Instance fuzzy logic class
        fuzLog = fl.FuzzyLogic()
        
        for episode in range(0, number_of_episodes):
            # Setting the next start position. 
            player_start = start_positions[episode]

            # Notify the server that we want to start the episode at the
            # player_start index. This function blocks until the server is
            # ready to start the episode.
            #print('Starting new episode...')
            client.start_episode(player_start)
            
            # Iterate every frame in the episode.
            frame_counter = 0
            continue_episode = True
            
            while continue_episode:
                try:
                        # Read the data produced by the server this frame.
                    measurements, sensor_data = client.read_data()

                    # Checking the lines of the road to guide the pilot
                    if args.smart_driver_SIA:
                        # Convert the frame to BGR
                        img = cv2.cvtColor(sensor_data['CameraRGB'].data,
                                        cv2.COLOR_RGB2BGR)
                        # Obtain the image with the lines of the road drawn and the
                        # degrees of the line relative the vertical of the camera
                        frame_data, distance, angle = eyes.get_road_line(img)
                        
                        # Writing the new images on disk
                        # Warning! You must create the dir 'Salida' in the same 
                        # level respect this script.
                        cv2.imwrite('Salida_Raw/ep' + str(episode) + 'fr' + str(frame_counter)
                                    + '.jpg', img)
                        cv2.imwrite('Salida/ep' + str(episode) + 'fr' + str(frame_counter)
                                    + '.jpg', frame_data)
                        
                        # Default behaviour will be go straight forward
                        next_steer = 0.0
                        # In case we receive a control signal from detection_car_driving
                        if  distance != 3666 and angle != 111:
                            next_steer = fuzLog.getForce(angle, distance)
                            
                        client.send_control(
                            steer=next_steer,
                            throttle=0.6,
                            brake=0.0,
                            hand_brake=False,
                            reverse=False)

                    else:
                        
                        # Run the default autopilot. 
                        # Together with the measurements, the server has sent the
                        # control that the in-game autopilot would do this frame. We
                        # can enable autopilot by sending back this control to the
                        # server.

                        control = measurements.player_measurements.autopilot_control
                        client.send_control(control)
        
                    # Save the images to disk if requested.
                    if args.save_images_to_disk:
                        for name, measurement in sensor_data.items():
                            filename = args.out_filename_format.format(episode, name, frame_counter)
                            measurement.save_to_disk(filename)

                    frame_counter += 1

                except KeyboardInterrupt:
                    print("Ending simulation")
                    continue_episode = False

def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='localhost',
        help='IP of the host server (default: localhost)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-q', '--quality-level',
        choices=['Low', 'Epic'],
        type=lambda s: s.title(),
        default='Epic',
        help='graphics quality level, a lower level makes the simulation run considerably faster.')
    argparser.add_argument(
        '-i', '--images-to-disk',
        action='store_true',
        dest='save_images_to_disk',
        help='save images (and Lidar data if active) to disk')
    argparser.add_argument(
        '-s', '--sia',
        action='store_true',
        dest='smart_driver_SIA',
        help='use the smart brain developed in SIA to pilot the vehicle')

    args = argparser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    args.out_filename_format = '_out/episode_{:0>4d}/{:s}/{:0>6d}'

    while True:
        try:

            run_carla_client(args)

            #print('Done.')
            return

        except TCPConnectionError as error:
            logging.error(error)
            time.sleep(1)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


