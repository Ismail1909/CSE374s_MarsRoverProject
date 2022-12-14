import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!
    
        # Steering proportional to the deviation results in
        # small offsets on straight lines and
        # large values in turns and open areas
    offset = 0.65 * np.std(Rover.nav_angles)
    # Example:
    # Check if we have vision data to make decisions with
    if Rover.samples_collected >= 5:
        distance = ((Rover.pos[0]-Rover.start_pos[0])**2 + (Rover.pos[1]-Rover.start_pos[1])**2)
        #if(distance <=10):
            #Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi)+12, -15, 15)
        if(distance <= 10):
            Rover.brake = 10
            while(1):
                Rover.throttle = 0

    if Rover.nav_angles is not None:
        
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            if Rover.vel <= 0.1 and not Rover.picking_up:
                if Rover.loop_count < 50 :
                    Rover.loop_count +=1
                else:
                        Rover.throttle = 0
                        Rover.brake = Rover.brake_set
                        Rover.steer = -15
                        Rover.mode = 'stop'
            else:
                Rover.loop_count=0
                """       
                Rover.vel=0
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
                    
                Rover.steer = np.clip(np.mean((Rover.nav_angles) * 180 / np.pi), -15, 15)
                Rover.brake = 0
                Rover.throttle = Rover.throttle_set """
            #go to the rock if exist and in the left side only
            if Rover.samples_angles is not None and np.mean(Rover.samples_angles) > -1 and np.min(Rover.samples_dists) < 40:
                    Rover.vel=0.1
                    mean = np.mean(Rover.samples_angles * 180 / np.pi)
                    if not np.isnan(mean):
                        Rover.steer = np.clip(mean, -15, 15)

            # Check the extent of navigable terrain
            elif len(Rover.nav_angles) >= Rover.stop_forward:
                #check if stuck

                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean((Rover.nav_angles+offset) * 180/np.pi), -15, 15)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'
        
        elif Rover.mode == 'stop':
                # If we're in stop mode but still moving keep braking
                if Rover.vel > 0.2:
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0

                # If we're not moving (vel < 0.2) then do something else
                elif Rover.vel <= 0.2:

                    # Now we're stopped and we have vision data to see if there's a path forward???
                    if Rover.loop_count < 50:
                        if len(Rover.nav_angles) < Rover.go_forward:
                            Rover.throttle = 0
                            # Release the brake to allow turning
                            Rover.brake = 0
                            # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                            # Could be more clever here about which way to turn
                            Rover.steer = -15 

                        # If we're stopped but see sufficient navigable terrain in front then go!
                        if len(Rover.nav_angles) >= Rover.go_forward:
                            # Set throttle back to stored value
                            Rover.throttle = Rover.throttle_set
                            # Release the brake
                            Rover.brake = 0

                            # Set steer to mean angle
                            Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi)+12, -15, 15)
                            Rover.mode = 'forward'

                    else:
                        #if stuck
                        if Rover.loop_count < 60:
                            Rover.throttle = 0
                            # Release the brake to allow turning
                            Rover.brake = 0
                            # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                            Rover.steer = -15 
                            Rover.loop_count += 1

                        else:
                            # Set throttle back to stored value
                            Rover.throttle = Rover.throttle_set
                            # Release the brake
                            Rover.brake = 0
                            # Set steer to mean angle
                            Rover.steer = -15
                            Rover.loop_count = 0
                            Rover.mode = 'forward'

                        

        """
        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    offset = 12
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi)+offset, -15, 15)
                    
                    Rover.mode = 'forward' """
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
    
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel > 0 and not Rover.picking_up:
        Rover.brake=Rover.brake_set
        Rover.vel=0
        Rover.throttle=0
        Rover.steer = 0
        Rover.send_pickup = True
        Rover.samples_collected += 1
        Rover.throttle=Rover.throttle_set
    
    return Rover
