"""
Motion Data Generator

This module generates realistic mouse movement and interaction data using Bezier curves,
human-like timing patterns, and sophisticated motion algorithms to bypass hCaptcha's
motion analysis systems.
"""

"""
WARNING: This code is for educational or authorized testing purposes only.
Unauthorized use to bypass anti-bot protections may violate laws or terms of service.
"""

import time
import random
import math
import json
from typing import List, Tuple, Dict, Any, Optional

import numpy as np
import bezier

class MotionDataGenerator:
    """
    Advanced motion data generator that creates human-like mouse movements,
    clicks, and interaction patterns for hCaptcha solving.
    """
    
    def __init__(self, screen_width: int = 1920, screen_height: int = 1080) -> None:
        """
        Initialize the motion data generator.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.base_speed = 1.0
        self.randomness = 0.3
        self.hesitation_chance = 0.15
        
        self.min_move_interval = 8
        self.max_move_interval = 35
        self.click_delay_range = (50, 150)
        
    def _Generate_BezierPath(self, start: Tuple[int, int], end: Tuple[int, int], control_points: int = 3, curvature: float = 0.3) -> List[Tuple[int, int]]:
        """
        Generate a natural mouse path using Bezier curves.
        
        Args:
            start: Starting point (x, y)
            end: Ending point (x, y)
            control_points: Number of control points for the curve
            curvature: Amount of curve (0.0 = straight line, 1.0 = very curved)
            
        Returns:
            List of (x, y) points along the path
        """
        try:
            distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            num_points = max(10, int(distance / 15))
            
            x_coords = []
            y_coords = []
            
            x_coords.append(start[0])
            y_coords.append(start[1])
            
            for i in range(1, control_points - 1):
                t = i / (control_points - 1)
                
                ctrl_x = start[0] + t * (end[0] - start[0])
                ctrl_y = start[1] + t * (end[1] - start[1])
                
                delta_x = end[0] - start[0]
                delta_y = end[1] - start[1]
                line_len = math.sqrt(delta_x**2 + delta_y**2)
                
                if line_len > 0:
                    normal_x = -delta_y / line_len
                    normal_y = delta_x / line_len
                    
                    lateral_offset = random.uniform(-curvature * distance * 0.2, curvature * distance * 0.2)
                    
                    ctrl_x += normal_x * lateral_offset
                    ctrl_y += normal_y * lateral_offset
                
                x_coords.append(ctrl_x)
                y_coords.append(ctrl_y)
            
            x_coords.append(end[0])
            y_coords.append(end[1])
            
            control_matrix = np.array([x_coords, y_coords])
            curve = bezier.Curve(control_matrix, degree=len(x_coords) - 1)
            
            t_values = np.linspace(0.0, 1.0, num_points)
            curve_points = curve.evaluate_multi(t_values)
            
            path_points = []
            for i in range(len(t_values)):
                x = int(round(curve_points[0][i]))
                y = int(round(curve_points[1][i]))
                
                x = max(0, min(self.screen_width - 1, x))
                y = max(0, min(self.screen_height - 1, y))
                
                path_points.append((x, y))
            
            dedup_path = [path_points[0]]
            for pt in path_points[1:]:
                if pt != dedup_path[-1]:
                    dedup_path.append(pt)
            
            return dedup_path
            
        except Exception:
            return self._LinearPath(start, end, max(10, int(distance / 20)))
    
    def _LinearPath(self, start: Tuple[int, int], end: Tuple[int, int], points: int) -> List[Tuple[int, int]]:
        """
        Generate a linear path as fallback.
        
        Args:
            start: Starting point
            end: Ending point
            points: Number of points
            
        Returns:
            List of points along linear path
        """
        path_points = []
        for i in range(points):
            t = i / (points - 1) if points > 1 else 0
            x = int(start[0] + t * (end[0] - start[0]))
            y = int(start[1] + t * (end[1] - start[1]))
            path_points.append((x, y))
        
        return path_points
    
    def _FakeTiming(self, path: List[Tuple[int, int]], base_time: int) -> List[List[int]]:
        """
        Add realistic human timing to mouse path.
        
        Args:
            path: List of (x, y) coordinates
            base_time: Base timestamp in milliseconds
            
        Returns:
            List of [x, y, timestamp] points
        """
        timed_points = []
        current_ts = base_time
        
        for i, (x, y) in enumerate(path):
            if i == 0:
                timed_points.append([x, y, current_ts])
                continue
            
            prev_x, prev_y = path[i - 1]
            distance = math.sqrt((x - prev_x)**2 + (y - prev_y)**2)

            base_interval = max(self.min_move_interval, min(self.max_move_interval, distance * 2))
            
            rand_factor = random.uniform(0.7, 1.3)
            step_ms = int(base_interval * rand_factor * self.base_speed)
            
            if random.random() < self.hesitation_chance:
                step_ms += random.randint(50, 200)
            
            current_ts += step_ms
            timed_points.append([x, y, current_ts])
        
        return timed_points
    
    def _Generate_MouseMovement(self, start: Tuple[int, int], end: Tuple[int, int], timestamp: Optional[int] = None) -> List[List[int]]:
        """
        Generate complete mouse movement from start to end.
        
        Args:
            start: Starting coordinates (x, y)
            end: Ending coordinates (x, y)
            timestamp: Base timestamp (uses current time if None)
            
        Returns:
            List of [x, y, timestamp] movement points
        """
        if timestamp is None:
            timestamp = int(time.time() * 1000)
        
        path_points = self._Generate_BezierPath(start, end)
        
        timed_path = self._FakeTiming(path_points, timestamp)
                
        return timed_path
    
    def _Generate_ClickSequence(self, position: Tuple[int, int], timestamp: Optional[int] = None, click_type: str = "single") -> Tuple[List[List[int]], List[List[int]]]:
        """
        Generate mouse down and up events for clicking.
        
        Args:
            position: Click position (x, y)
            timestamp: Base timestamp
            click_type: "single", "double", or "hold"
            
        Returns:
            Tuple of (mouse_down_events, mouse_up_events)
        """
        if timestamp is None:
            timestamp = int(time.time() * 1000)
        
        x, y = position
        down_events = []
        up_events = []
        
        if click_type == "single":
            down_time = timestamp
            up_time = timestamp + random.randint(*self.click_delay_range)
            
            down_events.append([x, y, down_time])
            up_events.append([x, y, up_time])
            
        elif click_type == "double":
            first_down = timestamp
            first_up = timestamp + random.randint(50, 100)
            second_down = first_up + random.randint(50, 150)
            second_up = second_down + random.randint(50, 100)
            
            down_events.extend([
                [x, y, first_down],
                [x, y, second_down]
            ])
            up_events.extend([
                [x, y, first_up],
                [x, y, second_up]
            ])
            
        elif click_type == "hold":
            down_time = timestamp
            up_time = timestamp + random.randint(500, 1500)
            
            down_events.append([x, y, down_time])
            up_events.append([x, y, up_time])
                
        return down_events, up_events
    
    def _Generate_Interaction(self, captcha_box: Dict[str, int], challenge_images: List[Dict[str, int]], selected_images: List[int]) -> Dict[str, Any]:
        """
        Generate complete interaction sequence for hCaptcha challenge.
        
        Args:
            captcha_box: Captcha container coordinates {"x": int, "y": int, "width": int, "height": int}
            challenge_images: List of image coordinates [{"x": int, "y": int, "width": int, "height": int}, ...]
            selected_images: List of image indices to select
            
        Returns:
            Complete motion data dictionary
        """
        start_ts = int(time.time() * 1000)
        current_ts = start_ts
        
        all_movements = []
        all_mouse_downs = []
        all_mouse_ups = []
        
        start_pos = (
            random.randint(100, self.screen_width - 100),
            random.randint(100, captcha_box["y"] - 50)
        )
                
        captcha_center = (
            captcha_box["x"] + captcha_box["width"] // 2,
            captcha_box["y"] + captcha_box["height"] // 2
        )
        
        movement = self._Generate_MouseMovement(start_pos, captcha_center, current_ts)
        all_movements.extend(movement)
        current_ts = movement[-1][2] + random.randint(100, 300)
        
        current_ts += random.randint(500, 1500)
        
        for i, image_index in enumerate(selected_images):
            if image_index >= len(challenge_images):
                continue
            
            image = challenge_images[image_index]
            
            click_x = image["x"] + random.randint(10, image["width"] - 10)
            click_y = image["y"] + random.randint(10, image["height"] - 10)
            click_pos = (click_x, click_y)

            last_pos = (all_movements[-1][0], all_movements[-1][1]) if all_movements else start_pos
            movement = self._Generate_MouseMovement(last_pos, click_pos, current_ts)
            all_movements.extend(movement)
            current_ts = movement[-1][2] + random.randint(50, 150)
            
            mouse_down, mouse_up = self._Generate_ClickSequence(click_pos, current_ts)
            all_mouse_downs.extend(mouse_down)
            all_mouse_ups.extend(mouse_up)
            current_ts = mouse_up[-1][2] + random.randint(200, 500)
            
            if i < len(selected_images) - 1:
                current_ts += random.randint(300, 800)
        
        submit_pos = (
            captcha_box["x"] + captcha_box["width"] // 2,
            captcha_box["y"] + captcha_box["height"] - 30
        )
        
        last_pos = (all_movements[-1][0], all_movements[-1][1]) if all_movements else captcha_center
        movement = self._Generate_MouseMovement(last_pos, submit_pos, current_ts)
        all_movements.extend(movement)
        current_ts = movement[-1][2] + random.randint(100, 200)

        mouse_down, mouse_up = self._Generate_ClickSequence(submit_pos, current_ts)
        all_mouse_downs.extend(mouse_down)
        all_mouse_ups.extend(mouse_up)
        
        if len(all_movements) > 1:
            total_duration = all_movements[-1][2] - all_movements[0][2]
            avg_period = total_duration / (len(all_movements) - 1)
        else:
            avg_period = 25.0
        
        motion_data = {
            "st": start_ts,
            "mm": all_movements,
            "md": all_mouse_downs,
            "mu": all_mouse_ups,
            "mm-mp": round(avg_period, 2),
            "v": 1
        }
        
        return motion_data
    
    def _Generate_BrowserData(self) -> Dict[str, Any]:
        """
        Generate top-level browser data for motion context.
        
        Returns:
            Dictionary containing browser and system information
        """
        return {
            "sc": {
                "availHeight": self.screen_height - 40,
                "availLeft": 0,
                "availTop": 0,
                "availWidth": self.screen_width,
                "colorDepth": 24,
                "height": self.screen_height,
                "pixelDepth": 24,
                "width": self.screen_width
            },
            "nv": {
                "appCodeName": "Mozilla",
                "appName": "Netscape",
                "appVersion": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "cookieEnabled": True,
                "hardwareConcurrency": random.choice([4, 6, 8, 12, 16]),
                "language": "en-US",
                "languages": ["en-US", "en"],
                "maxTouchPoints": 0,
                "onLine": True,
                "platform": "Win32",
                "plugins": [],
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            "dr": "",
            "inv": False,
            "exec": False,
            "wn": [
                [self.screen_width - 15, self.screen_height - 143, 2, int(time.time() * 1000)]
            ],
            "wn-mp": 0,
            "xy": [
                [random.randint(100, self.screen_width - 100), random.randint(100, self.screen_height - 100), 1, int(time.time() * 1000)]
            ],
            "xy-mp": 0
        }
    
    def _Final(self, captcha_box: Dict[str, int], challenge_images: List[Dict[str, int]], selected_images: List[int]) -> Dict[str, Any]:
        """
        Generate complete motion data including browser context.
        
        Args:
            captcha_box: Captcha container coordinates
            challenge_images: List of challenge image coordinates
            selected_images: List of selected image indices
            
        Returns:
            Complete motion data with browser context
        """
        motion_data = self._Generate_Interaction(captcha_box, challenge_images, selected_images)
        
        motion_data["topLevel"] = self._Generate_BrowserData()
        
        return motion_data
    
    def _NoiseAndCorrections(self, path: List[Tuple[int, int]], noise_level: float = 0.1) -> List[Tuple[int, int]]:
        """
        Add realistic noise and micro-corrections to mouse path.
        
        Args:
            path: Original mouse path
            noise_level: Amount of noise to add (0.0 to 1.0)
            
        Returns:
            Path with added noise and corrections
        """
        if not path or noise_level <= 0:
            return path
        
        noisy_path = []
        
        for i, (x, y) in enumerate(path):
            jitter_x = random.uniform(-noise_level * 3, noise_level * 3)
            jitter_y = random.uniform(-noise_level * 3, noise_level * 3)
            
            nx = int(x + jitter_x)
            ny = int(y + jitter_y)
            
            nx = max(0, min(self.screen_width - 1, nx))
            ny = max(0, min(self.screen_height - 1, ny))
            
            noisy_path.append((nx, ny))
            
            if i > 0 and random.random() < 0.05:
                cx = x + random.uniform(-1, 1)
                cy = y + random.uniform(-1, 1)
                
                cx = max(0, min(self.screen_width - 1, int(cx)))
                cy = max(0, min(self.screen_height - 1, int(cy)))
                
                noisy_path.append((cx, cy))
        
        return noisy_path
    
    def _Set_MotionParams(self, speed: float = 1.0, randomness: float = 0.3, hesitation_chance: float = 0.15) -> None:
        """
        Adjust motion generation parameters.
        
        Args:
            speed: Movement speed multiplier (higher = faster)
            randomness: Amount of randomness (0.0 to 1.0)
            hesitation_chance: Probability of hesitation (0.0 to 1.0)
        """
        self.base_speed = speed
        self.randomness = randomness
        self.hesitation_chance = hesitation_chance