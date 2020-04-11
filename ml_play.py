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
    now_pos = (97.5, 395)
    speed = -7
    cacu_speed = speed
    ini_y = 0.0
    final_x = 0.0
    fall_time = 0.0
    prelen_normal = 0
    prelen_hard = 0
    caculate_desti = False
    
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
            print("實際落下位置：", now_pos[0])
            ball_served = False
            now_pos = (97.5, 395)
            speed = -7
            cacu_speed = speed
            ini_y = 0.0
            final_x = 0.0
            fall_time = 0.0
            prelen_normal = 0
            prelen_hard = 0
            caculate_desti = False
            
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue
    
        pre_pos = now_pos
        # 3.3. Put the code here to handle the scene information
        now_pos = scene_info.ball
        plat = scene_info.platform
        len_normal = len(scene_info.bricks)
        len_hard = len(scene_info.hard_bricks)
        #print("x = ", now_pos[0])
        
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
            caculate_desti = True
else:
    speed = now_pos[0]-pre_pos[0]
    if now_pos[1]>pre_pos[1]: #球下降
        print("x = ", now_pos[0])
        if (len_normal!=prelen_normal) or (len_hard!=prelen_hard):
            speed = speed*(-1)
            caculate_desti = True
                
                if caculate_desti:
                    cacu_speed = speed
                    print(speed)
                    ini_y = now_pos[1]
                    final_x = now_pos[0]
                    fall_time = (400.0-ini_y)/abs(cacu_speed)
                    print("ini_y = ", ini_y)
                    print("now_pos[0] = ", now_pos[0])
                    print("fall_time = ", fall_time)
                    #print("abs(cacu_speed) = ", cacu_speed)
                    i = 0
                    while i < fall_time:
                        if (fall_time-i)<1:
                            final_x = final_x + cacu_speed*(fall_time-i)
                            break
                    
                        final_x = final_x + cacu_speed
                        print(final_x)
                        
                        if final_x<=0:
                            final_x = 0
                            cacu_speed = cacu_speed*(-1)
                elif final_x>=200-5:
                    final_x = 200-5
                        cacu_speed = cacu_speed*(-1)
                        
                        i = i+1
                    
                    final_x = final_x + 2.5
                    print("最終預測：", final_x)
                    caculate_desti = False
                        
                        if now_pos[0]>=pre_pos[0]: #球向右
                            if plat[0]+20<final_x:
                                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                                    elif plat[0]+20>final_x:
                                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                                            else: #球向左
                                                if plat[0]+20<final_x:
                                                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                                                        elif plat[0]+20>final_x:
                                                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                                                    else: #球上升
                                                        caculate_desti = True
                                                            
                                                            if plat[0]<80:
                                                                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                                                                    elif plat[0]>80:
                                                                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                                                                            else:
                                                                                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                                                                                    
                                                                                    prelen_normal = len_normal
                                                                                        prelen_hard = len_hard
#print("speed = ", speed)
