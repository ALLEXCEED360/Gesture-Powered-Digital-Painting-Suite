import cv2
import mediapipe as mp
import numpy as np
import os
from datetime import datetime
import time

class HandGestureDrawingApp:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
            model_complexity=1  # Faster detection
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Get actual frame dimensions
        ret, frame = self.cap.read()
        if ret:
            self.frame_height, self.frame_width = frame.shape[:2]
        else:
            self.frame_width, self.frame_height = 1280, 720
        
        # Canvas setup
        self.canvas = np.zeros((self.frame_height, self.frame_width, 3), np.uint8)
        
        # Color palette (BGR format)
        self.palette = [
            (255, 255, 255),  # White
            (0, 0, 255),      # Red
            (0, 255, 0),      # Green
            (255, 0, 0),      # Blue
            (0, 255, 255),    # Yellow
            (255, 0, 255),    # Magenta
            (255, 255, 0),    # Cyan
            (128, 0, 128),    # Purple
            (255, 165, 0),    # Orange
            (0, 128, 0),      # Dark Green
        ]
        
        self.current_color_index = 0
        self.current_color = self.palette[self.current_color_index]
        
        # Drawing settings
        self.brush_thickness = 8
        self.eraser_thickness = 40
        self.cursor_size = 12
        
        # Position tracking
        self.prev_x = None
        self.prev_y = None
        self.smoothing_factor = 0.7
        
        # Mode tracking
        self.current_mode = "IDLE"
        self.last_color_change_time = 0
        self.color_change_cooldown = 0.5  # 500ms cooldown
        
        # Create save directory
        self.save_dir = "draw_saves"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # Finger landmark indices
        self.finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        self.finger_pips = [3, 6, 10, 14, 18]  # PIP joints for comparison
        self.finger_mcps = [2, 5, 9, 13, 17]   # MCP joints
        
        print("🎨 Hand Gesture Drawing App Initialized!")
        print("📷 Camera resolution:", f"{self.frame_width}x{self.frame_height}")
        print("🎯 Ready to draw with your hands!")
        print("\n" + "="*50)
        print("CONTROLS:")
        print("👆 Index finger only → DRAW mode")
        print("✌️  Index + Middle → HOVER mode (cursor)")
        print("✋ All 5 fingers → ERASE mode")
        print("👍 Thumb only → CHANGE COLOR")
        print("\nKEYBOARD SHORTCUTS:")
        print("'c' → Clear canvas")
        print("'s' → Save drawing")
        print("'q' → Quit application")
        print("="*50 + "\n")
    
    def detect_finger_states(self, landmarks, hand_label="Right"):
        """Detect which fingers are up/down based on landmark positions"""
        finger_states = {
            "thumb": False,
            "index": False,
            "middle": False,
            "ring": False,
            "pinky": False
        }
        
        # Thumb detection (special case - bends sideways, direction depends on hand)
        thumb_tip_x = landmarks[self.finger_tips[0]].x
        thumb_mcp_x = landmarks[self.finger_mcps[0]].x  # Use MCP joint for better detection
        
        # For right hand: thumb up when tip is to the LEFT of MCP (due to mirror effect)
        # For left hand: thumb up when tip is to the RIGHT of MCP (due to mirror effect)
        if hand_label == "Right":
            finger_states["thumb"] = thumb_tip_x < thumb_mcp_x
        else:  # Left hand
            finger_states["thumb"] = thumb_tip_x > thumb_mcp_x
            
        # Other fingers (bend up/down) - same for both hands
        finger_names = ["index", "middle", "ring", "pinky"]
        for i, finger_name in enumerate(finger_names, 1):
            tip_y = landmarks[self.finger_tips[i]].y
            pip_y = landmarks[self.finger_pips[i]].y
            
            if tip_y < pip_y:  # Tip is higher than PIP joint
                finger_states[finger_name] = True
        
        return finger_states
    
    def determine_mode(self, finger_states):
        """Determine drawing mode based on finger states"""
        fingers_up = sum(finger_states.values())
        
        # All 5 fingers up → Erase mode
        if fingers_up == 5:
            return "ERASE"
        
        # Only index finger up → Draw mode
        elif finger_states["index"] and fingers_up == 1:
            return "DRAW"
        
        # Index + middle up → Hover mode
        elif finger_states["index"] and finger_states["middle"] and fingers_up == 2:
            return "HOVER"
        
        # Only thumb up → Color change mode
        elif finger_states["thumb"] and fingers_up == 1:
            return "COLOR_CHANGE"
        
        else:
            return "IDLE"
    
    def smooth_position(self, new_x, new_y):
        """Apply position smoothing to reduce jitter"""
        if self.prev_x is None or self.prev_y is None:
            return new_x, new_y
        
        smooth_x = int(self.prev_x * (1 - self.smoothing_factor) + new_x * self.smoothing_factor)
        smooth_y = int(self.prev_y * (1 - self.smoothing_factor) + new_y * self.smoothing_factor)
        
        return smooth_x, smooth_y
    
    def change_color(self):
        """Cycle to next color in palette"""
        current_time = time.time()
        if current_time - self.last_color_change_time > self.color_change_cooldown:
            self.current_color_index = (self.current_color_index + 1) % len(self.palette)
            self.current_color = self.palette[self.current_color_index]
            self.last_color_change_time = current_time
            print(f"🎨 Color changed to #{self.current_color_index + 1}: {self.get_color_name()}")
    
    def get_color_name(self):
        """Get human-readable color name"""
        color_names = ["White", "Red", "Green", "Blue", "Yellow", "Magenta", 
                      "Cyan", "Purple", "Orange", "Dark Green"]
        return color_names[self.current_color_index]
    
    def draw_on_canvas(self, x, y, mode):
        """Draw on the persistent canvas based on mode"""
        if mode == "DRAW":
            if self.prev_x is not None and self.prev_y is not None:
                cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y), 
                        self.current_color, self.brush_thickness)
            else:
                cv2.circle(self.canvas, (x, y), self.brush_thickness//2, 
                          self.current_color, -1)
        
        elif mode == "ERASE":
            cv2.circle(self.canvas, (x, y), self.eraser_thickness//2, 
                      (0, 0, 0), -1)
    
    def draw_cursor(self, frame, x, y, mode):
        """Draw cursor overlay on live frame"""
        if mode == "HOVER":
            cv2.circle(frame, (x, y), self.cursor_size, (255, 255, 255), 2)
            cv2.circle(frame, (x, y), 3, (255, 255, 255), -1)
        
        elif mode == "DRAW":
            cv2.circle(frame, (x, y), self.brush_thickness//2, self.current_color, -1)
            cv2.circle(frame, (x, y), self.brush_thickness//2 + 2, (255, 255, 255), 2)
        
        elif mode == "ERASE":
            cv2.circle(frame, (x, y), self.eraser_thickness//2, (0, 0, 0), -1)
            cv2.circle(frame, (x, y), self.eraser_thickness//2 + 2, (255, 255, 255), 2)
    
    def overlay_canvas_on_frame(self, frame):
        """Overlay the persistent canvas on the live camera frame"""
        # Create mask from canvas
        mask = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask_bin = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
        
        # Create inverse mask
        inv_mask = cv2.bitwise_not(mask_bin)
        
        # Apply masks
        bg = cv2.bitwise_and(frame, frame, mask=inv_mask)
        fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask_bin)
        
        # Combine
        result = cv2.add(bg, fg)
        return result
    
    def draw_hud(self, frame, mode, finger_states, hand_label="Unknown"):
        """Draw heads-up display with current status"""
        # Mode and status
        status_text = f"Mode: {mode} | Color: {self.get_color_name()} #{self.current_color_index + 1}/{len(self.palette)}"
        
        if mode in ["DRAW", "ERASE"]:
            thickness = self.brush_thickness if mode == "DRAW" else self.eraser_thickness
            status_text += f" | Brush: {thickness}px"
        
        if hand_label != "Unknown":
            status_text += f" | Hand: {hand_label}"
        
        # Background rectangle for text
        text_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        cv2.rectangle(frame, (10, 10), (text_size[0] + 20, 80), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (text_size[0] + 20, 80), (255, 255, 255), 2)
        
        # Status text
        cv2.putText(frame, status_text, (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                   (255, 255, 255), 2)
        
        # Controls text
        controls_text = "[c] clear  [s] save  [q] quit"
        cv2.putText(frame, controls_text, (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                   (200, 200, 200), 1)
        
        # Color indicator
        color_rect_x = frame.shape[1] - 80
        cv2.rectangle(frame, (color_rect_x, 10), (color_rect_x + 60, 60), 
                     self.current_color, -1)
        cv2.rectangle(frame, (color_rect_x, 10), (color_rect_x + 60, 60), 
                     (255, 255, 255), 2)
        
        # Finger states debug (small text)
        debug_y = 100
        for finger, state in finger_states.items():
            color = (0, 255, 0) if state else (0, 0, 255)
            text = f"{finger}: {'UP' if state else 'DOWN'}"
            if finger == "thumb":
                text += f" ({hand_label})"
            cv2.putText(frame, text, 
                       (15, debug_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            debug_y += 20
    
    def clear_canvas(self):
        """Clear the drawing canvas"""
        self.canvas = np.zeros((self.frame_height, self.frame_width, 3), np.uint8)
        print("🧹 Canvas cleared!")
    
    def save_drawing(self):
        """Save current canvas to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"drawing_{timestamp}.png"
        filepath = os.path.join(self.save_dir, filename)
        
        # Save just the canvas (without camera background)
        cv2.imwrite(filepath, self.canvas)
        print(f"💾 Drawing saved as: {filename}")
        
        # Also save combined version
        combined_filename = f"combined_{timestamp}.png"
        combined_filepath = os.path.join(self.save_dir, combined_filename)
        
        # Create a dummy frame for combined version
        dummy_frame = np.zeros((self.frame_height, self.frame_width, 3), np.uint8)
        combined = self.overlay_canvas_on_frame(dummy_frame)
        cv2.imwrite(combined_filepath, combined)
        print(f"💾 Combined version saved as: {combined_filename}")
    
    def run(self):
        """Main application loop"""
        print("🚀 Starting Hand Gesture Drawing App...")
        print("Position your hand in front of the camera to begin!")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Error: Could not read frame from camera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with MediaPipe
            results = self.hands.process(rgb_frame)
            
            finger_states = {
                "thumb": False,
                "index": False,
                "middle": False,
                "ring": False,
                "pinky": False
            }
            
            current_mode = "IDLE"
            hand_label = "Unknown"
            
            # Process hand landmarks if detected
            if results.multi_hand_landmarks:
                for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # Draw hand landmarks on frame
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, 
                                              self.mp_hands.HAND_CONNECTIONS)
                    
                    # Get hand label (Left or Right)
                    hand_label = "Right"  # Default
                    if results.multi_handedness:
                        hand_label = results.multi_handedness[i].classification[0].label
                    
                    # Get finger states with hand-specific detection
                    finger_states = self.detect_finger_states(hand_landmarks.landmark, hand_label)
                    
                    # Determine mode
                    current_mode = self.determine_mode(finger_states)
                    
                    # Get index finger tip position (primary cursor)
                    index_tip = hand_landmarks.landmark[8]
                    x = int(index_tip.x * self.frame_width)
                    y = int(index_tip.y * self.frame_height)
                    
                    # Apply smoothing
                    x, y = self.smooth_position(x, y)
                    
                    # Handle different modes
                    if current_mode == "COLOR_CHANGE":
                        self.change_color()
                        current_mode = "IDLE"  # Don't stay in color change mode
                    
                    elif current_mode in ["DRAW", "ERASE"]:
                        self.draw_on_canvas(x, y, current_mode)
                        self.prev_x, self.prev_y = x, y
                    
                    elif current_mode == "HOVER":
                        # Just show cursor, don't draw
                        self.prev_x, self.prev_y = x, y
                    
                    else:
                        # Reset previous position in idle mode
                        self.prev_x, self.prev_y = None, None
                    
                    # Draw cursor overlay
                    if current_mode in ["DRAW", "HOVER", "ERASE"]:
                        self.draw_cursor(frame, x, y, current_mode)
            
            else:
                # No hand detected, reset previous position
                self.prev_x, self.prev_y = None, None
                current_mode = "NO_HAND"
            
            # Update current mode
            self.current_mode = current_mode
            
            # Overlay canvas on frame
            final_frame = self.overlay_canvas_on_frame(frame)
            
            # Draw HUD
            self.draw_hud(final_frame, current_mode, finger_states, hand_label)
            
            # Display the frame
            cv2.imshow('🎨 Hand Gesture Drawing App', final_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("👋 Goodbye!")
                break
            elif key == ord('c'):
                self.clear_canvas()
            elif key == ord('s'):
                self.save_drawing()
            elif key == 27:  # ESC key
                print("👋 Goodbye!")
                break
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("🧹 Resources cleaned up successfully!")

# Main execution
if __name__ == "__main__":
    try:
        app = HandGestureDrawingApp()
        app.run()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        cv2.destroyAllWindows()