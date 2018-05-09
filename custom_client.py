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
    # Here we will run 4 episodes with 600 frames each.
    # One episode for each corner of the map
    number_of_episodes = 4
    frames_per_episode = 200

    # We assume the CARLA server is already waiting for a client to connect at
    # host:port.
    with make_carla_client(args.host, args.port) as client:
        #print('CarlaClient connected')
        
        if args.settings_filepath is None:
            
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
        
        else:

                # Alternatively, we can load these settings from a file.
                with open(args.settings_filepath, 'r') as fp:
                    settings = fp.read()

        # Now we load these settings into the server. The server replies
        # with a scene description containing the available start spots for
        # the player. Here we can provide a CarlaSettings object or a
        # CarlaSettings.ini file as string.
        client.load_settings(settings)
        
        # Setting the corners fo the map as starting positions. 
        start_positions = [46, 97, 67, 104]
        
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
            for frame in range(0, frames_per_episode):
            
                # Read the data produced by the server this frame.
                measurements, sensor_data = client.read_data()
                
                # Print some of the measurements.
                #print_measurements(measurements)

                # Checking the lines of the road to guide the pilot
                if args.smart_driver_SIA:
                    # Convert the frame to BGR
                    img = cv2.cvtColor(sensor_data['CameraRGB'].data,
                                    cv2.COLOR_RGB2BGR)
                    # Obtain the image with the lines of the road drawn and the
                    # degrees of the line relative the vertical of the camera
                    crazy_lines, degrees_list = eyes.get_road_line(img)
                    
                    # Writing the new images on disk
                    # Warning! You must create the dir 'Salida' in the same 
                    # level respect this script. 
                    cv2.imwrite('Salida/ep' + str(episode) + 'fr' + str(frame)
                                + '.jpg', crazy_lines)
                    
                    # Default behaviour will be go straight forward
                    next_steer = 0.0
                    # Get the average average angle from list
                    average_angle = 0.0
                    if len(degrees_list) > 0:
                        print('lista: ' + str(degrees_list))
                        for degree in degrees_list:
                            average_angle += degree
                            print(degree)
                        average_angle = average_angle/len(degrees_list)
                        print('media: ' + str(average_angle))
                        next_steer = fuzLog.getForce(-average_angle)
                        
                    #print(next_steer)
                    # TODO: wait to fix fuzzylogic module
                    client.send_control(
                        steer=next_steer,
                        throttle=0.5,
                        brake=0.0,
                        hand_brake=False,
                        reverse=False)
                    
                    # In the meantime we will use the default autopilot
                    #control = measurements.player_measurements.autopilot_control
                    #client.send_control(control)

                else:
                    
                    # Run the default autopilot. 
                    # Together with the measurements, the server has sent the
                    # control that the in-game autopilot would do this frame. We
                    # can enable autopilot by sending back this control to the
                    # server. We can modify it if wanted, here for instance we
                    # will add some noise to the steer.

                    control = measurements.player_measurements.autopilot_control
                    client.send_control(control)
    
                # Save the images to disk if requested.
                if args.save_images_to_disk:
                    for name, measurement in sensor_data.items():
                        filename = args.out_filename_format.format(episode, name, frame)
                        measurement.save_to_disk(filename)


def print_measurements(measurements):
    number_of_agents = len(measurements.non_player_agents)
    player_measurements = measurements.player_measurements
    message = 'Vehicle at ({pos_x:.1f}, {pos_y:.1f}), '
    message += '{speed:.0f} km/h, '
    message += 'Collision: {{vehicles={col_cars:.0f}, pedestrians={col_ped:.0f}, other={col_other:.0f}}}, '
    message += '{other_lane:.0f}% other lane, {offroad:.0f}% off-road, '
    message += '({agents_num:d} non-player agents in the scene)'
    message = message.format(
        pos_x=player_measurements.transform.location.x,
        pos_y=player_measurements.transform.location.y,
        speed=player_measurements.forward_speed * 3.6, # m/s -> km/h
        col_cars=player_measurements.collision_vehicles,
        col_ped=player_measurements.collision_pedestrians,
        col_other=player_measurements.collision_other,
        other_lane=100 * player_measurements.intersection_otherlane,
        offroad=100 * player_measurements.intersection_offroad,
        agents_num=number_of_agents)
    print_over_same_line(message)


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
        '-l', '--lidar',
        action='store_true',
        help='enable Lidar')
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
    argparser.add_argument(
        '-c', '--carla-settings',
        metavar='PATH',
        dest='settings_filepath',
        default=None,
        help='Path to a "CarlaSettings.ini" file')

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


