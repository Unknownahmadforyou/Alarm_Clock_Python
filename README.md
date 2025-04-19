# Alarm_Clock_Python
Code Structure Improvements Refactored to use object-oriented programming Better exception handling for robustness Multithreading for non-blocking alarm operation Organized into logical methods Proper comments and documentation  .The application now looks and feels like a modern desktop application with professional styling and behavior.

# Professional Alarm Clock

A modern, feature-rich alarm clock application built with Python and Tkinter.

![Alarm Clock Screenshot](screenshot.png)

## Features

- **Multiple Alarms**
  - Set multiple alarms with hour, minute, and second precision
  - Customizable alarm names
  - Snooze functionality with adjustable snooze time
  - Sound testing capability

- **Stopwatch**
  - Start, stop, and reset functionality
  - Lap time recording
  - Millisecond precision
  - Clean, easy-to-read display

- **World Clock**
  - Add multiple world clocks
  - Support for any timezone
  - Easy clock management
  - Real-time updates

- **World Map**
  - Visual timezone representation
  - Major city markers
  - Timezone information on hover
  - Interactive map interface

- **Settings**
  - Dark/Light theme toggle
  - Customizable alarm sounds
  - Persistent settings
  - User preferences

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)
- Pillow (PIL)
- pytz
- timezonefinder
- requests

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/professional-alarm-clock.git
cd professional-alarm-clock
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Set an alarm:
   - Navigate to the Alarm tab
   - Select the desired time
   - Enter an optional alarm name
   - Click "Set Alarm"

3. Use the stopwatch:
   - Go to the Stopwatch tab
   - Use Start, Stop, and Reset buttons
   - Record lap times as needed

4. Add world clocks:
   - Open the World Clock tab
   - Enter a city name
   - Select the timezone
   - Click "Add Clock"

5. Customize settings:
   - Access the Settings tab
   - Toggle between dark and light themes
   - Change alarm sounds
   - Adjust other preferences

## File Structure

```
professional-alarm-clock/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── assets/             # Resource files
    ├── sounds/         # Alarm sounds
    └── images/         # Application images
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework
- [Pillow](https://python-pillow.org/) for image handling
- [pytz](https://pythonhosted.org/pytz/) for timezone support
- [timezonefinder](https://github.com/MrMinimal64/timezonefinder) for timezone detection

## Support

For support, email support@example.com or open an issue in the repository.

## Version History

- 1.0.0
  - Initial release
  - Basic alarm functionality
  - Stopwatch feature
  - World clock support

- 1.1.0
  - Added world map visualization
  - Improved theme support
  - Enhanced settings management
  - Bug fixes and performance improvements
