# 🎨 Hand Gesture Drawing App

An interactive drawing application that lets you create digital art using only hand gestures! Draw, erase, and change colors in real-time using your webcam and computer vision.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8%2B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

### ✋ Gesture Controls
- **👆 Index Finger Only** → **DRAW** mode (creates colorful strokes)
- **✌️ Index + Middle Fingers** → **HOVER** mode (cursor without drawing)
- **✋ All 5 Fingers** → **ERASE** mode (large eraser brush)
- **👍 Thumb Only** → **COLOR CHANGE** mode (cycles through color palette)

### 🎨 Drawing Features
- **10-color palette** with instant color switching
- **Smooth line drawing** with position interpolation
- **Real-time canvas overlay** on live camera feed
- **Persistent drawing canvas** that maintains your artwork
- **Adjustable brush sizes** (8px draw, 40px erase)
- **Hand-specific detection** (works with both left and right hands)

### 📊 User Interface
- **Real-time HUD** showing current mode, color, and brush size
- **Visual color indicator** with current selection
- **Finger state debugging** display
- **Hand detection** (Left/Right) indicator
- **Mirror effect** for natural interaction

### ⌨️ Keyboard Shortcuts
- `c` → Clear canvas
- `s` → Save drawing (creates timestamped files)
- `q` or `ESC` → Quit application

## 🚀 Demo

![Demo GIF](demo.gif)
*Drawing with hand gestures in real-time*

## 📋 Requirements

- Python 3.7+
- Webcam/Camera
- Good lighting conditions
- Clear background for better hand detection

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/hand-gesture-drawing-app.git
cd hand-gesture-drawing-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python hand_gesture_draw.py
```

## 📦 Dependencies

- **OpenCV** (`opencv-python`) - Camera capture and image processing
- **MediaPipe** (`mediapipe`) - Hand detection and landmark tracking
- **NumPy** (`numpy`) - Canvas and array operations

## 🎮 How to Use

### Getting Started
1. **Launch the app** and position yourself in front of the camera
2. **Ensure good lighting** and a clear background
3. **Hold your hand** clearly visible in the camera frame
4. **Make gestures** to start drawing!

### Gesture Guide

| Gesture | Action | Description |
|---------|--------|-------------|
| 👆 | **Draw** | Extend only your index finger to draw lines |
| ✌️ | **Hover** | Extend index and middle fingers for cursor mode |
| ✋ | **Erase** | Spread all 5 fingers to activate eraser |
| 👍 | **Change Color** | Show only your thumb to cycle colors |

### Tips for Best Results
- **Good lighting** helps with hand detection
- **Steady movements** create smoother lines
- **Clear hand positions** improve gesture recognition
- **Keep hand in frame** for consistent tracking
- **Use deliberate gestures** for better mode switching

## 🎨 Color Palette

The app includes 10 vibrant colors:
1. ⚪ White
2. 🔴 Red
3. 🟢 Green
4. 🔵 Blue
5. 🟡 Yellow
6. 🟣 Magenta
7. 🩵 Cyan
8. 🟣 Purple
9. 🟠 Orange
10. 🟢 Dark Green

## 💾 File Structure

```
hand-gesture-drawing-app/
│
├── hand_gesture_draw.py      # Main application file
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
├── draw_saves/            # Auto-created folder for saved drawings

```

## 🔧 Technical Details

### Hand Detection Pipeline
1. **Camera Capture** → OpenCV captures webcam feed
2. **Hand Detection** → MediaPipe identifies 21 hand landmarks
3. **Gesture Recognition** → Custom algorithm determines finger states
4. **Mode Selection** → Gesture patterns trigger different modes
5. **Canvas Operations** → Drawing, erasing, or color changing
6. **Real-time Display** → Canvas overlay on live video feed

### Performance Optimizations
- **Model complexity 1** for faster MediaPipe processing
- **Position smoothing** (70% factor) reduces jitter
- **Efficient canvas masking** for clean overlay
- **Cooldown system** prevents rapid mode switching
- **Memory-efficient** numpy array operations

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs or issues
- ✨ Suggest new features
- 📚 Improve documentation
- 🧪 Add test cases
- 🎨 Enhance UI/UX

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

## 🚀 Future Enhancements

- [ ] **Adjustable brush sizes** with pinch gestures
- [ ] **Shape drawing** (circles, rectangles, lines)
- [ ] **Multi-hand support** (one draws, other selects tools)
- [ ] **Voice commands** for additional controls
- [ ] **Drawing templates** and backgrounds
- [ ] **Export to different formats** (SVG, PDF)
- [ ] **Recording feature** for timelapse videos
- [ ] **Mobile app version** using similar technology
- [ ] **Collaborative drawing** over network
- [ ] **3D drawing** in virtual space

## 🐛 Troubleshooting

### Common Issues

**Hand not detected:**
- Ensure good lighting conditions
- Check if camera is working properly
- Make sure hands are clearly visible
- Try repositioning relative to camera

**Gestures not working:**
- Keep fingers clearly separated
- Make deliberate, distinct gestures
- Ensure hand is fully in frame
- Check debug display for finger states

**Performance issues:**
- Close other camera applications
- Ensure sufficient system resources
- Lower camera resolution if needed
- Check if GPU acceleration is available

**Thumb detection problems:**
- The app auto-detects left/right hands
- Make clear thumb-up gestures
- Ensure thumb is not obscured
- Check hand label in HUD display

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe** team for excellent hand tracking technology
- **OpenCV** community for computer vision tools
- **Python** ecosystem for making development accessible
- **Open source contributors** who inspire innovation

## 📞 Contact

- **GitHub:** [@yourusername](https://github.com/ALLEXCEED360)
- **Email:** aryan138alam@gmail.com

---

### ⭐ Star this repository if you find it helpful!

**Happy Drawing!** 🎨✨
