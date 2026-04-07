#!/usr/bin/env python3
"""
Pepper in PyBullet - Chasing Balloons
Connected to ASD Dashboard
"""

import time
import threading
import random
import math
import requests
import pybullet as p
import pybullet_data

class PepperBalloonChaser:
    def __init__(self):
        print("🤖 Starting Pepper in PyBullet...")
        
        # Connect to PyBullet
        self.client = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.setRealTimeSimulation(1)
        
        # Load ground
        p.loadURDF("plane.urdf")
        
        # Load Pepper (using simple robot if Pepper URDF not found)
        try:
            self.pepper = p.loadURDF("r2d2.urdf", [0, 0, 0.5])
            print("✅ Robot loaded (r2d2)")
        except:
            # Create a simple robot
            col = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.3, 0.3, 0.6])
            vis = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.3, 0.3, 0.6], rgbaColor=[0.8, 0.8, 0.8, 1])
            self.pepper = p.createMultiBody(baseMass=10, baseCollisionShapeIndex=col, 
                                            baseVisualShapeIndex=vis, basePosition=[0, 0, 0.6])
            print("✅ Simple robot created")
        
        # Create balloons
        self.balloons = []
        self.create_balloons()
        
        # Robot position
        self.x, self.y = 0, 0
        self.walk_timer = 0
        self.head_yaw = 0
        
        # Dashboard URL
        self.dashboard_url = "http://localhost:5001"
        
        # Camera position
        p.resetDebugVisualizerCamera(cameraDistance=6, cameraYaw=45, 
                                      cameraPitch=-30, cameraTargetPosition=[0, 0, 1])
        
        print("✅ Pepper is walking and chasing balloons!")
        print("📌 Dashboard at: http://localhost:5001")
        
        # Start threads
        threading.Thread(target=self.walk_loop, daemon=True).start()
        threading.Thread(target=self.chase_balloons, daemon=True).start()
        threading.Thread(target=self.update_dashboard, daemon=True).start()
        
        # Main simulation loop
        self.run()
    
    def create_balloons(self):
        """Create colorful balloons"""
        colors = [
            [1, 0.2, 0.2, 1],  # Red
            [0.2, 1, 0.2, 1],  # Green
            [0.2, 0.2, 1, 1],  # Blue
            [1, 1, 0.2, 1],    # Yellow
            [1, 0.5, 0.2, 1],  # Orange
            [0.8, 0.2, 0.8, 1] # Purple
        ]
        
        for i in range(10):
            x = random.uniform(-3.5, 3.5)
            y = random.uniform(-2.8, 2.8)
            z = random.uniform(0.6, 2.2)
            color = colors[i % len(colors)]
            
            # Balloon body (sphere)
            visual = p.createVisualShape(p.GEOM_SPHERE, radius=0.18, rgbaColor=color)
            balloon = p.createMultiBody(baseMass=0, baseVisualShapeIndex=visual, 
                                        basePosition=[x, y, z])
            
            # String (small cylinder)
            string_vis = p.createVisualShape(p.GEOM_CYLINDER, radius=0.008, length=0.25, 
                                            rgbaColor=[0.4, 0.4, 0.4, 1])
            p.createMultiBody(baseMass=0, baseVisualShapeIndex=string_vis,
                             basePosition=[x, y, z - 0.2])
            
            self.balloons.append({
                'id': balloon,
                'x': x, 'y': y, 'z': z,
                'speed': random.uniform(0.008, 0.03)
            })
        
        print(f"🎈 Created {len(self.balloons)} balloons!")
    
    def walk_loop(self):
        """Make Pepper walk in a circle"""
        while True:
            self.walk_timer += 0.02
            self.x = 2.0 * math.cos(self.walk_timer * 0.4)
            self.y = 1.5 * math.sin(self.walk_timer * 0.6)
            p.resetBasePositionAndOrientation(self.pepper, [self.x, self.y, 0.5], [0, 0, 0, 1])
            time.sleep(0.08)
    
    def chase_balloons(self):
        """Head follows closest balloon"""
        while True:
            if self.balloons:
                # Find closest balloon
                closest = None
                min_dist = 999
                for b in self.balloons:
                    dist = math.sqrt((b['x'] - self.x)**2 + (b['y'] - self.y)**2)
                    if dist < min_dist:
                        min_dist = dist
                        closest = b
                
                if closest:
                    dx = closest['x'] - self.x
                    dy = closest['y'] - self.y
                    target_yaw = math.atan2(dy, dx)
                    self.head_yaw = self.head_yaw * 0.92 + target_yaw * 0.08
                    
                    # Update head position (if robot has head joint)
                    try:
                        p.setJointMotorControl2(self.pepper, 0, p.POSITION_CONTROL, 
                                                targetPosition=self.head_yaw)
                    except:
                        pass
            time.sleep(0.04)
    
    def update_dashboard(self):
        """Update dashboard with Pepper state"""
        while True:
            try:
                requests.post(f'{self.dashboard_url}/api/pepper-state',
                             json={
                                 'x': self.x, 'y': self.y,
                                 'balloons': len(self.balloons),
                                 'head_angle': self.head_yaw
                             }, timeout=1)
            except:
                pass
            time.sleep(2)
    
    def run(self):
        """Main simulation loop"""
        try:
            while True:
                # Update balloons (float up and down)
                for b in self.balloons:
                    b['z'] += b['speed']
                    if b['z'] > 2.5:
                        b['z'] = 0.5
                        b['x'] = random.uniform(-3.5, 3.5)
                        b['y'] = random.uniform(-2.8, 2.8)
                    p.resetBasePositionAndOrientation(b['id'], [b['x'], b['y'], b['z']], [0, 0, 0, 1])
                
                p.stepSimulation()
                time.sleep(1/60.)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping Pepper...")
            p.disconnect()

if __name__ == "__main__":
    PepperBalloonChaser()
