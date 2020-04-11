"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    prex = 93
    prey = 395
    m = 1
    dispx = -7
    dispy = -7
    f = 93
    prem = 1
    
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    
   
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue
        

        comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)

        # 3.3. Put the code here to handle the scene information
        if scene_info.ball[0] != prex:
            dispx = scene_info.ball[0] - prex
        if scene_info.ball[1] != prey:
            dispy = scene_info.ball[1] - prey
        
        m = dispy / dispx

        
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            if dispy > 0:
                
                forecast = (400 - scene_info.ball[1]) / m + scene_info.ball[0]
                ball_x = scene_info.ball[0]
                ball_y = scene_info.ball[1]

                if forecast < 0:  
                    collide_x = 0
                    collide_y = ball_y + (collide_x - ball_x) * m
                    m = m * -1
                    forecast = collide_x + (400 - collide_y) / m
                elif forecast > 200:
                    collide_x = 200
                    collide_y = ball_y + (collide_x - ball_x) * m
                    m = m * -1
                    forecast = collide_x + (400 - collide_y) / m


               
                
                    
                    
                
                print(forecast)

                if forecast > 0 and forecast < 200:
                    if forecast > scene_info.platform[0] + 20:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                
                    elif forecast < scene_info.platform[0] + 20:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)   
                
                       
            prex = scene_info.ball[0]
            prey = scene_info.ball[1]
            